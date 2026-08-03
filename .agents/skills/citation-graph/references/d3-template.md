# D3.js Force-Directed Citation Graph Template

Interactive HTML template for exploring citation networks in the browser.

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Citation Graph</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  body { margin: 0; font-family: Arial, sans-serif; }
  svg { width: 100vw; height: 100vh; }
  .node { cursor: pointer; }
  .node text { pointer-events: none; font-size: 10px; }
  .link { stroke-opacity: 0.6; }
  .tooltip {
    position: absolute; background: rgba(0,0,0,0.8); color: #fff;
    padding: 8px 12px; border-radius: 4px; font-size: 12px;
    pointer-events: none; max-width: 300px;
  }
  .legend {
    position: absolute; top: 10px; right: 10px; background: #fff;
    padding: 10px; border: 1px solid #ccc; border-radius: 4px;
  }
</style>
</head>
<body>
<div class="legend">
  <div><span style="color:#FF6B6B">&#9632;</span> Target Paper</div>
  <div><span style="color:#4ECDC4">&#9632;</span> Prior Work (cited by target)</div>
  <div><span style="color:#FFE66D">&#9632;</span> Derivative Work (cites target)</div>
</div>
<div id="tooltip" class="tooltip" style="display:none;"></div>
<script>
// === DATA: Replace this with actual citation data ===
const data = {
  nodes: [
    { id: "target", label: "Target Paper (2022)", year: 2022, citations: 150, type: "target" },
    { id: "prior_a", label: "Author A (2018)\nFoundational", year: 2018, citations: 500, type: "prior" },
    { id: "prior_b", label: "Author B (2019)\nKey Method", year: 2019, citations: 200, type: "prior" },
    { id: "deriv_x", label: "Author X (2023)\nExtension", year: 2023, citations: 30, type: "derivative" },
    { id: "deriv_y", label: "Author Y (2024)\nApplication", year: 2024, citations: 10, type: "derivative" }
  ],
  links: [
    { source: "target", target: "prior_a", type: "cites", influential: true },
    { source: "target", target: "prior_b", type: "cites", influential: false },
    { source: "deriv_x", target: "target", type: "cited-by", influential: true },
    { source: "deriv_y", target: "target", type: "cited-by", influential: false }
  ]
};

const colors = { target: "#FF6B6B", prior: "#4ECDC4", derivative: "#FFE66D" };

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("body").append("svg")
  .attr("width", width).attr("height", height);

const tooltip = document.getElementById("tooltip");

// Force simulation
const simulation = d3.forceSimulation(data.nodes)
  .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
  .force("charge", d3.forceManyBody().strength(-400))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collision", d3.forceCollide().radius(40));

// Links
const link = svg.append("g").selectAll("line")
  .data(data.links).join("line")
  .attr("class", "link")
  .attr("stroke", d => d.influential ? "#333" : "#999")
  .attr("stroke-width", d => d.influential ? 2.5 : 1.5)
  .attr("stroke-dasharray", d => d.type === "cites" ? "none" : "5,5");

// Nodes
const node = svg.append("g").selectAll("g")
  .data(data.nodes).join("g")
  .attr("class", "node")
  .call(d3.drag()
    .on("start", (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on("end", (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));

node.append("circle")
  .attr("r", d => Math.max(8, Math.sqrt(d.citations) * 1.5))
  .attr("fill", d => colors[d.type])
  .attr("stroke", d => d.type === "target" ? "#333" : "none")
  .attr("stroke-width", 2)
  .on("mouseover", (e, d) => {
    tooltip.style.display = "block";
    // Use textContent (safe) instead of innerHTML
    tooltip.textContent = d.label.replace(/\n/g, " ") + " | Year: " + d.year + " | Citations: " + d.citations;
  })
  .on("mousemove", e => {
    tooltip.style.left = (e.pageX + 10) + "px";
    tooltip.style.top = (e.pageY - 10) + "px";
  })
  .on("mouseout", () => { tooltip.style.display = "none"; });

node.append("text")
  .attr("dy", d => Math.max(8, Math.sqrt(d.citations) * 1.5) + 14)
  .attr("text-anchor", "middle")
  .selectAll("tspan")
  .data(d => d.label.split("\n"))
  .join("tspan")
  .attr("x", 0)
  .attr("dy", (d, i) => i * 12)
  .text(d => d);

// Tick
simulation.on("tick", () => {
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${d.x},${d.y})`);
});
</script>
</body>
</html>
```

## Usage Instructions

### Data Injection

Replace the `data` object in the script section with actual citation graph data. The expected schema:

```typescript
interface CitationGraphData {
  nodes: Array<{
    id: string;          // Unique paper identifier
    label: string;       // Display label (use \n for line breaks)
    year: number;        // Publication year
    citations: number;   // Citation count (used for node sizing)
    type: "target" | "prior" | "derivative";
  }>;
  links: Array<{
    source: string;      // Source node id
    target: string;      // Target node id
    type: "cites" | "cited-by";
    influential: boolean;
  }>;
}
```

### Visual Encoding

| Element | Encoding |
|---|---|
| **Node color** | Red = target, Teal = prior, Yellow = derivative |
| **Node size** | Proportional to `sqrt(citationCount)` |
| **Edge style** | Solid = cites (target→prior), Dashed = cited-by (derivative→target) |
| **Edge width** | Influential citations are thicker |
| **Edge direction** | From source to target (use stroke-dasharray to distinguish direction) |

### Customization

- **Adjust force strength**: Modify `forceManyBody().strength()` for tighter/looser layout
- **Change colors**: Edit the `colors` object
- **Add arrows**: Append `svg:defs` with marker elements for directional arrows
- **Zoom/pan**: Add `d3.zoom()` behavior to the SVG element
- **Filter nodes**: Add controls to show/hide by type, year range, or citation threshold
