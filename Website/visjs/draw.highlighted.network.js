// adapted from http://visjs.org/examples/network/exampleApplications/neighbourhoodHighlight.html
var network;
  var allNodes;
  var highlightActive = false;

  var nodesDataset = new vis.DataSet(nodes);
  var edgesDataset = new vis.DataSet(edges);

  function redrawAll() {
    var container = document.getElementById('mynetwork');
    var options = {
      nodes: {
        shape: 'dot',
        scaling: {
          min: 10,
          max: 30,
          label: {
            min: 8,
            max: 30,
            drawThreshold: 12,
            maxVisible: 20
          }
        },
        font: {
          size: 12,
          face: 'Tahoma'
        }
      },
      edges: {
        width: 0.15,
        color: 'darkgrey',
        smooth: {
          type: 'continuous'
        }
      },
      physics: false,
      interaction: {
        tooltipDelay: 200,
        hideEdgesOnDrag: true
      },
      configure: {
        enabled:false,
        showButton: true
      }
    };
    var data = {nodes:nodesDataset, edges:edgesDataset}


    network = new vis.Network(container, data, options);

    // get a JSON object
    allNodes = nodesDataset.get({returnType:"Object"});

    network.on("click",onClick);
    network.on("doubleClick",switchToLocalNeighbours)
  }


//click suppress when doubleclicking: cf.: https://github.com/almende/vis/issues/203
  var doubleClickTime = 0;
  var threshold = 200;

  function onClick(params) {
    var t0 = new Date();
    if (t0 - doubleClickTime > threshold) {
        setTimeout(function () {
            if (t0 - doubleClickTime > threshold) {
                neighbourhoodHighlight(params);
            }
        },threshold);
    }
  }

  function switchToLocalNeighbours(params){
    if (params.nodes.length > 0){
      var selectedId = params.nodes[0];
      var selectedName = allNodes[selectedId].label;
      if (!selectedName){
        selectedName = allNodes[selectedId].hiddenLabel;
      }
      selectedName = selectedName.replace(/ /g,'+');  //TBD better escaping is needed
      var ref = '?node='+selectedName
      window.location.href = "CRM_function_ring.html" + ref;
    } else {
      window.location.href = "CRM_function_ring.html";
    }

  }

  function neighbourhoodHighlight(params) {
    // if something is selected:
    if (params.nodes.length > 0) {
      highlightActive = true;
      var i,j;
      var selectedNode = params.nodes[0];
      var degrees = 2;

      // mark all nodes as hard to read.
      for (var nodeId in allNodes) {
        allNodes[nodeId].color = 'rgba(200,200,200,0.5)';
        if (allNodes[nodeId].hiddenLabel === undefined) {
          allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
          allNodes[nodeId].label = undefined;
        }
      }
      var connectedNodes = network.getConnectedNodes(selectedNode);
      var allConnectedNodes = [];

      // get the second degree nodes
      for (i = 1; i < degrees; i++) {
        for (j = 0; j < connectedNodes.length; j++) {
          allConnectedNodes = allConnectedNodes.concat(network.getConnectedNodes(connectedNodes[j]));
        }
      }

      // all second degree nodes are colored in black and get their label back
      for (i = 0; i < allConnectedNodes.length; i++) {
        allNodes[allConnectedNodes[i]].color = 'black';
        if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
          allNodes[allConnectedNodes[i]].label = allNodes[allConnectedNodes[i]].hiddenLabel;
          allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
        }
      }

      // all first degree nodes get their own color and their label back
      for (i = 0; i < connectedNodes.length; i++) {
        allNodes[connectedNodes[i]].color = undefined;
        if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
          allNodes[connectedNodes[i]].label = allNodes[connectedNodes[i]].hiddenLabel;
          allNodes[connectedNodes[i]].hiddenLabel = undefined;
        }
      }

      // the main node gets its own color and its label back
      allNodes[selectedNode].color = undefined;
      if (allNodes[selectedNode].hiddenLabel !== undefined) {
        allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
        allNodes[selectedNode].hiddenLabel = undefined;
      }
    }
    else if (highlightActive === true) {
      // reset all nodes
      for (var nodeId in allNodes) {
        allNodes[nodeId].color = undefined;
        if (allNodes[nodeId].hiddenLabel !== undefined) {
          allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
          allNodes[nodeId].hiddenLabel = undefined;
        }
      }
      highlightActive = false
    }

    // transform the object into an array
    var updateArray = [];
    for (nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodesDataset.update(updateArray);
  }

  redrawAll()
