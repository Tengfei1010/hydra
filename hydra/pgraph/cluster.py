# _*_ coding: utf-8 _*_
# This project is fllowing Pedram Amini's sulley, the core part is sully,
#  some part overwrite by me.
# See detail sulley form https://github.com/OpenRCE/sulley
# If there is a problem, please contact tutengfei.kevin@gmail.com
# Thank you!
"""
@the first author: Pedram Amini
@the second author: tutengfei.kevin
@contact: tutengfei.kevin@gmail.com
@source: https://github.com/tutengfei/hydra
"""

from hydra.pgraph import node


class Cluster:
    """

    """

    def __init__(self, id):
        """

        :return:
        """
        self.id = id
        self.nodes = {}

    def add_node(self, node):
        """

        :param node:
        :return:
        """
        if node.id not in self.nodes:
            self.nodes[node.id] = node
        return self

    def del_node(self, node_id):
        """

        :param node_id:
        :return:
        """
        self.nodes.pop(node_id)
        return self

    def find_node(self, attribute, value):
        """

        :param attribute:
        :param value:
        :return:
        """
        for node in self.nodes:
            if hasattr(node, attribute):
                if getattr(node, attribute) == value:
                    return node
        return None

    def render(self):
        pass