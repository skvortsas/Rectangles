from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QRectF, QPointF, Qt

from draggable_rect import DraggableRect
from connection_line import ConnectionLine


class RectanglesScene(QGraphicsScene):
    def __init__(self):
        super(RectanglesScene, self).__init__()
        self.setSceneRect(0, 0, 1000, 1000)
        self.selected_rect: DraggableRect | None = None

    def drawBackground(self, painter, rect):
        super(RectanglesScene, self).drawBackground(painter, rect)

        scene_rect = self.sceneRect()
        border_rect = QRectF(scene_rect.left(), scene_rect.top(), scene_rect.width(), scene_rect.height())
        painter.setPen(QPen(Qt.darkGray, 2, Qt.DashLine))
        painter.drawRect(border_rect)

    def mouseDoubleClickEvent(self, event):
        super(RectanglesScene, self).mouseDoubleClickEvent(event)

        scene_pos = event.scenePos()
        item = self.get_item_at_position(scene_pos)
        if isinstance(item, DraggableRect):
            self.handle_rect_selection(item)
        elif isinstance(item, ConnectionLine):
            self.handle_line_selection(item)
        else:
            self.create_rect_at_position(scene_pos)

    def mousePressEvent(self, event):
        item = self.get_item_at_position(event.scenePos())
        if item is None:
            self.change_selected_rect(None)
        super(RectanglesScene, self).mousePressEvent(event)

    def handle_rect_selection(self, rect: DraggableRect):
        if (self.selected_rect is not None and
                self.selected_rect != rect and
                rect not in self.selected_rect.connections):
            connection_line = ConnectionLine(self.selected_rect, rect)
            self.addItem(connection_line)
            # using objects as key to prevent lines duplication
            self.selected_rect.connections[rect] = connection_line
            rect.connections[self.selected_rect] = connection_line
            self.change_selected_rect(None)
        else:
            self.change_selected_rect(rect)

    def handle_line_selection(self, line: ConnectionLine):
        line.rect1.remove_connection(line.rect2)
        line.rect2.remove_connection(line.rect1)
        self.removeItem(line)

    def create_rect_at_position(self, pos: QPointF):
        is_pos_inside_of_scene = self.sceneRect().contains(pos)
        if not is_pos_inside_of_scene:
            return

        rect = DraggableRect(pos.x(), pos.y())
        top_left_rect_point = rect.pos()
        bottom_right_rect_point = QPointF(top_left_rect_point.x() + rect.rect().width(),
                                          top_left_rect_point.y() + rect.rect().height())
        rect_is_inside_of_scene = (self.sceneRect().contains(top_left_rect_point) and
                                   self.sceneRect().contains(bottom_right_rect_point))
        if not rect_is_inside_of_scene:
            return

        colliding_items = self.collidingItems(rect, Qt.IntersectsItemBoundingRect)
        # created rect can't collide only with other draggable rects, in other cases
        # we can add one
        for colliding_item in colliding_items:
            if isinstance(colliding_item, DraggableRect):
                return

        self.addItem(rect)

    def get_item_at_position(self, pos: QPointF):
        # self.views()[0] as view supposed to be the only one, change and compare with MainView to get the right one
        return self.itemAt(pos, self.views()[0].transform())

    def change_selected_rect(self, rect: DraggableRect | None):
        # if we had a selected rect - trigger its selection
        if self.selected_rect:
            self.selected_rect.trigger_rect_selection()
        # if we have a new rect - trigger its selection
        if rect:
            rect.trigger_rect_selection()
        self.selected_rect = rect
