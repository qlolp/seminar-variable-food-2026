# -*- coding: utf-8 -*-
"""Журнальная (цветная) версия CSS для фигур. Те же классы .fg-*, новая палитра."""

CSS_COLOR = """
<style>
figure.fg{margin:18pt 0 14pt;page-break-inside:avoid;}
.fg-cap{font-weight:bold;font-size:11.5pt;color:#1F3D33;margin-bottom:6pt;line-height:1.3;}
.fg-note{font-size:9.5pt;color:#444;margin-top:6pt;line-height:1.3;}
.fg-src{font-size:9pt;color:#6B7280;margin-top:3pt;line-height:1.3;}
.fg-h{font-weight:bold;font-size:10.5pt;color:#1F3D33;margin:0 0 3pt;}

.fg-grid{display:flex;flex-wrap:wrap;gap:8pt;margin-top:4pt;}
.fg-cell{flex:1 1 28%;border:1pt solid #C7BFAF;border-top:3pt solid #2F5D50;background:#FBFAF7;padding:7pt;font-size:9.5pt;line-height:1.35;}

.fg-flow{display:flex;flex-wrap:wrap;gap:6pt;align-items:center;margin-top:4pt;}
.fg-node{flex:1 1 12%;border:1.2pt solid #2F5D50;background:#EEF4F1;padding:4pt;font-size:9pt;text-align:center;display:flex;align-items:center;justify-content:center;min-width:60pt;}
.fg-arrow{text-align:center;font-size:14pt;line-height:1;color:#B57517;font-weight:bold;}

.fg-bar-row{display:flex;align-items:center;margin:3pt 0;}
.fg-bar-lab{width:34%;text-align:right;padding-right:6pt;line-height:1.15;font-size:9.5pt;}
.fg-bar{height:14pt;background:#2F5D50;}
.fg-bar.alt{background:#B57517;}
.fg-bar-val{font-size:9.5pt;font-weight:bold;padding-left:5pt;color:#1F3D33;}

table.fg-t{border-collapse:collapse;width:100%;font-size:10pt;margin-top:4pt;}
table.fg-t td,table.fg-t th{border:0.8pt solid #8FA79E;padding:3.5pt 5pt;vertical-align:top;text-align:left;}
table.fg-t th{background:#DCE6E0;color:#1F3D33;font-size:10pt;overflow-wrap:normal;word-break:normal;}

.hm-a{background:#BFD9BE;} .hm-b{background:#F2DC9B;} .hm-c{background:#E8A39B;} .hm-n{background:#E4E2DC;}

.fg-step{flex:1;border:1.2pt solid #2F5D50;padding:5pt;font-size:9.5pt;text-align:center;background:#EEF4F1;}
.fg-step.solid{background:#2F5D50;color:#fff;}
.fg-steps{display:flex;gap:6pt;align-items:flex-end;margin-top:4pt;}

.fg-tl{display:flex;gap:0;margin-top:4pt;}
.fg-tl-i{flex:1;border-top:3pt solid #2F5D50;padding:5pt 6pt;font-size:9.5pt;line-height:1.3;background:#FBFAF7;}
.fg-tl-i.acc{border-top-color:#B57517;}

.fg-dash{display:flex;flex-wrap:wrap;gap:8pt;margin-top:4pt;}
.fg-card{flex:1 1 20%;background:#1F3D33;color:#fff;padding:9pt;font-size:9.5pt;line-height:1.3;}
.fg-card b{display:block;font-size:17pt;color:#E8C37E;margin-bottom:3pt;}

.fg-circ{width:128pt;height:128pt;border:2pt solid #2F5D50;border-radius:65pt;display:flex;align-items:center;justify-content:center;text-align:center;font-size:8.5pt;line-height:1.2;padding:6pt;margin:0;background:#F4F7F5;box-sizing:border-box;}
.fg-circ b{font-size:8.8pt;color:#1F3D33;}
.fg-circ.c1{background:#DCE6E0;} .fg-circ.c2{background:#EFE6D2;} .fg-circ.c3{background:#E8EFEA;}
.fg-circs,.fg-circles{display:flex;align-items:center;justify-content:space-between;gap:10pt;margin-top:6pt;}

.page-inf{margin:10pt 0 10pt;page-break-before:always;}
.page-inf .fg-cap{font-size:16pt;color:#1F3D33;border-bottom:3pt solid #B57517;padding-bottom:7pt;margin-bottom:16pt;}
.page-inf .fg-grid{gap:12pt;}
.page-inf .fg-cell{flex:1 1 26%;border:1pt solid #C7BFAF;border-top:4.5pt solid #2F5D50;background:#FBFAF7;padding:13pt;font-size:11.5pt;line-height:1.5;min-height:115pt;}
.page-inf .fg-cell .fg-h{font-size:13pt;color:#B57517;letter-spacing:0.5pt;margin-bottom:5pt;}
.page-inf .fg-note{font-size:10.5pt;margin-top:12pt;}
.page-inf .fg-src{font-size:9.5pt;margin-top:5pt;}
.page-inf table.fg-t{font-size:11pt;margin-top:6pt;}
.page-inf table.fg-t th{font-size:11pt;padding:6pt 8pt;}
.page-inf table.fg-t td{padding:6pt 8pt;}
</style>
"""
