// ||================================||
// || D3 GRAPH                       ||
// ||================================||

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
    .attr('fill', 'white');

var vis = firstG
  .append('svg:g')

function rescale() {
  vis.attr("transform", d3.event.transform)
}

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
      .attr("class", ".nodes")
      .attr("r", 2)
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

// ||================================||
// || NODE SEARCHING                 ||
// ||================================||

var fuseOptions = {
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

var currentSelectedNodeId = ""

function getNodeById(nodeId) {
  var nodeId = nodeId.replace("/","_")
  return d3.select('#id-' + nodeId)
}

function initSelectBox(nodeList) {
  var results = nodeList.map(function(elt){
    var o = Object.assign({}, elt);
    o.text = elt.name;
    o.id = elt.id;
    return o;
  })
  // This relies on the first elt being representative of them all
  // Todo: Find better way to catagorize in JS or mandate labels in python
  var props = Object.keys(nodeList[0].properties).filter(function(elt) {
    return $.isNumeric(nodeList[0].properties[elt])
  })

  var propDict = props.map(function(key) {
    var propData = {}
    var max = -Infinity
    var min = Infinity
    nodeList.forEach(function(node) {
      propData[node.id] = node.properties[key]
      if (node.properties[key] > max) {
        max = node.properties[key]
      }
      if (node.properties[key] < min) {
        min = node.properties[key]
      }
    })
    var prop = {
      propData: propData,
      max: max,
      min: min,
      text: key,
      id: key
    }
    return prop
  })

  $("#node-search").select2({
    placeholder: "Select a node...",
    allowClear: true,
    data: results,
    dropdownParent: $("#search")
  });

  $("#property-search").select2({
    placeholder: "Select a property...",
    allowClear: true,
    data: propDict,
    dropdownParent: $("#sizing")
  });
}

$("#node-search").on("select2:select", function(e) {
  var nodeData = e.params.data
  getNodeById(nodeData.id).attr("class", "nodes selected")
  if (currentSelectedNodeId != "") {
    getNodeById(currentSelectedNodeId).attr("class", "nodes")
  }
    currentSelectedNodeId = nodeData.id
})

$("#property-search").on("select2:select", function(e) {
  var data = e.params.data

  range1 = [data.min, data.max]
  squaredRange2 = [1, 25]

  function convertRange( value, r1, r2 ) { 
    return ( value - r1[0] ) * ( r2[1] - r2[0] ) / ( r1[1] - r1[0] ) + r2[0];
  }

  for (var key in data.propData) {
    if (data.propData.hasOwnProperty(key)) {
      var outputRadius = convertRange(data.propData[key], range1, squaredRange2)
      getNodeById(key).attr("r", Math.sqrt(outputRadius))
    }
  }

})

$(".left-button").on("mouseover", function(e) {
  var targetId = e.currentTarget.id.split("-")[0]
  $("#" + targetId + ">.select2").css("right", "0px")
  $("#" + targetId).animate({
    right: "40px",
  }, 200, function(){})
  $("#" + targetId + ">.select2").animate({
    opacity: 100,
  }, 200, function(){})
})

$(".left-control").on("mouseleave", function(e) {
  var targetId = e.currentTarget.id
  console.log("leaving:", e)
  $("#" + targetId).animate({
    right: "-160px",
  }, 200, function(){
    $("#" + targetId + ">.select2").css("right", "-300px")
  })
  $("#" + targetId + ">.select2").animate({
    opacity: 0,
  }, 200, function(){})
  $("#" + targetId + ">select").select2("close")
})

// ||================================||
// || GRAPH TIME CONTROL             ||
// ||================================||

$(".right-button").on("click", function(e) {
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






