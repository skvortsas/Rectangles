import random
from PyQt5.QtGui import QColor, QLinearGradient, QBrush
from PyQt5.QtCore import QPointF, Qt, QRectF


def get_random_color():
    return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_select_gradient(rect: QRectF):
    gradient = QLinearGradient(QPointF(0, 0), QPointF(rect.width(), rect.height()))
    gradient.setColorAt(0, QColor(Qt.red))
    gradient.setColorAt(1, QColor(Qt.yellow))
    return QBrush(gradient)
