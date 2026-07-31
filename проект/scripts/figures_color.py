# -*- coding: utf-8 -*-
"""Журнальная (цветная) версия CSS для фигур. Те же классы .fg-*, палитра claude.ai."""

CSS_COLOR = """
<style>
figure.fg{margin:18pt 0 14pt;page-break-inside:avoid;}
.fg-cap{font-family:'PT Serif',serif;font-weight:bold;font-size:12pt;color:#141413;margin-bottom:6pt;line-height:1.3;}
.fg-note{font-size:9.5pt;color:#4A463C;margin-top:6pt;line-height:1.3;}
.fg-src{font-size:9pt;color:#8A8578;margin-top:3pt;line-height:1.3;}
.fg-h{font-weight:bold;font-size:10.5pt;color:#141413;margin:0 0 3pt;}

.fg-grid{display:flex;flex-wrap:wrap;gap:8pt;margin-top:4pt;}
.fg-cell{flex:1 1 28%;border:1pt solid #E5E2D8;border-top:3pt solid #D97757;background:#FFFFFF;padding:7pt;font-size:9.5pt;line-height:1.35;}

.fg-flow{display:flex;flex-wrap:wrap;gap:6pt;align-items:center;margin-top:4pt;}
.fg-node{flex:1 1 12%;border:1.2pt solid #D97757;background:#F7F4EC;padding:4pt;font-size:9pt;text-align:center;display:flex;align-items:center;justify-content:center;min-width:60pt;}
.fg-arrow{text-align:center;font-size:14pt;line-height:1;color:#B85C3D;font-weight:bold;}

.fg-bar-row{display:flex;align-items:center;margin:3pt 0;}
.fg-bar-lab{width:34%;text-align:right;padding-right:6pt;line-height:1.15;font-size:9.5pt;}
.fg-bar{height:14pt;background:#D97757;}
.fg-bar.alt{background:#B85C3D;}
.fg-bar-val{font-size:9.5pt;font-weight:bold;padding-left:5pt;color:#141413;}

table.fg-t{border-collapse:collapse;width:100%;font-size:10pt;margin-top:4pt;background:#FFFFFF;}
table.fg-t td,table.fg-t th{border:0.8pt solid #E5E2D8;padding:3.5pt 5pt;vertical-align:top;text-align:left;}
table.fg-t th{background:#F2EFE6;color:#141413;font-size:10pt;overflow-wrap:normal;word-break:normal;}

.hm-a{background:#DDEBD9;} .hm-b{background:#F4E3B0;} .hm-c{background:#EFB4A8;} .hm-n{background:#EDEAE2;}

.fg-step{flex:1;border:1.2pt solid #D97757;padding:5pt;font-size:9.5pt;text-align:center;background:#F7F4EC;}
.fg-step.solid{background:#D97757;color:#fff;}
.fg-steps{display:flex;gap:6pt;align-items:flex-end;margin-top:4pt;}

.fg-tl{display:flex;gap:0;margin-top:4pt;}
.fg-tl-i{flex:1;border-top:3pt solid #D97757;padding:5pt 6pt;font-size:9.5pt;line-height:1.3;background:#FFFFFF;}
.fg-tl-i.acc{border-top-color:#B85C3D;}

.fg-dash{display:flex;flex-wrap:wrap;gap:8pt;margin-top:4pt;}
.fg-card{flex:1 1 20%;background:#141413;color:#F9F9F7;padding:9pt;font-size:9.5pt;line-height:1.3;}
.fg-card b{display:block;font-size:17pt;color:#D97757;margin-bottom:3pt;}

.fg-circ{width:128pt;height:128pt;border:2pt solid #D97757;border-radius:65pt;display:flex;align-items:center;justify-content:center;text-align:center;font-size:8.5pt;line-height:1.2;padding:6pt;margin:0;background:#F7F4EC;box-sizing:border-box;}
.fg-circ b{font-size:8.8pt;color:#141413;}
.fg-circ.c1{background:#F2EFE6;} .fg-circ.c2{background:#F7E5DC;} .fg-circ.c3{background:#F7F4EC;}
.fg-circs,.fg-circles{display:flex;align-items:center;justify-content:space-between;gap:10pt;margin-top:6pt;}

.page-inf{margin:10pt 0 10pt;page-break-before:always;}
.page-inf .fg-cap{font-size:17pt;color:#141413;border-bottom:3pt solid #D97757;padding-bottom:7pt;margin-bottom:16pt;}
.page-inf .fg-grid{gap:12pt;}
.page-inf .fg-cell{flex:1 1 26%;border:1pt solid #E5E2D8;border-top:4.5pt solid #D97757;background:#FFFFFF;padding:13pt;font-size:11.5pt;line-height:1.5;min-height:115pt;}
.page-inf .fg-cell .fg-h{font-size:13pt;color:#B85C3D;letter-spacing:0.5pt;margin-bottom:5pt;}
.page-inf .fg-note{font-size:10.5pt;margin-top:12pt;}
.page-inf .fg-src{font-size:9.5pt;margin-top:5pt;}
.page-inf table.fg-t{font-size:11pt;margin-top:6pt;}
.page-inf table.fg-t th{font-size:11pt;padding:6pt 8pt;}
.page-inf table.fg-t td{padding:6pt 8pt;}
</style>
"""
