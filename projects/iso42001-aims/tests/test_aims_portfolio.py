from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def test_integrity_checker():
    result=subprocess.run([sys.executable, ROOT/"scripts/check_aims_portfolio.py"],capture_output=True,text=True)
    assert result.returncode==0, result.stdout+result.stderr
def test_synthetic_notice_and_no_iso_pdf():
    assert (ROOT/"DATA_SYNTHETIC_NOTICE.md").exists()
    assert not list(ROOT.rglob("*.pdf"))
