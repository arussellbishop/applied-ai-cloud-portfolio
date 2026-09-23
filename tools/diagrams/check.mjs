import { JSDOM } from 'jsdom';
import fs from 'node:fs';
import path from 'node:path';
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
const root = path.resolve(process.argv[2] || '.');
function* files(folder) {
  for (const entry of fs.readdirSync(folder, { withFileTypes: true })) {
    if (['.git', '.terraform', 'node_modules'].includes(entry.name)) continue;
    const full = path.join(folder, entry.name);
    if (entry.isDirectory()) yield* files(full);
    else if (entry.isFile()) yield full;
  }
}
const all = [...files(root)];
const markdown = all.filter(p => p.endsWith('.md')).map(p => [p, fs.readFileSync(p, 'utf8')]);
let count = 0;
for (const file of all.filter(p => p.endsWith('.mmd'))) {
  const source = fs.readFileSync(file, 'utf8');
  await mermaid.parse(source);
  if (!markdown.some(([, text]) => text.includes(source))) throw new Error(`Missing matching Markdown diagram: ${file}`);
  count++;
}
for (const [file, text] of markdown) {
  for (const match of text.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)) {
    try { await mermaid.parse(match[1]); } catch (error) { throw new Error(`${file}: ${error.message}`); }
    count++;
  }
}
if (count < 7) throw new Error('Required architecture views missing');
console.log(`Mermaid PASS: ${count} source/embedded diagrams; all standalone diagrams have matching Markdown.`);
