import { JSDOM } from 'jsdom';
import fs from 'node:fs';
import path from 'node:path';
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
const folder = process.argv[2];
for (const name of ['current-aws.mmd', 'multicloud.mmd']) {
  const source = fs.readFileSync(path.join(folder, name), 'utf8');
  await mermaid.parse(source);
  const markdown = fs.readFileSync(path.join(folder, 'README.md'), 'utf8');
  if (!markdown.includes(source)) throw new Error(`Diagram and Markdown differ: ${name}`);
  console.log(`${name}: syntax PASS; Markdown copy matches`);
}
