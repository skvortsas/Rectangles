from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtCore import QLineF, Qt
from PyQt5.QtGui import QPen

from draggable_rect import DraggableRect


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, rect1: DraggableRect, rect2: DraggableRect):
        super(ConnectionLine, self).__init__()
        self.rect1 = rect1
        self.rect2 = rect2
        self.update_position()
        self.setPen(QPen(Qt.black, 8))
        self.setZValue(1)

    def update_position(self):
        self.setLine(QLineF(self.rect1.mapToScene(self.rect1.rect().center()),
                            self.rect2.mapToScene(self.rect2.rect().center())))
