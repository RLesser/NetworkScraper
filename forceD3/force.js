// Zoom stuff

console.log(d3.select("#chart").style("width"))
console.log(d3.select("#chart").style("height"))

var width = parseInt(d3.select("#chart").style("width"), 10)
    height = parseInt(d3.select("#chart").style("height"), 10);

var selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null;

var outer = d3.select("#chart")
  .append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", "all");

var vis = outer
  .append('svg:g')
    .call(d3.zoom().on("zoom", rescale))
    .on("dblclick.zoom", null)
  .append('svg:g')
    .on("mousedown", mousedown);

vis.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'white');

function mousedown() {
  // if (!mousedown_node && !mousedown_link) {
  //   // allow panning if nothing is selected
  //   vis.call(d3.behavior.zoom().on("zoom"), rescale);
  //   return;
  // }
  console.log('test')
  vis.call(d3.zoom().on("zoom"), rescale);
  return;
}


function rescale() {
  vis.attr("transform", d3.event.transform);
}

// var min_zoom = 0.1;
// var max_zoom = 7;
// var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(1).strength(1))
    .force("charge", d3.forceManyBody().strength(-20).distanceMax(220))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .alphaDecay(0.0002);


var nodeList = []

d3.json("force.json", function(error, graph) {
  if (error) throw error;

  nodeList = graph.nodes

  var link = vis.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = vis.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", 2)
      .attr("fill", function(d) { return d3.rgb(d.color); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  node.append("title")
      .text(function(d) { return d.name; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  }
});

function dragstarted(d) {
  console.log("drag started on", d)
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}


//impliment fusejs fuzzy search eventually

var options = {
  shouldSort: true,
  threshold: 0.6,
  location: 0,
  distance: 100,
  maxPatternLength: 32,
  minMatchCharLength: 1,
  keys: [
    "id",
    "name"
]
};

$(document).ready(function() {
  console.log("test")
  results = nodeList.map(function(elt){
    var o = Object.assign({}, elt);
    o.text = elt.name;
    o.id = elt.id;
    return o;
  })
  console.log(results)
  $("#node-search").select2({
    placeholder: "Select a node...",
    allowClear: true,
    data: results
  });
  $("#node-search").select2("Robert Lesser")
});




