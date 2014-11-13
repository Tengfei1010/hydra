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
import copy

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
        return self.graph_sub(other_graph)

    def del_node(self, id):
        """

        :param id:
        :return:
        """
        if id in self.nodes:
            del self.nodes[id]

        return self

    def edges_from(self, id):
        """

        :param id:
        :return:
        """
        return [edge for edge in self.edges.values() if edge.src == id]

    def edges_to(self, id):
        """

        :param id:
        :return:
        """
        return [edge for edge in self.edges.values() if edge.dst == id]

    def find(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        for cluster in self.clusters:
            if hasattr(cluster, attribute):
                if getattr(cluster, attribute) == value:
                    return cluster

        return None

    def find_cluster_by_node(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        for cluster in self.clusters:
            for node in cluster:
                if hasattr(node, attribute):
                    if getattr(node, attribute) == value:
                        return cluster
        return None

    def find_edge(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        if attribute == "id" and value in self.edges:
            return self.edges[value]
        else:
            for edge in self.edges.values():
                if hasattr(edge, attribute):
                    if getattr(edge, attribute) == value:
                        return edge

        return None

    def find_node(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """

        if attribute == "id" and value in self.nodes:
            return self.nodes
        else:
            for node in self.nodes.values():
                if hasattr(node, attribute):
                    if getattr(node, attribute) == value:
                        return node

        return None

    def graph_cat(self, other_graph):
        """

        :param otther_graph:
        :return:
        """
        for other_node in other_graph.nodes.values():
            self.add_node(other_node)

        for other_edge in other_graph.edges.values():
            self.add_edge(other_edge)

        return self

    def graph_down(self, from_node_id, max_depth=-1):
        """

        :param from_node_id:
        :param max_depth:
        :return:
        """
        down_graph = Graph()
        from_node = self.find_node("id", from_node_id)

        if not from_node:
            print("Unable to resolve node %08x" % from_node_id)
            raise Exception

        levels_to_process = []
        current_depth = 1

        levels_to_process.append([from_node])

        for level in levels_to_process:
            next_level = []
            if current_depth > max_depth != -1:
                break

            for node in level:
                try:
                    down_graph.add_node(copy.copy(node))

                    for edge in self.edges_from(node, id):
                        to_add = self.find_node("id", edge.dst)

                        if not down_graph.find_node("id", edge.dst):
                            next_level.append(to_add)

                        down_graph.add_node(copy.copy(to_add))
                        down_graph.add_edge(copy.copy(edge))

                except copy.error:
                    print("There is exception in graph_down copy node.")
                    raise Exception

            if next_level:
                levels_to_process.append(next_level)
            current_depth += 1

            return down_graph

    def graph_intersect(self, other_graph):
        """

        :param other_graph:
        :return:
        """
        for node in self.nodes.values():
            if not other_graph.find_node("id", node.id):
                self.del_node(node.id)

        for edge in self.edges.values():
            if not other_graph.find_edge("id", edge.id):
                self.del_edge(edge.id)

        return self

    def graph_proximity(self, center_node_id, max_depth_up=2, max_depth_down=2):
        """

        :param center_node_id:
        :param max_depth_ip:
        :param max_depth_down:
        :return:
        """
        prox_graph = self.graph_down(center_node_id, max_depth_down)
        prox_graph.add_graph(self.graph_up(center_node_id, max_depth_up))

        return prox_graph

    def graph_sub(self, other_graph):
        """

        :param other_graph:
        :return:
        """
        for other_node in other_graph.nodes.values():
            self.del_node(other_node.id)

        for other_edge in other_graph.edges.values():
            self.del_edge(other_edge.id)

        return self

    def graph_up(self, from_node_id, max_depth=-1):
        """

        :param from_node_id:
        :param max_depth:
        :return:
        """
        up_graph = Graph()
        from_node = self.find_node("id", from_node_id)

        levels_to_process = []
        current_depth = 1

        levels_to_process.append([from_node])

        for level in levels_to_process:
            next_level = []

            if current_depth > max_depth != -1:
                break
            for node in level:
                try:
                    up_graph.add_node(copy.copy(node.id))

                    for edge in self.edges_to(node.id):
                        to_add = self.find_node("id", edge.src)

                        if not up_graph.find_node("id", edge.src):
                            next_level.append(to_add)

                        up_graph.add_node(copy.copy(to_add))
                        up_graph.add_node(copy.copy(edge))
                except copy.error:
                    print("There is exception in graph_up copy node.")
                    raise Exception

            if next_level:
                levels_to_process.append(next_level)

            current_depth += 1

            return up_graph

    def render_graph_gml(self):
        """

        :return:
        """
        gml = "Creator 'pGRAPH - Pedram Amini <pedram.amini@gmail.com>'\n "
        gml += 'directed 1\n'

        gml += 'graph [\n'

        for node in self.nodes.values():
            gml += node.render_node_gml(self)

        for edge in self.edges.values():
            gml += edge.render_edge_gml(self)

        gml += ']\n'

        #TODO : Complete cluster rendering
        """
        if len(self.clusters):
            gml += 'rootcluster ['\n'

            for cluster in self.clusters:
                gml += cluster.render()

            for node in self.nodes:
                if not self.find_cluster_by_node("id", node.id):
                gml += " vertex '%d'\n" % node.id
            gml += ']\n'

        """

        return gml

    def render_graph_graphviz(self):
        """

        :return:
        """

        import pydot

        dot_graph = pydot.Dot()

        for node in self.nodes.values():
            dot_graph.add_node(node.render_node_graphviz(self))

        for edge in self.edges.values():
            dot_graph.add_edge(edge.render_edge_gml(self))

        return dot_graph

    def render_graph_udraw(self):
        """

        :return:
        """
        udraw = ""

        for node in self.nodes.values():
            udraw += node.render_node_udraw(self)
            udraw += ','

        udraw = udraw[:-1] + ']'

        return udraw

    def render_graph_udraw_update(self):
        """

        :return:
        """
        udraw = '['

        for node in self.nodes.values():
            udraw += node.render_node_udraw_update(self)
            udraw += ','

        for edge in self.edges.values():
            udraw += edge.render_edge_udraw_update(self)
            udraw += ','

        udraw = udraw[:-1] + ']'

        return udraw

    def update_node_id(self, current_id, new_id):
        """

        :param current_id:
        :param new_id:
        :return:
        """

        if current_id not in self.nodes:
            return

        node = self.nodes[current_id]
        del self.nodes[current_id]

        node.id = new_id
        self.nodes[new_id] = node

        #udpate the edges
        for edge in [edge for edge in self.edges.values() if current_id in (edge.src, edge.dst)]:
            del self.edges[edge.id]

            if edge.src == current_id:
                edge.src = new_id
            if edge.dst == current_id:
                edge.dst = new_id

            edge.id = (edge.src << 32) + edge.dst

            self.edges[edge.id] = edge

    def sorted_nodes(self):
        """

        :return:
        """
        return sorted(self.nodes)




