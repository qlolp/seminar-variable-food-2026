// node pdf.js in.html out.pdf "Заголовок для колонтитула"
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [, , input, output, title] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + input, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const foot = `<div style="font-family:Inter,'DejaVu Sans',sans-serif;font-size:7pt;color:#5b6b73;width:100%;padding:0 16mm 0 20mm;display:flex;justify-content:space-between">
    <span>${title || ''}</span><span class="pageNumber"></span></div>`;
  await p.pdf({ path: output, format: 'A4', printBackground: true, displayHeaderFooter: true, outline: true, tagged: true,
    headerTemplate: '<span></span>', footerTemplate: foot,
    margin: { top: '18mm', bottom: '20mm', left: '20mm', right: '16mm' } });
  await b.close();
})();
