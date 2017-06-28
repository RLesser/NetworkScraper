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

var firstG = outer
  .append('svg:g')
    .call(d3.zoom().on("zoom", rescale))
    .on("dblclick.zoom", null)

firstG.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'lightblue');

var vis = firstG
  .append('svg:g')
    .on("mousedown", mousedown)
    .on("wheel", scroll)

var justAfterMouseDown = false
var justAfterScroll = false

function mousedown() {
  console.log("mouse down!")
  justAfterMouseDown = true
}

function scroll() {
  console.log("mouse scroll!")
  justAfterScroll = true
}

function rescale() {
  console.log("mousedown?", justAfterMouseDown)
  // if (justAfterMouseDown) {
  //   d3.event.transform.x = -1*d3.event.transform.x
  //   d3.event.transform.y = -1*d3.event.transform.y
  // }
  // if (justAfterScroll) {
  //   d3.event.transform.k = 1/d3.event.transform.k
  // }
  vis.attr("transform", d3.event.transform)
  //console.log("new round")
  //console.log("before:", d3.event.transform)
  // invTrans = d3.event.transform
  // invTrans.k = 1/d3.event.transform.k
  // invTrans.x = -1*d3.event.transform.x
  // invTrans.y = -1*d3.event.transform.y
  // console.log("after:", invTrans)
  //d3.select("rect").attr("transform", d3.event.transform.invert())
  justAfterMouseDown = false
  justAfterScroll = false
}

// var min_zoom = 0.1;
// var max_zoom = 7;
// var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(1).strength(1))
    .force("charge", d3.forceManyBody().strength(-20))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .alphaDecay(0.0002);


var nodeList = []

var graphPaused = false

d3.json("force.json", function(error, graph) {
  if (error) throw error;

  nodeList = graph.nodes
  initSelectBox(nodeList)

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
      .attr("id", function(d) {return ("id-" + d.id).replace("/","_")})
      .attr("r", 2)
      .attr("fill", function(d) { return d3.rgb(d.color); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  console.log(node)

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

function highlightNode(nodeId) {
  nodeId = nodeId.replace("/","_")
  console.log('#id-' + nodeId)
  var node = d3.select('#id-' + nodeId)
  node.attr("class", "nodes selected")
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

function initSelectBox(nodeList) {
  console.log(nodeList)
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
    data: results,
    dropdownParent: $("#search")
  });
}

$("#node-search").on("select2:select", function(e) {
  console.log(e.params.data)
  var nodeData = e.params.data
  highlightNode(nodeData.id)
})

$("#search-button").on("mouseover", function(e) {
  $("#search").animate({
    right: "40px"
  }, 200, function(){})
  $(".select2").animate({
    opacity: 100
  }, 200, function(){})
})

$("#search").on("mouseleave", function(e) {
  $("#search").animate({
    right: "-160px"
  }, 200, function(){})
  $(".select2").animate({
    opacity: 0
  }, 200, function(){})
  $("select").select2("close")
})

$(".button").on("click", function(e) {
  if (e.target.id == "pause-button") {
    $(e.target).css("display", "none")
    $("#play-button").css("display", "initial")
    simulation.stop()
  } else if (e.target.id == "play-button") {
    $(e.target).css("display", "none")
    $("#pause-button").css("display", "initial")
    simulation.restart()
  }
})




