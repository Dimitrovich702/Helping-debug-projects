const svg = createNewSvg('#gradient', '100%', '100%', d3);

const gradientAndXAxis = createNewGroup(svg);
gradientAndXAxis.attr('transform', 'translate(0, 24)');

const gradient = gradientAndXAxis
  .append('defs')
  .append('linearGradient')
  .attr('id', 'bar-gradient')
  .attr('x1', '0%')
  .attr('y1', '0%')
  .attr('x2', '100%')
  .attr('y2', '0%');

const gradientSettings = [{ offset: '0%', stopColor: 'blue' }, { offset: '100%', stopColor: 'red' }]; // the list
gradient.selectAll('stop')
  .data(gradientSettings)
  .enter()
  .append('stop')
  .attr('offset', d => d.offset)
  .attr('stop-color', d => d.stopColor);

gradientAndXAxis
  .append('rect')
  .attr('x', 0)
  .attr('y', 0)
  .attr('width', '100%')
  .attr('height', 10)
  .style('fill', 'url(#bar-gradient)');

const margin = { left: 20, right: 20 }; // idk more 
const width = 800;
const height = 200;
const xScale = d3.scaleLinear().range([margin.left, width - margin.right]);
let xAxisGroup = createNewGroup(gradientAndXAxis).attr('class', 'x-axis').attr('transform', 'translate(10, 10)');

xAxisGroup.selectAll('.tick line').remove();

xAxisGroup
  .selectAll('.tick text')
  .style('fill', 'white')
  .style('font-size', '12px');

function createNewSvg(elementId, width, height, d3) {
  return d3.select(elementId).append('svg').attr('width', width).attr('height', height);
}
//idk when u paying me
function createNewGroup(svg) {
  return svg.append('g');
}

updateXAxis([1, ]);

function updateXAxis(range) {
  const svgWidth = parseFloat(svg.style('width').replace('px', ''));

  xScale.domain(range).range([0, svgWidth - margin.left]);

  const xAxis = d3.axisBottom(xScale).ticks(range[1]);

  xAxisGroup.transition().duration(500).call(xAxis);
}
