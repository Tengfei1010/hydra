# _*_ coding: utf-8 _*_
# This project is fllowing Pedram Amini's sulley, the core part is sully, some part overwrite by me.
# See detail sulley form https://github.com/OpenRCE/sulley
# If there is a problem, please contact tutengfei.kevin@gmail.com
# Thank you!
"""
@the first author: Pedram Amini
@he second author: tutengfei.kevin
@contact: tutengfei.kevin@gmail.com
@source: https://github.com/tutengfei/hydra
"""


class Edge:
    """

    """
    def __init__(self, src, dst):
        self.id = (src << 32) + dst
        self.src = src
        self.dst = dst

        #general graph attributes
        self.color = 0x000000
        self.label = ""

        #gml relevant attributes
        self.gml_arrow = "none"
        self.gml_stipple = 1
        self.gml_line_width = 1.0

    def render_edge_gml(self, graph):
        """

        :param graph:
        :return:
        """

        src = graph.find_node("id", self.src)
        dst = graph.find_node("id", self.dst)
