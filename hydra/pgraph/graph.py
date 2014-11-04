# _*_ coding: utf-8 _*_
# This project is fllowing Pedram Amini's sulley, the core part is sully,
#  some part overwrite by me.
# See detail sulley form https://github.com/OpenRCE/sulley
# If there is a problem, please contact tutengfei.kevin@gmail.com
# Thank you!
"""
@the first author: Pedram Amini
@he second author: tutengfei.kevin
@contact: tutengfei.kevin@gmail.com
@source: https://github.com/tutengfei/hydra
"""

from hydra.pgraph.edge import Edge
from hydra.pgraph.node import Node


class Graph:
    """

    """
    #TODO Add support for clusters
    #TODO Potentially swap node list with a node dictionary for increased
    #  performance
    def __init__(self, id=None):
        self.id = id
        self.clusters = []
        self.nodes = {}
        self.edges = {}

    def add_cluster(self, cluster):
        """
        add a pgraph cluster to the graph
        :param cluster: pGRAPH Cluster
        :return: cluster: Cluster to add to graph
        """
        self.clusters.append(cluster)
        return self

    def add_edge(self, edge, prevent_dups=True):
        """
        Add a Pgraph edge to the graph. Ensures a node exists for both the source and destination of the side.
        :param edge: pGRAPH Edge, Edge to add graph
        :param prevent_dups: Boolean
        :return:
        """
        #new property in python3
        if prevent_dups:
            if edge.id in self.edges:
                return self

        if self.find_node("id", edge.src) and self.find_node("id", edge.dst):
            self.edges[edge.id] = edge

        return self

    def add_graph(self, anthor_graph):
        #TODO ADD SUPPORT FOR CLUSTERS, SEE graph_cat()
        """
        Alias of graph_cat(). Concatenate the other graph into the current one.
        :param anthor_graph: pgraph graph
        :return: Graph to concatenate into this one.

        """
        return self.graph_cat(anthor_graph)

    def add_node(self, node):
        """

        :param node:
        :return:
        """
        node.number = len(self.nodes)
        if node.id not in self.nodes:
            self.nodes[node.id] = node

        return self

    def del_cluster(self, id):
        """
        Remove a cluster from the graph
        :param id: Mixed
        :return: Identifier of cluster to remove from graph
        """
        for cluster in self.clusters:
            if cluster.id == id:
                self.clusters.remove(cluster)
                break

        return self

    def del_edge(self, id=None, src=None, dst=None):
        """

        :param id:
        :param src:
        :param dst:
        :return:
        """

        if not id:
            id = (src << 32) + dst

        if id in self.edges:
            del self.edges[id]

        return self

    def del_graph(self, other_graph):
        """

        :param other_graph:
        :return:
        """
        pass


