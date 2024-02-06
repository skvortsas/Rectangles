import random
from PyQt5.QtGui import QColor


def get_random_color():
    return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
