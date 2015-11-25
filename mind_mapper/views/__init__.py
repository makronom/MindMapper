from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView, QQuickItem
from mind_mapper.controllers import Controller
import sys
import os


class View(object):

    shapes = ["rectangle", "ellipse"]
    edgetypes = ["line", "curve"]

    def __init__(self):
        self._controller = Controller(self)
        self._gui = QGuiApplication(sys.argv)

        self._qml_dir = os.path.dirname(os.path.realpath(__file__))
        self._main = QQuickView()
        self._main.setResizeMode(QQuickView.SizeRootObjectToView)
        self._main.setSource(QUrl(self._qml_dir + '/main.qml'))

        self._main.rootObject().create_node.connect(
            self._controller.create_node)
        self._main.rootObject().mouse_position.connect(
            self._controller.mouse_position)
        self._main.rootObject().save.connect(
            self._controller.save)
        self._main.rootObject().load.connect(
            self._controller.load)
        self._main.rootObject().lose_focus.connect(
            self._controller.lose_focus)
        self._main.rootObject().node_color_sel.connect(
            self._controller.node_color_sel)
        self._main.rootObject().edge_color_sel.connect(
            self._controller.edge_color_sel)
        self._main.rootObject().window_resize.connect(
            self._controller.window_resize)
        self._main.rootObject().edge_type_sel.connect(
            self._controller.edge_type_sel)
        self._main.setProperty("width", 1000)
        self._main.setProperty("height", 800)
        self._main.show()

    def run(self):
        return self._gui.exec_()

    def create_node(self, node):
        # Creates new node from source QML and puts it inside of main window
        qml_node = QQuickView(QUrl(self._qml_dir + '/shapes/' +
                                   self.shapes[node.shape] + '.qml'),
                              self._main)

        workspace = self._main.rootObject().findChild(QQuickItem, "workspace")

        # Sets all properties
        qml_node.rootObject().setProperty("parent", workspace)
        qml_node.rootObject().setProperty("objectId", str(node.id))
        qml_node.rootObject().setProperty("backgroundColor",
                                          str(node.background))
        qml_node.rootObject().setProperty("width", str(node.width))
        qml_node.rootObject().setProperty("height", str(node.height))
        qml_node.rootObject().setProperty("text", str(node.text.text))

        # Sets drag boundaries
        qml_node.rootObject().setProperty("workspaceWidth",
                                          str(workspace.property("width")))
        qml_node.rootObject().setProperty("workspaceHeight",
                                          str(workspace.property("height")))

        # Signal connection
        qml_node.rootObject().node_delete.connect(
            self._controller.node_delete)
        qml_node.rootObject().node_text_changed.connect(
            self._controller.node_text_changed)
        qml_node.rootObject().node_position_changed.connect(
            self._controller.node_position_changed)
        qml_node.rootObject().node_connect.connect(
            self._controller.node_connect)

        # Position to mouse click
        qml_node.rootObject().setX(node.x - node.width / 2)
        qml_node.rootObject().setY(node.y - node.height / 2)
        qml_node.rootObject().setZ(2)

        return qml_node

    def create_edge(self, edge, node1, node2):
        qml_edge = QQuickView(QUrl(self._qml_dir + '/edges/' +
                                   self.edgetypes[edge.type] + '.qml'),
                              self._main)
        workspace = self._main.rootObject().findChild(QQuickItem, "workspace")

        qml_edge.rootObject().setProperty("parent", workspace)
        qml_edge.rootObject().setProperty("objectId", str(edge.id))
        qml_edge.rootObject().setZ(1)

        qml_edge.rootObject().setProperty(
            "width", workspace.property("width"))
        qml_edge.rootObject().setProperty(
            "height", workspace.property("height"))

        qml_edge.rootObject().setProperty("ctrlX", str(edge.x))
        qml_edge.rootObject().setProperty("ctrlY", str(edge.y))
        qml_edge.rootObject().setProperty("startX", str(node1.x))
        qml_edge.rootObject().setProperty("startY", str(node1.y))
        qml_edge.rootObject().setProperty("endX", str(node2.x))
        qml_edge.rootObject().setProperty("endY", str(node2.y))
        qml_edge.rootObject().setProperty("color", str(edge.color))
        qml_edge.rootObject().setProperty("thickness", str(edge.thickness))
        qml_edge.rootObject().setProperty("spiked", str(edge.spiked))
        qml_edge.rootObject().setProperty("arrow", str(edge.arrow))

        # Sets drag boundaries
        qml_edge.rootObject().setProperty("workspaceWidth",
                                          str(workspace.property("width")))
        qml_edge.rootObject().setProperty("workspaceHeight",
                                          str(workspace.property("height")))

        # Signal connection
        qml_edge.rootObject().edge_delete.connect(
            self._controller.edge_delete)
        qml_edge.rootObject().edge_position_changed.connect(
            self._controller.edge_position_changed)

        return qml_edge

    def node_update(self, node):
        pass

    def clicked(self, x):
        print(x)
