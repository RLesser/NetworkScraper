// ||================================||
// || D3 GRAPH                       ||
// ||================================||

var width = parseInt(d3.select("#chart").style("width"), 10)
    height = parseInt(d3.select("#chart").style("height"), 10);

var selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null;

var defaultRadius = 2,
    defaultColor = "lightgray"

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

d3.json("force.json", function(error, graph) {
  if (error) throw error;

  nodeList = graph.nodes
  // console.log(nodeList)
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
      .attr("id", function(d) {return d.id})
      .attr("fill", defaultColor)
      .attr("r", defaultRadius)
      .attr("size", "")
      .attr("category", "")
      .attr("name", function(d) { return d.name })
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
  if (!d3.event.active) simulation.alphaTarget(0.3);
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
// || INITIALIZATION FUNCTIONS       ||
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
  return d3.select('#' + $.escapeSelector(nodeId))
}

function getAllNodes() {
  return $(".nodes").children()
}

function setNodeTitle(nodeObj) {
  var size = nodeObj.attr("size")
  var category = nodeObj.attr("category")
  var name = nodeObj.attr("name")
  var titleStr = name
  if (size != "") {
    titleStr += " [" + size + "]"
  }
  if (category != "") {
    titleStr += " - " + category
  }
  nodeObj.select("title").text(titleStr)
}

function getNumericProperties(nodeList) {
  var numericProps = Object.keys(nodeList[0].properties).filter(function(elt) {
    return $.isNumeric(nodeList[0].properties[elt])
  })

  var numericPropDict = numericProps.map(function(key) {
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

  return numericPropDict
}

var categorySortedLists = {}

function getCategoricalProperties(nodeList) {
  var nonNumericProps = Object.keys(nodeList[0].properties).filter(function(elt) {
    return !$.isNumeric(nodeList[0].properties[elt])
  })

  // Get object with keys as nodes and values as category value
  // Also create an object with the count of each category value
  var nonNumericPropDict = nonNumericProps.map(function(key) {
    var propData = {}
    var countKeeper = {}
    nodeList.forEach(function(node) {
      var value = node.properties[key]
      propData[node.id] = value
      if (countKeeper[value] == undefined) {
        countKeeper[value] = 1
      } else {
        countKeeper[value] += 1
      }
    })

    // category values are sorted by number of occurences
    var sortedList = Object.keys(countKeeper).sort(function(a, b) {
      return -(countKeeper[a] - countKeeper[b])
    })

    var sortedPairs = sortedList.map(function(key) {
      return [key, countKeeper[key]]
    })

    // If more than a third of nodes are unique categories, invalid category
    if (sortedList.length * 3 >= nodeList.length) {
      return "Invalid Category"
    }

    categorySortedLists[key] = sortedPairs

    // for each node, find the index of value in the sorted list, get corresponding color

    var nodeIdToColor = {}
    for (var nodeId in propData) {
      color = COLOR_LIST[sortedList.indexOf(propData[nodeId].toString())]
      nodeIdToColor[nodeId] = color
    }
    
    // console.log(nodeIdToColor)    

    var category = {
      catData: nodeIdToColor,
      catName: propData, 
      text: key,
      id: key
    }

    return category
  })

  nonNumericPropDict = nonNumericPropDict.filter(function(elt) {
    return !(elt == "Invalid Category")
  })

  return nonNumericPropDict
}

function initSelectBox(nodeList) {
  var results = nodeList.map(function(elt){
    var o = Object.assign({}, elt);
    o.text = elt.name;
    o.id = elt.id;
    return o;
  })

  // console.log(nodeList)
  if (nodeList[0].hasOwnProperty("properties")) {
    var numericData = getNumericProperties(nodeList)

    // Note: numeric properties that are to be treated categorically must be strings, not numbers
    var categoricalData = getCategoricalProperties(nodeList)
  } else {
    var numericData = categoricalData = {
      text: "No Properties Found",
      selectable: false
    }
  }
  


  $("#node-search").select2({
    placeholder: "Select a node...",
    allowClear: true,
    data: results,
    dropdownParent: $("#search")
  });

  $("#property-search").select2({
    placeholder: "Select a property...",
    allowClear: true,
    data: numericData,
    dropdownParent: $("#sizing")
  });

  $("#category-search").select2({
    placeholder: "Select a category...",
    allowClear: true,
    data: categoricalData,
    dropdownParent: $("#coloring")
  });
}

// ||================================||
// || NODE CONTROL INTERACTION       ||
// ||================================||

$("#node-search").on("select2:select", function(e) {
  var nodeData = e.params.data
  var node = getNodeById(nodeData.id)
  node.attr("class", "nodes selected")
  if (currentSelectedNodeId != "") {
    node.attr("class", "nodes")
  }
    currentSelectedNodeId = nodeData.id
})

$("#node-search").on("select2:unselect", function(e) {
  getNodeById(currentSelectedNodeId).attr("class", "nodes")
})

$("#property-search").on("select2:select", function(e) {
  var data = e.params.data

  range1 = [data.min, data.max]
  squaredRange2 = [4, 36]

  function convertRange( value, r1, r2 ) { 
    return ( value - r1[0] ) * ( r2[1] - r2[0] ) / ( r1[1] - r1[0] ) + r2[0];
  }

  for (var key in data.propData) {
    if (data.propData.hasOwnProperty(key)) {
      var node = getNodeById(key)
      var outputRadius = convertRange(data.propData[key], range1, squaredRange2)
      node.attr("r", Math.sqrt(outputRadius))
      node.attr("size", data.propData[key])
      setNodeTitle(node)
    }
  }
})

$("#property-search").on("select2:unselect", function(e) {
  for (var key in e.params.data.propData) {
    if (e.params.data.propData.hasOwnProperty(key)) {
      var node = getNodeById(key)
      node.attr("r", defaultRadius)
      node.attr("size", "")
      setNodeTitle(node)
    }
  }
})

$("#category-search").on("select2:select", function(e) {
  var data = e.params.data
  // a little hacky but alright
  $.when(
    populateLegend(data.id)
  ).done(function() {
    $("#coloring-legend").removeClass("hidden")
  })
  // console.log(data)
  for (var key in data.catData) {
    if (data.catData.hasOwnProperty(key)) {
      var node = getNodeById(key)
      node.attr("fill", data.catData[key])   
      node.attr("category", data.catName[key])
      setNodeTitle(node) 
    }
  }
})

$("#category-search").on("select2:unselect", function(e) {
  $("#coloring-legend").addClass("hidden")
  for (var key in e.params.data.catData) {
    if (e.params.data.catData.hasOwnProperty(key)) {
      var node = getNodeById(key)
      node.attr("fill", defaultColor)
      node.attr("category", "")
      setNodeTitle(node) 
    }
  }
})


$(".left-button").on("mouseover", function(e) {
  var targetId = e.currentTarget.id.split("-")[0]
  $("#" + targetId + ">.select2").css("pointer-events", "initial")
  $("#" + targetId).animate({
    right: "40px",
  }, 200, function(){})
  $("#" + targetId + ">.select2").animate({
    opacity: 100,
  }, 200, function(){})
})

$(".left-control").on("mouseleave", function(e) {
  var targetId = e.currentTarget.id
  $("#" + targetId + ">.select2").css("pointer-events", "none")
  $("#" + targetId).animate({
    right: "-160px",
  }, 200, function(){})
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

// ||================================||
// || NODE LEGEND CONTROL            ||
// ||================================||

var generateLegendElement = function(elementData, color) {
  var elementHTML = [
   "<div class='legend-elt'>",
   "  <div class='legend-color-num' style='background-color:" + color + ";'>",
        elementData[1],
   "  </div>",
   "  <div class='legend-value-name'>",
        elementData[0],
   "  </div>",
   "</div>",
   ""
  ].join("\n")
  return elementHTML
}

var populateLegend = function(category) {
  $("#coloring-legend").css("height","20px")
  $("#coloring-legend").css("width","20px")
  var contentDiv = $("#coloring-legend>.legend-content")
  contentDiv.html("")
  var categoryData = categorySortedLists[category]
  var colorIdx = 0
  categoryData.forEach(function(elt) {
    var color = COLOR_LIST[colorIdx]
    contentDiv.append(generateLegendElement(elt, color))
    colorIdx += 1
  })
}

var fadeNode = function(mode, valuesToAffect, exceptions) {
  var action = ""
  if (mode == "fade") {
    action = function(node) { node.addClass("faded-node") }
  } else {
    action = function(node) { node.removeClass("faded-node") }
  }

  console.log(valuesToAffect, exceptions)
  $.each(getAllNodes(), function(nodeIdx, nodeVal) {
    var node = $(nodeVal)
    console.log(node.attr("category"))
    if (valuesToAffect == "all") {
      if ($.inArray(node.attr("category"), exceptions)) {
        console.log(mode, "all")
        action(node)
      }
    } else if (!$.inArray(node.attr("category"), valuesToAffect)) {
      console.log(mode, "specifically")
      action(node)
    }
  })
}


$(".bottom-legend").hover(function(e) {
  if (!$(this).children(".legend-bar").hasClass("click-anim")) {
    $(this).stop(true).animate({
      width: "160px"
    }, 200, function() {
      if (!$(this).children(".legend-bar").hasClass("expanded")) {
        $("#legend-expand").fadeIn(50)
      }
    })
  }
}, function(e) {
  if (!$(this).children(".legend-bar").hasClass("expanded") &&
      !$(this).children(".legend-bar").hasClass("click-anim")) {
    $(this).stop(true).animate({
      width: "20px"
    }, 200, function() {})
    $("#legend-expand").fadeOut(50)
  }
})

$(".legend-bar").click(function(e) {
  $(this).addClass("click-anim")
  if (!$(this).hasClass("expanded")) {
    $(this).addClass("expanded")
    $.when($("#legend-expand").fadeOut(50)).done(function() {
      $("#legend-retract").fadeIn(50)    
    })
    $(this).parent().animate({
      height: "240px"
    }, 200, function() {
      $(this).children(".legend-bar").removeClass("click-anim")
    })
    $(this).parent().children(".legend-content").animate({
      height: "220px"
    }, 200, function() {})
  } else {
    $(this).removeClass("expanded")
    $.when($("#legend-retract").fadeOut(50)).done(function() {
      $("#legend-expand").fadeIn(50)    
    })
    $(this).parent().animate({
      height: "20px"
    }, 200, function() {
      $("#legend-expand").fadeOut(50)
      $(this).animate({
        width: "20px"
      }, 200, function() {
        $(this).children(".legend-bar").removeClass("click-anim")
      })
    })
    $(this).parent().children(".legend-content").animate({
      height: "0px"
    }, 200, function() {})
  }
})

$(".legend-content").on("click", ".legend-elt", function(e) {
  $(this).toggleClass("selected-elt")
  var currentCategory = $(this).children(".legend-value-name").text()
  if ($(this).hasClass("selected-elt")) {
    $(this).parent().attr("num-selected", 
                          function(i, oldval) { return parseInt(oldval, 10) + 1})
    if ($(this).parent().attr("num-selected") == 1) {
      console.log("only one selected")
      fadeNode("fade", "all", [$.trim(currentCategory)])
    } else {
      fadeNode("unfade", [$.trim(currentCategory)], [])
    }

  } else {
    $(this).parent().attr("num-selected", 
                          function(i, oldval) { return parseInt(oldval, 10) - 1})
    if ($(this).parent().attr("num-selected") == 0) {
      console.log("zero selected")
      fadeNode("unfade", "all", [])
    } else {
      fadeNode("fade", [$.trim(currentCategory)], [])
    }
  }
})






//Color list from here: https://jnnnnn.blogspot.com.au/2017/02/distinct-colours-2.html

COLOR_LIST = ["#1b70fc", "#faff16", "#d50527", "#158940", "#f898fd", 
              "#24c9d7", "#cb9b64", "#866888", "#22e67a", "#e509ae", 
              "#9dabfa", "#437e8a", "#b21bff", "#ff7b91", "#94aa05", 
              "#ac5906", "#82a68d", "#fe6616", "#7a7352", "#f9bc0f", 
              "#b65d66", "#07a2e6", "#c091ae", "#8a91a7", "#88fc07", 
              "#ea42fe", "#9e8010", "#10b437", "#c281fe", "#f92b75", 
              "#07c99d", "#a946aa", "#bfd544", "#16977e", "#ff6ac8", 
              "#a88178", "#5776a9", "#678007", "#fa9316", "#85c070", 
              "#6aa2a9", "#989e5d", "#fe9169", "#cd714a", "#6ed014", 
              "#c5639c", "#c23271", "#698ffc", "#678275", "#c5a121", 
              "#a978ba", "#ee534e", "#d24506", "#59c3fa", "#ca7b0a", 
              "#6f7385", "#9a634a", "#48aa6f", "#ad9ad0", "#d7908c", 
              "#6a8a53", "#8c46fc", "#8f5ab8", "#fd1105", "#7ea7cf", 
              "#d77cd1", "#a9804b", "#0688b4", "#6a9f3e", "#ee8fba", 
              "#a67389", "#9e8cfe", "#bd443c", "#6d63ff", "#d110d5", 
              "#798cc3", "#df5f83", "#b1b853", "#bb59d8", "#1d960c", 
              "#867ba8", "#18acc9", "#25b3a7", "#f3db1d", "#938c6d", 
              "#936a24", "#a964fb", "#92e460", "#a05787", "#9c87a0", 
              "#20c773", "#8b696d", "#78762d", "#e154c6", "#40835f", 
              "#d73656", "#1afd5c", "#c4f546", "#3d88d8", "#bd3896", 
              "#1397a3", "#f940a5", "#66aeff", "#d097e7", "#fe6ef9", 
              "#d86507", "#8b900a", "#d47270", "#e8ac48", "#cf7c97", 
              "#cebb11", "#718a90", "#e78139", "#ff7463", "#bea1fd"]




