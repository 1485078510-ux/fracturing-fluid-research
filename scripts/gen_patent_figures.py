#!/usr/bin/env python3
"""生成专利申请三张附图的 .drawio XML 文件"""

import os

output_dir = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# ═══════════════════════════════════════════════════════════════
# 图1: 改性稀土铝酸盐荧光粉结构示意图 (核壳结构)
# ═══════════════════════════════════════════════════════════════
fig1_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1" id="fig1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="750" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 标题 -->
        <mxCell id="2" value="图1  改性稀土铝酸盐荧光粉结构示意图" style="text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fontFamily=SimHei;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="250" y="15" width="600" height="35" as="geometry" />
        </mxCell>

        <!-- === 核壳结构主体：三层同心圆 / 截面示意 === -->

        <!-- PEG4000 外层 (最大圆，最底层) -->
        <mxCell id="3" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;strokeWidth=2;opacity=60;" vertex="1" parent="1">
          <mxGeometry x="170" y="100" width="440" height="440" as="geometry" />
        </mxCell>

        <!-- KH550 中间层 -->
        <mxCell id="4" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;strokeWidth=2;opacity=65;" vertex="1" parent="1">
          <mxGeometry x="220" y="150" width="340" height="340" as="geometry" />
        </mxCell>

        <!-- 荧光粉基体核心 (最小圆，最顶层) -->
        <mxCell id="5" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="270" y="200" width="240" height="240" as="geometry" />
        </mxCell>

        <!-- 核心标签 -->
        <mxCell id="6" value="SrAl₂O₄:Eu²⁺,Dy³⁺&#xa;荧光粉基体" style="text;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fontFamily=SimHei;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="300" y="275" width="180" height="50" as="geometry" />
        </mxCell>

        <!-- === 图层标注引线 === -->

        <!-- PEG外层标注 -->
        <mxCell id="10" value="" style="endArrow=none;html=1;strokeColor=#82b366;strokeWidth=1.5;dashed=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="390" y="90" as="sourcePoint" />
            <mxPoint x="560" y="60" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="11" value="PEG4000 物理屏蔽层&#xa;(空间位阻 + 渗透排斥)" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontFamily=SimSun;fontColor=#2d6a2d;" vertex="1" parent="1">
          <mxGeometry x="565" y="35" width="200" height="50" as="geometry" />
        </mxCell>

        <!-- KH550层标注 -->
        <mxCell id="12" value="" style="endArrow=none;html=1;strokeColor=#6c8ebf;strokeWidth=1.5;dashed=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="390" y="140" as="sourcePoint" />
            <mxPoint x="560" y="120" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="13" value="KH550 硅烷偶联剂&#xa;化学键合层 (Si-O-Al)" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontFamily=SimSun;fontColor=#1a4d8f;" vertex="1" parent="1">
          <mxGeometry x="565" y="100" width="200" height="50" as="geometry" />
        </mxCell>

        <!-- -NH₂ 活性氨基标注 (在KH550层外缘) -->
        <mxCell id="14" value="" style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=1.5;dashed=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="240" y="320" as="sourcePoint" />
            <mxPoint x="80" y="300" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="15" value="-NH₂&#xa;活性氨基官能团" style="text;html=1;align=right;verticalAlign=middle;fontSize=11;fontFamily=SimSun;fontColor=#b85450;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="20" y="275" width="130" height="50" as="geometry" />
        </mxCell>

        <!-- === 右侧：化学键合细节放大示意 === -->
        <mxCell id="20" value="化学键合细节" style="text;html=1;align=center;verticalAlign=middle;fontSize=12;fontStyle=1;fontFamily=SimHei;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="650" y="220" width="120" height="25" as="geometry" />
        </mxCell>

        <!-- 放大区域边框 -->
        <mxCell id="21" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=1;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="640" y="250" width="340" height="250" as="geometry" />
        </mxCell>

        <!-- 荧光粉表面 (底部) -->
        <mxCell id="22" value="SrAl₂O₄ 基体表面" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="660" y="440" width="300" height="30" as="geometry" />
        </mxCell>

        <!-- 表面 -OH 基团 -->
        <mxCell id="23" value="-OH" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="680" y="420" width="40" height="20" as="geometry" />
        </mxCell>
        <mxCell id="24" value="-OH" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="750" y="420" width="40" height="20" as="geometry" />
        </mxCell>
        <mxCell id="25" value="-OH" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="890" y="420" width="40" height="20" as="geometry" />
        </mxCell>

        <!-- KH550 分子示意 -->
        <mxCell id="26" value="KH550" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="700" y="360" width="70" height="55" as="geometry" />
        </mxCell>
        <mxCell id="27" value="KH550" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="830" y="360" width="70" height="55" as="geometry" />
        </mxCell>

        <!-- Si-O-Al 键标注 -->
        <mxCell id="28" value="Si-O-Al&#xa;共价键" style="text;html=1;align=center;verticalAlign=middle;fontSize=9;fontFamily=SimSun;fontColor=#1a4d8f;fontStyle=2;" vertex="1" parent="1">
          <mxGeometry x="715" y="415" width="60" height="30" as="geometry" />
        </mxCell>
        <mxCell id="29" value="Si-O-Al&#xa;共价键" style="text;html=1;align=center;verticalAlign=middle;fontSize=9;fontFamily=SimSun;fontColor=#1a4d8f;fontStyle=2;" vertex="1" parent="1">
          <mxGeometry x="845" y="415" width="60" height="30" as="geometry" />
        </mxCell>

        <!-- PEG链示意 (波浪线) -->
        <mxCell id="30" value="PEG4000 链段&#xa;~~~~~~~~" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#2d6a2d;" vertex="1" parent="1">
          <mxGeometry x="680" y="270" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="31" value="PEG4000 链段&#xa;~~~~~~~~" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#2d6a2d;" vertex="1" parent="1">
          <mxGeometry x="840" y="270" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- -NH₂ 标注 (在KH550末端) -->
        <mxCell id="32" value="-NH₂" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#b85450;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="710" y="330" width="50" height="25" as="geometry" />
        </mxCell>
        <mxCell id="33" value="-NH₂" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#b85450;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="840" y="330" width="50" height="25" as="geometry" />
        </mxCell>

        <!-- 图例区 -->
        <mxCell id="40" value="图例" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;fontFamily=SimHei;" vertex="1" parent="1">
          <mxGeometry x="650" y="520" width="50" height="20" as="geometry" />
        </mxCell>
        <mxCell id="41" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="650" y="545" width="30" height="15" as="geometry" />
        </mxCell>
        <mxCell id="42" value="PEG外层" style="text;html=1;align=left;verticalAlign=middle;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="685" y="543" width="70" height="20" as="geometry" />
        </mxCell>
        <mxCell id="43" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="760" y="545" width="30" height="15" as="geometry" />
        </mxCell>
        <mxCell id="44" value="KH550内层" style="text;html=1;align=left;verticalAlign=middle;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="795" y="543" width="80" height="20" as="geometry" />
        </mxCell>
        <mxCell id="45" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="880" y="545" width="30" height="15" as="geometry" />
        </mxCell>
        <mxCell id="46" value="基体核心" style="text;html=1;align=left;verticalAlign=middle;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="915" y="543" width="65" height="20" as="geometry" />
        </mxCell>

        <!-- 破胶响应说明 -->
        <mxCell id="50" value="破胶响应: 过硫酸铵 + 储层温度 → PEG脱附降解 → 暴露 -NH₂" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#d79b00;fontStyle=2;" vertex="1" parent="1">
          <mxGeometry x="200" y="580" width="500" height="25" as="geometry" />
        </mxCell>

        <!-- 底部状态切换示意 -->
        <mxCell id="51" value="分散态 (注入阶段)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;fontFamily=SimHei;" vertex="1" parent="1">
          <mxGeometry x="220" y="620" width="160" height="35" as="geometry" />
        </mxCell>
        <mxCell id="52" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#d79b00;strokeWidth=2;" edge="1" parent="1" source="51" target="53">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="53" value="锚定态 (关井破胶后)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=10;fontFamily=SimHei;" vertex="1" parent="1">
          <mxGeometry x="480" y="620" width="160" height="35" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

# ═══════════════════════════════════════════════════════════════
# 图2: 母液预配+在线稀释 现场施工工艺流程图
# ═══════════════════════════════════════════════════════════════
fig2_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1" id="fig2">
    <mxGraphModel dx="1800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1650" pageHeight="500" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 标题 -->
        <mxCell id="2" value="图2  荧光压裂液体系"母液预配+在线稀释"现场施工工艺流程图" style="text;html=1;align=center;verticalAlign=middle;fontSize=15;fontStyle=1;fontFamily=SimHei;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="400" y="10" width="750" height="35" as="geometry" />
        </mxCell>

        <!-- ===== 上排：母液预配段 ===== -->
        <mxCell id="3" value="【母液预配段】" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;fontFamily=SimHei;fontColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="30" y="60" width="120" height="22" as="geometry" />
        </mxCell>

        <!-- 原材料 -->
        <mxCell id="10" value="改性荧光粉&#xa;+ 分散助剂&#xa;+ 去离子水" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontFamily=SimSun;fontStyle=0;" vertex="1" parent="1">
          <mxGeometry x="30" y="90" width="130" height="65" as="geometry" />
        </mxCell>

        <!-- 箭头 10->20 -->
        <mxCell id="11" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="10" target="20">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 高速剪切/超声分散 -->
        <mxCell id="20" value="高速剪切分散&#xa;(5000-15000 rpm)&#xa;+ 超声辅助" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="210" y="90" width="160" height="65" as="geometry" />
        </mxCell>

        <!-- 箭头 20->30 -->
        <mxCell id="21" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="20" target="30">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 荧光母液储罐 (圆柱形) -->
        <mxCell id="30" value="荧光母液储罐&#xa;(20-80 g/L)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontFamily=SimSun;size=15;" vertex="1" parent="1">
          <mxGeometry x="420" y="80" width="140" height="85" as="geometry" />
        </mxCell>

        <!-- ===== 下排：在线稀释段 ===== -->
        <mxCell id="4" value="【在线稀释与泵注段】" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;fontFamily=SimHei;fontColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="30" y="230" width="150" height="22" as="geometry" />
        </mxCell>

        <!-- 箭头 30->40 (向下然后向右) -->
        <mxCell id="31" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="30" target="40">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="490" y="200" />
              <mxPoint x="670" y="200" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- 在线计量泵 -->
        <mxCell id="40" value="在线计量泵&#xa;(0.1-2.0 vol%)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="600" y="250" width="140" height="65" as="geometry" />
        </mxCell>

        <!-- 箭头 40->50 -->
        <mxCell id="41" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="40" target="50">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 静态混合器 -->
        <mxCell id="50" value="静态混合器" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;fontFamily=SimSun;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="790" y="250" width="130" height="65" as="geometry" />
        </mxCell>

        <!-- HPG基液主流 (从上向下进入静态混合器) -->
        <mxCell id="55" value="HPG 基液主流&#xa;(0.3-1.0 wt%)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="795" y="120" width="120" height="55" as="geometry" />
        </mxCell>
        <mxCell id="56" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#666666;strokeWidth=2;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="55" target="50">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 箭头 50->60 -->
        <mxCell id="51" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="50" target="60">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 荧光压裂液终液 -->
        <mxCell id="60" value="荧光压裂液终液" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;fontFamily=SimHei;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="970" y="250" width="150" height="65" as="geometry" />
        </mxCell>

        <!-- 箭头 60->70 -->
        <mxCell id="61" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="60" target="70">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 压裂泵车 -->
        <mxCell id="70" value="压裂泵车" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="1170" y="250" width="120" height="65" as="geometry" />
        </mxCell>

        <!-- 箭头 70->80 -->
        <mxCell id="71" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="70" target="80">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 井口 -> 目标压裂层段 -->
        <mxCell id="80" value="井口 → 目标&#xa;压裂层段" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;fontFamily=SimHei;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1340" y="245" width="130" height="75" as="geometry" />
        </mxCell>

        <!-- ===== 标注区域 ===== -->
        <!-- 性能标准标注 -->
        <mxCell id="90" value="满足标准:&#xa;SY/T 6376-2008&#xa;SY/T 5107-2016" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=10;fontFamily=SimSun;fontColor=#666666;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="30" y="340" width="140" height="60" as="geometry" />
        </mxCell>

        <!-- 工艺条件标注 -->
        <mxCell id="91" value="工艺条件:&#xa;储层温度 60-150°C&#xa;关井时间 6-48 h" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=10;fontFamily=SimSun;fontColor=#666666;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="200" y="340" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- 支撑剂添加标注 -->
        <mxCell id="92" value="支撑剂&#xa;(混合后泵入)" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10;fontFamily=SimSun;" vertex="1" parent="1">
          <mxGeometry x="620" y="350" width="100" height="55" as="geometry" />
        </mxCell>

        <!-- 箭头 92->70 虚线 -->
        <mxCell id="93" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#d6b656;strokeWidth=1.5;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="92" target="70">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

# ═══════════════════════════════════════════════════════════════
# 图3: 压裂裂缝荧光示踪方法流程框图
# ═══════════════════════════════════════════════════════════════
fig3_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1" id="fig3">
    <mxGraphModel dx="1000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="1150" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 标题 -->
        <mxCell id="2" value="图3  压裂裂缝荧光示踪方法流程框图" style="text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fontFamily=SimHei;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="200" y="15" width="600" height="35" as="geometry" />
        </mxCell>

        <!-- ===== 阶段一：注入阶段 ===== -->
        <mxCell id="10" value="一、注入阶段" style="swimlane;startSize=28;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;fontFamily=SimHei;fontStyle=1;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="70" width="880" height="160" as="geometry" />
        </mxCell>

        <mxCell id="11" value="荧光压裂液终液&#xa;+ 支撑剂混合" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f0fc;strokeColor=#6c8ebf;fontSize=11;fontFamily=SimSun;" vertex="1" parent="10">
          <mxGeometry x="30" y="50" width="150" height="60" as="geometry" />
        </mxCell>

        <mxCell id="12" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="10" source="11" target="13">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="13" value="压裂泵注系统&#xa;泵入目标层段" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f0fc;strokeColor=#6c8ebf;fontSize=11;fontFamily=SimSun;" vertex="1" parent="10">
          <mxGeometry x="230" y="50" width="150" height="60" as="geometry" />
        </mxCell>

        <mxCell id="14" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="10" source="13" target="15">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="15" value="荧光粉随携砂液&#xa;运移至水力裂缝" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f0fc;strokeColor=#6c8ebf;fontSize=11;fontFamily=SimSun;" vertex="1" parent="10">
          <mxGeometry x="430" y="50" width="150" height="60" as="geometry" />
        </mxCell>

        <mxCell id="16" value="颗粒均匀分散&#xa;(PEG空间位阻稳定)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;fontFamily=SimSun;fontStyle=2;" vertex="1" parent="10">
          <mxGeometry x="650" y="50" width="150" height="60" as="geometry" />
        </mxCell>

        <!-- 阶段一→二 箭头 -->
        <mxCell id="17" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#d79b00;strokeWidth=3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="10" target="20">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="18" value="停泵关井" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#d79b00;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="440" y="235" width="80" height="20" as="geometry" />
        </mxCell>

        <!-- ===== 阶段二：关井破胶阶段 ===== -->
        <mxCell id="20" value="二、关井破胶阶段 (储层温度60-150°C, 密闭6-48 h)" style="swimlane;startSize=28;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=13;fontFamily=SimHei;fontStyle=1;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="260" width="880" height="220" as="geometry" />
        </mxCell>

        <!-- 过硫酸铵作用 -->
        <mxCell id="21" value="过硫酸铵热分解&#xa;产生 SO₄•⁻" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff9e6;strokeColor=#d6b656;fontSize=11;fontFamily=SimSun;" vertex="1" parent="20">
          <mxGeometry x="30" y="50" width="140" height="55" as="geometry" />
        </mxCell>

        <mxCell id="22" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="20" source="21" target="23">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- 两个并行效应 -->
        <mxCell id="23" value="交联键氧化断裂&#xa;冻胶网络解体" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff9e6;strokeColor=#d6b656;fontSize=11;fontFamily=SimSun;" vertex="1" parent="20">
          <mxGeometry x="210" y="50" width="150" height="55" as="geometry" />
        </mxCell>

        <mxCell id="24" value="PEG醚键氧化断链&#xa;生成低分子量碎片" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;fontFamily=SimSun;" vertex="1" parent="20">
          <mxGeometry x="210" y="125" width="150" height="55" as="geometry" />
        </mxCell>

        <mxCell id="25" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="20" source="21" target="24">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="195" y="152" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- PEG脱附 -->
        <mxCell id="26" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="20" source="24" target="27">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="27" value="PEG外层脱附降解&#xa;暴露KH550活性氨基" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;fontFamily=SimSun;fontStyle=1;" vertex="1" parent="20">
          <mxGeometry x="410" y="125" width="170" height="55" as="geometry" />
        </mxCell>

        <mxCell id="28" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="20" source="27" target="29">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="29" value="-NH₂ 与砂岩 Si-OH&#xa;静电吸引 + 氢键&#xa;+ 化学缩合锚定" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;fontFamily=SimSun;fontStyle=1;" vertex="1" parent="20">
          <mxGeometry x="630" y="115" width="180" height="65" as="geometry" />
        </mxCell>

        <!-- 阶段二→三 箭头 -->
        <mxCell id="30" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#d79b00;strokeWidth=3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="20" target="40">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="31" value="破胶完成，开井" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#d79b00;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="435" y="485" width="100" height="20" as="geometry" />
        </mxCell>

        <!-- ===== 阶段三：返排阶段 ===== -->
        <mxCell id="40" value="三、返排阶段" style="swimlane;startSize=28;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=13;fontFamily=SimHei;fontStyle=1;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="510" width="880" height="140" as="geometry" />
        </mxCell>

        <mxCell id="41" value="开井返排" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f0e6f5;strokeColor=#9673a6;fontSize=11;fontFamily=SimSun;" vertex="1" parent="40">
          <mxGeometry x="50" y="50" width="120" height="50" as="geometry" />
        </mxCell>

        <mxCell id="42" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="40" source="41" target="43">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="43" value="破胶残渣 + 未锚定&#xa;荧光粉 → 排出井筒" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f0e6f5;strokeColor=#9673a6;fontSize=11;fontFamily=SimSun;" vertex="1" parent="40">
          <mxGeometry x="220" y="45" width="180" height="55" as="geometry" />
        </mxCell>

        <mxCell id="44" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="40" source="43" target="45">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="45" value="锚定荧光粉&#xa;牢固保留于壁面" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontFamily=SimSun;fontStyle=1;" vertex="1" parent="40">
          <mxGeometry x="450" y="45" width="150" height="55" as="geometry" />
        </mxCell>

        <mxCell id="46" value="净残留率 &gt; 90%" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;fontFamily=SimSun;fontColor=#2d6a2d;fontStyle=1;" vertex="1" parent="40">
          <mxGeometry x="650" y="50" width="110" height="45" as="geometry" />
        </mxCell>

        <!-- 阶段三→四 箭头 -->
        <mxCell id="47" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#d79b00;strokeWidth=3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="40" target="50">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="48" value="压后取心作业" style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontFamily=SimSun;fontColor=#d79b00;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="440" y="655" width="90" height="20" as="geometry" />
        </mxCell>

        <!-- ===== 阶段四：取心与检测阶段 ===== -->
        <mxCell id="50" value="四、取心与检测阶段" style="swimlane;startSize=28;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;fontFamily=SimHei;fontStyle=1;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="60" y="680" width="880" height="180" as="geometry" />
        </mxCell>

        <mxCell id="51" value="压后取心&#xa;(含裂缝岩心)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e8;strokeColor=#82b366;fontSize=11;fontFamily=SimSun;" vertex="1" parent="50">
          <mxGeometry x="30" y="50" width="130" height="55" as="geometry" />
        </mxCell>

        <mxCell id="52" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="50" source="51" target="53">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="53" value="紫外光源照射&#xa;(波长365 nm)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e8;strokeColor=#82b366;fontSize=11;fontFamily=SimSun;" vertex="1" parent="50">
          <mxGeometry x="210" y="50" width="140" height="55" as="geometry" />
        </mxCell>

        <mxCell id="54" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="50" source="53" target="55">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="55" value="观察/拍照记录&#xa;裂缝壁面荧光分布" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e8;strokeColor=#82b366;fontSize=11;fontFamily=SimSun;" vertex="1" parent="50">
          <mxGeometry x="400" y="50" width="160" height="55" as="geometry" />
        </mxCell>

        <mxCell id="56" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#333333;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="50" source="55" target="57">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="57" value="确定压裂液&#xa;波及范围" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;fontFamily=SimHei;fontStyle=1;" vertex="1" parent="50">
          <mxGeometry x="610" y="50" width="140" height="55" as="geometry" />
        </mxCell>

        <!-- 绿色荧光标注 -->
        <mxCell id="58" value="绿色荧光&#xa;(~520 nm发射)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#b7e1b0;strokeColor=#82b366;fontSize=10;fontFamily=SimSun;fontColor=#2d6a2d;fontStyle=1;" vertex="1" parent="50">
          <mxGeometry x="780" y="45" width="90" height="65" as="geometry" />
        </mxCell>

        <!-- ===== 底部总结 ===== -->
        <mxCell id="60" value="核心创新：利用压裂施工自身"注入→关井→返排"时序，无需额外触发剂，实现"分散态→锚定态"自发功能切换" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;fontFamily=SimHei;fontStyle=1;align=center;" vertex="1" parent="1">
          <mxGeometry x="100" y="900" width="800" height="45" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

# ═══════════════════════════════════════════════════════════════
# 写入文件
# ═══════════════════════════════════════════════════════════════
files = {
    'fig1_core_shell_structure.drawio': fig1_xml,
    'fig2_process_flow.drawio': fig2_xml,
    'fig3_method_flowchart.drawio': fig3_xml,
}

for filename, content in files.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Saved: {filepath}')

print('\nAll 3 patent figures generated successfully.')
print('Open these files in draw.io desktop or https://app.diagrams.net/ to view and export.')