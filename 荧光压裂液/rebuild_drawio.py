import re

with open('fig1_core_shell_structure.drawio', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract the mxGraphModel attributes from template
m = re.search(r'<mxGraphModel([^>]*)>', template)
model_attrs = m.group(1) if m else ''

# Build cells content
cells = '''
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="t0" value="荧光粉表面改性工艺流程" style="text;html=1;align=center;verticalAlign=middle;fontFamily=Microsoft YaHei;fontSize=26;fontStyle=1;fontColor=#1565C0;" vertex="1" parent="1">
          <mxGeometry x="350" y="20" width="600" height="40" as="geometry"/>
        </mxCell>

        <mxCell id="f1" value="" style="rounded=1;fillColor=#FAFBFC;strokeColor=#BBDEFB;strokeWidth=2;arcSize=6;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="560" height="430" as="geometry"/>
        </mxCell>

        <mxCell id="s1h" value="" style="rounded=1;fillColor=#1565C0;strokeColor=none;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="560" height="44" as="geometry"/>
        </mxCell>
        <mxCell id="s1t" value="STEP 1    KH550 化学锚固" style="text;html=1;align=left;verticalAlign=middle;fontFamily=Microsoft YaHei;fontSize=18;fontStyle=1;fontColor=#FFFFFF;spacingLeft=20;" vertex="1" parent="1">
          <mxGeometry x="40" y="82" width="560" height="40" as="geometry"/>
        </mxCell>

        <mxCell id="s1a" value="荧光粉&lt;br&gt;&lt;font style=&quot;font-size:10px&quot; color=&quot;#666666&quot;&gt;SrAl&lt;sub&gt;2&lt;/sub&gt;O&lt;sub&gt;4&lt;/sub&gt;:Eu&lt;sup&gt;2+&lt;/sup&gt;,Dy&lt;sup&gt;3+&lt;/sup&gt;&lt;/font&gt;" style="rounded=1;html=1;fillColor=#E3F2FD;strokeColor=#64B5F6;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="90" y="148" width="210" height="52" as="geometry"/>
        </mxCell>
        <mxCell id="s1b" value="乙醇-水 (95:5)" style="rounded=1;html=1;fillColor=#E3F2FD;strokeColor=#64B5F6;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="340" y="148" width="210" height="52" as="geometry"/>
        </mxCell>
        <mxCell id="s1ab" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#64B5F6;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="305" y="174" as="sourcePoint"/><mxPoint x="335" y="174" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s1v1" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="320" y="204" as="sourcePoint"/><mxPoint x="320" y="236" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s1c" value="加入 KH550 (2.0 wt%)    乙酸调 pH 4.5" style="rounded=1;html=1;fillColor=#BBDEFB;strokeColor=#1565C0;strokeWidth=2;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="90" y="240" width="460" height="48" as="geometry"/>
        </mxCell>

        <mxCell id="s1v2" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="320" y="292" as="sourcePoint"/><mxPoint x="320" y="320" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s1d" value="室温搅拌 2 h -> 60 degC 干燥固化 1 h" style="rounded=1;html=1;fillColor=#BBDEFB;strokeColor=#1565C0;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="90" y="324" width="460" height="48" as="geometry"/>
        </mxCell>

        <mxCell id="s1v3" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="320" y="376" as="sourcePoint"/><mxPoint x="320" y="404" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s1r" value="KH550-荧光粉     Si-O-Al 共价键锚固    预置 -NH2" style="rounded=1;html=1;fillColor=#90CAF9;strokeColor=#1565C0;strokeWidth=2;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;fontColor=#0D47A1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="75" y="408" width="490" height="44" as="geometry"/>
        </mxCell>

        <mxCell id="big" value="" style="endArrow=block;html=1;strokeWidth=4;strokeColor=#0D47A1;endFill=1;endSize=14;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="615" y="295" as="sourcePoint"/><mxPoint x="695" y="295" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="f2" value="" style="rounded=1;fillColor=#FAFBFC;strokeColor=#B2EBF2;strokeWidth=2;arcSize=6;shadow=1;" vertex="1" parent="1">
          <mxGeometry x="710" y="80" width="560" height="430" as="geometry"/>
        </mxCell>

        <mxCell id="s2h" value="" style="rounded=1;fillColor=#00838F;strokeColor=none;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="710" y="80" width="560" height="44" as="geometry"/>
        </mxCell>
        <mxCell id="s2t" value="STEP 2    PEG4000 物理屏蔽" style="text;html=1;align=left;verticalAlign=middle;fontFamily=Microsoft YaHei;fontSize=18;fontStyle=1;fontColor=#FFFFFF;spacingLeft=20;" vertex="1" parent="1">
          <mxGeometry x="710" y="82" width="560" height="40" as="geometry"/>
        </mxCell>

        <mxCell id="s2a" value="KH550-荧光粉（步骤一产物）" style="rounded=1;html=1;fillColor=#E0F7FA;strokeColor=#4DD0E1;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="760" y="148" width="280" height="52" as="geometry"/>
        </mxCell>

        <mxCell id="s2v1" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="990" y="204" as="sourcePoint"/><mxPoint x="990" y="236" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s2b" value="加入 PEG4000 (3.0 wt%)    Mn = 4000" style="rounded=1;html=1;fillColor=#B2EBF2;strokeColor=#00838F;strokeWidth=2;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="760" y="240" width="460" height="48" as="geometry"/>
        </mxCell>

        <mxCell id="s2v2" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="990" y="292" as="sourcePoint"/><mxPoint x="990" y="320" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s2c" value="室温搅拌 1 h -> 离心洗涤 -> 60 degC 干燥" style="rounded=1;html=1;fillColor=#B2EBF2;strokeColor=#00838F;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="760" y="324" width="460" height="48" as="geometry"/>
        </mxCell>

        <mxCell id="s2v3" value="" style="endArrow=classic;html=1;strokeWidth=2;strokeColor=#90A4AE;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"><mxPoint x="990" y="376" as="sourcePoint"/><mxPoint x="990" y="404" as="targetPoint"/></mxGeometry>
        </mxCell>

        <mxCell id="s2r" value="改性荧光粉     KH550 内层 - PEG 外层     双层包覆" style="rounded=1;html=1;fillColor=#80DEEA;strokeColor=#00838F;strokeWidth=2;fontFamily=Microsoft YaHei;fontSize=14;fontStyle=1;fontColor=#006064;arcSize=10;" vertex="1" parent="1">
          <mxGeometry x="745" y="408" width="490" height="44" as="geometry"/>
        </mxCell>

        <mxCell id="bot" value="" style="rounded=1;fillColor=#E3F2FD;strokeColor=#64B5F6;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="540" width="1230" height="46" as="geometry"/>
        </mxCell>
        <mxCell id="bott" value="设计原理：KH550 以 Si-O-Al 共价键锚固并预置氨基  |  PEG4000 以氢键/范德华力物理缠绕提供空间位阻  |  注入时 PEG 屏蔽保障分散 -> 关井时高温脱 PEG -> 氨基暴露 -> 壁面锚定" style="text;html=1;align=center;verticalAlign=middle;fontFamily=Microsoft YaHei;fontSize=13;fontStyle=1;fontColor=#0D47A1;" vertex="1" parent="1">
          <mxGeometry x="55" y="546" width="1200" height="36" as="geometry"/>
        </mxCell>
'''

# Build complete file from template structure
# Replace everything between <root> and </root>
root_start = template.index('<root>')
root_end = template.index('</root>') + len('</root>')

final = template[:root_start + len('<root>')] + '\n' + cells + '\n      ' + template[root_end - len('</root>'):]

with open('fig_surface_modification.drawio', 'w', encoding='utf-8') as f:
    f.write(final)

import xml.etree.ElementTree as ET
try:
    ET.parse('fig_surface_modification.drawio')
    print('Valid XML - file ready')
except ET.ParseError as e:
    print(f'XML Error: {e}')