   // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 200 - margin.top - margin.bottom;
        height = 200 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#my_graph")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    let data = {
  "nodes": [
    {
      "id": 1,
      "name": "A"
    },
    {
      "id": 2,
      "name": "B"
    },
    {
      "id": 3,
      "name": "C"
    }
  ],
  "links": [

    {
      "source": 1,
      "target": 2,
        "score": 10
    },
    {
      "source": 1,
      "target": 3,
        "score": 20
    },
    {
      "source": 1,
      "target": 2,
        "score": 30
    }
  ]
}


        // Initialize the links
        var link = svg
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .style("stroke", "#aaa")
            .style("stroke-width", function(d) {return `${d.score/10}px`})

   var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .style("background", "#000")
    .style("color", "white")
    .text("a simple tooltip");

        // Initialize the nodes
        var node = svg
            .selectAll("circle")
            .data(data.nodes)
            .enter()
            .append("g")
            .attr("transform", function(d){return "translate("+d.x+",80)"})
            .append("circle")
            .attr("r", 10)
            .style("fill", "#39f")
            .on("mouseover", function(d){tooltip.text(d.name); return tooltip.style("visibility", "visible");})
      .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

        // Let's list the force we wanna apply on the network
        var simulation = d3.forceSimulation(data.nodes)                 // Force algorithm is applied to data.nodes
            .force("link", d3.forceLink()                               // This force provides links between nodes
                .id(function(d) { return d.id; })                     // This provide  the id of a node
                .links(data.links)                                    // and this the list of links
            )
            .force("charge", d3.forceManyBody().strength(-600))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
            .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the svg area
            .on("end", ticked);

        // This function is run at each iteration of the force algorithm, updating the nodes position.
        function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("cx", function (d) { return d.x+6; })
                .attr("cy", function(d) { return d.y-6; })
        }


        let my_graph = document.getElementById('my_graph');
        let cells = my_graph.getElementsByTagName('g');

        for (let cell of cells) {

        }

