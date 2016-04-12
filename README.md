CONTENTS OF THIS FILE
---------------------
   
 * Introduction
 * Requirements
 * Contents of files


INTRODUCTION
------------

This workflow visualizes the network of Dutch pensions funds board members. It was written in January and February 2016 by Michael E. Rose.

Execute python scripts in descending order to generate .js files (after adapting local variables) and open .html files in any browser.

REQUIREMENTS
------------

The following python packages are required:

* Python 2.7
* NetworkX (http://networkx.github.io/) and all dependents
* PyGraphviz (https://pygraphviz.github.io/)
* Webbrowser that allows JS

CONTENTS OF FILES
-----------------

* [`002_generate_networks_CRM.py`](002_generate_networks_CRM.py): Generate .gexf files using .csv file(s) from "CRM". Only the cleaned files has been used, so no harmonizing of fielnames is used. Person's board functions are roughly consolidated into three categories without remainer.
* [`005_create_lists.py`](005_create_lists.py): Generate list as .csv on individual board members, their unique identifier, their clustering coefficient, their rank according to their betweenness centrality, their rank according to their eigenvector centrality and their board positions and functions. Easy to extend.
* [`010_get_website_network.py`](010_get_website_network.py): Generate three .js files per network providing the data needed for visualization. Two .js files generate a network view and differ by the group content (betweenness centrality and function). Node positioning according to a Fruchterman-Reingold algorithm. Node information is taken from the node parameter `meta` The remaining network generates a ring view and contains only connections.
* .html files in [`./Website`](./Website): There are two libraries that we use: The first is [vis.js](http://visjs.org/) and used to visualize large networks. [`./Website/visjs/draw.highlighted.network.js`](./Website/visjs/draw.highlighted.network.js) steers the behavior to a certain degree: Disable physics, highlight on click, etc. The other library is [`d3plus`](http://d3plus.org/) and used to visualize ring networks. A node as starting (focal) node should be provided.


