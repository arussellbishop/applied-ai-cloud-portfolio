"""State-transition and security tests; no production or Docker writes."""
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('receiver', Path(__file__).with_name('deploy.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class DeploymentTests(unittest.TestCase):
    def test_reject_non_main(self):
        with patch.object(r, 'api', return_value={'object': {'sha': 'b' * 40}}):
            with self.assertRaises(ValueError): r.verify_ci('a' * 40)

    def test_reject_failed_ci(self):
        data = [{'object': {'sha': 'a' * 40}}, {'workflow_runs': [{'head_sha': 'a' * 40, 'conclusion': 'failure'}]}]
        with patch.object(r, 'api', side_effect=data):
            with self.assertRaises(ValueError): r.verify_ci('a' * 40)

    def test_reject_archive_traversal_and_symlink(self):
        for name, kind in [('repo/site/../../escape.html', tarfile.REGTYPE), ('repo/site/index.html', tarfile.SYMTYPE)]:
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode='w:gz') as archive:
                item = tarfile.TarInfo(name); item.type = kind; archive.addfile(item)
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError): r.extract_site(stream.getvalue(), Path(directory))

    def setup_slots(self, directory):
        base = Path(directory); bg = base / 'bluegreen'; bg.mkdir(); (bg / 'reports').mkdir()
        slots = {}
        for slot, sha in [('blue', 'a' * 40), ('green', 'b' * 40)]:
            release = base / sha; (release / 'portfolio/site').mkdir(parents=True)
            (release / 'portfolio/site/index.html').write_text('Applied AI Systems')
            slots[slot] = {'sha': sha, 'slot': slot, 'release': str(release), 'containers': {'portfolio': slot + '-web', 'api': slot + '-api'}}
        value = {'active': 'blue', 'previous': 'green', 'slots': slots}
        (bg / 'state.json').write_text(json.dumps(value))
        return base, bg, value

    def test_unhealthy_candidate_never_switches_or_removes_active(self):
        with tempfile.TemporaryDirectory() as directory:
            base,bg,value = self.setup_slots(directory)
            candidate = dict(value['slots']['green'], sha='c' * 40)
            with patch.object(r,'BASE',base), patch.object(r,'BG',bg), patch.object(r,'verify_ci'), patch.object(r,'prepare',return_value=candidate), patch.object(r,'internal_health',side_effect=[None,RuntimeError('unhealthy'),None]), patch.object(r,'remove') as remove, patch.object(r,'start'), patch.object(r,'switch') as switch, patch.object(r,'public_health'):
                with self.assertRaisesRegex(RuntimeError,'unhealthy'): r.deploy('c' * 40)
                switch.assert_not_called()
                self.assertEqual(r.state()['active'],'blue')
                self.assertNotIn(value['slots']['blue'],[call.args[0] for call in remove.call_args_list])
                report=json.loads((bg/'reports'/('c'*40+'.json')).read_text())
                self.assertEqual(report['traffic_switch'],'NOT_SWITCHED')
                self.assertEqual(report['candidate_health'],'FAIL')

    def test_switch_failure_restores_previous_and_journal_clears(self):
        with tempfile.TemporaryDirectory() as directory:
            base,bg,value=self.setup_slots(directory)
            with patch.object(r,'BASE',base),patch.object(r,'BG',bg),patch.object(r,'internal_health'),patch.object(r,'reload_proxy') as reload,patch.object(r,'public_health',side_effect=[RuntimeError('bad public'),None]):
                with self.assertRaises(r.TrafficSwitchError):r.switch(value,'green')
                self.assertEqual([call.args[0] for call in reload.call_args_list],['green','blue'])
                self.assertEqual(r.state()['active'],'blue')
                self.assertFalse((bg/'transaction.json').exists())

    def test_wrong_sha_fails_private_health_before_switch(self):
        with tempfile.TemporaryDirectory() as directory:
            base,bg,value=self.setup_slots(directory)
            objects=[{'Name':'/'+name,'State':{'Health':{'Status':'healthy'},'OOMKilled':False},'NetworkSettings':{'Networks':{'applied-ai-private':{'IPAddress':'127.0.0.1'}}}} for name in value['slots']['green']['containers'].values()]
            with patch.object(r,'run',return_value=json.dumps(objects).encode()),patch.object(r,'fetch',side_effect=[json.dumps({'status':'ok','release':'wrong'}).encode(),b'Applied AI Systems']),patch.object(r.time,'sleep'):
                with self.assertRaises(RuntimeError):r.internal_health(value['slots']['green'],attempts=1)

    def test_rollback_rejects_stale_sha(self):
        with patch.object(r,'state',return_value={'active':'blue','slots':{'blue':{'sha':'b'*40}}}),patch.object(r,'switch') as switch:
            with self.assertRaises(ValueError):r.rollback('a'*40)
            switch.assert_not_called()

    def test_memory_pressure_blocks_candidate_command(self):
        resource=r.Resources();resource.unsafe=True
        with patch.object(r,'RESOURCES',resource),patch.object(r.subprocess,'Popen') as process:
            with self.assertRaisesRegex(RuntimeError,'Unsafe memory'):r.run('must-not-execute')
            process.assert_not_called()

    def test_confirmation_preserves_deployment_resource_peak(self):
        with tempfile.TemporaryDirectory() as directory:
            base,bg,value=self.setup_slots(directory)
            resource=r.Resources();resource.minimum=800;resource.peak_used=1100
            with patch.object(r,'BASE',base),patch.object(r,'BG',bg),patch.object(r,'RESOURCES',resource):
                r.report('a'*40,final_status='RUNNING')
                resource.minimum=1200;resource.peak_used=700
                result=r.report('a'*40,final_status='SUCCESS')
                self.assertEqual(result['minimum_available_mib'],800)
                self.assertEqual(result['peak_host_used_mib'],1100)

    def test_crash_journal_restores_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            base,bg,value=self.setup_slots(directory)
            (bg/'transaction.json').write_text(json.dumps(value))
            with patch.object(r,'BASE',base),patch.object(r,'BG',bg),patch.object(r,'internal_health'),patch.object(r,'reload_proxy') as reload,patch.object(r,'public_health'):
                r.recover_transaction()
                self.assertEqual(reload.call_args.args[0],'blue')
                self.assertFalse((bg/'transaction.json').exists())


if __name__ == '__main__': unittest.main()
