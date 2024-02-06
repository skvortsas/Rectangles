from PyQt5.QtWidgets import QGraphicsRectItem, QApplication
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF

from utils.colors import get_random_color
from utils.constants import RECT_SHORT_SIDE_LENGTH


class DraggableRect(QGraphicsRectItem):
    def __init__(self, x, y):
        super(DraggableRect, self).__init__(0, 0, RECT_SHORT_SIDE_LENGTH * 2, RECT_SHORT_SIDE_LENGTH)
        init_pos = QPointF(x - self.rect().width() / 2, y - self.rect().height() / 2)
        random_color = get_random_color()
        self.setPos(init_pos)
        self.setBrush(QBrush(random_color))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.connections = {}

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            future_pos = super(DraggableRect, self).itemChange(change, value)

            scene_rect = self.scene().sceneRect()

            # limiting rectangle position inside the scene
            new_x = min(max(future_pos.x(), scene_rect.left()), scene_rect.right() - self.rect().width())
            new_y = min(max(future_pos.y(), scene_rect.top()), scene_rect.bottom() - self.rect().height())
            corrected_pos = QPointF(new_x, new_y)

            for item in self.scene().items():
                if item != self and isinstance(item, DraggableRect):
                    # return previous position if collision detected
                    if QRectF(corrected_pos, self.rect().size()).intersects(item.rect().translated(item.pos())):
                        return self.pos()

            # update connected lines only when we move the rect
            for connection_line in self.connections.values():
                connection_line.update_position()
            return corrected_pos

        return super(DraggableRect, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setOpacity(0.7)
        super(DraggableRect, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setOpacity(1.0)
        super(DraggableRect, self).mouseReleaseEvent(event)

    def remove_connection(self, rect_remove_connection_with):
        del self.connections[rect_remove_connection_with]
