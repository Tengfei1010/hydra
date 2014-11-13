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
import pydot


class Node:
    """

    """

    def __init__(self, id=None):
        self.id = id
        self.number = 0
        #gengeral graph attributes
        self.color = 0xEEF7FF
        self.border_color = 0xEEEEEE
        self.label = ""
        self.shape = "box"
        #gml relevant attributes
        self.gml_width = 0.0
        self.gml_height = 0.0
        self.gml_pattern = "1"
        self.gml_stipple = 1
        self.gml_type = 1.0
        self.gml_width_shape = 1.0

    def render_node_gml(self, graph):
        """
        :param graph: pgraph.graph
        :return: Top level graph object containing the current node
        :rtype: String
        :return : GML node description
        """
        chunked_label = ""
        cursor = 0

        while cursor < len(self.label):
            amount = 200

            #if the end of the current chunk contains a backslash or
            #  double-quote, back of some.
            if cursor + amount < len(self.label):
                while self.label[cursor + amount] == '\\' or \
                                self.label[cursor + amount] == "":
                    amount -= 1
            chunked_label += self.label[cursor:cursor + amount] + "\\\n"
            cursor += amount

        #if node width and height were not explicitly specified,
        # make a best effort guess to create something nice.
        if not self.gml_width:
            self.gml_width = len(self.label) * 10

        if not self.gml_height:
            self.gml_height = len(self.label.split()) * 20

        #construct the node of definition
        node = '  node [\n'
        node += '    id %d\n' % self.number
        node += '    template "oreas:std:rect"\n'
        node += '    label "'
        node += '<!--%08x-->\\\n' % self.id
        node += chunked_label + '"\n'
        node += '    graphics [\n'
        node += '      w %f\n' % self.gml_width
        node += '      h %f\n' % self.gml_height
        node += '      fill "#%06x"\n' % self.color
        node += '      line "#%06x"\n' % self.border_color
        node += '      pattern "%s"\n' % self.gml_pattern
        node += '      stipple %d\n' % self.gml_stipple
        node += '      lineWidth %f\n' % self.gml_line_width
        node += '      type "%s"\n' % self.gml_type
        node += '      width %f\n' % self.gml_width_shape
        node += '    ]\n'
        node += '  ]\n'

        return node

    def render_node_graphviz(self, graph):
        """
        Render a node suitable for use in a Pydot graph using the set internal attributes.

        @type  graph: pgraph.graph
        @param graph: Top level graph object containing the current node

        @rtype:  pydot.Node
        @return: Pydot object representing node
        """
        dot_node = pydot.Node(self.id)

        dot_node.label = '<<font face="lucida console">%s</font>>' % self.label.rstrip("\r\n")
        dot_node.label = dot_node.label.replace("\\n", '<br/>')
        dot_node.shape = self.shape
        dot_node.color = "#%06x" % self.color
        dot_node.fillcolor = "#%06x" % self.color

        return dot_node

    def render_node_draw(self, graph):
        """
        Render a node description suitable for use in a uDraw file using the set internal attributes.

        @type  graph: pgraph.graph
        @param graph: Top level graph object containing the current node

        @rtype:  String
        @return: uDraw node description.
        """
        # translate newlines for uDraw.
        self.label = self.label.replace("\n", "\\n")

        # if an image was specified for this node, update the shape and include the image tag.
        if self.udraw_image:
            self.shape = "image"
            udraw_image = 'a("IMAGE","%s"),' % self.udraw_image
        else:
            udraw_image = ""

        udraw = 'l("%08x",' % self.id
        udraw += 'n("",'  # open node
        udraw += '['  # open attributes
        udraw += udraw_image
        udraw += 'a("_GO","%s"),' % self.shape
        udraw += 'a("COLOR","#%06x"),' % self.color
        udraw += 'a("OBJECT","%s"),' % self.label
        udraw += 'a("FONTFAMILY","courier"),'
        udraw += 'a("INFO","%s"),' % self.udraw_info
        udraw += 'a("BORDER","none")'
        udraw += '],'  # close attributes
        udraw += '['  # open edges

        edges = graph.edges_from(self.id)

        for edge in edges:
            udraw += edge.render_edge_udraw(graph)
            udraw += ','

        if edges:
            udraw = udraw[0:-1]

        udraw += ']))'

        return udraw

    def render_node_udraw_update(self):
        '''
        Render a node update description suitable for use in a uDraw file using the set internal attributes.

        @rtype:  String
        @return: uDraw node update description.
        '''

        # translate newlines for uDraw.
        self.label = self.label.replace("\n", "\\n")

        # if an image was specified for this node, update the shape and include the image tag.
        if self.udraw_image:
            self.shape = "image"
            udraw_image = 'a("IMAGE","%s"),' % self.udraw_image
        else:
            udraw_image = ""

        udraw = 'new_node("%08x","",' % self.id
        udraw += '['
        udraw += udraw_image
        udraw += 'a("_GO","%s"),' % self.shape
        udraw += 'a("COLOR","#%06x"),' % self.color
        udraw += 'a("OBJECT","%s"),' % self.label
        udraw += 'a("FONTFAMILY","courier"),'
        udraw += 'a("INFO","%s"),' % self.udraw_info
        udraw += 'a("BORDER","none")'
        udraw += ']'
        udraw += ')'

        return udraw

