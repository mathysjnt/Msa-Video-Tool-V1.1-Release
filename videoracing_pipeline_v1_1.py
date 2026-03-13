"""
MotorSport Academy — VideoRacing Pipeline v1.1
Dark / light theme edition
"""
import sys, os, re, json, math, queue, sqlite3, subprocess, threading, shutil, time, base64, tempfile, hashlib, uuid, webbrowser
from datetime import datetime
from pathlib import Path
from urllib import error as urlerror, request as urlrequest

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QTextEdit, QHeaderView, QAbstractItemView, QProgressBar,
    QFileDialog, QFrame, QDialog, QFormLayout, QScrollArea,
    QSpinBox, QComboBox, QDialogButtonBox, QSizePolicy,
    QCheckBox, QTabWidget,
    QSlider, QGridLayout, QSystemTrayIcon, QStyle, QShortcut,
    QListView, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QGraphicsBlurEffect,
    QAbstractSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray, QTimer, QSize, QRect, QRectF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import (
    QColor, QPalette, QPainter, QRadialGradient, QLinearGradient, QPainterPath,
    QBrush, QPen, QFont, QPixmap, QIcon, QKeySequence
)
try:
    from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
    HAS_SVG = True
except ImportError:
    HAS_SVG = False

try:
    import cv2
    import numpy as np
    MP_FACE_DETECTION = None
    OPENCV_FACE_CASCADE = None
    try:
        cascade_path = str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
        if os.path.exists(cascade_path):
            cascade = cv2.CascadeClassifier(cascade_path)
            if not cascade.empty():
                OPENCV_FACE_CASCADE = cascade
    except Exception:
        OPENCV_FACE_CASCADE = None
    HAS_AUTO_DETECT = OPENCV_FACE_CASCADE is not None
except ImportError:
    cv2 = None
    np = None
    MP_FACE_DETECTION = None
    OPENCV_FACE_CASCADE = None
    HAS_AUTO_DETECT = False

# ══════════════════════════════════════════════════════════════
#  LOGO SVG (tout blanc, embarqué)
# ══════════════════════════════════════════════════════════════
LOGO_SVG_B64 = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iQ2FscXVlXzEiIGRhdGEtbmFtZT0iQ2FscXVlIDEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDk3OC44OSAzMDUuMjgiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNmZmZmZmY7CiAgICAgIH0KCiAgICAgIC5jbHMtMSwgLmNscy0yIHsKICAgICAgICBzdHJva2Utd2lkdGg6IDBweDsKICAgICAgfQoKICAgICAgLmNscy0yIHsKICAgICAgICBmaWxsOiAjZmZmOwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvZGVmcz4KICA8Zz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0ibTE2MC41MiwyNC44N2wtMjIuODgsMTE2LjA4aC0zMC4zNWwxMS45NC02MS4xOS0zOC42NCw0OS43NWgtMTQuNDNsLTIxLjA2LTQ5Ljc1LTEyLjI3LDYxLjE5SDIuNjVMMjUuODcsMjQuODdoMjYuN2wyNy4yLDY3LjE2LDUyLjczLTY3LjE2aDI4LjAzWiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0yIiBkPSJtMTgxLjQyLDEzNy4zOWMtNy4wOC0zLjM3LTEyLjU1LTguMTUtMTYuNDItMTQuMzQtMy44Ny02LjE5LTUuOC0xMy4zOC01LjgtMjEuNTYsMC05Ljg0LDIuMzgtMTguNjgsNy4xMy0yNi41Myw0Ljc1LTcuODUsMTEuMzMtMTQuMDQsMTkuNzMtMTguNTcsOC40LTQuNTMsMTcuODUtNi44LDI4LjM2LTYuOCw5LjUxLDAsMTcuOCwxLjY5LDI0Ljg4LDUuMDYsNy4wNywzLjM3LDEyLjU1LDguMTMsMTYuNDIsMTQuMjYsMy44Nyw2LjE0LDUuOCwxMy4yOSw1LjgsMjEuNDgsMCw5Ljg0LTIuMzgsMTguNzEtNy4xMywyNi42Mi00Ljc1LDcuOTEtMTEuMywxNC4xMi0xOS42NSwxOC42Ni04LjM1LDQuNTMtMTcuODMsNi44LTI4LjQ0LDYuOC05LjUxLDAtMTcuOC0xLjY4LTI0Ljg4LTUuMDZabTQyLjEyLTI3LjI4YzMuOTgtNC42NCw1Ljk3LTEwLjY3LDUuOTctMTguMDgsMC01LjMxLTEuNDktOS41MS00LjQ4LTEyLjYtMi45OC0zLjA5LTcuMTMtNC42NC0xMi40NC00LjY0LTYuMywwLTExLjQ0LDIuMzItMTUuNDIsNi45Ni0zLjk4LDQuNjQtNS45NywxMC43Mi01Ljk3LDE4LjI0LDAsNS4zMSwxLjQ5LDkuNDgsNC40OCwxMi41MiwyLjk4LDMuMDQsNy4xMyw0LjU2LDEyLjQ0LDQuNTYsNi4zLDAsMTEuNDQtMi4zMiwxNS40Mi02Ljk2WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0yIiBkPSJtMzA1LjQ2LDEwNy40NmMtLjIyLDEuNTUtLjMzLDIuNTQtLjMzLDIuOTgsMCw1LjA5LDIuNzYsNy42Myw4LjI5LDcuNjMsMi45OCwwLDYuMTQtLjg4LDkuNDUtMi42NWwzLjk4LDIxLjcyYy02LjE5LDMuNTQtMTMuOTksNS4zMS0yMy4zOCw1LjMxcy0xNi42Ny0yLjMyLTIyLjE0LTYuOTdjLTUuNDctNC42NC04LjIxLTExLjExLTguMjEtMTkuNCwwLTMuMjEuMjctNi4wMi44My04LjQ2bDUuOTctMjkuNjhoLTEzLjI3bDQuODEtMjMuNTVoMTMuMWw0LjY0LTIzLjM4aDMxLjUxbC00LjY0LDIzLjM4aDIwLjRsLTQuNjQsMjMuNTVoLTIwLjRsLTUuOTcsMjkuNTJaIi8+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Im0zNTcuMiwxMzcuMzljLTcuMDgtMy4zNy0xMi41NS04LjE1LTE2LjQyLTE0LjM0LTMuODctNi4xOS01LjgtMTMuMzgtNS44LTIxLjU2LDAtOS44NCwyLjM4LTE4LjY4LDcuMTMtMjYuNTMsNC43NS03Ljg1LDExLjMzLTE0LjA0LDE5LjczLTE4LjU3LDguNC00LjUzLDE3Ljg1LTYuOCwyOC4zNi02LjgsOS41MSwwLDE3LjgsMS42OSwyNC44OCw1LjA2LDcuMDcsMy4zNywxMi41NSw4LjEzLDE2LjQyLDE0LjI2LDMuODcsNi4xNCw1LjgsMTMuMjksNS44LDIxLjQ4LDAsOS44NC0yLjM4LDE4LjcxLTcuMTMsMjYuNjItNC43NSw3LjkxLTExLjMsMTQuMTItMTkuNjUsMTguNjYtOC4zNSw0LjUzLTE3LjgzLDYuOC0yOC40NCw2LjgtOS41MSwwLTE3LjgtMS42OC0yNC44OC01LjA2Wm00Mi4xMi0yNy4yOGMzLjk4LTQuNjQsNS45Ny0xMC42Nyw1Ljk3LTE4LjA4LDAtNS4zMS0xLjQ5LTkuNTEtNC40OC0xMi42LTIuOTgtMy4wOS03LjEzLTQuNjQtMTIuNDQtNC42NC02LjMsMC0xMS40NCwyLjMyLTE1LjQyLDYuOTYtMy45OCw0LjY0LTUuOTcsMTAuNzItNS45NywxOC4yNCwwLDUuMzEsMS40OSw5LjQ4LDQuNDgsMTIuNTIsMi45OCwzLjA0LDcuMTMsNC41NiwxMi40NCw0LjU2LDYuMywwLDExLjQ0LTIuMzIsMTUuNDItNi45NloiLz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0ibTUxNy43Miw0OS41OGwtNS40NywyOC4zNmMtMi43Ny0uMzMtNS4xNC0uNS03LjEzLS41LTcuMDgsMC0xMi43NCwxLjY5LTE3LDUuMDYtNC4yNiwzLjM3LTcuMSw4LjcxLTguNTQsMTZsLTguNjIsNDIuNDVoLTMxLjUxbDE3LjkxLTg5Ljg4aDI5Ljg1bC0xLjk5LDkuOTVjNy41Mi03LjYzLDE4LjM1LTExLjQ0LDMyLjUtMTEuNDRaIi8+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Im01MjYuNjgsMTM5Ljc5Yy04LjYyLTIuMzItMTUuNjUtNS4zMS0yMS4wNi04Ljk2bDEyLjkzLTI0LjU0YzUuODYsMy43NiwxMi4xMSw2LjYxLDE4Ljc0LDguNTQsNi42MywxLjk0LDEzLjI3LDIuOSwxOS45LDIuOXMxMS4xOS0uOTEsMTQuNjgtMi43NCw1LjIyLTQuMzQsNS4yMi03LjU1YzAtMi43Ni0xLjU4LTQuOTItNC43My02LjQ3LTMuMTUtMS41NS04LjA0LTMuMjEtMTQuNjgtNC45OC03LjUyLTEuOTktMTMuNzYtNC4wMS0xOC43NC02LjA1LTQuOTctMi4wNC05LjI2LTUuMTctMTIuODUtOS4zNy0zLjU5LTQuMi01LjM5LTkuNzMtNS4zOS0xNi41OCwwLTguMjksMi4yNi0xNS41Niw2LjgtMjEuODEsNC41My02LjI0LDExLTExLjA4LDE5LjQtMTQuNTEsOC40LTMuNDMsMTguMjQtNS4xNCwyOS41Mi01LjE0LDguMjksMCwxNi4wMy44NiwyMy4yMiwyLjU3LDcuMTgsMS43MiwxMy4zOCw0LjE3LDE4LjU3LDcuMzhsLTExLjk0LDI0LjM4Yy00LjUzLTIuODctOS41NC01LjA2LTE1LjAxLTYuNTUtNS40Ny0xLjQ5LTExLjA4LTIuMjQtMTYuODMtMi4yNC02LjUyLDAtMTEuNjQsMS4wNS0xNS4zNCwzLjE1LTMuNzEsMi4xLTUuNTYsNC44MS01LjU2LDguMTMsMCwyLjg4LDEuNiw1LjA5LDQuODEsNi42MywzLjIxLDEuNTUsOC4xOCwzLjIxLDE0LjkyLDQuOTcsNy41MiwxLjg4LDEzLjc0LDMuODEsMTguNjYsNS44LDQuOTIsMS45OSw5LjE1LDUuMDMsMTIuNjksOS4xMiwzLjU0LDQuMDksNS4zMSw5LjQ1LDUuMzEsMTYuMDksMCw4LjE4LTIuMywxNS40LTYuODgsMjEuNjQtNC41OSw2LjI1LTExLjExLDExLjA4LTE5LjU3LDE0LjUxLTguNDYsMy40My0xOC4yNyw1LjE0LTI5LjQzLDUuMTQtOS42MiwwLTE4Ljc0LTEuMTYtMjcuMzYtMy40OFoiLz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0ibTcwNC4yLDU0LjQ3YzUuOCwzLjI2LDEwLjQ3LDcuOTksMTQuMDEsMTQuMTgsMy41NCw2LjE5LDUuMzEsMTMuNDMsNS4zMSwyMS43MiwwLDkuODQtMi4xOCwxOC43MS02LjU1LDI2LjYyLTQuMzcsNy45MS0xMC4yOCwxNC4xMi0xNy43NCwxOC42Ni03LjQ2LDQuNTMtMTUuNjIsNi44LTI0LjQ2LDYuOC0xMy4wNSwwLTIyLjIyLTQuMDktMjcuNTMtMTIuMjdsLTguNjIsNDIuOTVoLTMxLjUxbDI0LjM4LTEyMi4wNWgyOS44NWwtMS44Miw4LjQ2YzcuMTktNi42MywxNS44Ni05Ljk1LDI2LjA0LTkuOTUsNi42MywwLDEyLjg1LDEuNjMsMTguNjYsNC44OVptLTE4LjQ5LDU1LjY0YzMuOTgtNC42NCw1Ljk3LTEwLjY3LDUuOTctMTguMDgsMC01LjMxLTEuNTItOS41MS00LjU2LTEyLjYtMy4wNC0zLjA5LTcuMjEtNC42NC0xMi41Mi00LjY0LTYuMywwLTExLjQ0LDIuMzItMTUuNDIsNi45Ni0zLjk4LDQuNjQtNS45NywxMC43Mi01Ljk3LDE4LjI0LDAsNS4zMSwxLjUyLDkuNDgsNC41NiwxMi41MiwzLjA0LDMuMDQsNy4yMSw0LjU2LDEyLjUyLDQuNTYsNi4zLDAsMTEuNDQtMi4zMiwxNS40Mi02Ljk2WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJtNzUwLjg4LDEzNy4zOWMtNy4wOC0zLjM3LTEyLjU1LTguMTUtMTYuNDItMTQuMzQtMy44Ny02LjE5LTUuOC0xMy4zOC01LjgtMjEuNTYsMC05Ljg0LDIuMzgtMTguNjgsNy4xMy0yNi41Myw0Ljc1LTcuODUsMTEuMzMtMTQuMDQsMTkuNzMtMTguNTcsOC40LTQuNTMsMTcuODUtNi44LDI4LjM2LTYuOCw5LjUxLDAsMTcuOCwxLjY5LDI0Ljg3LDUuMDYsNy4wNywzLjM3LDEyLjU1LDguMTMsMTYuNDIsMTQuMjYsMy44Nyw2LjE0LDUuOCwxMy4yOSw1LjgsMjEuNDgsMCw5Ljg0LTIuMzgsMTguNzEtNy4xMywyNi42Mi00Ljc1LDcuOTEtMTEuMywxNC4xMi0xOS42NSwxOC42Ni04LjM1LDQuNTMtMTcuODMsNi44LTI4LjQ0LDYuOC05LjUxLDAtMTcuOC0xLjY4LTI0Ljg4LTUuMDZabTQyLjEyLTI3LjI4YzMuOTgtNC42NCw1Ljk3LTEwLjY3LDUuOTctMTguMDgsMC01LjMxLTEuNDktOS41MS00LjQ4LTEyLjYtMi45OS0zLjA5LTcuMTMtNC42NC0xMi40NC00LjY0LTYuMywwLTExLjQ0LDIuMzItMTUuNDIsNi45Ni0zLjk4LDQuNjQtNS45NywxMC43Mi01Ljk3LDE4LjI0LDAsNS4zMSwxLjQ5LDkuNDgsNC40OCwxMi41MiwyLjk5LDMuMDQsNy4xMyw0LjU2LDEyLjQ0LDQuNTYsNi4zLDAsMTEuNDQtMi4zMiwxNS40Mi02Ljk2WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJtOTExLjQsNDkuNThsLTUuNDcsMjguMzZjLTIuNzYtLjMzLTUuMTQtLjUtNy4xMy0uNS03LjA4LDAtMTIuNzQsMS42OS0xNyw1LjA2LTQuMjYsMy4zNy03LjEsOC43MS04LjU0LDE2bC04LjYyLDQyLjQ1aC0zMS41MWwxNy45MS04OS44OGgyOS44NWwtMS45OSw5Ljk1YzcuNTItNy42MywxOC4zNS0xMS40NCwzMi41LTExLjQ0WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJtOTQ3Ljg4LDEwNy40NmMtLjIyLDEuNTUtLjMzLDIuNTQtLjMzLDIuOTgsMCw1LjA5LDIuNzYsNy42Myw4LjI5LDcuNjMsMi45OSwwLDYuMTQtLjg4LDkuNDUtMi42NWwzLjk4LDIxLjcyYy02LjE5LDMuNTQtMTMuOTksNS4zMS0yMy4zOCw1LjMxcy0xNi42Ny0yLjMyLTIyLjE0LTYuOTdjLTUuNDctNC42NC04LjIxLTExLjExLTguMjEtMTkuNCwwLTMuMjEuMjctNi4wMi44My04LjQ2bDUuOTctMjkuNjhoLTEzLjI3bDQuODEtMjMuNTVoMTMuMWw0LjY0LTIzLjM4aDMxLjUxbC00LjY0LDIzLjM4aDIwLjRsLTQuNjQsMjMuNTVoLTIwLjRsLTUuOTcsMjkuNTJaIi8+CiAgPC9nPgogIDxnPgogICAgPHBhdGggY2xhc3M9ImNscy0yIiBkPSJtMjQwLjA0LDI1NS40OGgtNDAuODJsLTguMDUsMTguODloLTE1LjYzbDM2Ljc0LTgxLjYzaDE0LjkzbDM2Ljg1LDgxLjYzaC0xNS44NmwtOC4xNi0xOC44OVptLTUuMDEtMTEuOWwtMTUuMzktMzUuNjktMTUuMjgsMzUuNjloMzAuNjdaIi8+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Im0zMDYuMjIsMjcwLjEyYy02LjY1LTMuNjItMTEuODYtOC42MS0xNS42My0xNC45OS0zLjc3LTYuMzctNS42Ni0xMy41Ny01LjY2LTIxLjU4czEuOS0xNS4yLDUuNzEtMjEuNThjMy44MS02LjM3LDkuMDQtMTEuMzcsMTUuNjktMTQuOTlzMTQuMDktNS40MiwyMi4zMy01LjQyYzYuNjksMCwxMi43OSwxLjE3LDE4LjMxLDMuNSw1LjUyLDIuMzMsMTAuMTgsNS43MSwxMy45OSwxMC4xNWwtOS44LDkuMjFjLTUuOTEtNi4zNy0xMy4xOC05LjU2LTIxLjgxLTkuNTYtNS42LDAtMTAuNjEsMS4yMi0xNS4wNCwzLjY3cy03Ljg5LDUuODUtMTAuMzgsMTAuMjFjLTIuNDksNC4zNS0zLjczLDkuMjktMy43MywxNC44MXMxLjI0LDEwLjQ2LDMuNzMsMTQuODFjMi40OSw0LjM2LDUuOTUsNy43NiwxMC4zOCwxMC4yMSw0LjQzLDIuNDUsOS40NSwzLjY3LDE1LjA0LDMuNjcsOC42MywwLDE1LjktMy4yMiwyMS44MS05LjY4bDkuOCw5LjMzYy0zLjgxLDQuNDMtOC41LDcuODEtMTQuMDUsMTAuMTUtNS41NiwyLjMzLTExLjY4LDMuNS0xOC4zNywzLjUtOC4yNCwwLTE1LjY5LTEuODEtMjIuMzMtNS40MloiLz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0ibTQ0NC4yNCwyNTUuNDhoLTQwLjgybC04LjA1LDE4Ljg5aC0xNS42M2wzNi43NC04MS42M2gxNC45M2wzNi44NSw4MS42M2gtMTUuODZsLTguMTYtMTguODlabS01LjAxLTExLjlsLTE1LjM5LTM1LjY5LTE1LjI4LDM1LjY5aDMwLjY3WiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0yIiBkPSJtNDk2LjEzLDE5Mi43NGgzNS42OWM4LjcxLDAsMTYuNDQsMS42OSwyMy4yMSw1LjA3czEyLjAxLDguMTYsMTUuNzQsMTQuMzRjMy43Myw2LjE4LDUuNiwxMy4zMiw1LjYsMjEuNHMtMS44NywxNS4yMi01LjYsMjEuNGMtMy43Myw2LjE4LTguOTgsMTAuOTYtMTUuNzQsMTQuMzQtNi43NywzLjM4LTE0LjUsNS4wNy0yMy4yMSw1LjA3aC0zNS42OXYtODEuNjNabTM0Ljk5LDY4LjgxYzUuOTksMCwxMS4yNS0xLjE1LDE1LjgtMy40NCw0LjU1LTIuMjksOC4wNS01LjU2LDEwLjUtOS44LDIuNDUtNC4yNCwzLjY3LTkuMTYsMy42Ny0xNC43NXMtMS4yMi0xMC41MS0zLjY3LTE0Ljc1Yy0yLjQ1LTQuMjQtNS45NS03LjUtMTAuNS05LjgtNC41NS0yLjI5LTkuODItMy40NC0xNS44LTMuNDRoLTE5LjgzdjU1Ljk4aDE5LjgzWiIvPgogICAgPHBhdGggY2xhc3M9ImNscy0yIiBkPSJtNjcxLjE4LDI2MS42N3YxMi43MWgtNjEuMjN2LTgxLjYzaDU5LjU5djEyLjcxaC00NC40M3YyMS4yMmgzOS40MnYxMi40OGgtMzkuNDJ2MjIuNTFoNDYuMDdaIi8+CiAgICA8cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Im03ODAuNTcsMjc0LjM4bC0uMTItNTQuMTEtMjYuODIsNDQuNzhoLTYuNzZsLTI2LjgyLTQ0LjA4djUzLjQxaC0xNC40NnYtODEuNjNoMTIuNDhsMzIuNDIsNTQuMTEsMzEuODQtNTQuMTFoMTIuNDhsLjEyLDgxLjYzaC0xNC4zNFoiLz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0ibTg2OS42NywyNDUuNTd2MjguODFoLTE1LjE2di0yOC41N2wtMzIuMDctNTMuMDZoMTYuMjFsMjMuOTEsMzkuNzcsMjQuMTQtMzkuNzdoMTQuOTNsLTMxLjk2LDUyLjgzWiIvPgogIDwvZz4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Im0xMTMuOTcsMjc1LjMxaDM3LjQ3YzEyLjE2LTI4LjM5LDI0LjMyLTU2Ljc4LDM2LjQ4LTg1LjE3aC0zNy40N2MtMTIuMTYsMjguMzktMjQuMzIsNTYuNzgtMzYuNDgsODUuMTdaIi8+CiAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJtODQuODYsMjc1LjMxaDE1Ljg4YzEyLjE2LTI4LjM5LDI0LjMyLTU2Ljc4LDM2LjQ4LTg1LjE3aC0xNi42MmMtMTEuOTEsMjguMzktMjMuODIsNTYuNzgtMzUuNzMsODUuMTdaIi8+CiAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJtNjEuMzcsMjc1LjMxaDguNTZjMTIuMTYtMjguMzksMjQuMzItNTYuNzgsMzYuNDgtODUuMTdoLTkuNDdjLTExLjg2LDI4LjM5LTIzLjcxLDU2Ljc4LTM1LjU3LDg1LjE3WiIvPgo8L3N2Zz4="

ACCENT = "#ff7a00"
UI_FONT = "Segoe UI"
UI_FONT_FALLBACK = "Arial"
MONO_FONT = "Consolas"
IS_WINDOWS = sys.platform.startswith("win")
FONT_SCALE = 1.14 if IS_WINDOWS else 1.0
UI_SCALE = 1.12 if IS_WINDOWS else 1.0
RADIUS_SCALE = 1.16 if IS_WINDOWS else 1.0
APP_NAME = "MSA Video Tool"
APP_VERSION = "1.1.0"
APP_ICON_FILE = "Icon.png"
BRAND_LOGO_CANDIDATES = (
    "Logo réduit M blanc.svg",
    "Logo réduit M blanc.svg",
    os.path.join("icons", "Logo réduit M blanc.svg"),
    os.path.join("icons", "Logo réduit M blanc.svg"),
    os.path.join("Icons", "Logo réduit M blanc.svg"),
    os.path.join("Icons", "Logo réduit M blanc.svg"),
)
APP_ICON_CANDIDATES = (
    os.path.join("icons", "Icon V2.svg"),
    os.path.join("Icons", "Icon V2.svg"),
    os.path.join("icons", "Icon V2.png"),
    os.path.join("Icons", "Icon V2.png"),
    APP_ICON_FILE,
)
BUNDLED_MEDIA_SDK_HINTS = (
    os.path.join("MediaSDK", "bin", "MSASDKBridge.exe"),
    os.path.join("MediaSDK", "bin", "MediaSDKTest.exe"),
    os.path.join("MediaSDK", "bin"),
    os.path.join("vendor", "MediaSDK", "bin", "MSASDKBridge.exe"),
    os.path.join("vendor", "MediaSDK", "bin", "MediaSDKTest.exe"),
    os.path.join("vendor", "MediaSDK", "bin"),
    os.path.join(
        "Windows_CameraSDK-2.1.1_MediaSDK-3.1.3",
        "MediaSDK-3.1.3-20260128-win64",
        "MediaSDK",
        "bin",
        "MSASDKBridge.exe",
    ),
    os.path.join(
        "Windows_CameraSDK-2.1.1_MediaSDK-3.1.3",
        "MediaSDK-3.1.3-20260128-win64",
        "MediaSDK",
        "bin",
        "MediaSDKTest.exe",
    ),
    os.path.join(
        "Windows_CameraSDK-2.1.1_MediaSDK-3.1.3",
        "MediaSDK-3.1.3-20260128-win64",
        "MediaSDK",
        "bin",
    ),
)
QUEUE_DROP_EXTENSIONS = {".mp4", ".mov", ".insv", ".mkv"}
AUTO_IMPORT_VOLUME_NAME = "Insta360 X5"
AUTO_IMPORT_INPUT_DIRNAME = "input"
AUTO_IMPORT_DCIM_DIRNAME = "DCIM"
AUTO_IMPORT_SCAN_INTERVAL_MS = 2500
AUTO_IMPORT_STABLE_SEC = 2.0
THEME_MODE_ITEMS = (
    ("dark", "Sombre"),
    ("light", "Clair"),
)

THEME_PALETTES = {
    "dark": {
        "bg": "#08090B",
        "bg_mid": "#0D0F12",
        "bg_card": "#13161A",
        "bg_card_2": "#181C21",
        "text_hi": "#F7F9FC",
        "text_mid": "#BCC5D1",
        "text_lo": "#6E7886",
        "sand": "#DDE4EC",
        "green": "#38D793",
        "blue": "#8DB8FF",
        "red": "#FF6969",
        "border": "rgba(255,255,255,16)",
        "border_hi": "rgba(255,255,255,32)",
        "side_shell_bg": "rgba(14,16,19,236)",
        "hero_gradient": "qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 rgba(20,22,26,244), stop:0.58 rgba(15,17,20,240), stop:1 rgba(10,11,13,236))",
        "summary_card_bg": "rgba(18,20,24,238)",
        "table_shell_bg": "rgba(9,10,12,240)",
        "status_shell_bg": "rgba(15,17,20,230)",
        "tool_bg": "rgba(255,255,255,7)",
        "tool_border": "rgba(255,255,255,10)",
        "tool_hover_bg": "rgba(255,255,255,12)",
        "tool_hover_border": "rgba(255,255,255,18)",
        "tool_active_bg": "rgba(255,122,0,18)",
        "tool_active_border": "rgba(255,122,0,74)",
        "ghost_bg": "rgba(255,255,255,6)",
        "ghost_border": "rgba(255,255,255,10)",
        "ghost_hover_bg": "rgba(255,255,255,11)",
        "ghost_hover_border": "rgba(255,255,255,18)",
        "btn_pax_text": "rgba(255,244,230,210)",
        "btn_pax_filled": "rgba(255,255,255,230)",
        "btn_pax_hover": "#ffffff",
        "toggle_bg": "rgba(255,255,255,16)",
        "toggle_border": "rgba(255,255,255,10)",
        "toggle_hover_border": "rgba(255,255,255,18)",
        "toggle_checked_1": "#ff7a00",
        "toggle_checked_2": "#ff9b2f",
        "toggle_checked_border": "rgba(255,122,0,110)",
        "toggle_knob_bg": "#ffffff",
        "toggle_knob_border": "rgba(18,22,28,28)",
        "input_bg": "rgba(255,255,255,5)",
        "input_border": "rgba(255,255,255,10)",
        "input_focus_bg": "rgba(255,122,0,10)",
        "input_focus_border": "rgba(255,122,0,120)",
        "combo_popup_bg": "rgba(21,27,35,248)",
        "combo_popup_border": "rgba(255,255,255,12)",
        "combo_item_selected_bg": "rgba(255,255,255,9)",
        "combo_item_selected_border": "rgba(255,255,255,8)",
        "combo_item_hover_bg": "rgba(255,122,0,16)",
        "checkbox_bg": "rgba(0,0,0,30)",
        "checkbox_border": "rgba(255,244,230,20)",
        "log_bg": "rgba(7,10,14,204)",
        "log_border": "rgba(255,255,255,9)",
        "log_text": "rgba(255,255,255,235)",
        "progress_bg": "rgba(255,244,230,8)",
        "progress_fill_end": "#ffa040",
        "scroll_handle_bg": "rgba(255,244,230,18)",
        "scroll_handle_hover": "rgba(255,122,0,70)",
        "settings_card_bg": "rgba(19,25,32,238)",
        "chip_bg": "rgba(255,255,255,7)",
        "chip_border": "rgba(255,255,255,10)",
        "launch_disabled_bg": "#16191D",
        "launch_disabled_text": "rgba(255,255,255,115)",
        "launch_disabled_border": "rgba(255,255,255,18)",
        "launch_inactive_bg": "#171A1F",
        "launch_inactive_text": "rgba(255,255,255,190)",
        "launch_inactive_border": "rgba(255,255,255,18)",
        "table_select_bg": "rgba(255,122,0,10)",
        "row_selected_bg": "rgba(255,122,0,18)",
        "header_border": "rgba(255,122,0,38)",
        "header_border_soft": "rgba(255,122,0,36)",
        "logo_color": "#ffffff",
        "palette_window": "#09090F",
        "palette_window_text": "#ECEEF5",
        "palette_base": "#0E101A",
        "palette_text": "#ECEEF5",
        "palette_button": "#0E101A",
        "palette_button_text": "#ECEEF5",
        "palette_highlight_text": "#09090F",
    },
    "light": {
        "bg": "#F5F3EF",
        "bg_mid": "#EFECE6",
        "bg_card": "#FCFBF8",
        "bg_card_2": "#F6F3EE",
        "text_hi": "#15202B",
        "text_mid": "#5F6977",
        "text_lo": "#8C96A2",
        "sand": "#445260",
        "green": "#149A68",
        "blue": "#3C7DFF",
        "red": "#C85757",
        "border": "rgba(21,32,43,18)",
        "border_hi": "rgba(21,32,43,30)",
        "side_shell_bg": "rgba(250,248,244,238)",
        "hero_gradient": "qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 rgba(252,251,248,247), stop:0.58 rgba(247,244,239,244), stop:1 rgba(242,239,234,240))",
        "summary_card_bg": "rgba(252,251,248,242)",
        "table_shell_bg": "rgba(252,251,248,244)",
        "status_shell_bg": "rgba(252,251,248,232)",
        "tool_bg": "rgba(21,32,43,4)",
        "tool_border": "rgba(21,32,43,10)",
        "tool_hover_bg": "rgba(21,32,43,7)",
        "tool_hover_border": "rgba(21,32,43,18)",
        "tool_active_bg": "rgba(255,122,0,10)",
        "tool_active_border": "rgba(255,122,0,42)",
        "ghost_bg": "rgba(21,32,43,4)",
        "ghost_border": "rgba(21,32,43,10)",
        "ghost_hover_bg": "rgba(21,32,43,7)",
        "ghost_hover_border": "rgba(21,32,43,18)",
        "btn_pax_text": "#475566",
        "btn_pax_filled": "#15202B",
        "btn_pax_hover": "#0F1720",
        "toggle_bg": "rgba(21,32,43,12)",
        "toggle_border": "rgba(21,32,43,10)",
        "toggle_hover_border": "rgba(21,32,43,18)",
        "toggle_checked_1": "#ff7a00",
        "toggle_checked_2": "#ff9b2f",
        "toggle_checked_border": "rgba(255,122,0,110)",
        "toggle_knob_bg": "#ffffff",
        "toggle_knob_border": "rgba(21,32,43,18)",
        "input_bg": "rgba(21,32,43,5)",
        "input_border": "rgba(21,32,43,10)",
        "input_focus_bg": "rgba(255,122,0,8)",
        "input_focus_border": "rgba(255,122,0,110)",
        "combo_popup_bg": "rgba(255,252,247,248)",
        "combo_popup_border": "rgba(21,32,43,12)",
        "combo_item_selected_bg": "rgba(21,32,43,7)",
        "combo_item_selected_border": "rgba(21,32,43,10)",
        "combo_item_hover_bg": "rgba(255,122,0,12)",
        "checkbox_bg": "rgba(21,32,43,6)",
        "checkbox_border": "rgba(21,32,43,18)",
        "log_bg": "rgba(255,255,255,235)",
        "log_border": "rgba(21,32,43,12)",
        "log_text": "#15202B",
        "progress_bg": "rgba(21,32,43,8)",
        "progress_fill_end": "#ffb060",
        "scroll_handle_bg": "rgba(21,32,43,16)",
        "scroll_handle_hover": "rgba(255,122,0,74)",
        "settings_card_bg": "rgba(255,252,247,240)",
        "chip_bg": "rgba(21,32,43,5)",
        "chip_border": "rgba(21,32,43,10)",
        "launch_disabled_bg": "#E6E1D9",
        "launch_disabled_text": "rgba(21,32,43,145)",
        "launch_disabled_border": "rgba(21,32,43,16)",
        "launch_inactive_bg": "#E8E3DB",
        "launch_inactive_text": "#5D6672",
        "launch_inactive_border": "rgba(21,32,43,16)",
        "table_select_bg": "rgba(255,122,0,8)",
        "row_selected_bg": "rgba(255,122,0,12)",
        "header_border": "rgba(255,122,0,28)",
        "header_border_soft": "rgba(255,122,0,30)",
        "logo_color": "#15202B",
        "palette_window": "#F4EFE8",
        "palette_window_text": "#15202B",
        "palette_base": "#FFFCF8",
        "palette_text": "#15202B",
        "palette_button": "#FFFCF8",
        "palette_button_text": "#15202B",
        "palette_highlight_text": "#140C04",
    },
}

CURRENT_THEME_MODE = "dark"
C = dict(THEME_PALETTES[CURRENT_THEME_MODE])


def ui_font(value):
    return max(1, int(round(float(value) * FONT_SCALE)))


def ui_px(value):
    return max(1, int(round(float(value) * UI_SCALE)))


def ui_radius(value):
    return max(1, int(round(float(value) * RADIUS_SCALE)))


def normalize_theme_mode(mode):
    mode = str(mode or "dark").strip().lower()
    return mode if mode in THEME_PALETTES else "dark"


def theme_display_name(mode):
    mode = normalize_theme_mode(mode)
    for key, label in THEME_MODE_ITEMS:
        if key == mode:
            return label
    return "Sombre"


def build_stylesheet(c):
    fz = ui_font
    px = ui_px
    rd = ui_radius
    return f"""
QMainWindow, QDialog {{
    background-color: {c['bg']};
    color: {c['text_hi']};
    font-family: '{UI_FONT}', '{UI_FONT_FALLBACK}', sans-serif;
    font-size: {fz(13)}px;
    font-weight: 500;
}}

QWidget {{
    background: transparent;
    color: {c['text_hi']};
    font-family: '{UI_FONT}', '{UI_FONT_FALLBACK}', sans-serif;
    font-size: {fz(13)}px;
    font-weight: 500;
}}

QTableWidget {{
    background: transparent;
    border: none;
    gridline-color: transparent;
    outline: none;
    selection-background-color: transparent;
}}
QTableWidget::item {{
    background: transparent;
    border: none;
    padding: 0 {px(14)}px;
    color: {c['text_hi']};
    font-weight: 500;
    font-size: {fz(13)}px;
}}
QTableWidget::item:selected {{
    background: {c['row_selected_bg']};
    color: {c['text_hi']};
}}
QHeaderView {{
    background: transparent;
    border: none;
}}
QHeaderView::section {{
    background: transparent;
    color: {c['text_lo']};
    border: none;
    border-bottom: 1px solid {c['header_border']};
    padding: 0 {px(14)}px;
    height: {px(42)}px;
    font-size: {fz(10)}px;
    letter-spacing: 2.5px;
    font-weight: 700;
    font-family: '{UI_FONT}', sans-serif;
}}

QWidget#app_shell {{
    background: transparent;
}}
QWidget#side_shell {{
    background: {c['side_shell_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(24)}px;
}}
QWidget#content_shell {{
    background: transparent;
}}
QFrame#hero_shell {{
    background: {c['hero_gradient']};
    border: 1px solid {c['border']};
    border-radius: {rd(28)}px;
}}
QFrame#summary_card {{
    background: {c['summary_card_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(22)}px;
}}
QWidget#table_shell {{
    background: {c['table_shell_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(28)}px;
}}
QWidget#status_shell {{
    background: {c['status_shell_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(18)}px;
}}
QFrame#theme_toggle_shell {{
    background: {c['ghost_bg']};
    border: 1px solid {c['ghost_border']};
    border-radius: {rd(16)}px;
}}
QLabel#theme_toggle_icon {{
    background: transparent;
    border: none;
}}

QPushButton#btn_launch_active {{
    background-color: #ff8a1a;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #ffbe72, stop:0.52 #ff8a1a, stop:1 #e16400);
    color: #140c04;
    border: 1px solid rgba(255,244,230,48);
    border-radius: {rd(18)}px;
    padding: 0 {px(24)}px;
    height: {px(48)}px;
    font-size: {fz(13)}px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-align: center;
    qproperty-icon: none;
    font-family: '{UI_FONT}', sans-serif;
}}
QPushButton#btn_launch_active:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #ffc98b, stop:1 #ff7a00);
}}
QPushButton#btn_launch_active:pressed {{
    background: #c86010;
}}
QPushButton#btn_launch_active:disabled {{
    background-color: {c['launch_disabled_bg']};
    background: {c['launch_disabled_bg']};
    color: {c['launch_disabled_text']};
    border: 1px solid {c['launch_disabled_border']};
}}
QPushButton#btn_launch_inactive {{
    background-color: {c['launch_inactive_bg']};
    background: {c['launch_inactive_bg']};
    color: {c['launch_inactive_text']};
    border: 1px solid {c['launch_inactive_border']};
    border-radius: {rd(18)}px;
    padding: 0 {px(24)}px;
    height: {px(48)}px;
    font-size: {fz(13)}px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-align: center;
    qproperty-icon: none;
    font-family: '{UI_FONT}', sans-serif;
}}
QPushButton#btn_launch_inactive:hover {{
    background-color: {c['launch_inactive_bg']};
    background: {c['launch_inactive_bg']};
    color: {c['launch_inactive_text']};
    border: 1px solid {c['launch_inactive_border']};
}}
QPushButton#btn_launch_inactive:pressed {{
    background-color: {c['launch_inactive_bg']};
    background: {c['launch_inactive_bg']};
}}
QPushButton#btn_launch_inactive:disabled {{
    background-color: {c['launch_disabled_bg']};
    background: {c['launch_disabled_bg']};
    color: {c['launch_disabled_text']};
    border: 1px solid {c['launch_disabled_border']};
}}

QPushButton#btn_tool {{
    background: {c['tool_bg']};
    color: {c['text_mid']};
    border: 1px solid {c['tool_border']};
    border-radius: {rd(14)}px;
    font-size: {fz(14)}px;
    width: {px(46)}px; height: {px(46)}px;
    min-width: {px(46)}px; max-width: {px(46)}px;
    min-height: {px(46)}px; max-height: {px(46)}px;
}}
QPushButton#btn_tool:hover {{
    background: {c['tool_hover_bg']};
    color: {c['text_hi']};
    border-color: {c['tool_hover_border']};
}}
QPushButton#btn_tool[active="true"] {{
    background: {c['tool_active_bg']};
    color: {c['text_hi']};
    border-color: {c['tool_active_border']};
}}

QPushButton#btn_ghost {{
    background: {c['ghost_bg']};
    color: {c['text_mid']};
    border: 1px solid {c['ghost_border']};
    border-radius: {rd(16)}px;
    padding: 0 {px(18)}px;
    height: {px(42)}px;
    font-size: {fz(12)}px;
    font-family: '{UI_FONT}', sans-serif;
}}
QPushButton#btn_ghost:hover {{
    background: {c['ghost_hover_bg']};
    color: {c['text_hi']};
    border-color: {c['ghost_hover_border']};
}}

QPushButton#btn_del {{
    background: transparent;
    color: {c['text_lo']};
    border: none;
    font-size: {fz(15)}px;
    border-radius: {rd(6)}px;
    width: {px(32)}px; height: {px(32)}px;
    min-width: {px(32)}px; max-width: {px(32)}px;
}}
QPushButton#btn_del:hover {{
    background: rgba(239,68,68,15);
    color: {c['red']};
}}

QPushButton#btn_retry {{
    background: transparent;
    color: {c['red']};
    border: 1px solid rgba(239,68,68,40);
    border-radius: {rd(7)}px;
    padding: 0 {px(14)}px;
    height: {px(30)}px;
    font-size: {fz(11)}px;
    font-weight: 600;
    font-family: '{UI_FONT}', sans-serif;
}}
QPushButton#btn_retry:hover {{ background: rgba(239,68,68,12); }}

QPushButton#btn_pax {{
    background: transparent;
    color: {c['btn_pax_text']};
    border: none;
    border-radius: 0;
    padding: 0 {px(2)}px;
    height: {px(26)}px;
    font-size: {fz(12)}px;
    font-weight: 700;
    text-align: left;
    font-family: '{UI_FONT}', sans-serif;
}}
QPushButton#btn_pax:hover {{
    background: transparent;
    color: {c['btn_pax_hover']};
}}
QPushButton#btn_pax[filled="true"] {{
    color: {c['btn_pax_filled']};
    background: transparent;
}}

QPushButton#toggle_switch {{
    background: {c['toggle_bg']};
    border: 1px solid {c['toggle_border']};
    border-radius: {rd(12)}px;
    padding: 0;
}}
QPushButton#toggle_switch:hover {{
    border-color: {c['toggle_hover_border']};
}}
QPushButton#toggle_switch:checked {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {c['toggle_checked_1']}, stop:1 {c['toggle_checked_2']});
    border-color: {c['toggle_checked_border']};
}}
QFrame#toggle_knob {{
    background: {c['toggle_knob_bg']};
    border: 1px solid {c['toggle_knob_border']};
    border-radius: {rd(9)}px;
}}

QLineEdit, QSpinBox, QComboBox {{
    background: {c['input_bg']};
    border: 1px solid {c['input_border']};
    border-radius: {rd(12)}px;
    color: {c['text_hi']};
    padding: {px(9)}px {px(14)}px;
    font-size: {fz(12)}px;
    font-family: '{UI_FONT}', sans-serif;
}}
QAbstractSpinBox {{
    padding-left: 14px;
}}
QAbstractSpinBox QLineEdit, QSpinBox QLineEdit {{
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    selection-background-color: rgba(255,122,0,34);
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border-color: {c['input_focus_border']};
    background: {c['input_focus_bg']};
}}
QComboBox {{
    padding-right: {px(34)}px;
}}
QComboBox::drop-down {{
    border: none;
    width: {px(28)}px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0px;
    height: 0px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 0px;
    border: none;
    background: transparent;
}}
QSpinBox::up-arrow, QSpinBox::down-arrow {{
    width: 0px;
    height: 0px;
}}
QComboBox QAbstractItemView, QListView#combo_popup {{
    background: {c['combo_popup_bg']};
    border: 1px solid {c['combo_popup_border']};
    border-radius: 16px;
    outline: none;
    padding: 8px;
    color: {c['text_hi']};
    selection-background-color: transparent;
    font-family: '{UI_FONT}', sans-serif;
}}
QComboBox QAbstractItemView::item, QListView#combo_popup::item {{
    min-height: 36px;
    border-radius: 12px;
    padding: 0 14px;
    margin: 2px 4px;
    color: {c['text_hi']};
    background: transparent;
}}
QComboBox QAbstractItemView::item:selected, QListView#combo_popup::item:selected {{
    background: {c['combo_item_selected_bg']};
    color: {c['text_hi']};
    border: 1px solid {c['combo_item_selected_border']};
}}
QComboBox QAbstractItemView::item:hover, QListView#combo_popup::item:hover {{
    background: {c['combo_item_hover_bg']};
}}
QCheckBox {{
    color: {c['text_hi']};
    spacing: 9px;
    font-family: '{UI_FONT}', sans-serif;
}}
QCheckBox::indicator {{
    width: {px(18)}px; height: {px(18)}px;
    border: 1px solid {c['checkbox_border']};
    border-radius: {rd(6)}px;
    background: {c['checkbox_bg']};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
}}

QTextEdit#log_view {{
    background: {c['log_bg']};
    border: 1px solid {c['log_border']};
    color: {c['log_text']};
    font-size: {fz(11)}px;
    font-family: '{MONO_FONT}', 'Courier New', monospace;
    padding: {px(12)}px;
    border-radius: {rd(16)}px;
}}

QProgressBar {{
    background: {c['progress_bg']};
    border: none; border-radius: 3px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {ACCENT}, stop:1 {c['progress_fill_end']});
    border-radius: 3px;
}}

QScrollBar:vertical {{
    background: transparent; width: 4px;
}}
QScrollBar::handle:vertical {{
    background: {c['scroll_handle_bg']};
    border-radius: 2px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {c['scroll_handle_hover']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ height: 0; }}

QDialog {{ background: {c['bg_mid']}; }}
QTabWidget::pane {{
    border: none;
    background: transparent;
    top: 10px;
}}
QTabBar::tab {{
    background: {c['ghost_bg']};
    color: {c['text_mid']};
    padding: {px(12)}px {px(18)}px;
    border: 1px solid {c['ghost_border']};
    border-radius: {rd(16)}px;
    margin-right: {px(8)}px;
    font-size: {fz(11)}px; letter-spacing: 0.6px;
    font-weight: 700;
    font-family: '{UI_FONT}', sans-serif;
}}
QTabBar::tab:selected {{
    color: {c['text_hi']};
    background: {c['tool_hover_bg']};
    border-color: {c['tool_hover_border']};
}}
QTabBar::tab:hover {{
    color: {c['text_hi']};
    background: {c['ghost_hover_bg']};
}}
QFrame#settings_card {{
    background: {c['settings_card_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(24)}px;
}}
QFrame#settings_header {{
    background: {c['settings_card_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(28)}px;
}}
QFrame#settings_footer {{
    background: {c['settings_card_bg']};
    border: 1px solid {c['border']};
    border-radius: {rd(24)}px;
}}
QWidget#settings_row {{
    background: {c['ghost_bg']};
    border: 1px solid {c['ghost_border']};
    border-radius: {rd(16)}px;
}}
QWidget#settings_row:hover {{
    background: {c['ghost_hover_bg']};
    border-color: {c['tool_hover_border']};
}}
QLabel#section_eyebrow {{
    color: {ACCENT};
    font-size: {fz(10)}px;
    font-weight: 800;
    letter-spacing: 2px;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#section_title {{
    color: {c['text_hi']};
    font-size: {fz(16)}px;
    font-weight: 800;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#section_subtitle {{
    color: {c['text_mid']};
    font-size: {fz(11)}px;
    font-weight: 600;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#field_label {{
    color: {c['sand']};
    font-size: {fz(10)}px;
    font-weight: 700;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#settings_title {{
    color: {c['text_hi']};
    font-size: {fz(26)}px;
    font-weight: 800;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#settings_subtitle {{
    color: {c['text_mid']};
    font-size: {fz(12)}px;
    font-weight: 600;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#settings_footer_hint {{
    color: {c['text_mid']};
    font-size: {fz(11)}px;
    font-weight: 600;
    font-family: '{UI_FONT}', sans-serif;
}}
QLabel#hero_eyebrow {{
    color: {ACCENT};
    font-size: {fz(10)}px;
    font-weight: 800;
    letter-spacing: 2px;
}}
QLabel#hero_title {{
    color: {c['text_hi']};
    font-size: {fz(28)}px;
    font-weight: 800;
}}
QLabel#hero_subtitle {{
    color: {c['text_mid']};
    font-size: {fz(12)}px;
    font-weight: 600;
}}
QLabel#chip_label {{
    background: {c['chip_bg']};
    border: 1px solid {c['chip_border']};
    border-radius: {rd(15)}px;
    padding: {px(7)}px {px(12)}px;
    font-size: {fz(11)}px;
    font-weight: 700;
}}
QLabel#summary_value {{
    color: {c['text_hi']};
    font-size: {fz(22)}px;
    font-weight: 800;
}}
QLabel#summary_label {{
    color: {c['text_lo']};
    font-size: {fz(10)}px;
    font-weight: 700;
    letter-spacing: 1.5px;
}}
"""


def build_qpalette(c):
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(c["palette_window"]))
    pal.setColor(QPalette.WindowText, QColor(c["palette_window_text"]))
    pal.setColor(QPalette.Base, QColor(c["palette_base"]))
    pal.setColor(QPalette.AlternateBase, QColor(c["bg_card"]))
    pal.setColor(QPalette.Text, QColor(c["palette_text"]))
    pal.setColor(QPalette.Button, QColor(c["palette_button"]))
    pal.setColor(QPalette.ButtonText, QColor(c["palette_button_text"]))
    pal.setColor(QPalette.Highlight, QColor(ACCENT))
    pal.setColor(QPalette.HighlightedText, QColor(c["palette_highlight_text"]))
    pal.setColor(QPalette.ToolTipBase, QColor(c["palette_base"]))
    pal.setColor(QPalette.ToolTipText, QColor(c["text_hi"]))
    return pal


def apply_theme_mode(mode):
    global CURRENT_THEME_MODE, C, STYLESHEET
    CURRENT_THEME_MODE = normalize_theme_mode(mode)
    C = dict(THEME_PALETTES[CURRENT_THEME_MODE])
    STYLESHEET = build_stylesheet(C)
    app = QApplication.instance()
    if app is not None:
        app.setPalette(build_qpalette(C))
        app.setStyleSheet(STYLESHEET)


STYLESHEET = build_stylesheet(C)


# ══════════════════════════════════════════════════════════════
#  STATUTS & PRESET
# ══════════════════════════════════════════════════════════════
class Status:
    WAITING    = "waiting"
    PROCESSING = "processing"
    DONE       = "done"
    ERROR      = "error"

STATUS_CFG = {
    Status.WAITING:    ("En attente",   "text_lo", "clock"),
    Status.PROCESSING: ("En cours",     "blue",    "loader"),
    Status.DONE:       ("Terminé",      "green",   "check"),
    Status.ERROR:      ("Erreur",       "red",     "close"),
}

DEFAULT_PRESET = {
    "road_yaw": 0, "road_pitch": -10, "road_roll": 0,
    "road_hfov": 90, "road_vfov": 60,
    "cabin_yaw": 180, "cabin_pitch": -5, "cabin_roll": 0,
    "cabin_hfov": 120, "cabin_vfov": 80,
    "output_width": 1920, "output_height": 1080,
    "output_preset": "1080p", "output_fps": 0,
    "pip_width": 480, "pip_height": 270, "pip_margin": 20,
    "pip_position": "top_right",
    "quality_mode": "Équilibré",
    "insv_processing_mode": "Turbo",
    "video_bitrate": "12M", "preset_encode": "ultrafast", "crf": 22, "v360_interp": "line",
    "use_nvenc": True,
    "separate_files": False,
    "add_watermark": False, "watermark_path": "", "watermark_opacity": 80,
    "auto_open_output": True,
    "gen_thumbnail": True,
    "auto_reframe": False,
    "auto_analysis_seconds": 3,
    "auto_sample_count": 2,
    "auto_cabin_search_step": 45,
    "auto_cabin_min_conf": 0.5,
    "preview_before_render": True,
    "preview_timeout_sec": 180,
    "preview_timecode": 1.5,
    "output_prefix": "MSA",
    "output_date_folder": True,
    "ffmpeg_validated": False,
    "ffmpeg_resolved_path": "",
    "media_sdk_validated": False,
    "media_sdk_resolved_path": "",
    "sdk_autodetect_attempted": False,
    "delivery_enabled": False,
    "delivery_mock_mode": True,
    "delivery_send_email": True,
    "delivery_send_sms": False,
    "delivery_sender_name": "Motorsport Academy",
    "delivery_backend_url": "",
    "delivery_api_key": "",
    "delivery_link_ttl_days": 7,
    "update_auto_check": True,
    "update_manifest_url": "",
    "update_postponed_version": "",
    "theme_mode": "dark",
    "media_sdk_path": "", "ffmpeg_path": "", "output_dir": "",
}

QUALITY_PROFILES = {
    "Rapide": {"video_bitrate": "10M", "preset_encode": "ultrafast", "crf": 24, "v360_interp": "line"},
    "Équilibré": {"video_bitrate": "12M", "preset_encode": "ultrafast", "crf": 22, "v360_interp": "line"},
    "Haute qualité": {"video_bitrate": "15M", "preset_encode": "fast", "crf": 20, "v360_interp": "line"},
    "Personnalisé": {},
}
INSV_PROCESSING_MODES = {
    "Express": {
        "output_size": (1440, 720),
        "stitch_type": "template",
        "bitrate_bps": 8_000_000,
        "label": "Express : priorité vitesse, sortie 1440x720",
    },
    "Turbo": {
        "output_size": (1920, 960),
        "stitch_type": "template",
        "bitrate_bps": 10_000_000,
        "label": "Turbo : stitch rapide 1920x960",
    },
    "Standard": {
        "output_size": (2560, 1280),
        "stitch_type": "template",
        "bitrate_bps": 14_000_000,
        "label": "Standard : meilleur compromis vitesse/qualité",
    },
    "Qualité": {
        "output_size": None,
        "stitch_type": "optflow",
        "bitrate_bps": 24_000_000,
        "label": "Qualité : résolution 360 élevée pour recadrage fin",
    },
}
REFRAME_PRESETS_FILE = os.path.join(str(Path.home()), ".msa_reframe_presets.json")
STITCH_CACHE_DIR = os.path.join(str(Path.home()), ".msa_video_tool_cache", "stitch")
PREVIEW_CACHE_DIR = os.path.join(str(Path.home()), ".msa_video_tool_cache", "preview")
INPUT_STAGE_DIR = os.path.join(str(Path.home()), ".msa_video_tool_cache", "input_stage")
STITCH_CACHE_VERSION = 1
PREVIEW_CACHE_VERSION = 1
INPUT_STAGE_VERSION = 1
AUTO_STAGE_SLOW_INSV_INPUTS = True
INPUT_STAGE_CACHE_LOCK = threading.Lock()
SESSION_OUTPUT_MODE_KEY = "session_output_mode"
SESSION_OUTPUT_MODE_360 = "360_mp4"
DIRECT_360_LABEL = "360 MP4"
DIRECT_360_CHOICE_LABEL = "Mode direct · 360 MP4"
DELIVERY_CHUNK_SIZE = 8 * 1024 * 1024
UPDATE_CHECK_TIMEOUT_SEC = 8
DELIVERY_STATUS_LABELS = {
    "": "",
    "queued": "En attente",
    "uploading": "Upload",
    "processing": "Encodage",
    "sent": "Envoyé",
    "error": "Erreur",
}
OUTPUT_RESOLUTION_PRESETS = [
    ("custom", "Personnalise", None),
    ("720p", "720p", (1280, 720)),
    ("1080p", "1080p", (1920, 1080)),
    ("4k", "4K", (3840, 2160)),
    ("8k", "8K", (7680, 4320)),
]
OUTPUT_RESOLUTION_PRESET_MAP = {
    key: size for key, _label, size in OUTPUT_RESOLUTION_PRESETS if size is not None
}
OUTPUT_FPS_OPTIONS = [
    (0, "Source"),
    (24, "24 fps"),
    (25, "25 fps"),
    (30, "30 fps"),
    (50, "50 fps"),
    (60, "60 fps"),
]
REFRAME_PRESET_KEYS = [
    "road_yaw", "road_pitch", "road_hfov", "road_vfov",
    "cabin_yaw", "cabin_pitch", "cabin_hfov", "cabin_vfov",
    "pip_width", "pip_height", "pip_position",
]

def format_elapsed_label(seconds):
    seconds = max(0, int(round(float(seconds))))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def match_output_resolution_preset(width, height):
    try:
        size = (int(width), int(height))
    except Exception:
        return "custom"
    for key, preset_size in OUTPUT_RESOLUTION_PRESET_MAP.items():
        if preset_size == size:
            return key
    return "custom"


def normalize_output_preset(value, width, height):
    key = str(value or "").strip().lower()
    if key in {preset_key for preset_key, _label, _size in OUTPUT_RESOLUTION_PRESETS}:
        return key
    return match_output_resolution_preset(width, height)


def resolve_output_fps(preset):
    try:
        fps = int(float((preset or {}).get("output_fps", 0) or 0))
    except Exception:
        fps = 0
    return fps if fps > 0 else 0


def output_fps_args(preset):
    fps = resolve_output_fps(preset)
    return ["-r", str(fps)] if fps > 0 else []


def format_bitrate_bps(value):
    try:
        bps = max(0, int(value))
    except Exception:
        return ""
    if bps <= 0:
        return ""
    mbps = bps / 1_000_000.0
    if abs(mbps - round(mbps)) < 0.05:
        return f"{int(round(mbps))} Mb/s"
    return f"{mbps:.1f} Mb/s"

def load_reframe_presets():
    try:
        if os.path.exists(REFRAME_PRESETS_FILE):
            with open(REFRAME_PRESETS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return {}

def save_reframe_presets(data):
    try:
        with open(REFRAME_PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def normalize_delivery_recipients(data):
    recipients = []
    if not isinstance(data, list):
        return recipients
    for item in data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "") or "").strip()
        email = str(item.get("email", "") or "").strip()
        phone = str(item.get("phone", "") or "").strip()
        if not (name or email or phone):
            continue
        if not (email or phone):
            continue
        recipients.append({"name": name, "email": email, "phone": phone})
    return recipients


def summarize_delivery_recipients(recipients):
    recipients = normalize_delivery_recipients(recipients)
    count = len(recipients)
    if count <= 0:
        return "Ajouter clients…"
    label = f"{count} client(s)"
    names = [str(item.get("name") or "").strip() for item in recipients]
    names = [name for name in names if name]
    if names:
        label += " · " + " / ".join(names[:2])
        if len(names) > 2:
            label += "…"
    return label


def delivery_status_label(status):
    return DELIVERY_STATUS_LABELS.get(str(status or "").strip().lower(), "")


def compute_file_sha256(path_value, chunk_size=DELIVERY_CHUNK_SIZE):
    digest = hashlib.sha256()
    with open(path_value, "rb") as handle:
        while True:
            chunk = handle.read(int(chunk_size))
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def build_delivery_headers(api_key="", extra_headers=None, content_type="application/json"):
    headers = {"Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    token = str(api_key or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if isinstance(extra_headers, dict):
        headers.update({str(k): str(v) for k, v in extra_headers.items()})
    return headers


def http_json_request(url, method="GET", payload=None, headers=None, timeout=60):
    body = None
    req_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    request = urlrequest.Request(url, data=body, headers=req_headers, method=str(method or "GET").upper())
    try:
        with urlrequest.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            data = json.loads(raw) if raw.strip() else {}
            return {"ok": True, "status": getattr(response, "status", 200), "data": data, "raw": raw}
    except urlerror.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        try:
            data = json.loads(raw) if raw.strip() else {}
        except Exception:
            data = {"error": raw or str(exc)}
        return {"ok": False, "status": getattr(exc, "code", 500), "data": data, "raw": raw, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "status": 0, "data": {}, "raw": "", "error": str(exc)}


def parse_version_tuple(value):
    parts = [int(p) for p in re.findall(r"\d+", str(value or ""))]
    return tuple(parts or [0])


def is_newer_version(candidate, current):
    cand = parse_version_tuple(candidate)
    cur = parse_version_tuple(current)
    size = max(len(cand), len(cur))
    cand += (0,) * (size - len(cand))
    cur += (0,) * (size - len(cur))
    return cand > cur


def normalize_release_notes(value):
    if isinstance(value, list):
        lines = [str(item).strip() for item in value if str(item).strip()]
        return "\n".join(f"- {line}" for line in lines[:6])
    return str(value or "").strip()


def normalize_update_manifest_payload(data):
    payload = data if isinstance(data, dict) else {}
    version = str(payload.get("version") or payload.get("latest_version") or "").strip()
    download_url = str(
        payload.get("download_url")
        or payload.get("download")
        or payload.get("url")
        or payload.get("html_url")
        or ""
    ).strip()
    return {
        "title": str(payload.get("title") or "Nouvelle version disponible").strip(),
        "version": version,
        "download_url": download_url,
        "notes": normalize_release_notes(
            payload.get("notes") or payload.get("release_notes") or payload.get("changelog") or ""
        ),
    }


def build_update_prompt_message(current_version, latest_version, notes=""):
    lines = [
        f"Version installée : {current_version}",
        f"Nouvelle version : {latest_version}",
    ]
    notes = str(notes or "").strip()
    if notes:
        lines.extend(["", "Notes de version :", notes])
    lines.extend(["", "Télécharger la nouvelle version maintenant ?"])
    return "\n".join(lines)


def open_external_url(url):
    target = str(url or "").strip()
    if not target:
        return False
    try:
        if sys.platform == "win32":
            os.startfile(target)
            return True
        if sys.platform == "darwin":
            subprocess.Popen(["open", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        subprocess.Popen(["xdg-open", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        pass
    try:
        return bool(webbrowser.open(target, new=2))
    except Exception:
        return False


def find_curl_binary():
    candidates = [shutil.which("curl")]
    if os.name == "nt":
        candidates.append(r"C:\Windows\System32\curl.exe")
    candidates.append("curl")
    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        if candidate == "curl" or os.path.exists(candidate):
            return candidate
    return None


def upload_file_http(url, file_path, method="PUT", headers=None, timeout=3600):
    curl_bin = find_curl_binary()
    if not curl_bin:
        return {"ok": False, "error": "curl introuvable pour l'upload HTTP"}
    cmd = [curl_bin, "--fail", "--silent", "--show-error", "--location", "-X", str(method or "PUT").upper()]
    for key, value in (headers or {}).items():
        cmd.extend(["-H", f"{key}: {value}"])
    cmd.extend(["-T", str(file_path), str(url)])
    result = run_process(cmd, capture_output=True, text=True, timeout=timeout)
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def extract_reframe_preset_payload(data):
    if not isinstance(data, dict):
        return {}
    return {k: data[k] for k in REFRAME_PRESET_KEYS if k in data}


def resolve_session_output_mode(name="", payload=None):
    payload = payload if isinstance(payload, dict) else {}
    mode = str(payload.get(SESSION_OUTPUT_MODE_KEY, "") or "").strip().lower()
    if mode == SESSION_OUTPUT_MODE_360:
        return SESSION_OUTPUT_MODE_360
    compact_name = re.sub(r"\s+", "", str(name or "").strip().lower())
    compact_name = compact_name.replace("·", "").replace(".", "")
    if compact_name in {"360mp4", "modedirect360mp4"}:
        return SESSION_OUTPUT_MODE_360
    return ""


def describe_reframe_preset(name):
    if resolve_session_output_mode(name):
        return DIRECT_360_LABEL
    return name.strip() if str(name or "").strip() else "Popup"


def describe_reframe_choice(name):
    if resolve_session_output_mode(name):
        return DIRECT_360_CHOICE_LABEL
    return "Popup automatique" if not str(name or "").strip() else str(name).strip()


def ensure_stitch_cache_dir():
    path = Path(STITCH_CACHE_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_preview_cache_dir():
    path = Path(PREVIEW_CACHE_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_input_stage_dir():
    path = Path(INPUT_STAGE_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def session_stitch_cache_path(session_id, filename=""):
    safe_name = re.sub(r"[^\w\-]+", "_", str(filename or f"session_{session_id}")).strip("_") or f"session_{session_id}"
    safe_name = safe_name[:80]
    return str(ensure_stitch_cache_dir() / f"sid_{int(session_id)}_{safe_name}_equirect.mp4")


def session_preview_cache_dir(session_id, filename=""):
    safe_name = re.sub(r"[^\w\-]+", "_", str(filename or f"session_{session_id}")).strip("_") or f"session_{session_id}"
    safe_name = safe_name[:80]
    return str(ensure_preview_cache_dir() / f"sid_{int(session_id)}_{safe_name}")


def session_preview_cache_meta_path(session_id, filename=""):
    return str(Path(session_preview_cache_dir(session_id, filename)) / "preview_meta.json")


def safe_unlink(path_value):
    try:
        path = Path(str(path_value or "")).expanduser()
        if path.exists():
            path.unlink()
    except Exception:
        pass


def safe_rmtree(path_value):
    try:
        path = Path(str(path_value or "")).expanduser()
        if path.exists() and path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass


def _normalized_path(path_value):
    path = str(Path(path_value).expanduser().resolve())
    return path.lower() if os.name == "nt" else path


def file_signature(path_value):
    path = Path(path_value).expanduser().resolve()
    stat = path.stat()
    return {
        "path": _normalized_path(path),
        "size": int(stat.st_size),
        "mtime_ns": int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))),
    }

# ══════════════════════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════════════════════
class Database:
    def __init__(self, path="pipeline.db"):
        self.conn  = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        self._init()

    def _init(self):
        try:
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            self.conn.execute("PRAGMA temp_store=MEMORY")
            self.conn.execute("PRAGMA cache_size=-20000")
        except Exception:
            pass
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                filename     TEXT NOT NULL,
                filepath     TEXT NOT NULL,
                passengers   TEXT DEFAULT '[]',
                delivery_recipients TEXT DEFAULT '[]',
                delivery_status TEXT DEFAULT '',
                delivery_result_json TEXT DEFAULT '',
                reframe_preset_name TEXT DEFAULT '',
                reframe_preset_payload TEXT DEFAULT '',
                stitch_cache_path TEXT DEFAULT '',
                stitch_cache_meta TEXT DEFAULT '',
                status       TEXT DEFAULT 'waiting',
                progress     INTEGER DEFAULT 0,
                error_msg    TEXT DEFAULT '',
                output_paths TEXT DEFAULT '[]',
                sort_index   INTEGER DEFAULT 0,
                created_at   TEXT, updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT, videos_done INTEGER DEFAULT 0, total_sec REAL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_sort_index ON sessions(sort_index, id);
            CREATE INDEX IF NOT EXISTS idx_sessions_status_sort ON sessions(status, sort_index, id);
            CREATE INDEX IF NOT EXISTS idx_stats_date ON stats(date);
        """)
        try:
            cols = [r[1] for r in self.conn.execute("PRAGMA table_info(sessions)").fetchall()]
            if 'sort_index' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN sort_index INTEGER DEFAULT 0")
                self.conn.execute("UPDATE sessions SET sort_index=id WHERE sort_index IS NULL OR sort_index=0")
            if 'reframe_preset_name' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN reframe_preset_name TEXT DEFAULT ''")
            if 'reframe_preset_payload' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN reframe_preset_payload TEXT DEFAULT ''")
            if 'delivery_recipients' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN delivery_recipients TEXT DEFAULT '[]'")
            if 'delivery_status' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN delivery_status TEXT DEFAULT ''")
            if 'delivery_result_json' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN delivery_result_json TEXT DEFAULT ''")
            if 'stitch_cache_path' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN stitch_cache_path TEXT DEFAULT ''")
            if 'stitch_cache_meta' not in cols:
                self.conn.execute("ALTER TABLE sessions ADD COLUMN stitch_cache_meta TEXT DEFAULT ''")
        except Exception:
            pass
        self.conn.commit()

    def add_session(self, filename, filepath):
        now = datetime.now().isoformat()
        with self._lock:
            next_sort = self.conn.execute("SELECT COALESCE(MAX(sort_index),0)+1 FROM sessions").fetchone()[0]
            c = self.conn.execute(
                "INSERT INTO sessions (filename,filepath,sort_index,created_at,updated_at) VALUES(?,?,?,?,?)",
                (filename, filepath, next_sort, now, now))
            self.conn.commit(); return c.lastrowid

    def add_sessions(self, filepaths):
        rows = []
        now = datetime.now().isoformat()
        with self._lock:
            next_sort = self.conn.execute("SELECT COALESCE(MAX(sort_index),0)+1 FROM sessions").fetchone()[0]
            for filepath in filepaths:
                filename = Path(filepath).stem
                c = self.conn.execute(
                    "INSERT INTO sessions (filename,filepath,sort_index,created_at,updated_at) VALUES(?,?,?,?,?)",
                    (filename, filepath, next_sort, now, now))
                rows.append((c.lastrowid, filename, filepath))
                next_sort += 1
            self.conn.commit()
        return rows

    def delete_session(self, sid):
        with self._lock:
            row = self.conn.execute("SELECT stitch_cache_path FROM sessions WHERE id=?", (sid,)).fetchone()
            cache_path = row[0] if row and row[0] else ""
            self.conn.execute("DELETE FROM sessions WHERE id=?", (sid,))
            cache_refs = 0
            if cache_path:
                cache_refs = self.conn.execute(
                    "SELECT COUNT(*) FROM sessions WHERE stitch_cache_path=?",
                    (cache_path,),
                ).fetchone()[0]
            self.conn.commit()
            if cache_path and cache_refs <= 0:
                return cache_path
            return ""

    def update_session(self, sid, **kw):
        kw['updated_at'] = datetime.now().isoformat()
        cols = ",".join(f"{k}=?" for k in kw)
        with self._lock:
            self.conn.execute(f"UPDATE sessions SET {cols} WHERE id=?", [*kw.values(), sid])
            self.conn.commit()

    def update_sessions_reframe(self, session_ids, preset_name, payload_json):
        now = datetime.now().isoformat()
        with self._lock:
            for sid in session_ids:
                self.conn.execute(
                    "UPDATE sessions SET reframe_preset_name=?, reframe_preset_payload=?, updated_at=? WHERE id=?",
                    (preset_name, payload_json, now, sid),
                )
            self.conn.commit()

    def update_session_delivery(self, sid, recipients_json=None, status=None, result_json=None):
        values = {}
        if recipients_json is not None:
            values["delivery_recipients"] = recipients_json
        if status is not None:
            values["delivery_status"] = status
        if result_json is not None:
            values["delivery_result_json"] = result_json
        if values:
            self.update_session(sid, **values)

    def get_session_cache(self, sid):
        row = self.conn.execute(
            "SELECT stitch_cache_path, stitch_cache_meta FROM sessions WHERE id=?",
            (sid,),
        ).fetchone()
        return row or ("", "")

    def update_session_cache(self, sid, cache_path, cache_meta_json):
        now = datetime.now().isoformat()
        with self._lock:
            self.conn.execute(
                "UPDATE sessions SET stitch_cache_path=?, stitch_cache_meta=?, updated_at=? WHERE id=?",
                (cache_path or "", cache_meta_json or "", now, sid),
            )
            self.conn.commit()

    def cache_path_referenced_elsewhere(self, cache_path, exclude_sid=None):
        cache_path = str(cache_path or "").strip()
        if not cache_path:
            return False
        params = [cache_path]
        sql = "SELECT COUNT(*) FROM sessions WHERE stitch_cache_path=?"
        if exclude_sid is not None:
            sql += " AND id <> ?"
            params.append(exclude_sid)
        count = self.conn.execute(sql, params).fetchone()[0]
        return bool(count and int(count) > 0)

    def find_matching_stitch_cache(self, source_path, preset=None, exclude_sid=None):
        expected_meta = build_stitch_cache_signature(source_path, preset)
        params = []
        sql = (
            "SELECT id, stitch_cache_path, stitch_cache_meta "
            "FROM sessions WHERE stitch_cache_path <> ''"
        )
        if exclude_sid is not None:
            sql += " AND id <> ?"
            params.append(exclude_sid)
        sql += " ORDER BY updated_at DESC, id DESC"
        rows = self.conn.execute(sql, params).fetchall()
        for other_sid, cache_path, cache_meta_json in rows:
            try:
                cache_meta = json.loads(cache_meta_json or "{}")
            except Exception:
                continue
            cache_ok, _cache_reason, _expected_meta = validate_stitch_cache(cache_path, cache_meta, source_path, preset=preset)
            if cache_ok:
                return {
                    "sid": other_sid,
                    "cache_path": cache_path,
                    "cache_meta_json": json.dumps(expected_meta, ensure_ascii=False),
                    "expected_meta": expected_meta,
                }
        return None

    def get_all(self):
        return self.conn.execute(
            "SELECT id,filename,passengers,delivery_recipients,delivery_status,delivery_result_json,reframe_preset_name,reframe_preset_payload,status,progress,error_msg,output_paths FROM sessions ORDER BY sort_index, id"
        ).fetchall()

    def get_pending(self):
        return self.conn.execute(
            "SELECT id,filename,filepath,passengers,reframe_preset_name,reframe_preset_payload FROM sessions WHERE status=? ORDER BY sort_index, id",
            (Status.WAITING,)).fetchall()

    def move_session(self, sid, direction):
        with self._lock:
            rows = self.conn.execute(
                "SELECT id, sort_index, status FROM sessions ORDER BY sort_index, id"
            ).fetchall()
            idx = next((i for i, r in enumerate(rows) if r[0] == sid), None)
            if idx is None:
                return False
            target = idx + direction
            if target < 0 or target >= len(rows):
                return False
            other = rows[target]
            if rows[idx][2] != Status.WAITING or other[2] != Status.WAITING:
                return False
            self.conn.execute("UPDATE sessions SET sort_index=? WHERE id=?", (other[1], sid))
            self.conn.execute("UPDATE sessions SET sort_index=? WHERE id=?", (rows[idx][1], other[0]))
            self.conn.commit()
            return True

    def set_order(self, ordered_ids):
        with self._lock:
            if not ordered_ids:
                return False
            rows = self.conn.execute("SELECT id FROM sessions ORDER BY sort_index, id").fetchall()
            existing = [r[0] for r in rows]
            if set(existing) != set(ordered_ids):
                return False
            for idx, sid in enumerate(ordered_ids, start=1):
                self.conn.execute("UPDATE sessions SET sort_index=? WHERE id=?", (idx, sid))
            self.conn.commit()
            return True

    def reset(self, sid):
        self.update_session(sid, status=Status.WAITING, progress=0, error_msg='')

    def clear(self):
        with self._lock:
            rows = self.conn.execute(
                "SELECT stitch_cache_path FROM sessions WHERE stitch_cache_path <> ''"
            ).fetchall()
            self.conn.execute("DELETE FROM sessions")
            self.conn.commit()
            unique_paths = []
            seen = set()
            for row in rows:
                if not row or not row[0]:
                    continue
                cache_path = row[0]
                if cache_path in seen:
                    continue
                seen.add(cache_path)
                unique_paths.append(cache_path)
            return unique_paths

    def add_stat(self, sec):
        today = datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            r = self.conn.execute("SELECT id,videos_done,total_sec FROM stats WHERE date=?",(today,)).fetchone()
            if r: self.conn.execute("UPDATE stats SET videos_done=?,total_sec=? WHERE id=?",(r[1]+1,r[2]+sec,r[0]))
            else:  self.conn.execute("INSERT INTO stats (date,videos_done,total_sec) VALUES(?,?,?)",(today,1,sec))
            self.conn.commit()

    def get_stats_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        r = self.conn.execute("SELECT videos_done,total_sec FROM stats WHERE date=?",(today,)).fetchone()
        return r or (0, 0.0)

    def existing_filepath_keys(self):
        with self._lock:
            rows = self.conn.execute("SELECT filepath FROM sessions").fetchall()
        keys = set()
        for row in rows:
            if row and row[0]:
                keys.add(normalized_path_key(row[0]))
        return keys

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
SDK_EXECUTABLE_NAMES = (
    "MSASDKBridge.exe", "MSASDKBridge",
    "MediaSDKTest.exe", "MediaSDKTest",
    "RealTimeStitcherSDKTest.exe", "RealTimeStitcherSDKTest",
    "ProStitcher.exe", "ProStitcher",
    "Insta360Stitcher.exe", "Insta360Stitcher",
)
IMAGE_SOURCE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SDK_PROGRESS_RE = re.compile(r"process\s*=\s*(\d+)\s*%", re.IGNORECASE)
SDK_SEARCH_HINTS = ("sdk", "insta360", "media", "camera", "stitch", "windows_camerasdk", "mediasdk")

SVG_ICON_TEMPLATES = {
    "sun": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="4.2" stroke="{color}" stroke-width="1.8"/><path d="M12 2.8v2.4M12 18.8v2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M2.8 12h2.4M18.8 12h2.4M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "moon": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M14.6 3.4a8.7 8.7 0 1 0 6 14.8 7.5 7.5 0 1 1-6-14.8Z" stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "settings": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M4 7h10M17 7h3M10 17H4M20 17h-6M14 7a2 2 0 1 1 4 0 2 2 0 0 1-4 0Zm-4 10a2 2 0 1 1 4 0 2 2 0 0 1-4 0Z" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "list": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "trash": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M4 7h16M9 7V4h6v3M8 11v6M12 11v6M16 11v6M6 7l1 12h10l1-12" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "compass": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="{color}" stroke-width="1.8"/><path d="M14.8 9.2 13 13l-3.8 1.8L11 11l3.8-1.8Z" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "plus": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "pause": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M9 5v14M15 5v14" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/></svg>',
    "stop": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><rect x="6.5" y="6.5" width="11" height="11" rx="1.6" stroke="{color}" stroke-width="1.8"/></svg>',
    "play": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="m9 7 8 5-8 5V7Z" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M7 7l10 10M17 7 7 17" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "retry": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M20 11a8 8 0 1 0 2 5.3M20 11V5m0 6h-6" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "mail": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><rect x="4" y="6.5" width="16" height="11" rx="2" stroke="{color}" stroke-width="1.8"/><path d="m6 8 6 4 6-4" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="m5.5 12.5 4.2 4.2L18.5 8" stroke="{color}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="{color}" stroke-width="1.8"/><path d="M12 8v4l2.8 1.8" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "loader": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M12 4a8 8 0 1 1-7.2 4.5" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "info": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="{color}" stroke-width="1.8"/><path d="M12 10.2v5.2M12 7.8h.01" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="M12 5.4 18.7 17H5.3L12 5.4Z" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 9.5v3.8M12 15.8h.01" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chevron_down": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"><path d="m7 10 5 5 5-5" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def resource_path(*parts):
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, *parts)


def app_runtime_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.abspath(os.path.dirname(__file__))


def app_input_dir(ensure=True):
    path = os.path.join(app_runtime_dir(), AUTO_IMPORT_INPUT_DIRNAME)
    if ensure:
        os.makedirs(path, exist_ok=True)
    return path


def normalized_path_key(path_value):
    try:
        raw = str(path_value or "")
    except Exception:
        raw = ""
    return os.path.normcase(os.path.abspath(raw))


def normalize_volume_name(name):
    return " ".join(str(name or "").strip().split()).casefold()


def list_mounted_storage_roots():
    mounts = []
    if sys.platform == "darwin":
        volumes_root = Path("/Volumes")
        if volumes_root.exists():
            for child in sorted(volumes_root.iterdir(), key=lambda item: item.name.lower()):
                if child.is_dir():
                    mounts.append((child.name, str(child)))
        return mounts
    if os.name == "nt":
        try:
            import ctypes
            from string import ascii_uppercase

            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            volume_buffer = ctypes.create_unicode_buffer(1024)
            fs_buffer = ctypes.create_unicode_buffer(1024)
            serial = ctypes.c_uint()
            max_component_length = ctypes.c_uint()
            flags = ctypes.c_uint()
            for index, letter in enumerate(ascii_uppercase):
                if not (bitmask & (1 << index)):
                    continue
                root = f"{letter}:\\"
                label = ""
                try:
                    ok = ctypes.windll.kernel32.GetVolumeInformationW(
                        ctypes.c_wchar_p(root),
                        volume_buffer,
                        len(volume_buffer),
                        ctypes.byref(serial),
                        ctypes.byref(max_component_length),
                        ctypes.byref(flags),
                        fs_buffer,
                        len(fs_buffer),
                    )
                    if ok:
                        label = volume_buffer.value or ""
                except Exception:
                    label = ""
                mounts.append((label or letter, root))
        except Exception:
            return []
        return mounts
    for base_path in ("/media", "/run/media", "/mnt", "/Volumes"):
        base = Path(base_path)
        if not base.exists():
            continue
        for child in sorted(base.iterdir(), key=lambda item: item.name.lower()):
            if child.is_dir():
                mounts.append((child.name, str(child)))
    return mounts


def find_named_volume_mount(volume_name):
    target = normalize_volume_name(volume_name)
    if not target:
        return ""
    for label, root in list_mounted_storage_roots():
        if normalize_volume_name(label) == target or normalize_volume_name(Path(root).name) == target:
            return root
    return ""


def find_dcim_dir(mount_root):
    if not mount_root:
        return ""
    root = Path(mount_root)
    if not root.exists():
        return ""
    try:
        for child in root.iterdir():
            if child.is_dir() and child.name.casefold() == AUTO_IMPORT_DCIM_DIRNAME.casefold():
                return str(child)
    except Exception:
        return ""
    return ""


def iter_media_files(root_dir):
    root = Path(root_dir)
    if not root.exists():
        return []
    files = []
    try:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in QUEUE_DROP_EXTENSIONS:
                files.append(str(path))
    except Exception:
        return []
    files.sort(key=lambda item: item.lower())
    return files


def is_path_stable(path_value, min_age_sec=AUTO_IMPORT_STABLE_SEC):
    try:
        stat = os.stat(path_value)
    except OSError:
        return False
    if stat.st_size <= 0:
        return False
    return (time.time() - stat.st_mtime) >= float(min_age_sec)


def unique_destination_path(path_value):
    candidate = Path(path_value)
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    idx = 1
    while True:
        probe = candidate.with_name(f"{stem}_{idx}{suffix}")
        if not probe.exists():
            return probe
        idx += 1


def move_media_tree_to_input(dcim_dir, input_dir):
    src_root = Path(dcim_dir)
    dst_root = Path(input_dir)
    dst_root.mkdir(parents=True, exist_ok=True)
    moved = []
    for source_path_str in iter_media_files(dcim_dir):
        source_path = Path(source_path_str)
        try:
            relative_path = source_path.relative_to(src_root)
        except ValueError:
            relative_path = Path(source_path.name)
        destination_path = unique_destination_path(dst_root / relative_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(destination_path))
        moved.append(str(destination_path))
    try:
        empty_dirs = sorted(
            [path for path in src_root.rglob("*") if path.is_dir()],
            key=lambda item: len(item.parts),
            reverse=True,
        )
        for directory in empty_dirs:
            try:
                directory.rmdir()
            except OSError:
                continue
    except Exception:
        pass
    return moved


def find_existing_resource(*candidate_parts):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    for candidate in candidate_parts:
        if not candidate:
            continue
        bundled = resource_path(candidate)
        if os.path.exists(bundled):
            return bundled
        local = os.path.join(base_dir, candidate)
        if os.path.exists(local):
            return local
    return ""


def find_bundled_sdk_binary():
    seen = set()
    for candidate in BUNDLED_MEDIA_SDK_HINTS:
        existing = find_existing_resource(candidate)
        if not existing or existing in seen:
            continue
        seen.add(existing)
        resolved, _base = resolve_sdk_binary(existing)
        if resolved:
            return resolved
    return ""


def is_runtime_bundled_path(path_value):
    raw = (path_value or "").strip()
    if not raw:
        return False
    try:
        resolved = str(Path(raw).expanduser().resolve())
    except Exception:
        resolved = os.path.abspath(raw)

    meipass = getattr(sys, "_MEIPASS", "")
    if meipass:
        try:
            meipass_resolved = str(Path(meipass).resolve())
        except Exception:
            meipass_resolved = os.path.abspath(meipass)
        prefix = meipass_resolved.rstrip(os.sep) + os.sep
        if resolved == meipass_resolved or resolved.startswith(prefix):
            return True
    return False


def device_pixel_ratio():
    app = QApplication.instance()
    if app:
        try:
            screen = app.primaryScreen()
            if screen:
                return max(1.0, float(screen.devicePixelRatio()))
        except Exception:
            pass
    return 1.0


def available_screen_geometry(widget=None):
    app = QApplication.instance()
    screen = None
    if widget is not None:
        try:
            handle = widget.windowHandle()
            if handle is not None:
                screen = handle.screen()
        except Exception:
            screen = None
    if screen is None and app:
        try:
            screen = app.primaryScreen()
        except Exception:
            screen = None
    return screen.availableGeometry() if screen else QRect(0, 0, 1440, 900)


def apply_initial_window_size(widget, width_ratio=0.9, height_ratio=0.88, min_width=1180, min_height=760, max_width=None, max_height=None):
    geo = available_screen_geometry(widget)
    target_w = max(int(min_width), int(geo.width() * float(width_ratio)))
    target_h = max(int(min_height), int(geo.height() * float(height_ratio)))
    if max_width is not None:
        target_w = min(int(max_width), target_w)
    if max_height is not None:
        target_h = min(int(max_height), target_h)
    target_w = min(target_w, max(int(min_width), geo.width() - 24))
    target_h = min(target_h, max(int(min_height), geo.height() - 24))
    widget.resize(target_w, target_h)
    widget.move(
        geo.x() + max(0, (geo.width() - target_w) // 2),
        geo.y() + max(0, (geo.height() - target_h) // 2),
    )


def _render_svg_markup(svg_markup, width, height):
    if not HAS_SVG:
        return QPixmap()
    renderer = QSvgRenderer(QByteArray(svg_markup.encode("utf-8")))
    if not renderer.isValid():
        return QPixmap()
    oversample = max(2, int(round(device_pixel_ratio())))
    render_w = max(1, int(width * oversample))
    render_h = max(1, int(height * oversample))
    pixmap = QPixmap(render_w, render_h)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    target = QRectF(0, 0, render_w, render_h)
    view_box = renderer.viewBoxF()
    if not view_box.isNull() and view_box.width() > 0 and view_box.height() > 0:
        source_ratio = view_box.width() / view_box.height()
        target_ratio = render_w / max(1.0, float(render_h))
        if source_ratio > target_ratio:
            target_h = render_w / source_ratio
            target = QRectF(0, (render_h - target_h) / 2.0, render_w, target_h)
        else:
            target_w = render_h * source_ratio
            target = QRectF((render_w - target_w) / 2.0, 0, target_w, render_h)
    renderer.render(painter, target)
    painter.end()
    pixmap.setDevicePixelRatio(float(oversample))
    return pixmap


def svg_pixmap(name, color=None, size=18):
    svg_template = SVG_ICON_TEMPLATES.get(name)
    if not svg_template or not HAS_SVG:
        return QPixmap()
    svg_markup = svg_template.format(color=color or C["text_mid"])
    return _render_svg_markup(svg_markup, size, size)


def svg_icon(name, color=None, size=18):
    pixmap = svg_pixmap(name, color=color, size=size)
    if pixmap.isNull():
        return QIcon()
    return QIcon(pixmap)


def apply_button_icon(button, icon_name, color=None, size=16):
    icon = svg_icon(icon_name, color=color, size=size)
    button.setIcon(icon)
    button.setIconSize(QSize(size, size))


def icon_label(icon_name, color=None, size=18):
    label = QLabel()
    label.setFixedSize(size, size)
    label.setPixmap(svg_pixmap(icon_name, color=color, size=size))
    label.setStyleSheet("background:transparent; border:none;")
    return label


def configure_spinbox(spinbox):
    spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
    spinbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    editor = spinbox.lineEdit()
    if editor is not None:
        editor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        editor.setFrame(False)
        editor.setTextMargins(0, 0, 0, 0)
        editor.setStyleSheet("background:transparent; border:none; padding:0; margin:0;")
    return spinbox


def create_combo_popup_view(parent=None):
    view = QListView(parent)
    view.setObjectName("combo_popup")
    view.setSpacing(2)
    view.setUniformItemSizes(True)
    view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setFrameShape(QFrame.NoFrame)
    return view


def app_icon():
    icon_path = find_existing_resource(*APP_ICON_CANDIDATES)
    return QIcon(icon_path) if icon_path else QIcon()


def brand_logo_path():
    return find_existing_resource(*BRAND_LOGO_CANDIDATES)


def _force_svg_monochrome(svg_markup, color="#ffffff"):
    svg_markup = re.sub(r'fill\s*:\s*#[0-9A-Fa-f]{3,8}', f'fill: {color}', svg_markup)
    svg_markup = re.sub(r'fill=\"#[0-9A-Fa-f]{3,8}\"', f'fill="{color}"', svg_markup)
    svg_markup = re.sub(r'stroke\s*:\s*#[0-9A-Fa-f]{3,8}', f'stroke: {color}', svg_markup)
    svg_markup = re.sub(r'stroke=\"#[0-9A-Fa-f]{3,8}\"', f'stroke="{color}"', svg_markup)
    return svg_markup


def brand_logo_pixmap(width=56, height=24, color="#ffffff"):
    logo_path = brand_logo_path()
    if HAS_SVG and logo_path and logo_path.lower().endswith(".svg"):
        try:
            svg_markup = Path(logo_path).read_text(encoding="utf-8")
            svg_markup = _force_svg_monochrome(svg_markup, color=color)
            return _render_svg_markup(svg_markup, width, height)
        except Exception:
            pass
    pixmap = QPixmap()
    if logo_path:
        raw = QPixmap(logo_path)
        if not raw.isNull():
            pixmap = raw.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return pixmap


def brand_logo_widget(width=56, height=24, color="#ffffff"):
    label = QLabel()
    label.setFixedSize(width, height)
    label.setAlignment(Qt.AlignCenter)
    pixmap = brand_logo_pixmap(width=width, height=height, color=color)
    if not pixmap.isNull():
        label.setPixmap(pixmap)
    return label


def hidden_process_kwargs():
    if os.name != "nt":
        return {}
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return {"creationflags": creationflags, "startupinfo": startupinfo}


def run_process(cmd, timeout=None, **kwargs):
    params = dict(kwargs)
    params.update(hidden_process_kwargs())
    return subprocess.run(cmd, timeout=timeout, **params)


def popen_process(cmd, **kwargs):
    params = dict(kwargs)
    params.update(hidden_process_kwargs())
    return subprocess.Popen(cmd, **params)


def find_ffprobe(ffmpeg_path):
    if not ffmpeg_path:
        return None
    path_obj = Path(ffmpeg_path)
    candidates = []
    if path_obj.name.lower() == "ffmpeg.exe":
        candidates.append(str(path_obj.with_name("ffprobe.exe")))
    elif path_obj.name.lower() == "ffmpeg":
        candidates.append(str(path_obj.with_name("ffprobe")))
    candidates.extend([
        resource_path("ffmpeg", "ffprobe.exe"),
        resource_path("ffmpeg", "ffprobe"),
        shutil.which("ffprobe"),
    ])
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def find_ffmpeg(custom=""):
    candidates = [
        custom,
        resource_path("ffmpeg", "ffmpeg.exe"),
        resource_path("ffmpeg", "ffmpeg"),
        resource_path("ffmpeg.exe"),
        resource_path("ffmpeg"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        shutil.which("ffmpeg"),
        "ffmpeg",
    ]
    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            result = run_process([candidate, "-version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return candidate
        except Exception:
            continue
    return None


def ffmpeg_diagnostic(custom=""):
    result = {
        "ok": False,
        "status": "FFmpeg introuvable",
        "version": "",
        "resolved_path": "",
        "source": "",
        "logs": [],
    }
    result["logs"].append("Diagnostic FFmpeg")
    candidate = find_ffmpeg(custom)
    if not candidate:
        result["logs"].append("Aucun exécutable FFmpeg utilisable n'a été trouvé.")
        return result
    try:
        proc = run_process([candidate, "-version"], capture_output=True, text=True, timeout=5)
        first_line = (proc.stdout or "").splitlines()[0] if proc.stdout else ""
        version = first_line.split(" ")[2] if len(first_line.split(" ")) > 2 else "?"
        result["ok"] = proc.returncode == 0
        result["version"] = version
        result["resolved_path"] = candidate
        if candidate.startswith(resource_path("ffmpeg")) or candidate == resource_path("ffmpeg.exe"):
            result["source"] = "embarqué"
        elif custom and os.path.abspath(candidate) == os.path.abspath(custom):
            result["source"] = "personnalisé"
        else:
            result["source"] = "système"
        result["status"] = f"FFmpeg {version} OK ({result['source']})"
        result["logs"].append(f"Chemin résolu : {candidate}")
        result["logs"].append(f"Version : {first_line or 'inconnue'}")
        if os.name == "nt":
            result["logs"].append("Lancement Windows configuré avec CREATE_NO_WINDOW.")
        return result
    except Exception as exc:
        result["logs"].append(f"Échec du lancement FFmpeg : {exc}")
        return result


def is_still_image_source(path_value):
    try:
        return Path(str(path_value)).suffix.lower() in IMAGE_SOURCE_EXTENSIONS
    except Exception:
        return False


def resolve_insv_processing_mode(preset=None):
    mode = str((preset or {}).get("insv_processing_mode", "Turbo") or "Turbo").strip()
    if mode not in INSV_PROCESSING_MODES:
        mode = "Turbo"
    return mode


def describe_insv_processing_mode(mode):
    return INSV_PROCESSING_MODES.get(mode, INSV_PROCESSING_MODES["Turbo"])["label"]


def resolve_sdk_output_bitrate(preset=None):
    mode = resolve_insv_processing_mode(preset)
    bitrate_bps = INSV_PROCESSING_MODES.get(mode, {}).get("bitrate_bps")
    try:
        return max(0, int(bitrate_bps or 0))
    except Exception:
        return 0


def compute_sdk_output_size(preset=None):
    data = preset or {}
    mode = resolve_insv_processing_mode(data)
    fixed_size = INSV_PROCESSING_MODES.get(mode, {}).get("output_size")
    if fixed_size:
        width, height = fixed_size
        return int(width), int(height)
    output_width = max(1280, int(float(data.get("output_width", 1920) or 1920)))
    road_hfov = float(data.get("road_hfov", 90) or 90)
    road_hfov = max(60.0, min(150.0, road_hfov))
    recommended = int(math.ceil(output_width * 360.0 / road_hfov))
    max_cap = 5760 if output_width <= 1920 else 7680
    width = max(3840, min(max_cap, recommended))
    width = max(960, int(math.ceil(width / 32.0) * 32))
    height = max(480, int(width / 2))
    return width, height


def compute_sdk_preview_size(preset=None):
    mode = resolve_insv_processing_mode(preset)
    output_width = max(1280, int(float((preset or {}).get("output_width", 1920) or 1920)))
    if mode == "Express":
        width = 960
    else:
        width = 1280 if output_width <= 1920 else 1536
    width = max(960, int(math.ceil(width / 32.0) * 32))
    height = max(480, int(width / 2))
    return width, height


def resolve_sdk_stitch_type(preset=None):
    mode = resolve_insv_processing_mode(preset)
    stitch_type = INSV_PROCESSING_MODES.get(mode, {}).get("stitch_type", "optflow")
    explicit = str((preset or {}).get("insv_stitch_type", "") or "").strip().lower()
    if explicit in {"template", "optflow", "dynamicstitch", "aistitch"} and mode == "Qualité":
        stitch_type = explicit
    if stitch_type not in {"template", "optflow", "dynamicstitch", "aistitch"}:
        stitch_type = "optflow"
    return stitch_type


def resolve_sdk_preview_stitch_type(preset=None):
    stitch_type = str((preset or {}).get("insv_preview_stitch_type", "template") or "template").strip().lower()
    if stitch_type not in {"template", "optflow", "dynamicstitch", "aistitch"}:
        stitch_type = "template"
    return stitch_type


def build_stitch_cache_signature(source_path, preset=None):
    inputs = discover_insv_inputs(str(source_path))
    width, height = compute_sdk_output_size(preset)
    return {
        "version": STITCH_CACHE_VERSION,
        "processing_mode": resolve_insv_processing_mode(preset),
        "stitch_type": resolve_sdk_stitch_type(preset),
        "output_size": f"{width}x{height}",
        "bitrate_bps": resolve_sdk_output_bitrate(preset),
        "inputs": [file_signature(path) for path in inputs],
    }


def build_preview_cache_signature(source_path, preset=None):
    inputs = discover_insv_inputs(str(source_path))
    width, height = compute_sdk_preview_size(preset)
    return {
        "version": PREVIEW_CACHE_VERSION,
        "stitch_type": resolve_sdk_preview_stitch_type(preset),
        "output_size": f"{width}x{height}",
        "inputs": [file_signature(path) for path in inputs],
    }


def validate_stitch_cache(cache_path, cache_meta, source_path, preset=None):
    expected_meta = build_stitch_cache_signature(source_path, preset)
    cache_file = Path(str(cache_path or "")).expanduser() if cache_path else None
    if cache_file is None or not cache_file.exists() or cache_file.stat().st_size <= 0:
        return False, "cache absent", expected_meta
    if not isinstance(cache_meta, dict):
        return False, "métadonnées cache absentes", expected_meta
    expected_subset = {key: expected_meta.get(key) for key in ("version", "processing_mode", "stitch_type", "output_size", "inputs")}
    current_subset = {key: cache_meta.get(key) for key in ("version", "processing_mode", "stitch_type", "output_size", "inputs")}
    if current_subset != expected_subset:
        return False, "source ou paramètres de stitch modifiés", expected_meta
    return True, "ok", expected_meta


def find_preview_cache_image(preview_dir):
    preview_path = Path(str(preview_dir or "")).expanduser()
    if not preview_path.exists():
        return None
    images = sorted(preview_path.glob("*.jpg")) or sorted(preview_path.glob("*.png"))
    return str(images[0]) if images else None


def validate_preview_cache(preview_dir, cache_meta, source_path, preset=None):
    expected_meta = build_preview_cache_signature(source_path, preset)
    image_path = find_preview_cache_image(preview_dir)
    if not image_path or not Path(image_path).exists():
        return False, "aperçu absent", expected_meta, None
    if not isinstance(cache_meta, dict):
        return False, "métadonnées aperçu absentes", expected_meta, None
    expected_subset = {key: expected_meta.get(key) for key in ("version", "stitch_type", "output_size", "inputs")}
    current_subset = {key: cache_meta.get(key) for key in ("version", "stitch_type", "output_size", "inputs")}
    if current_subset != expected_subset:
        return False, "source ou paramètres aperçu modifiés", expected_meta, None
    return True, "ok", expected_meta, image_path


def build_input_stage_signature(input_paths):
    return {
        "version": INPUT_STAGE_VERSION,
        "inputs": [file_signature(path) for path in input_paths],
    }


def _windows_drive_type(path_value):
    if os.name != "nt":
        return None
    try:
        import ctypes

        resolved = str(Path(path_value).expanduser().resolve())
        if resolved.startswith("\\\\"):
            return 4
        drive, _tail = os.path.splitdrive(resolved)
        if not drive:
            return None
        get_drive_type = ctypes.windll.kernel32.GetDriveTypeW
        get_drive_type.argtypes = [ctypes.c_wchar_p]
        get_drive_type.restype = ctypes.c_uint
        return int(get_drive_type(drive + "\\"))
    except Exception:
        return None


def should_stage_insv_inputs(input_paths):
    inputs = [str(Path(path).expanduser().resolve()) for path in input_paths]
    if not AUTO_STAGE_SLOW_INSV_INPUTS or not inputs:
        return False, ""
    if os.name == "nt":
        for path in inputs:
            drive_type = _windows_drive_type(path)
            if drive_type == 2:
                return True, "support amovible"
            if drive_type == 4 or str(path).startswith("\\\\"):
                return True, "partage réseau"
        return False, ""
    lowered = [path.lower() for path in inputs]
    if sys.platform == "darwin" and any(path.startswith("/volumes/") for path in lowered):
        return True, "volume externe"
    if any(path.startswith(prefix) for path in lowered for prefix in ("/media/", "/mnt/")):
        return True, "volume externe"
    return False, ""


def _input_stage_paths(stage_dir, input_paths):
    stage_root = Path(stage_dir)
    destinations = []
    used_names = set()
    for index, input_path in enumerate(input_paths, start=1):
        name = Path(input_path).name
        target_name = name if name.lower() not in used_names else f"{index:02d}_{name}"
        used_names.add(target_name.lower())
        destinations.append(stage_root / target_name)
    return destinations


def prepare_insv_inputs_for_sdk(input_paths, log_fn=None):
    inputs = [str(Path(path).expanduser().resolve()) for path in input_paths]
    should_stage, stage_reason = should_stage_insv_inputs(inputs)
    if not should_stage:
        return {
            "inputs": inputs,
            "staged": False,
            "reused": False,
            "reason": "",
            "stage_dir": "",
        }

    signature = build_input_stage_signature(inputs)
    digest = hashlib.sha256(json.dumps(signature, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:24]
    stage_dir = ensure_input_stage_dir() / digest
    meta_path = stage_dir / "stage_meta.json"
    staged_paths = [str(path) for path in _input_stage_paths(stage_dir, inputs)]

    with INPUT_STAGE_CACHE_LOCK:
        try:
            stage_meta = {}
            if meta_path.exists():
                try:
                    with open(meta_path, "r", encoding="utf-8") as handle:
                        stage_meta = json.load(handle)
                except Exception:
                    stage_meta = {}
            if stage_meta.get("signature") == signature and all(Path(path).exists() and Path(path).stat().st_size > 0 for path in staged_paths):
                if log_fn:
                    log_fn(f"Entrées INSV locales réutilisées ({stage_reason})")
                return {
                    "inputs": staged_paths,
                    "staged": True,
                    "reused": True,
                    "reason": stage_reason,
                    "stage_dir": str(stage_dir),
                }

            safe_rmtree(stage_dir)
            stage_dir.mkdir(parents=True, exist_ok=True)
            if log_fn:
                log_fn(f"Support INSV lent détecté ({stage_reason}) — copie locale avant stitching…")
            destinations = _input_stage_paths(stage_dir, inputs)
            for src_path, dst_path in zip(inputs, destinations):
                shutil.copy2(src_path, dst_path)
            with open(meta_path, "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "signature": signature,
                        "reason": stage_reason,
                        "created_at": datetime.now().isoformat(timespec="seconds"),
                    },
                    handle,
                    ensure_ascii=False,
                    indent=2,
                )
            if log_fn:
                log_fn(f"Entrées INSV préparées localement : {stage_dir.name}")
            return {
                "inputs": [str(path) for path in destinations],
                "staged": True,
                "reused": False,
                "reason": stage_reason,
                "stage_dir": str(stage_dir),
            }
        except Exception as exc:
            if log_fn:
                log_fn(f"Préparation locale INSV ignorée — {exc}")
            return {
                "inputs": inputs,
                "staged": False,
                "reused": False,
                "reason": "",
                "stage_dir": "",
            }


def build_sdk_command(sdk_path, inputs, preset=None, output_path="", cpu_fallback=False):
    assets = resolve_sdk_assets(sdk_path)
    width, height = compute_sdk_output_size(preset)
    stitch_type = resolve_sdk_stitch_type(preset)
    bitrate_bps = resolve_sdk_output_bitrate(preset)
    image_processing_accel = "cpu" if cpu_fallback else "auto"

    cmd = [sdk_path]
    if assets["model_dir"]:
        cmd.extend(["-model_root_dir", assets["model_dir"]])
    cmd.extend([
        "-stitch_type", stitch_type,
        "-output_size", f"{width}x{height}",
        "-image_processing_accel", image_processing_accel,
        "-inputs", *[str(p) for p in inputs],
    ])
    if bitrate_bps > 0:
        cmd.extend(["-bitrate", str(int(bitrate_bps))])
    if output_path:
        cmd.extend(["-output", str(output_path)])
    cmd.extend(["-enable_flowstate", "-enable_directionlock"])
    if cpu_fallback:
        cmd.extend(["-disable_cuda", "-enable_soft_encode", "-enable_soft_decode"])
    return cmd, {
        "bin_dir": assets["bin_dir"] or None,
        "model_dir": assets["model_dir"],
        "output_size": f"{width}x{height}",
        "stitch_type": stitch_type,
        "output_bitrate_bps": bitrate_bps,
        "used_cpu_fallback": cpu_fallback,
    }


def build_sdk_preview_command(sdk_path, inputs, image_sequence_dir, preset=None, cpu_fallback=False, image_type="jpg", frame_index=0):
    assets = resolve_sdk_assets(sdk_path)
    width, height = compute_sdk_preview_size(preset)
    stitch_type = resolve_sdk_preview_stitch_type(preset)
    image_processing_accel = "cpu" if cpu_fallback else "auto"

    cmd = [sdk_path]
    if assets["model_dir"]:
        cmd.extend(["-model_root_dir", assets["model_dir"]])
    cmd.extend([
        "-stitch_type", stitch_type,
        "-output_size", f"{width}x{height}",
        "-image_processing_accel", image_processing_accel,
        "-inputs", *[str(p) for p in inputs],
        "-image_sequence_dir", str(image_sequence_dir),
        "-image_type", image_type,
        "-export_frame_index", str(int(frame_index)),
        "-enable_flowstate",
        "-enable_directionlock",
    ])
    if cpu_fallback:
        cmd.extend(["-disable_cuda"])
    return cmd, {
        "bin_dir": assets["bin_dir"] or None,
        "model_dir": assets["model_dir"],
        "output_size": f"{width}x{height}",
        "stitch_type": stitch_type,
        "used_cpu_fallback": cpu_fallback,
        "image_type": image_type,
    }


def _run_monitored_process(cmd, cwd=None, timeout=600, line_handler=None):
    proc = popen_process(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    events = queue.Queue()
    lines = []

    def reader():
        partial = []
        try:
            while True:
                ch = proc.stdout.read(1)
                if not ch:
                    break
                if ch in "\r\n":
                    text = "".join(partial).strip()
                    if text:
                        events.put(text)
                    partial = []
                else:
                    partial.append(ch)
        except Exception as exc:
            msg = str(exc).strip()
            if msg:
                events.put(msg)
        finally:
            text = "".join(partial).strip()
            if text:
                events.put(text)
            events.put(None)

    reader_thread = threading.Thread(target=reader, daemon=True)
    reader_thread.start()
    started = time.time()
    stream_closed = False
    timed_out = False

    while True:
        if timeout and (time.time() - started) > timeout and proc.poll() is None:
            timed_out = True
            try:
                proc.kill()
            except Exception:
                pass
            break
        try:
            item = events.get(timeout=0.2)
            if item is None:
                stream_closed = True
            else:
                lines.append(item)
                if line_handler:
                    line_handler(item)
        except queue.Empty:
            pass
        if proc.poll() is not None and stream_closed:
            break

    try:
        proc.wait(timeout=5)
    except Exception:
        pass
    reader_thread.join(timeout=1)

    while True:
        try:
            item = events.get_nowait()
        except queue.Empty:
            break
        if item is None:
            continue
        lines.append(item)
        if line_handler:
            line_handler(item)

    return {
        "returncode": proc.returncode if proc.returncode is not None else -9,
        "stdout": "\n".join(lines),
        "stderr": "",
        "timed_out": timed_out,
        "cmd": cmd,
        "lines": lines,
    }



def resolve_sdk_binary(path_value):
    raw = (path_value or "").strip()
    if not raw:
        return None, None
    path = Path(raw).expanduser()
    if path.is_file():
        return str(path), str(path.parent)
    if not path.is_dir():
        return None, None
    preferred_patterns = [
        "MediaSDK*/MediaSDK/bin/MSASDKBridge.exe",
        "MediaSDK*/MediaSDK/bin/MediaSDKTest.exe",
        "MediaSDK*/MediaSDK/bin/RealTimeStitcherSDKTest.exe",
        "MediaSDK/bin/MSASDKBridge.exe",
        "MediaSDK/bin/MediaSDKTest.exe",
        "MediaSDK/bin/RealTimeStitcherSDKTest.exe",
        "*/MediaSDK/bin/MSASDKBridge.exe",
        "*/MediaSDK/bin/MediaSDKTest.exe",
        "*/MediaSDK/bin/RealTimeStitcherSDKTest.exe",
    ]
    for pattern in preferred_patterns:
        matches = sorted(path.glob(pattern))
        if matches:
            match = matches[0]
            return str(match), str(match.parent)
    for name in SDK_EXECUTABLE_NAMES:
        candidate = path / name
        if candidate.exists():
            return str(candidate), str(path)
    exe_candidates = sorted(path.rglob("*.exe"))
    preferred_names = {"msasdkbridge.exe", "mediasdktest.exe", "realtimestitchersdktest.exe"}
    for candidate in exe_candidates:
        if candidate.name.lower() in preferred_names:
            return str(candidate), str(candidate.parent)
    for candidate in exe_candidates:
        lname = candidate.name.lower()
        if "camera" in lname:
            continue
        if any(token in lname for token in ("sdk", "stitch", "insta360", "media")):
            return str(candidate), str(candidate.parent)
    return None, str(path)


def candidate_sdk_search_roots():
    roots = []
    exe_dir = Path(getattr(sys, "executable", __file__)).resolve().parent
    script_dir = Path(__file__).resolve().parent
    cwd_dir = Path.cwd().resolve()
    home_dir = Path.home().resolve()

    def add_root(path_value, max_depth):
        if not path_value:
            return
        try:
            path = Path(path_value).expanduser().resolve()
        except Exception:
            path = Path(path_value).expanduser()
        if not path.exists():
            return
        key = str(path).lower()
        if any(existing[0] == key for existing in roots):
            return
        roots.append((key, str(path), int(max(2, max_depth))))

    add_root(exe_dir, 4)
    add_root(script_dir, 4)
    add_root(cwd_dir, 4)
    for bundled_hint in BUNDLED_MEDIA_SDK_HINTS:
        existing = find_existing_resource(bundled_hint)
        if not existing:
            continue
        existing_path = Path(existing)
        add_root(existing_path if existing_path.is_dir() else existing_path.parent, 3)
    add_root(home_dir / "Documents", 5)
    add_root(home_dir / "Downloads", 5)
    add_root(home_dir / "Desktop", 4)
    add_root(home_dir, 3)

    if os.name == "nt":
        env_roots = [
            (os.environ.get("USERPROFILE"), 4),
            (os.environ.get("LOCALAPPDATA"), 4),
            (os.environ.get("ProgramFiles"), 3),
            (os.environ.get("ProgramFiles(x86)"), 3),
            (os.environ.get("OneDrive"), 4),
        ]
        for env_path, depth in env_roots:
            add_root(env_path, depth)
            if env_path:
                add_root(Path(env_path) / "Documents", max(3, depth))
                add_root(Path(env_path) / "Downloads", max(3, depth))
                add_root(Path(env_path) / "Desktop", max(3, depth))
    return [(path_str, max_depth) for _key, path_str, max_depth in roots]


def _score_sdk_candidate(executable_path):
    path_obj = Path(executable_path)
    lower_name = path_obj.name.lower()
    lower_path = str(path_obj).lower()
    score = 0
    if lower_name == "msasdkbridge.exe":
        score += 650
    elif lower_name == "mediasdktest.exe":
        score += 500
    elif lower_name == "realtimestitchersdktest.exe":
        score += 350
    elif "insta360" in lower_name or "prostitcher" in lower_name:
        score += 220
    if "mediasdk" in lower_path:
        score += 200
    if f"{os.sep}bin{os.sep}" in lower_path:
        score += 80
    assets = resolve_sdk_assets(executable_path)
    if assets.get("model_dir"):
        score += 120
    score += min(80, int(assets.get("dll_count", 0)))
    return score


def autodetect_media_sdk(search_roots=None):
    result = {
        "ok": False,
        "status": "SDK non trouvé automatiquement",
        "resolved_path": "",
        "logs": [],
        "searched_roots": [],
        "candidates": [],
    }
    roots = search_roots or candidate_sdk_search_roots()
    if not roots:
        result["logs"].append("Aucun emplacement probable à analyser.")
        return result

    seen_candidates = set()
    ranked_candidates = []
    preferred_names = {name.lower() for name in SDK_EXECUTABLE_NAMES}

    for root_str, max_depth in roots:
        root = Path(root_str)
        if not root.exists():
            continue
        result["searched_roots"].append(root_str)
        result["logs"].append(f"Scan SDK : {root_str}")

        direct_resolved, _base = resolve_sdk_binary(root_str)
        if direct_resolved:
            key = str(Path(direct_resolved))
            if key not in seen_candidates:
                seen_candidates.add(key)
                ranked_candidates.append(( _score_sdk_candidate(direct_resolved), direct_resolved))

        try:
            for dirpath, dirnames, filenames in os.walk(root_str):
                current = Path(dirpath)
                try:
                    depth = len(current.relative_to(root).parts)
                except Exception:
                    depth = 0

                if depth >= max_depth:
                    dirnames[:] = []
                else:
                    filtered = []
                    for name in dirnames:
                        lname = name.lower()
                        if depth <= 1 or any(token in lname for token in SDK_SEARCH_HINTS):
                            filtered.append(name)
                    dirnames[:] = filtered

                hit_name = next((name for name in filenames if name.lower() in preferred_names), None)
                if not hit_name:
                    continue
                candidate = str(current / hit_name)
                if candidate in seen_candidates:
                    continue
                seen_candidates.add(candidate)
                ranked_candidates.append((_score_sdk_candidate(candidate), candidate))
        except Exception as exc:
            result["logs"].append(f"Avertissement : scan impossible sur {root_str} — {exc}")

    if not ranked_candidates:
        result["logs"].append("Aucun exécutable MediaSDK plausible n'a été trouvé.")
        return result

    ranked_candidates.sort(key=lambda item: (-item[0], item[1].lower()))
    result["candidates"] = [path for _score, path in ranked_candidates[:5]]
    best_score, best_path = ranked_candidates[0]
    result["logs"].append(f"Meilleur candidat : {best_path} (score {best_score})")

    diag = sdk_diagnostic(best_path)
    result["logs"].extend(diag.get("logs", []))
    result["resolved_path"] = diag.get("resolved_path", best_path)
    result["ok"] = diag.get("ok", False)
    if result["ok"]:
        result["status"] = "SDK détecté automatiquement"
    else:
        result["status"] = diag.get("status", result["status"])
    return result


def resolve_sdk_assets(sdk_binary):
    sdk_path = Path(sdk_binary)
    base_dir = sdk_path.parent
    candidates = [
        base_dir / "models",
        base_dir.parent / "models",
        base_dir.parent / "MediaSDK" / "models",
    ]
    model_dir = next((str(p) for p in candidates if p.exists() and p.is_dir()), "")
    return {
        "bin_dir": str(base_dir),
        "model_dir": model_dir,
        "dll_count": len(list(base_dir.glob("*.dll"))),
    }


def sdk_diagnostic(path_value):
    result = {
        "ok": False,
        "status": "SDK non configuré",
        "resolved_path": "",
        "base_dir": "",
        "logs": [],
        "warnings": [],
    }
    raw = (path_value or "").strip()
    if not raw:
        bundled = find_bundled_sdk_binary()
        if not bundled:
            result["logs"].append("Aucun chemin SDK n'est renseigné.")
            return result
        raw = bundled
        result["logs"].append(f"SDK embarqué détecté : {bundled}")

    given = Path(raw).expanduser()
    result["logs"].append(f"Chemin fourni : {given}")
    if not given.exists():
        bundled = find_bundled_sdk_binary()
        if bundled:
            raw = bundled
            given = Path(raw).expanduser()
            result["logs"].append("Le chemin renseigné est indisponible, fallback sur le SDK embarqué.")
            result["logs"].append(f"SDK embarqué détecté : {given}")
        else:
            result["status"] = "Chemin SDK invalide"
            result["logs"].append("Le chemin n'existe pas.")
            return result

    resolved, base_dir = resolve_sdk_binary(str(given))
    result["base_dir"] = base_dir or ""
    if not resolved:
        result["status"] = "Exécutable SDK introuvable"
        result["logs"].append("Aucun exécutable SDK n'a été détecté dans ce dossier.")
        return result

    base_path = Path(base_dir or Path(resolved).parent)
    assets = resolve_sdk_assets(resolved)
    result["resolved_path"] = resolved
    result["logs"].append(f"Exécutable détecté : {resolved}")
    dlls = list(base_path.glob("*.dll")) + list(base_path.rglob("*.dll"))
    model_dirs = []
    if assets["model_dir"]:
        model_dirs.append(Path(assets["model_dir"]))
    model_dirs.extend([p for p in base_path.iterdir() if p.is_dir() and any(token in p.name.lower() for token in ("model", "resource", "assets"))])
    seen_model_dirs = []
    seen_model_dir_keys = set()
    for model_dir in model_dirs:
        key = str(model_dir.resolve()) if model_dir.exists() else str(model_dir)
        if key not in seen_model_dir_keys:
            seen_model_dir_keys.add(key)
            seen_model_dirs.append(model_dir)
    model_dirs = seen_model_dirs
    if dlls:
        result["logs"].append(f"Binaires natifs détectés : {len(dlls)} DLL")
    else:
        result["warnings"].append("Aucune DLL détectée à côté du SDK.")
    if model_dirs:
        result["logs"].append("Ressources détectées : " + ", ".join(p.name for p in model_dirs[:4]))
    else:
        result["warnings"].append("Aucun dossier de modèles/ressources détecté.")

    try:
        test = run_process([resolved, "-help"], capture_output=True, text=True, timeout=8, cwd=assets["bin_dir"] or None)
        if test.returncode not in (0, 1):
            result["warnings"].append(f"Retour SDK inattendu : {test.returncode}")
        result["ok"] = True
        result["status"] = "SDK détecté"
        result["logs"].append("L'exécutable SDK répond à une commande simple.")
        if assets["model_dir"]:
            result["logs"].append(f"Dossier modèles : {assets['model_dir']}")
        else:
            result["warnings"].append("Dossier models introuvable pour le MediaSDK.")
    except subprocess.TimeoutExpired:
        result["ok"] = True
        result["status"] = "SDK détecté"
        result["logs"].append("Le SDK n'a pas répondu à -help à temps, mais la structure MediaSDK est valide.")
        if assets["model_dir"]:
            result["logs"].append(f"Dossier modèles : {assets['model_dir']}")
        else:
            result["warnings"].append("Dossier models introuvable pour le MediaSDK.")
    except Exception as exc:
        result["status"] = "SDK détecté mais non lançable"
        result["logs"].append(f"Échec de lancement du SDK : {exc}")
        return result

    for warning in result["warnings"]:
        result["logs"].append(f"Avertissement : {warning}")
    return result


def discover_insv_inputs(path_value):
    src = Path(path_value)
    if not src.exists():
        raise FileNotFoundError(f"Fichier introuvable : {src}")
    inputs = [src]
    match = re.search(r"_(00|10)_", src.name, re.IGNORECASE)
    if match:
        other = "10" if match.group(1) == "00" else "00"
        partner_name = re.sub(r"_(00|10)_", f"_{other}_", src.name, count=1, flags=re.IGNORECASE)
        partner = src.with_name(partner_name)
        if partner.exists():
            ordered = sorted([src, partner], key=lambda p: p.name)
            inputs = ordered
    return [str(p) for p in inputs]


def run_sdk_stitch(sdk_path, inputs, output_path, timeout=600, preset=None, log_fn=None, progress_fn=None):
    attempts = []
    last_result = None

    for idx, cpu_fallback in enumerate((False, True), start=1):
        try:
            out_path = Path(output_path)
            if out_path.exists():
                out_path.unlink()
        except Exception:
            pass
        cmd, meta = build_sdk_command(
            sdk_path,
            inputs,
            preset=preset,
            output_path=output_path,
            cpu_fallback=cpu_fallback,
        )
        if log_fn:
            mode_label = "CPU logiciel" if cpu_fallback else "GPU/auto"
            bitrate_label = format_bitrate_bps(meta.get("output_bitrate_bps"))
            bitrate_suffix = f" · {bitrate_label}" if bitrate_label else ""
            log_fn(f"SDK tentative {idx}/2 · {mode_label} · {meta['stitch_type']} · {meta['output_size']}{bitrate_suffix}")

        seen_progress = -10

        def handle_line(line):
            nonlocal seen_progress
            clean = str(line or "").strip()
            if not clean:
                return
            match = SDK_PROGRESS_RE.search(clean)
            if match:
                pct = max(0, min(100, int(match.group(1))))
                if progress_fn:
                    progress_fn(pct)
                if log_fn and pct >= seen_progress + 10:
                    log_fn(f"SDK {pct}%")
                    seen_progress = pct
                return
            if log_fn and any(token in clean.lower() for token in ("start stitch", "end stitch", "cost =", "error")):
                log_fn(f"SDK {clean}")

        result = _run_monitored_process(cmd, cwd=meta["bin_dir"], timeout=timeout, line_handler=handle_line)
        result.update(meta)
        result["attempt_index"] = idx
        result["attempts"] = attempts
        if result["returncode"] == 0 and Path(output_path).exists() and Path(output_path).stat().st_size > 0:
            result["ok"] = True
            return result
        attempts.append(result)
        last_result = result
        if not cpu_fallback and log_fn:
            log_fn("Le SDK n'a pas produit de MP4 exploitable. Relance en mode CPU.")

    if last_result is None:
        last_result = {"returncode": -1, "stdout": "", "stderr": "", "timed_out": False, "attempts": []}
    last_result["ok"] = False
    last_result["attempts"] = attempts
    return last_result


def run_sdk_preview_frame(sdk_path, inputs, image_sequence_dir, timeout=90, preset=None, log_fn=None):
    attempts = []
    output_dir = Path(image_sequence_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, cpu_fallback in enumerate((False, True), start=1):
        for img in list(output_dir.glob("*.jpg")) + list(output_dir.glob("*.png")):
            safe_unlink(img)
        cmd, meta = build_sdk_preview_command(
            sdk_path,
            inputs,
            image_sequence_dir,
            preset=preset,
            cpu_fallback=cpu_fallback,
            image_type="jpg",
            frame_index=0,
        )
        if log_fn:
            mode_label = "CPU logiciel" if cpu_fallback else "GPU/auto"
            log_fn(f"Aperçu INSV {idx}/2 · {mode_label} · {meta['output_size']}")

        result = _run_monitored_process(cmd, cwd=meta["bin_dir"], timeout=timeout)
        result.update(meta)
        images = sorted(output_dir.glob("*.jpg")) or sorted(output_dir.glob("*.png"))
        if result["returncode"] == 0 and images:
            result["ok"] = True
            result["image_path"] = str(images[0])
            return result
        attempts.append(result)
        if not cpu_fallback and log_fn:
            log_fn("Aperçu INSV relancé en mode CPU.")

    last_result = attempts[-1] if attempts else {"returncode": -1, "stdout": "", "stderr": "", "timed_out": False}
    last_result["ok"] = False
    last_result["attempts"] = attempts
    return last_result

def get_duration(ffmpeg, path):
    probe = find_ffprobe(ffmpeg)
    if not probe:
        return None
    try:
        r = run_process([probe,"-v","error","-show_entries","format=duration",
            "-of","default=noprint_wrappers=1:nokey=1",path],
            capture_output=True,text=True,timeout=30)
        return float(r.stdout.strip())
    except: return None

def pip_pos(position, margin):
    return {"bottom_right":f"W-w-{margin}:H-h-{margin}","bottom_left":f"{margin}:H-h-{margin}",
            "top_right":f"W-w-{margin}:{margin}","top_left":f"{margin}:{margin}"}.get(position,f"W-w-{margin}:H-h-{margin}")


def norm_yaw(yaw):
    while yaw > 180: yaw -= 360
    while yaw <= -180: yaw += 360
    return int(round(yaw))


def ffmpeg_common_args():
    return ["-hide_banner", "-loglevel", "error", "-nostats", "-threads", "0"]


def run_ffmpeg(ffmpeg, args, timeout=120):
    cmd=[ffmpeg, *ffmpeg_common_args(), *args]
    return run_process(cmd, capture_output=True, text=True, timeout=timeout)


def media_input_args(source_path, ts=None):
    if is_still_image_source(source_path):
        return ["-i", str(source_path)]
    args = []
    if ts is not None:
        args.extend(["-ss", f"{float(ts):.2f}"])
    args.extend(["-i", str(source_path)])
    return args


def best_video_encoder_args(preset):
    bitrate = preset.get("video_bitrate", "12M")
    if sys.platform == "darwin":
        return [
            "-c:v", "h264_videotoolbox",
            "-realtime", "true",
            "-b:v", bitrate,
            "-maxrate", bitrate,
            "-bufsize", str(max(2, int(float(bitrate[:-1]) * 2)) if bitrate.endswith("M") and bitrate[:-1].isdigit() else 24) + "M" if bitrate.endswith("M") else bitrate,
            "-profile:v", "high",
            "-pix_fmt", "yuv420p"
        ]
    if preset.get("use_nvenc") and sys.platform == "win32":
        return ["-c:v", "h264_nvenc", "-preset", "p1", "-tune", "ll", "-b:v", bitrate, "-pix_fmt", "yuv420p"]
    return ["-c:v", "libx264", "-preset", preset.get("preset_encode", "ultrafast"), "-crf", str(preset.get("crf", 22)), "-pix_fmt", "yuv420p"]


def render_view_frame(ffmpeg, video_path, out_path, yaw, pitch, hfov, vfov, ts, w=960, h=540, timeout=60, interp="line"):
    vf=(f"v360=e:rectilinear:yaw={yaw}:pitch={pitch}:roll=0:"
        f"h_fov={hfov}:v_fov={vfov}:w={w}:h={h}:interp={interp}")
    args=["-y", *media_input_args(video_path, ts), "-frames:v", "1", "-vf", vf, str(out_path)]
    return run_ffmpeg(ffmpeg, args, timeout=timeout)


def build_preview_image(ffmpeg, video_path, params, work_dir, preview_name="preview.jpg"):
    if cv2 is None:
        return None
    ts=float(params.get("preview_timecode", 1.5))
    route_path=os.path.join(work_dir, "preview_route.jpg")
    cabin_path=os.path.join(work_dir, "preview_cabin.jpg")
    composite_path=os.path.join(work_dir, preview_name)
    interp = params.get("v360_interp", "line")
    rr=render_view_frame(ffmpeg, video_path, route_path, params.get("road_yaw",0), params.get("road_pitch",0), params.get("road_hfov",90), params.get("road_vfov",60), ts, w=960, h=540, interp=interp)
    rc=render_view_frame(ffmpeg, video_path, cabin_path, params.get("cabin_yaw",180), params.get("cabin_pitch",-5), params.get("cabin_hfov",120), params.get("cabin_vfov",80), ts, w=max(320,int(params.get("pip_width",480))), h=max(180,int(params.get("pip_height",270))), interp=interp)
    if rr.returncode != 0 or rc.returncode != 0 or not os.path.exists(route_path) or not os.path.exists(cabin_path):
        return None
    bg=cv2.imread(route_path)
    pip=cv2.imread(cabin_path)
    if bg is None or pip is None:
        return None
    bg_h, bg_w = bg.shape[:2]
    target_w=min(bg_w-40, max(220, int(params.get("pip_width", 480))))
    target_h=min(bg_h-40, max(124, int(params.get("pip_height", 270))))
    pip=cv2.resize(pip, (target_w, target_h), interpolation=cv2.INTER_AREA)
    margin=int(params.get("pip_margin",20))
    pos=params.get("pip_position","top_right")
    if pos == "top_left":
        x, y = margin, margin
    elif pos == "top_right":
        x, y = bg_w - target_w - margin, margin
    elif pos == "bottom_left":
        x, y = margin, bg_h - target_h - margin
    else:
        x, y = bg_w - target_w - margin, bg_h - target_h - margin
    x=max(0, min(bg_w-target_w, x)); y=max(0, min(bg_h-target_h, y))
    cv2.rectangle(bg, (x-3, y-3), (x+target_w+3, y+target_h+3), (255,255,255), 2)
    bg[y:y+target_h, x:x+target_w] = pip
    cv2.imwrite(composite_path, bg)
    return composite_path




def _detect_faces_opencv(frame):
    if cv2 is None or OPENCV_FACE_CASCADE is None or frame is None or getattr(frame, "size", 0) == 0:
        return []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = OPENCV_FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if faces is None:
        return []
    return [tuple(map(int, f)) for f in faces]

def _face_score(detections, frame_shape=None):
    if not detections:
        return 0.0
    frame_area = 1.0
    if frame_shape is not None and len(frame_shape) >= 2:
        frame_area = max(1.0, float(frame_shape[0] * frame_shape[1]))
    score = 0.0
    for det in detections:
        if len(det) >= 4:
            x, y, w, h = det[:4]
            area = max(0.0, float(w)) * max(0.0, float(h))
            score += area / frame_area
    return float(score)


def _road_score(frame):
    """Heuristique simple pour trouver une vue route exploitable.
    On favorise une perspective avec des lignes fortes dans la moitié basse
    et un point de fuite proche du centre horizontal dans la moitié haute.
    """
    if frame is None or frame.size == 0:
        return 0.0

    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 70, 180)
    roi = edges[int(h * 0.18):, :]
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=45,
                            minLineLength=max(30, int(w * 0.08)), maxLineGap=25)
    if lines is None:
        return 0.0

    left = []
    right = []
    length_score = 0.0
    y_off = int(h * 0.18)
    for raw in lines[:, 0, :]:
        x1, y1, x2, y2 = map(float, raw)
        y1 += y_off
        y2 += y_off
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) < 1e-3:
            continue
        slope = dy / dx
        length = float((dx * dx + dy * dy) ** 0.5)
        if abs(slope) < 0.25:
            continue
        if max(y1, y2) < h * 0.45:
            continue
        length_score += length
        if slope < 0:
            left.append((x1, y1, x2, y2, slope, length))
        else:
            right.append((x1, y1, x2, y2, slope, length))

    if not left or not right:
        return min(length_score / 1500.0, 1.0) * 0.35

    vanishing_scores = []
    for l in sorted(left, key=lambda x: x[5], reverse=True)[:6]:
        for r in sorted(right, key=lambda x: x[5], reverse=True)[:6]:
            x1, y1, x2, y2, _, _ = l
            x3, y3, x4, y4, _, _ = r
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(den) < 1e-6:
                continue
            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
            if -0.2 * w <= px <= 1.2 * w and -0.1 * h <= py <= 0.75 * h:
                center_dx = abs(px - (w / 2)) / (w / 2)
                vp_y = max(0.0, min(1.0, py / max(h * 0.6, 1)))
                score = max(0.0, 1.0 - center_dx) * (1.15 - vp_y)
                vanishing_scores.append(score)

    vp_score = max(vanishing_scores) if vanishing_scores else 0.0
    density_score = min(length_score / 2200.0, 1.0)
    return float(vp_score * 0.7 + density_score * 0.3)


def _load_extra_cascades():
    """Charge les cascades OpenCV disponibles (front + profil)."""
    cascades = []
    if cv2 is None:
        return cascades
    try:
        base = Path(cv2.data.haarcascades)
        for xml in ["haarcascade_frontalface_default.xml",
                    "haarcascade_frontalface_alt2.xml",
                    "haarcascade_profileface.xml"]:
            p = base / xml
            if p.exists():
                c = cv2.CascadeClassifier(str(p))
                if not c.empty():
                    cascades.append(c)
    except Exception:
        pass
    return cascades

_EXTRA_CASCADES = None  # chargé à la demande

def _detect_faces_multi(frame):
    """Détection multi-cascade : frontal + profil + miroir profil."""
    global _EXTRA_CASCADES
    if cv2 is None or frame is None or getattr(frame, "size", 0) == 0:
        return []
    if _EXTRA_CASCADES is None:
        _EXTRA_CASCADES = _load_extra_cascades()
    if not _EXTRA_CASCADES and OPENCV_FACE_CASCADE is None:
        return []

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray_flipped = cv2.flip(gray, 1)  # miroir pour profil droit→gauche

    all_faces = []
    cascades = _EXTRA_CASCADES if _EXTRA_CASCADES else [OPENCV_FACE_CASCADE]
    for cas in cascades:
        for g in [gray, gray_flipped]:
            try:
                faces = cas.detectMultiScale(
                    g, scaleFactor=1.08, minNeighbors=4,
                    minSize=(24, 24), flags=cv2.CASCADE_SCALE_IMAGE)
                if faces is not None and len(faces) > 0:
                    all_faces.extend([tuple(map(int, f)) for f in faces])
            except Exception:
                pass
    return all_faces


def _render_frame(ffmpeg, video_path, out_path, yaw, pitch, hfov, vfov, ts, w=640, h=360):
    """Extrait une frame rectilinéaire depuis une vidéo 360°."""
    vf = (f"v360=e:rectilinear:yaw={yaw}:pitch={pitch}:roll=0:"
          f"h_fov={hfov}:v_fov={vfov}:w={w}:h={h}:interp=linear")
    return run_ffmpeg(ffmpeg,
        ["-y", *media_input_args(video_path, ts),
         "-frames:v", "1", "-vf", vf, str(out_path)],
        timeout=40)


def auto_detect_reframe(ffmpeg, video_path, preset, work_dir, log_fn=None):
    """
    Détection auto en DEUX PASSES :
      Passe 1 — balayage grossier à 30° sur plusieurs timestamps (évite les 5s initiales)
      Passe 2 — raffinement à 5° autour des meilleurs candidats

    Habitacle : détection visage multi-cascade (front + profil + miroir)
    Route     : heuristique lignes/point de fuite (Canny + Hough)
    """
    if not HAS_AUTO_DETECT:
        return {"success": False, "reason": "opencv requis ou cascade visage OpenCV indisponible"}
    if not ffmpeg or (not os.path.isfile(ffmpeg) and ffmpeg != 'ffmpeg'):
        return {"success": False, "reason": "ffmpeg introuvable"}

    # Paramètres
    sample_count = max(1, int(preset.get("auto_sample_count", 2)))
    analysis_seconds = max(6, int(preset.get("auto_analysis_seconds", 12)))

    cabin_pitch = int(preset.get("cabin_pitch", -5))
    cabin_hfov  = int(preset.get("cabin_hfov", 120))
    cabin_vfov  = int(preset.get("cabin_vfov", 80))
    road_pitch  = int(preset.get("road_pitch", -10))
    road_hfov   = int(preset.get("road_hfov", 90))
    road_vfov   = int(preset.get("road_vfov", 60))

    # Timestamps : démarre à 5s minimum pour éviter garage/préparation
    t_start = max(5.0, float(preset.get("preview_timecode", 5.0)))
    t_end   = max(t_start + 1.0, float(analysis_seconds))
    timestamps = list(np.linspace(t_start, t_end, num=max(2, sample_count)))

    best_cabin = {"score": 0.0, "yaw": None, "faces": 0}
    best_road  = {"score": 0.0, "yaw": None}

    if log_fn:
        log_fn(f"Auto-cadrage passe 1/2 : balayage 30° sur {len(timestamps)} images…")

    # ── PASSE 1 : balayage grossier à 30° ──────────────────────
    coarse_yaws = list(range(-180, 181, 30))  # 13 yaws

    coarse_cabin_scores = {}  # yaw → score max
    coarse_road_scores  = {}

    for ts in timestamps:
        for yaw in coarse_yaws:
            tag = f"{int(ts*10)}_{yaw}"

            # Habitacle
            cabin_img = os.path.join(work_dir, f"c1_{tag}.jpg")
            r = _render_frame(ffmpeg, video_path, cabin_img, yaw, cabin_pitch, cabin_hfov, cabin_vfov, ts)
            if r.returncode == 0 and os.path.exists(cabin_img):
                frame = cv2.imread(cabin_img)
                if frame is not None:
                    faces = _detect_faces_multi(frame)
                    sc = _face_score(faces, frame.shape)
                    coarse_cabin_scores[yaw] = max(coarse_cabin_scores.get(yaw, 0.0), sc)
                    if sc > best_cabin["score"]:
                        best_cabin = {"score": sc, "yaw": yaw, "faces": len(faces)}

            # Route
            road_img = os.path.join(work_dir, f"r1_{tag}.jpg")
            r = _render_frame(ffmpeg, video_path, road_img, yaw, road_pitch, road_hfov, road_vfov, ts)
            if r.returncode == 0 and os.path.exists(road_img):
                frame = cv2.imread(road_img)
                sc = _road_score(frame)
                coarse_road_scores[yaw] = max(coarse_road_scores.get(yaw, 0.0), sc)
                if sc > best_road["score"]:
                    best_road = {"score": sc, "yaw": yaw}

    # ── PASSE 2 : raffinement à 5° autour des tops candidats ───
    def top_candidates(scores_dict, n=3):
        """Retourne les n meilleurs yaws triés par score décroissant."""
        return [y for y, _ in sorted(scores_dict.items(), key=lambda x: -x[1])][:n]

    cabin_tops = top_candidates(coarse_cabin_scores, n=3)
    road_tops  = top_candidates(coarse_road_scores, n=3)

    # Yaws fins : ±25° autour de chaque top candidat, pas de 5°
    def fine_yaws(tops):
        seen = set()
        result = []
        for cy in tops:
            for delta in range(-25, 26, 5):
                y = norm_yaw(cy + delta)
                if y not in seen:
                    seen.add(y); result.append(y)
        return result

    if log_fn:
        log_fn(f"Auto-cadrage passe 2/2 : raffinement 5° (cabin tops={cabin_tops}, road tops={road_tops})…")

    ts_ref = timestamps[len(timestamps)//2]  # timestamp du milieu pour la passe 2

    for yaw in fine_yaws(cabin_tops):
        cabin_img = os.path.join(work_dir, f"c2_{yaw}.jpg")
        r = _render_frame(ffmpeg, video_path, cabin_img, yaw, cabin_pitch, cabin_hfov, cabin_vfov, ts_ref)
        if r.returncode == 0 and os.path.exists(cabin_img):
            frame = cv2.imread(cabin_img)
            if frame is not None:
                faces = _detect_faces_multi(frame)
                sc = _face_score(faces, frame.shape)
                if sc > best_cabin["score"]:
                    best_cabin = {"score": sc, "yaw": yaw, "faces": len(faces)}

    for yaw in fine_yaws(road_tops):
        road_img = os.path.join(work_dir, f"r2_{yaw}.jpg")
        r = _render_frame(ffmpeg, video_path, road_img, yaw, road_pitch, road_hfov, road_vfov, ts_ref)
        if r.returncode == 0 and os.path.exists(road_img):
            frame = cv2.imread(road_img)
            sc = _road_score(frame)
            if sc > best_road["score"]:
                best_road = {"score": sc, "yaw": yaw}

    # ── Résultats ───────────────────────────────────────────────
    updates = {"success": False}
    reasons = []

    if best_cabin["yaw"] is not None and best_cabin["score"] > 0:
        updates["cabin_yaw"]   = norm_yaw(best_cabin["yaw"])
        updates["faces"]       = best_cabin["faces"]
        updates["cabin_score"] = round(best_cabin["score"], 4)
    else:
        reasons.append("aucun visage détecté")

    if best_road["yaw"] is not None and best_road["score"] > 0:
        updates["road_yaw"]   = norm_yaw(best_road["yaw"])
        updates["road_score"] = round(best_road["score"], 4)
    else:
        reasons.append("route non détectée")

    if "cabin_yaw" in updates or "road_yaw" in updates:
        updates["success"] = True
        if log_fn:
            cm = (f"habitacle yaw={updates['cabin_yaw']}° visages={updates.get('faces',0)} "
                  f"score={updates.get('cabin_score',0):.4f}") if "cabin_yaw" in updates else "habitacle: échec"
            rm = (f"route yaw={updates['road_yaw']}° "
                  f"score={updates.get('road_score',0):.4f}") if "road_yaw" in updates else "route: échec"
            log_fn(f"Auto-cadrage résultat : {cm} | {rm}")
        return updates

    updates["reason"] = " / ".join(reasons) if reasons else "analyse impossible"
    return updates


# ══════════════════════════════════════════════════════════════
#  WORKER FFMPEG
# ══════════════════════════════════════════════════════════════
class SessionWorker(QThread):
    sig_progress = pyqtSignal(int, int)
    sig_status   = pyqtSignal(int, str)
    sig_stage    = pyqtSignal(int, str)
    sig_log      = pyqtSignal(str)
    sig_error    = pyqtSignal(int, str)
    sig_done_one = pyqtSignal(int, float)
    sig_preview_request = pyqtSignal(int, dict)
    sig_eta = pyqtSignal(int, str)

    def __init__(self, sid, filename, filepath, passengers, reframe_preset_name, reframe_preset_payload, db, preset, ffmpeg):
        super().__init__()
        self.sid=sid; self.filename=filename; self.filepath=filepath
        self.passengers=passengers; self.db=db; self.preset=preset
        self.reframe_preset_name = reframe_preset_name or ""
        self.reframe_preset_payload = reframe_preset_payload or {}
        self.ffmpeg=ffmpeg; self._proc=None; self._t0=None
        self._sdk_info = None
        self._preview_event = threading.Event()
        self._preview_reply = None

    def set_preview_reply(self, payload):
        self._preview_reply = payload
        self._preview_event.set()

    def _apply_preview_reply(self, params, reply):
        if not isinstance(reply, dict):
            return False
        if reply.get("mode") == "skip_auto":
            self.sig_log.emit(f"[{self._ts()}]   ⚠ Recadrage automatique ignoré par validation manuelle")
            return True
        for key in ["road_yaw", "road_pitch", "cabin_yaw", "cabin_pitch", "pip_width", "pip_height", "pip_position"]:
            if key in reply:
                params[key] = reply[key]
        self.sig_log.emit(f"[{self._ts()}]   ✓ Cadrage validé")
        return True

    def _open_preview_dialog(self, sid, source_path, params, work_dir):
        os.makedirs(work_dir, exist_ok=True)
        preview_payload = dict(params)
        preview_payload["preview_timecode"] = float(params.get("preview_timecode", 1.5))
        preview_path = build_preview_image(self.ffmpeg, source_path, preview_payload, work_dir, preview_name=f"preview_{self.sid}.jpg")
        preview_payload["preview_path"] = preview_path
        preview_payload["video_path"] = str(source_path)
        preview_payload["work_dir"] = work_dir
        self._preview_event.clear()
        self._preview_reply = None
        self.sig_preview_request.emit(sid, preview_payload)
        self._preview_event.wait(timeout=int(params.get("preview_timeout_sec", 180)))
        return self._preview_reply

    def _set_stage(self, sid, stage_label):
        self.sig_stage.emit(sid, str(stage_label or ""))

    def _get_sdk_info(self):
        if self._sdk_info is None:
            sdk_path = self.preset.get("media_sdk_resolved_path", "").strip() or self.preset.get("media_sdk_path", "").strip()
            self._sdk_info = sdk_diagnostic(sdk_path)
        if not self._sdk_info.get("ok"):
            raise RuntimeError("Export INSV impossible : SDK non validé.")
        return self._sdk_info

    def _build_insv_preview_source(self, src, sid):
        sdk_info = self._get_sdk_info()
        preview_dir = session_preview_cache_dir(sid, self.filename)
        preview_meta_path = session_preview_cache_meta_path(sid, self.filename)
        try:
            with open(preview_meta_path, "r", encoding="utf-8") as f:
                preview_meta = json.load(f)
        except Exception:
            preview_meta = {}
        cache_ok, cache_reason, expected_preview_meta, image_path = validate_preview_cache(preview_dir, preview_meta, str(src), preset=self.preset)
        if cache_ok and image_path:
            self._set_stage(sid, "Aperçu 360")
            self.sig_log.emit(f"[{self._ts()}] ✓ {self.filename} — Aperçu 360 réutilisé")
            return image_path

        inputs = discover_insv_inputs(str(src))
        prepared_inputs = prepare_insv_inputs_for_sdk(
            inputs,
            log_fn=lambda m: self.sig_log.emit(f"[{self._ts()}]   {m}"),
        )
        inputs = prepared_inputs["inputs"]
        safe_rmtree(preview_dir)
        Path(preview_dir).mkdir(parents=True, exist_ok=True)
        self.sig_log.emit(f"[{self._ts()}] ▶ {self.filename} — Aperçu rapide première frame…")
        if cache_reason not in {"aperçu absent", "métadonnées aperçu absentes"}:
            self.sig_log.emit(f"[{self._ts()}]   Cache aperçu invalidé : {cache_reason}")
        self._set_stage(sid, "Aperçu 360")
        result = run_sdk_preview_frame(
            sdk_info["resolved_path"],
            inputs,
            preview_dir,
            timeout=90,
            preset=self.preset,
            log_fn=lambda m: self.sig_log.emit(f"[{self._ts()}]   {m}"),
        )
        if result.get("ok") and result.get("image_path"):
            try:
                with open(preview_meta_path, "w", encoding="utf-8") as f:
                    json.dump(expected_preview_meta, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
            self.sig_log.emit(f"[{self._ts()}]   ✓ Aperçu INSV prêt")
            return str(result["image_path"])
        detail = (result.get("stderr") or result.get("stdout") or "").strip()
        self.sig_log.emit(f"[{self._ts()}]   ⚠ Aperçu INSV rapide indisponible — {detail[-200:] or 'fallback sur le flux standard'}")
        return ""

    def _resolve_reframe_params(self, preview_source, sid):
        p = dict(self.preset)
        session_reframe = extract_reframe_preset_payload(self.reframe_preset_payload)
        if session_reframe:
            p.update(session_reframe)
            self.sig_log.emit(f"[{self._ts()}]   ✓ Preset recadrage appliqué : {self.reframe_preset_name}")
            return p

        work_dir = None
        allow_auto_reframe = p.get("auto_reframe") and not is_still_image_source(preview_source)
        if allow_auto_reframe:
            self._set_stage(sid, "Recadrage")
            try:
                import tempfile as _tf
                work_dir = _tf.mkdtemp(prefix="msa_autoframe_")
                os.makedirs(work_dir, exist_ok=True)
                result = auto_detect_reframe(self.ffmpeg, preview_source, p, work_dir,
                                             lambda m: self.sig_log.emit(f"[{self._ts()}]   {m}"))
                if result.get("success"):
                    if "cabin_yaw" in result:
                        p["cabin_yaw"] = result["cabin_yaw"]
                    if "road_yaw" in result:
                        p["road_yaw"] = result["road_yaw"]
                    self.sig_log.emit(f"[{self._ts()}]   ✓ Auto-cadrage appliqué")
                else:
                    self.sig_log.emit(f"[{self._ts()}]   ⚠ Auto-cadrage ignoré — {result.get('reason','erreur')}" )
            except Exception as e:
                self.sig_log.emit(f"[{self._ts()}]   ⚠ Auto-cadrage en échec — {e}")

        if p.get("preview_before_render", True):
            self._set_stage(sid, "Recadrage")
            try:
                if not work_dir:
                    import tempfile as _tf
                    work_dir = _tf.mkdtemp(prefix="msa_manualframe_")
                reply = self._open_preview_dialog(sid, preview_source, p, work_dir)
                if not self._apply_preview_reply(p, reply):
                    self.sig_log.emit(f"[{self._ts()}]   ⚠ Validation cadrage ignorée (timeout)")
            except Exception as e:
                self.sig_log.emit(f"[{self._ts()}]   ⚠ Ouverture du recadrage manuel en échec — {e}")
        return p

    def run(self):
        import tempfile
        sid=self.sid; src=Path(self.filepath)
        label=self.filename
        session_output_mode = resolve_session_output_mode(self.reframe_preset_name, self.reframe_preset_payload)
        self._t0=time.time()
        # Utilise un dossier temp système pour éviter les erreurs sur volumes read-only (ex: clé Insta360)
        tmp = Path(tempfile.mkdtemp(prefix=f"msa_pipeline_{sid}_"))
        try:
            tmp.mkdir(exist_ok=True)
            self.sig_status.emit(sid, Status.PROCESSING)
            self.db.update_session(sid, status=Status.PROCESSING)

            ext = src.suffix.lower()
            resolved_params = None
            if ext == '.insv':
                preview_allowed = (
                    session_output_mode != SESSION_OUTPUT_MODE_360
                    and
                    not extract_reframe_preset_payload(self.reframe_preset_payload)
                    and self.preset.get("preview_before_render", True)
                    and not self.preset.get("auto_reframe")
                )
                if preview_allowed:
                    preview_source = self._build_insv_preview_source(src, sid)
                    if preview_source:
                        resolved_params = self._resolve_reframe_params(preview_source, sid)
                equirect = Path(self._stitch(src, sid))
            else:
                self.sig_log.emit(f"[{self._ts()}] ✓ {self.filename} — MP4 prêt")
                self._set_stage(sid, "Export final")
                equirect=src; self.sig_progress.emit(sid,15)

            composite=tmp/"composite.mp4"
            if session_output_mode == SESSION_OUTPUT_MODE_360:
                self.sig_log.emit(f"[{self._ts()}] ▶ Export direct 360 MP4…")
                self._export_direct_360(str(equirect), str(composite), sid)
            else:
                self.sig_log.emit(f"[{self._ts()}] ▶ Reframing + PiP…")
                self._pipeline(str(equirect), str(composite), sid, resolved_params=resolved_params)

            if session_output_mode != SESSION_OUTPUT_MODE_360 and self.preset.get("add_watermark") and self.preset.get("watermark_path"):
                wm_out=tmp/"wm.mp4"
                self._watermark(str(composite), str(wm_out))
                if wm_out.exists(): composite=wm_out

            out_dir=self._outdir(); os.makedirs(out_dir, exist_ok=True)
            thumbnail_source = None
            if self.preset.get("gen_thumbnail"):
                thumb_path = tmp/"thumb.jpg"
                self._thumb(str(composite), str(thumb_path))
                if thumb_path.exists() and thumb_path.stat().st_size > 0:
                    thumbnail_source = thumb_path
            out_paths=[]
            for name in [self.filename]:
                fname=self._fname(name); dst=os.path.join(out_dir,fname)
                shutil.copyfile(str(composite), dst); out_paths.append(dst)
                self.sig_log.emit(f"[{self._ts()}]   → {fname}")
                if thumbnail_source:
                    shutil.copyfile(str(thumbnail_source), dst.replace(".mp4","_thumb.jpg"))

            shutil.rmtree(tmp, ignore_errors=True)
            elapsed=time.time()-self._t0
            self.sig_progress.emit(sid,100)
            self.db.update_session(sid,status=Status.DONE,progress=100,output_paths=json.dumps(out_paths))
            self._set_stage(sid, "")
            self.sig_status.emit(sid,Status.DONE)
            self.sig_done_one.emit(sid, elapsed)
            self.sig_log.emit(f"[{self._ts()}] ✅ {label} ({elapsed:.0f}s) → {out_dir}")
            if self.preset.get("auto_open_output"): self._open(out_dir)

        except Exception as e:
            shutil.rmtree(tmp, ignore_errors=True)
            err=str(e); self.db.update_session(sid,status=Status.ERROR,error_msg=err)
            self._set_stage(sid, "")
            self.sig_status.emit(sid,Status.ERROR); self.sig_error.emit(sid,err)
            self.sig_log.emit(f"[{self._ts()}] ❌ {label} — {err}")

    def _stitch(self, src, sid):
        sdk_info = self._get_sdk_info()

        cache_path, cache_meta_json = self.db.get_session_cache(sid)
        cache_path = (cache_path or "").strip() or session_stitch_cache_path(sid, self.filename)
        try:
            cache_meta = json.loads(cache_meta_json or "{}")
        except Exception:
            cache_meta = {}
        cache_ok, cache_reason, expected_cache_meta = validate_stitch_cache(cache_path, cache_meta, str(src), preset=self.preset)
        if cache_ok:
            self._set_stage(sid, "Cache 360")
            self.sig_log.emit(f"[{self._ts()}] ✓ {self.filename} — Stitch 360 réutilisé depuis le cache")
            self.sig_log.emit(f"[{self._ts()}]   Cache : {Path(cache_path).name}")
            self.sig_progress.emit(sid,25)
            return cache_path

        shared_cache = self.db.find_matching_stitch_cache(str(src), preset=self.preset, exclude_sid=sid)
        if shared_cache:
            cache_path = shared_cache["cache_path"]
            expected_cache_meta = shared_cache["expected_meta"]
            self.db.update_session_cache(sid, cache_path, shared_cache["cache_meta_json"])
            self._set_stage(sid, "Cache 360")
            self.sig_log.emit(f"[{self._ts()}] ✓ {self.filename} — Stitch 360 réutilisé depuis une autre session")
            self.sig_log.emit(f"[{self._ts()}]   Cache : {Path(cache_path).name} · session #{shared_cache['sid']}")
            self.sig_progress.emit(sid,25)
            return cache_path

        self.sig_log.emit(f"[{self._ts()}] ▶ {self.filename} — Stitching 360…")
        if cache_reason != "cache absent":
            self.sig_log.emit(f"[{self._ts()}]   Cache invalidé : {cache_reason}")
        self._set_stage(sid, "SDK 360")
        inputs = discover_insv_inputs(str(src))
        prepared_inputs = prepare_insv_inputs_for_sdk(
            inputs,
            log_fn=lambda m: self.sig_log.emit(f"[{self._ts()}]   {m}"),
        )
        inputs = prepared_inputs["inputs"]
        self.sig_log.emit(f"[{self._ts()}]   SDK : {Path(sdk_info['resolved_path']).name}")
        self.sig_log.emit(f"[{self._ts()}]   Entrées : {', '.join(Path(p).name for p in inputs)}")
        insv_mode = resolve_insv_processing_mode(self.preset)
        self.sig_log.emit(f"[{self._ts()}]   Mode INSV : {insv_mode}")
        stitch_width, stitch_height = compute_sdk_output_size(self.preset)
        stitch_bitrate = resolve_sdk_output_bitrate(self.preset)
        self.sig_log.emit(f"[{self._ts()}]   Sortie équirectangulaire : {stitch_width}x{stitch_height}")
        if stitch_bitrate > 0:
            self.sig_log.emit(f"[{self._ts()}]   Bitrate intermédiaire : {format_bitrate_bps(stitch_bitrate)}")
        stitch_output_path = cache_path
        if self.db.cache_path_referenced_elsewhere(cache_path, exclude_sid=sid):
            stitch_output_path = session_stitch_cache_path(sid, self.filename)
            self.sig_log.emit(f"[{self._ts()}]   Cache partagé détecté — nouveau stitch isolé pour cette session")
        Path(stitch_output_path).parent.mkdir(parents=True, exist_ok=True)
        safe_unlink(stitch_output_path)
        r = run_sdk_stitch(
            sdk_info["resolved_path"],
            inputs,
            stitch_output_path,
            timeout=900,
            preset=self.preset,
            log_fn=lambda m: self.sig_log.emit(f"[{self._ts()}]   {m}"),
            progress_fn=lambda pct: self.sig_progress.emit(sid, 5 + int(max(0, min(100, pct)) * 0.20)),
        )
        cache_file = Path(stitch_output_path)
        if not r.get("ok") or not cache_file.exists() or cache_file.stat().st_size == 0:
            detail = (r.get("stderr") or r.get("stdout") or "").strip()
            safe_unlink(stitch_output_path)
            raise RuntimeError(f"Media SDK : {detail[-300:] or 'stitching échoué'}")
        self.db.update_session_cache(sid, stitch_output_path, json.dumps(expected_cache_meta, ensure_ascii=False))
        self.sig_log.emit(f"[{self._ts()}]   ✓ Stitch 360 mis en cache")
        self.sig_progress.emit(sid,25)
        return stitch_output_path

    def _export_direct_360(self, source, output, sid):
        self._set_stage(sid, "360 MP4")
        src_path = Path(source)
        fps_args = output_fps_args(self.preset)
        if src_path.suffix.lower() == ".mp4" and not fps_args:
            shutil.copyfile(str(src_path), output)
            self.sig_progress.emit(sid, 90)
            return

        p = dict(self.preset)
        venc = best_video_encoder_args(p)
        cmd = [
            self.ffmpeg, *ffmpeg_common_args(), "-progress", "pipe:2", "-y",
            "-i", source,
            "-map", "0:v:0", "-map", "0:a?",
            *venc,
            "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart",
            *fps_args,
            output,
        ]
        dur = get_duration(self.ffmpeg, source)
        proc = popen_process(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self._proc = proc
        out_sec = 0.0
        for line in proc.stderr:
            if line.startswith("out_time_ms="):
                try:
                    out_sec = int(line.split("=", 1)[1].strip()) / 1000000.0
                except Exception:
                    out_sec = 0.0
                if dur:
                    pct = int(25 + min(out_sec / dur, 1.0) * 65)
                    self.sig_progress.emit(sid, pct)
        proc.wait()
        if proc.returncode != 0 or not os.path.exists(output) or os.path.getsize(output) == 0:
            detail = (proc.stderr.read() if proc.stderr else "") or ""
            raise RuntimeError(f"Export 360 MP4 : {detail[-300:] or 'échec FFmpeg'}")
        self.sig_progress.emit(sid, 90)

    def _pipeline(self, equirect, output, sid, resolved_params=None):
        p = dict(resolved_params) if resolved_params else self._resolve_reframe_params(equirect, sid)
        self._set_stage(sid, "Export final")
        ow,oh=p['output_width'],p['output_height']
        pw,ph=p['pip_width'],p['pip_height']
        pos=pip_pos(p.get("pip_position","top_right"),p['pip_margin'])
        interp = p.get("v360_interp", "line")
        fps_args = output_fps_args(p)
        fc=(f"[0:v]v360=e:rectilinear:yaw={p['road_yaw']}:pitch={p['road_pitch']}"
            f":roll=0:h_fov={p['road_hfov']}:v_fov={p['road_vfov']}:w={ow}:h={oh}:interp={interp}[road];"
            f"[0:v]v360=e:rectilinear:yaw={p['cabin_yaw']}:pitch={p['cabin_pitch']}"
            f":roll=0:h_fov={p['cabin_hfov']}:v_fov={p['cabin_vfov']}:w={pw}:h={ph}:interp={interp}[cabin];"
            f"[road][cabin]overlay={pos}[out]")
        venc = best_video_encoder_args(p)
        cmd=[self.ffmpeg, *ffmpeg_common_args(), "-progress","pipe:2","-y","-i",equirect,"-filter_complex",fc,
             "-map","[out]","-map","0:a?", *venc,
             "-c:a","aac","-b:a","96k","-movflags","+faststart", *fps_args, output]
        dur=get_duration(self.ffmpeg, equirect)
        proc=popen_process(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self._proc=proc
        out_sec = 0.0
        last_eta_emit = 0.0
        for line in proc.stderr:
            if line.startswith("out_time_ms="):
                try:
                    out_sec = int(line.split("=",1)[1].strip()) / 1000000.0
                except Exception:
                    out_sec = 0.0
                if dur:
                    pct=int(25+min(out_sec/dur,1.0)*65)
                    self.sig_progress.emit(sid,pct)
                    elapsed = max(0.001, time.time() - self._t0)
                    if out_sec > 0.5 and time.time() - last_eta_emit > 0.8:
                        remaining = max(0.0, elapsed * (dur - out_sec) / out_sec)
                        self.sig_eta.emit(sid, f"{int(remaining//60):02d}:{int(remaining%60):02d}")
                        last_eta_emit = time.time()
        proc.wait(); self._proc=None
        self.sig_eta.emit(sid, "")
        if proc.returncode!=0: raise RuntimeError(f"FFmpeg échoué (code {proc.returncode})")

    def _watermark(self, src, output):
        wm=self.preset.get("watermark_path",""); opa=self.preset.get("watermark_opacity",80)/100.0
        if not os.path.isfile(wm): return
        venc = best_video_encoder_args(self.preset)
        cmd=[self.ffmpeg, *ffmpeg_common_args(), "-y","-i",src,"-i",wm,
             "-filter_complex",f"[1:v]scale=iw*0.15:-1,format=rgba,colorchannelmixer=aa={opa}[logo];[0:v][logo]overlay=W-w-30:H-h-30[out]",
             "-map","[out]","-map","0:a?", *venc, "-c:a","copy","-movflags","+faststart",output]
        run_process(cmd,capture_output=True,timeout=600)

    def _thumb(self, src, output):
        run_ffmpeg(self.ffmpeg,["-y","-ss","00:00:05","-i",src,"-vframes","1","-q:v","3",output],timeout=20)

    def _fname(self, name):
        prefix=self.preset.get("output_prefix","").strip()
        safe=re.sub(r'[^\w\-]','_',name)
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        return "_".join(p for p in [prefix,safe,ts] if p)+".mp4"

    def _outdir(self):
        base=self.preset.get("output_dir","").strip()
        if not base: base=os.path.join(os.path.dirname(self.filepath),"output")
        if self.preset.get("output_date_folder"):
            base=os.path.join(base,datetime.now().strftime("%Y-%m-%d"))
        return base

    def _open(self, path):
        try:
            if sys.platform=="win32": os.startfile(path)
            elif sys.platform=="darwin": subprocess.Popen(["open",path])
            else: subprocess.Popen(["xdg-open",path])
        except: pass

    def _ts(self): return datetime.now().strftime("%H:%M:%S")

# ══════════════════════════════════════════════════════════════
#  BATCH MANAGER
# ══════════════════════════════════════════════════════════════
class BatchManager:
    def __init__(self, db, preset, ffmpeg):
        self.db=db; self.preset=preset; self.ffmpeg=ffmpeg
        self.workers={}; self.running=False; self.paused=False; self.pause_after_current=False; self._q=[]; self._cb={}; self.on_done=None

    def start(self, sessions, cb):
        self.running=True; self.paused=False; self.pause_after_current=False; self._q=list(sessions); self._cb=cb; self._next()

    def _next(self):
        if self.pause_after_current:
            self.running=False
            self.paused=True
            self.pause_after_current=False
            return
        if not self._q or not self.running:
            done = not self._q
            self.running=False
            self.paused=False if done else self.paused
            if done and self.on_done: self.on_done()
            return
        sid,fname,fpath,pj,reframe_name,reframe_payload_json=self._q.pop(0)
        try: pax=json.loads(pj or "[]")
        except: pax=[]
        try: reframe_payload = json.loads(reframe_payload_json or "{}")
        except Exception: reframe_payload = {}
        w=SessionWorker(sid,fname,fpath,pax,reframe_name,reframe_payload,self.db,self.preset,self.ffmpeg)
        w.sig_progress.connect(self._cb['progress']); w.sig_status.connect(self._cb['status'])
        w.sig_stage.connect(self._cb.get('stage',lambda sid, txt: None))
        w.sig_log.connect(self._cb['log']); w.sig_error.connect(self._cb['error'])
        w.sig_done_one.connect(self._cb.get('done_one',lambda sid, elapsed: None))
        w.sig_eta.connect(self._cb.get('eta',lambda sid, txt: None))
        if self._cb.get('preview'):
            w.sig_preview_request.connect(lambda sid_, data, worker=w: self._cb['preview'](worker, sid_, data))
        w.finished.connect(self._next); self.workers[sid]=w; w.start()

    def queue_size(self):
        return len(self._q)

    def request_pause(self):
        if self.running:
            self.pause_after_current=True

    def resume(self):
        if self.paused and self._q:
            self.running=True
            self.paused=False
            self._next()

    def stop(self):
        self.running=False
        self.paused=False
        self.pause_after_current=False
        for w in self.workers.values():
            if w.isRunning():
                if w._proc: w._proc.terminate()
                w.terminate()


class SdkAutodetectWorker(QThread):
    sig_done = pyqtSignal(object)

    def run(self):
        try:
            result = autodetect_media_sdk()
        except Exception as exc:
            result = {
                "ok": False,
                "status": "Échec de détection automatique",
                "resolved_path": "",
                "logs": [f"Échec de détection automatique : {exc}"],
            }
        self.sig_done.emit(result)


class UpdateCheckWorker(QThread):
    sig_done = pyqtSignal(object)

    def __init__(self, current_version, manifest_url):
        super().__init__()
        self.current_version = str(current_version or "").strip()
        self.manifest_url = str(manifest_url or "").strip()

    def run(self):
        if not self.manifest_url:
            self.sig_done.emit({"ok": False, "skipped": True, "error": "URL du manifeste vide."})
            return
        try:
            response = http_json_request(self.manifest_url, timeout=UPDATE_CHECK_TIMEOUT_SEC)
            if not response.get("ok"):
                self.sig_done.emit(
                    {
                        "ok": False,
                        "skipped": False,
                        "error": response.get("error") or "Échec réseau pendant la vérification.",
                        "status": response.get("status", 0),
                    }
                )
                return
            payload = normalize_update_manifest_payload(response.get("data"))
            latest_version = payload["version"]
            if not latest_version:
                self.sig_done.emit(
                    {
                        "ok": False,
                        "skipped": False,
                        "error": "Le manifeste ne contient pas de champ 'version'.",
                    }
                )
                return
            self.sig_done.emit(
                {
                    "ok": True,
                    "manifest_url": self.manifest_url,
                    "current_version": self.current_version,
                    "latest_version": latest_version,
                    "download_url": payload["download_url"],
                    "notes": payload["notes"],
                    "title": payload["title"],
                    "has_update": is_newer_version(latest_version, self.current_version),
                }
            )
        except Exception as exc:
            self.sig_done.emit({"ok": False, "skipped": False, "error": str(exc)})


class PreviewWarmupWorker(QThread):
    sig_done = pyqtSignal(object)

    def __init__(self, sid, filename, filepath, preset):
        super().__init__()
        self.sid = sid
        self.filename = filename
        self.filepath = filepath
        self.preset = dict(preset or {})

    def run(self):
        result = {
            "ok": False,
            "sid": self.sid,
            "filename": self.filename,
            "logs": [],
            "image_path": "",
            "cache_hit": False,
        }
        try:
            source_path = Path(self.filepath)
            if source_path.suffix.lower() != ".insv" or not source_path.exists():
                self.sig_done.emit(result)
                return

            preview_dir = session_preview_cache_dir(self.sid, self.filename)
            preview_meta_path = session_preview_cache_meta_path(self.sid, self.filename)
            try:
                with open(preview_meta_path, "r", encoding="utf-8") as f:
                    preview_meta = json.load(f)
            except Exception:
                preview_meta = {}
            cache_ok, _cache_reason, expected_preview_meta, image_path = validate_preview_cache(preview_dir, preview_meta, str(source_path), preset=self.preset)
            if cache_ok and image_path:
                result["ok"] = True
                result["image_path"] = image_path
                result["cache_hit"] = True
                self.sig_done.emit(result)
                return

            sdk_path = self.preset.get("media_sdk_resolved_path", "").strip() or self.preset.get("media_sdk_path", "").strip()
            sdk_info = sdk_diagnostic(sdk_path)
            if not sdk_info.get("ok"):
                result["logs"].append("Aperçu INSV non préchauffé : SDK non validé.")
                self.sig_done.emit(result)
                return

            safe_rmtree(preview_dir)
            Path(preview_dir).mkdir(parents=True, exist_ok=True)
            sdk_result = run_sdk_preview_frame(
                sdk_info["resolved_path"],
                discover_insv_inputs(str(source_path)),
                preview_dir,
                timeout=90,
                preset=self.preset,
            )
            if sdk_result.get("ok") and sdk_result.get("image_path"):
                try:
                    with open(preview_meta_path, "w", encoding="utf-8") as f:
                        json.dump(expected_preview_meta, f, ensure_ascii=False, indent=2)
                except Exception:
                    pass
                result["ok"] = True
                result["image_path"] = sdk_result["image_path"]
                result["logs"].append("Aperçu INSV préchauffé.")
            else:
                detail = (sdk_result.get("stderr") or sdk_result.get("stdout") or "").strip()
                if detail:
                    result["logs"].append(f"Aperçu INSV non préchauffé : {detail[-200:]}")
        except Exception as exc:
            result["logs"].append(f"Aperçu INSV non préchauffé : {exc}")
        self.sig_done.emit(result)


class DeliveryWorker(QThread):
    sig_log = pyqtSignal(str)
    sig_status = pyqtSignal(int, str)
    sig_done = pyqtSignal(int, object)
    sig_error = pyqtSignal(int, str)

    def __init__(self, sid, session_name, output_paths, recipients, preset):
        super().__init__()
        self.sid = sid
        self.session_name = session_name
        self.output_paths = [str(p) for p in (output_paths or []) if str(p or "").strip()]
        self.recipients = normalize_delivery_recipients(recipients)
        self.preset = dict(preset or {})

    def run(self):
        try:
            if not self.output_paths:
                raise RuntimeError("Aucun MP4 exporté à livrer.")
            if not self.recipients:
                raise RuntimeError("Aucun destinataire renseigné pour cette session.")
            self.sig_status.emit(self.sid, "uploading")
            if self.preset.get("delivery_mock_mode", False):
                result = self._simulate_delivery()
            else:
                result = self._deliver_via_backend()
            self.sig_status.emit(self.sid, "sent")
            self.sig_done.emit(self.sid, result)
        except Exception as exc:
            self.sig_status.emit(self.sid, "error")
            self.sig_error.emit(self.sid, str(exc))

    def _simulate_delivery(self):
        assets = []
        self.sig_log.emit(f"[{self._ts()}] ☁ Livraison simulée — {self.session_name}")
        for output_path in self.output_paths:
            file_name = Path(output_path).name
            self.sig_log.emit(f"[{self._ts()}]   Hash {file_name}…")
            sha256 = compute_file_sha256(output_path)
            time.sleep(0.3)
            self.sig_log.emit(f"[{self._ts()}]   Upload simulé : {file_name}")
            time.sleep(0.4)
            fake_uid = sha256[:12]
            assets.append({
                "asset_id": f"mock_{fake_uid}",
                "file_name": file_name,
                "sha256": sha256,
                "watch_url": f"https://video.motorsport-academy.test/watch/{fake_uid}",
            })
        self.sig_status.emit(self.sid, "processing")
        time.sleep(0.4)
        sent_count = len(self.recipients)
        self.sig_log.emit(f"[{self._ts()}]   Envoi simulé à {sent_count} client(s)")
        return {
            "mode": "mock",
            "assets": assets,
            "sent_count": sent_count,
            "recipients": self.recipients,
        }

    def _deliver_via_backend(self):
        backend_url = str(self.preset.get("delivery_backend_url", "") or "").strip().rstrip("/")
        api_key = str(self.preset.get("delivery_api_key", "") or "").strip()
        if not backend_url:
            raise RuntimeError("Backend Stream non configuré.")
        if not api_key:
            raise RuntimeError("Clé API livraison absente.")

        assets = []
        for output_path in self.output_paths:
            file_name = Path(output_path).name
            file_size = int(Path(output_path).stat().st_size)
            self.sig_log.emit(f"[{self._ts()}] ☁ Préparation Stream : {file_name}")
            sha256 = compute_file_sha256(output_path)
            prepare = http_json_request(
                f"{backend_url}/api/v1/deliveries/prepare",
                method="POST",
                payload={
                    "session_id": int(self.sid),
                    "session_name": self.session_name,
                    "file_name": file_name,
                    "file_size": file_size,
                    "sha256": sha256,
                },
                headers=build_delivery_headers(api_key),
                timeout=120,
            )
            if not prepare["ok"]:
                detail = prepare.get("data", {}).get("error") or prepare.get("error") or "préparation impossible"
                raise RuntimeError(f"Préparation Stream échouée : {detail}")
            payload = prepare.get("data", {}) or {}
            asset_id = str(payload.get("asset_id") or "").strip()
            upload_url = str(payload.get("upload_url") or "").strip()
            upload_headers = payload.get("upload_headers") if isinstance(payload.get("upload_headers"), dict) else {}
            if not asset_id:
                raise RuntimeError("Réponse backend invalide : asset_id absent.")
            if not payload.get("existing"):
                if not upload_url:
                    raise RuntimeError("Réponse backend invalide : upload_url absente.")
                self.sig_log.emit(f"[{self._ts()}]   Upload Stream : {file_name}")
                upload = upload_file_http(
                    upload_url,
                    output_path,
                    method=payload.get("upload_method", "PUT"),
                    headers=upload_headers,
                    timeout=7200,
                )
                if not upload.get("ok"):
                    detail = (upload.get("stderr") or upload.get("stdout") or upload.get("error") or "").strip()
                    raise RuntimeError(f"Upload Stream échoué : {detail[-240:] or file_name}")
            else:
                self.sig_log.emit(f"[{self._ts()}]   Asset Stream déjà présent : {file_name}")

            self.sig_status.emit(self.sid, "processing")
            finalize = http_json_request(
                f"{backend_url}/api/v1/deliveries/finalize",
                method="POST",
                payload={"asset_id": asset_id},
                headers=build_delivery_headers(api_key),
                timeout=1800,
            )
            if not finalize["ok"]:
                detail = finalize.get("data", {}).get("error") or finalize.get("error") or "finalisation impossible"
                raise RuntimeError(f"Finalisation Stream échouée : {detail}")
            asset_payload = finalize.get("data", {}) or {}
            assets.append({
                "asset_id": asset_id,
                "file_name": file_name,
                "sha256": sha256,
                "watch_url": asset_payload.get("watch_url", ""),
                "stream_uid": asset_payload.get("stream_uid", ""),
            })

        delivery = http_json_request(
            f"{backend_url}/api/v1/deliveries/send",
            method="POST",
            payload={
                "session_id": int(self.sid),
                "session_name": self.session_name,
                "assets": assets,
                "recipients": self.recipients,
                "send_email": bool(self.preset.get("delivery_send_email", True)),
                "send_sms": bool(self.preset.get("delivery_send_sms", False)),
                "sender_name": str(self.preset.get("delivery_sender_name", "Motorsport Academy") or "Motorsport Academy"),
                "link_ttl_days": int(self.preset.get("delivery_link_ttl_days", 7) or 7),
            },
            headers=build_delivery_headers(api_key),
            timeout=300,
        )
        if not delivery["ok"]:
            detail = delivery.get("data", {}).get("error") or delivery.get("error") or "envoi impossible"
            raise RuntimeError(f"Envoi client échoué : {detail}")
        result = delivery.get("data", {}) or {}
        result["assets"] = assets
        result["mode"] = "backend"
        return result

    def _ts(self):
        return datetime.now().strftime("%H:%M:%S")

# ══════════════════════════════════════════════════════════════
#  WIDGETS CUSTOM — transparents, sans fond parasite
# ══════════════════════════════════════════════════════════════

class TransparentWidget(QWidget):
    """Widget de base 100% transparent pour usage dans les cellules de table."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background: transparent; border: none;")


class ElidedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = ""
        self.set_elided_text(text)

    def set_elided_text(self, text):
        self._full_text = str(text or "")
        self.setToolTip(self._full_text if self._full_text else "")
        self._apply_elision()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_elision()

    def _apply_elision(self):
        width = max(0, self.contentsRect().width())
        if width <= 0:
            super().setText(self._full_text)
            return
        display = self.fontMetrics().elidedText(self._full_text, Qt.ElideRight, width)
        super().setText(display)


class ToggleSwitch(QPushButton):
    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setObjectName("toggle_switch")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setText("")
        self.setFixedSize(ui_px(44), ui_px(24))
        self._glow = QGraphicsDropShadowEffect(self)
        self._glow.setOffset(0, 0)
        self._glow.setBlurRadius(14)
        self._glow.setColor(QColor(255, 122, 0, 0))
        self.setGraphicsEffect(self._glow)
        self.knob = QFrame(self)
        self.knob.setObjectName("toggle_knob")
        self.knob.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.toggled.connect(self._sync_knob)
        self.setChecked(bool(checked))
        self._sync_knob()

    def sizeHint(self):
        return QSize(ui_px(44), ui_px(24))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_knob()

    def _sync_knob(self):
        margin = 3
        knob_d = max(18, self.height() - (margin * 2))
        knob_y = (self.height() - knob_d) // 2
        knob_x = self.width() - knob_d - margin if self.isChecked() else margin
        self.knob.setGeometry(int(knob_x), int(knob_y), int(knob_d), int(knob_d))
        self.knob.raise_()
        if self.isChecked():
            self._glow.setBlurRadius(16)
            self._glow.setColor(QColor(255, 122, 0, 72))
        else:
            self._glow.setBlurRadius(10)
            self._glow.setColor(QColor(255, 122, 0, 0))


class InlineProgressWidget(TransparentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(ui_px(152))
        self.setFixedHeight(ui_px(16))

    def setValue(self, value):
        value = max(0, min(100, int(value or 0)))
        if value == self._value:
            return
        self._value = value
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(0, 0, -1, -1)
        if rect.width() <= 0 or rect.height() <= 0:
            p.end()
            return

        radius = rect.height() / 2.0
        track_path = QPainterPath()
        track_path.addRoundedRect(QRectF(rect), radius, radius)
        p.fillPath(track_path, QColor(C["progress_bg"]))
        p.setPen(QPen(QColor(C["chip_border"]), 1))
        p.drawPath(track_path)

        fill_width = int(rect.width() * (self._value / 100.0))
        if fill_width > 0:
            fill_rect = QRectF(rect.x(), rect.y(), fill_width, rect.height())
            fill_path = QPainterPath()
            fill_path.addRoundedRect(fill_rect, radius, radius)
            grad = QLinearGradient(rect.topLeft(), rect.topRight())
            grad.setColorAt(0, QColor(ACCENT))
            grad.setColorAt(1, QColor(C["progress_fill_end"]))
            p.fillPath(fill_path, grad)

        text_rect = rect.adjusted(ui_px(6), 0, -ui_px(6), 0)
        text = f"{self._value}%"
        font = QFont(UI_FONT)
        font.setPixelSize(ui_font(10))
        font.setWeight(QFont.DemiBold)
        p.setFont(font)

        outside_color = QColor(C["text_hi"])
        inside_color = QColor("#1A0F05")
        p.setPen(outside_color)
        p.drawText(text_rect, Qt.AlignCenter, text)

        if fill_width > 0:
            p.save()
            p.setClipRect(QRect(rect.x(), rect.y(), fill_width, rect.height()))
            p.setPen(inside_color)
            p.drawText(text_rect, Qt.AlignCenter, text)
            p.restore()

        p.end()


class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setView(create_combo_popup_view(self))
        self._arrow = QLabel(self)
        self._arrow.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._arrow.setFixedSize(12, 12)
        self._sync_arrow()

    def _sync_arrow(self):
        self._arrow.setPixmap(svg_pixmap("chevron_down", color=C["text_lo"], size=12))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        x = self.width() - 24
        y = (self.height() - self._arrow.height()) // 2
        self._arrow.move(max(0, x), max(0, y))


class InlineActionWidget(TransparentWidget):
    clicked = pyqtSignal()

    def __init__(self, icon_name, parent=None):
        super().__init__(parent)
        self._icon_name = icon_name
        self._hover = False
        self._filled = False
        self._text = ""
        self._base_color = C["text_hi"]
        self._hover_color = "#ffffff"
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(26)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(8)

        self.icon = QLabel()
        self.icon.setFixedSize(16, 16)
        self.icon.setStyleSheet("background:transparent; border:none;")
        self.label = QLabel()
        self.label.setStyleSheet("background:transparent; border:none;")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(self.icon, 0, Qt.AlignVCenter)
        layout.addWidget(self.label, 1)
        layout.addStretch()
        self._refresh()

    def set_content(self, text, base_color=None, filled=False, hover_color="#ffffff"):
        self._text = str(text or "")
        self._filled = bool(filled)
        self._base_color = base_color or C["text_hi"]
        self._hover_color = hover_color or "#ffffff"
        self._refresh()

    def _refresh(self):
        current_color = self._hover_color if self._hover else self._base_color
        self.icon.setPixmap(svg_pixmap(self._icon_name, color=current_color, size=16))
        self.label.setText(self._text)
        self.label.setStyleSheet(
            f"color:{current_color}; font-size:11px; font-weight:{700 if self._filled else 650};"
            "background:transparent; border:none; font-family:'Segoe UI',sans-serif;"
        )

    def enterEvent(self, event):
        self._hover = True
        self._refresh()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._refresh()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            event.accept()
            return
        super().mouseReleaseEvent(event)


class QueueTableWidget(QTableWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._reorder_enabled = False
        self.setDragEnabled(False)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(False)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def set_reorder_enabled(self, enabled: bool):
        self._reorder_enabled = False

    def _extract_local_files(self, mime_data):
        if not mime_data or not mime_data.hasUrls():
            return []
        paths = []
        for url in mime_data.urls():
            if not url.isLocalFile():
                continue
            path = url.toLocalFile()
            if not path or not os.path.isfile(path):
                continue
            if Path(path).suffix.lower() not in QUEUE_DROP_EXTENSIONS:
                continue
            paths.append(path)
        deduped = []
        seen = set()
        for path in paths:
            key = os.path.normcase(os.path.abspath(path))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(path)
        return deduped

    def dragEnterEvent(self, event):
        files = self._extract_local_files(event.mimeData())
        if files:
            event.acceptProposedAction()
            return
        event.ignore()

    def dragMoveEvent(self, event):
        files = self._extract_local_files(event.mimeData())
        if files:
            event.acceptProposedAction()
            return
        event.ignore()

    def dropEvent(self, event):
        files = self._extract_local_files(event.mimeData())
        if files:
            self.files_dropped.emit(files)
            event.acceptProposedAction()
            return
        event.ignore()


class StatusWidget(TransparentWidget):
    def __init__(self, status=Status.WAITING):
        super().__init__()
        self.setMinimumHeight(ui_px(44))
        root = QVBoxLayout(self)
        root.setContentsMargins(ui_px(8), ui_px(6), ui_px(8), ui_px(6))
        root.setSpacing(ui_px(4))

        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(ui_px(8))

        self.dot = QLabel()
        self.dot.setFixedSize(ui_px(16), ui_px(16))
        self.lbl = ElidedLabel()
        self.lbl.setMinimumWidth(0)
        self.lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.extra = ElidedLabel()
        self.extra.setMinimumWidth(0)
        self.extra.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bar = InlineProgressWidget()
        self.bar.hide()

        for w in [self.dot, self.lbl, self.extra, self.bar]:
            w.setStyleSheet("background:transparent; border:none;")

        top.addWidget(self.dot, 0, Qt.AlignVCenter)
        top.addWidget(self.lbl, 1)
        root.addLayout(top)
        root.addWidget(self.extra)
        root.addWidget(self.bar)
        self._state = None
        self.set_status(status)

    def set_status(self, s, pct=0, extra_text=""):
        state = (s, int(pct or 0), str(extra_text or ""))
        if state == self._state:
            return
        self._state = state
        txt, col_key, icon = STATUS_CFG.get(s, ("—", "text_lo", "·"))
        col = C.get(col_key, C["text_lo"])
        self.dot.setPixmap(svg_pixmap(icon, color=col, size=ui_px(16)))
        self.lbl.setStyleSheet(
            f"color:{col}; font-size:{ui_font(12)}px; font-weight:700; background:transparent; border:none;"
        )
        self.lbl.set_elided_text(txt)
        self.extra.setStyleSheet(
            f"color:{C['text_mid']}; font-size:{ui_font(11)}px; background:transparent; border:none;"
        )
        self.extra.setVisible(bool(extra_text))
        self.extra.set_elided_text(extra_text if extra_text else "")
        if s == Status.PROCESSING:
            pct = max(0, min(100, int(pct or 0)))
            self.bar.show()
            self.bar.setValue(pct)
        else:
            self.bar.hide()


class ReframePresetBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("btn_pax")
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        apply_button_icon(self, "compass", color=C["text_hi"], size=ui_px(16))
        self.setIconSize(QSize(ui_px(16), ui_px(16)))

    def set_preset(self, preset_name):
        label = describe_reframe_preset(preset_name)
        if preset_name:
            self.setText(label)
            self.setProperty("filled", "true")
        else:
            self.setText("Popup auto")
            self.setProperty("filled", "false")
        self.style().unpolish(self)
        self.style().polish(self)


class DeliveryRecipientsBtn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("btn_pax")
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        apply_button_icon(self, "mail", color=C["text_hi"], size=ui_px(16))
        self.setIconSize(QSize(ui_px(16), ui_px(16)))

    def set_delivery(self, recipients, status=""):
        recipients = normalize_delivery_recipients(recipients)
        status_txt = delivery_status_label(status)
        if recipients:
            base = summarize_delivery_recipients(recipients)
            self.setProperty("filled", "true")
            tooltip = []
            for recipient in recipients:
                bits = [recipient.get("name", "").strip() or "Client"]
                if recipient.get("email"):
                    bits.append(recipient["email"])
                if recipient.get("phone"):
                    bits.append(recipient["phone"])
                tooltip.append(" · ".join(bits))
            if status_txt:
                tooltip.insert(0, f"Statut livraison : {status_txt}")
            self.setToolTip("\n".join(tooltip))
        else:
            base = "Ajouter clients…"
            self.setProperty("filled", "false")
            self.setToolTip("Associer un ou plusieurs clients à cette vidéo.")
        if status_txt and recipients:
            base += f" · {status_txt}"
        self.setText(base)
        self.style().unpolish(self)
        self.style().polish(self)


class RowSeparator(QWidget):
    """Ligne séparatrice subtile entre les rows."""
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(255,255,255,8), 1))
        p.drawLine(0, self.height()-1, self.width(), self.height()-1)
        p.end()


# ══════════════════════════════════════════════════════════════
#  DIALOG LOGS
# ══════════════════════════════════════════════════════════════
class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Journal — {APP_NAME}")
        self.setWindowIcon(app_icon())
        self.resize(780, 460)
        self.setStyleSheet(STYLESHEET)

        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(12)

        hdr = QHBoxLayout()
        title = QLabel("Journal d'activité")
        title.setStyleSheet(f"color:{C['text_hi']}; font-size:14px; font-weight:700; font-family:'{UI_FONT}',sans-serif;")
        btn_clear = QPushButton("Effacer")
        btn_clear.setObjectName("btn_ghost")
        btn_clear.setFixedSize(80, 32)
        btn_clear.clicked.connect(lambda: self.log_box.clear())
        hdr.addWidget(title); hdr.addStretch(); hdr.addWidget(btn_clear)
        l.addLayout(hdr)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("log_view")
        self.log_box.setReadOnly(True)
        self.log_box.setLineWrapMode(QTextEdit.NoWrap)
        l.addWidget(self.log_box)

        btn_close = QPushButton("Fermer")
        btn_close.setObjectName("btn_ghost")
        btn_close.setFixedHeight(36)
        btn_close.clicked.connect(self.hide)
        l.addWidget(btn_close, alignment=Qt.AlignRight)

    def append(self, msg):
        self.log_box.append(msg)
        sb = self.log_box.verticalScrollBar()
        sb.setValue(sb.maximum())


class AppMessageDialog(QDialog):
    def __init__(self, title, message, parent=None, icon_name="info", accent=False, confirm_text="OK", cancel_text=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(app_icon())
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        header = QHBoxLayout()
        header.setSpacing(14)

        badge = QFrame()
        badge.setFixedSize(48, 48)
        badge.setStyleSheet(
            f"background:{'rgba(255,122,0,18)' if accent else 'rgba(255,255,255,8)'};"
            f"border:1px solid {'rgba(255,122,0,36)' if accent else 'rgba(255,255,255,12)'};"
            "border-radius:24px;"
        )
        badge_layout = QVBoxLayout(badge)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.addWidget(icon_label(icon_name, color=ACCENT if accent else C["text_hi"], size=22), 0, Qt.AlignCenter)
        header.addWidget(badge, 0, Qt.AlignTop)

        text_col = QVBoxLayout()
        text_col.setSpacing(8)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color:{C['text_hi']}; font-size:18px; font-weight:800;")
        title_lbl.setWordWrap(True)
        body_lbl = QLabel(message)
        body_lbl.setStyleSheet(f"color:{C['text_mid']}; font-size:12px; font-weight:600;")
        body_lbl.setWordWrap(True)
        body_lbl.setTextFormat(Qt.PlainText)
        text_col.addWidget(title_lbl)
        text_col.addWidget(body_lbl)
        header.addLayout(text_col, 1)
        layout.addLayout(header)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()
        if cancel_text:
            btn_cancel = QPushButton(cancel_text)
            btn_cancel.setObjectName("btn_ghost")
            btn_cancel.setFixedHeight(40)
            btn_cancel.clicked.connect(self.reject)
            buttons.addWidget(btn_cancel)
        btn_ok = QPushButton(confirm_text)
        btn_ok.setObjectName("btn_launch_active" if accent else "btn_ghost")
        btn_ok.setFixedHeight(40)
        buttons.addWidget(btn_ok)
        if accent:
            apply_button_icon(btn_ok, "check", color="#140c04", size=16)
        btn_ok.clicked.connect(self.accept)
        layout.addLayout(buttons)


class TextEntryDialog(QDialog):
    def __init__(self, title, label_text, value="", placeholder="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(app_icon())
        self.setModal(True)
        self.setMinimumWidth(460)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color:{C['text_hi']}; font-size:18px; font-weight:800;")
        desc_lbl = QLabel(label_text)
        desc_lbl.setStyleSheet(f"color:{C['text_mid']}; font-size:12px; font-weight:600;")
        self.edit = QLineEdit(value)
        self.edit.setPlaceholderText(placeholder)
        self.edit.setMinimumHeight(44)
        layout.addWidget(title_lbl)
        layout.addWidget(desc_lbl)
        layout.addWidget(self.edit)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setObjectName("btn_ghost")
        btn_cancel.setFixedHeight(40)
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Enregistrer")
        btn_ok.setObjectName("btn_launch_active")
        btn_ok.setFixedHeight(40)
        apply_button_icon(btn_ok, "check", color="#140c04", size=16)
        btn_ok.clicked.connect(self.accept)
        buttons.addWidget(btn_cancel)
        buttons.addWidget(btn_ok)
        layout.addLayout(buttons)

    def text_value(self):
        return self.edit.text().strip()


def show_info_message(parent, title, message, icon_name="info", accent=False):
    dlg = AppMessageDialog(title, message, parent=parent, icon_name=icon_name, accent=accent, confirm_text="OK")
    return dlg.exec_()


def ask_confirmation(parent, title, message, confirm_text="Confirmer", cancel_text="Annuler", icon_name="alert", accent=True):
    dlg = AppMessageDialog(
        title,
        message,
        parent=parent,
        icon_name=icon_name,
        accent=accent,
        confirm_text=confirm_text,
        cancel_text=cancel_text,
    )
    return dlg.exec_() == QDialog.Accepted


class DeliveryRecipientsDialog(QDialog):
    def __init__(self, recipients, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Livraison client")
        self.setWindowIcon(app_icon())
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setStyleSheet(STYLESHEET)
        l = QVBoxLayout(self); l.setSpacing(14); l.setContentsMargins(24, 22, 24, 22)

        title = QLabel("Destinataires")
        title.setStyleSheet(f"color:{C['text_hi']}; font-size:18px; font-weight:800; font-family:'{UI_FONT}',sans-serif;")
        sub = QLabel("Renseigne jusqu'à 5 clients. Chaque ligne doit contenir au moins un email ou un numéro.")
        sub.setStyleSheet(f"color:{C['text_mid']}; font-size:11px; font-weight:600;")
        sub.setWordWrap(True)
        l.addWidget(title)
        l.addWidget(sub)

        self.inputs = []
        recipients = normalize_delivery_recipients(recipients)
        for idx in range(5):
            row = QGridLayout()
            row.setHorizontalSpacing(10)
            row.setVerticalSpacing(8)
            badge = QLabel(f"{idx+1}")
            badge.setFixedWidth(20)
            badge.setStyleSheet(f"color:{ACCENT if idx == 0 else C['text_lo']}; font-weight:700; font-size:13px;")
            name = QLineEdit()
            email = QLineEdit()
            phone = QLineEdit()
            name.setPlaceholderText("Nom client")
            email.setPlaceholderText("Email")
            phone.setPlaceholderText("Téléphone / WhatsApp")
            if idx < len(recipients):
                name.setText(recipients[idx].get("name", ""))
                email.setText(recipients[idx].get("email", ""))
                phone.setText(recipients[idx].get("phone", ""))
            row.addWidget(badge, 0, 0)
            row.addWidget(name, 0, 1)
            row.addWidget(email, 0, 2)
            row.addWidget(phone, 0, 3)
            row.setColumnStretch(1, 2)
            row.setColumnStretch(2, 3)
            row.setColumnStretch(3, 2)
            l.addLayout(row)
            self.inputs.append((name, email, phone))

        helper = QLabel("Astuce : la même vidéo peut être envoyée automatiquement à plusieurs clients.")
        helper.setStyleSheet(f"color:{C['text_lo']}; font-size:11px;")
        helper.setWordWrap(True)
        l.addWidget(helper)

        btns = QHBoxLayout(); btns.setSpacing(10)
        bc = QPushButton("Annuler"); bc.setObjectName("btn_ghost"); bc.setFixedHeight(38)
        bo = QPushButton("Confirmer"); bo.setObjectName("btn_launch_active"); bo.setFixedHeight(38)
        bc.clicked.connect(self.reject); bo.clicked.connect(self.accept)
        btns.addWidget(bc); btns.addStretch(); btns.addWidget(bo)
        l.addLayout(btns)

    def get_recipients(self):
        recipients = []
        for name, email, phone in self.inputs:
            row = {
                "name": name.text().strip(),
                "email": email.text().strip(),
                "phone": phone.text().strip(),
            }
            if row["name"] or row["email"] or row["phone"]:
                recipients.append(row)
        return normalize_delivery_recipients(recipients)


class PresetChoiceDialog(QDialog):
    def __init__(self, items, current_value="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preset de recadrage")
        self.setWindowIcon(app_icon())
        self.setFixedWidth(560)
        self.setStyleSheet(STYLESHEET)
        self._apply_all = False
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 22, 24, 22)

        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        title_row.addWidget(icon_label("compass", color=ACCENT, size=18))
        title = QLabel("Choisir un preset à appliquer")
        title.setStyleSheet(f"color:{C['text_hi']}; font-size:15px; font-weight:700; font-family:'{UI_FONT}',sans-serif;")
        title_row.addWidget(title)
        title_row.addStretch()
        layout.addLayout(title_row)

        subtitle = QLabel("Choisis un preset de recadrage, ou un export direct 360 sans recadrage ni PiP.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color:{C['text_mid']}; font-size:11px; font-family:'{UI_FONT}',sans-serif;")
        layout.addWidget(subtitle)

        self.combo = StyledComboBox()
        self.combo.setFixedHeight(46)
        self.combo.addItems(items)
        if current_value and current_value in items:
            self.combo.setCurrentText(current_value)
        layout.addWidget(self.combo)

        note = QLabel("`360 MP4` est un mode de sortie direct. Il ne s'agit pas d'un preset de cadrage.")
        note.setWordWrap(True)
        note.setStyleSheet(f"color:{ACCENT}; font-size:11px; font-weight:700; font-family:'{UI_FONT}',sans-serif;")
        layout.addWidget(note)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setObjectName("btn_ghost")
        btn_cancel.setFixedHeight(40)
        btn_all = QPushButton("Appliquer à toute la queue")
        btn_all.setObjectName("btn_ghost")
        btn_all.setFixedHeight(40)
        btn_ok = QPushButton("Confirmer")
        btn_ok.setObjectName("btn_launch_active")
        btn_ok.setFixedHeight(40)
        apply_button_icon(btn_ok, "check", color="#140c04", size=16)
        btn_cancel.clicked.connect(self.reject)
        btn_all.clicked.connect(self._accept_apply_all)
        btn_ok.clicked.connect(self.accept)
        buttons.addWidget(btn_cancel)
        buttons.addWidget(btn_all)
        buttons.addStretch()
        buttons.addWidget(btn_ok)
        layout.addLayout(buttons)

    def selected_value(self):
        return self.combo.currentText().strip()

    def _accept_apply_all(self):
        self._apply_all = True
        self.accept()

    def apply_to_all(self):
        return self._apply_all




# ══════════════════════════════════════════════════════════════
#  DIALOG PRÉVIEW CADRAGE — vue duale route + habitacle
# ══════════════════════════════════════════════════════════════
class ReframePreviewDialog(QDialog):
    def __init__(self, ffmpeg_path, payload, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Validation du cadrage")
        self.resize(1200, 820)
        self.setStyleSheet(STYLESHEET + """
            QSlider::groove:horizontal {
                background: rgba(255,255,255,10);
                height: 4px; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: """ + ACCENT + """;
                border: none;
                width: 16px; height: 16px; margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: """ + ACCENT + """;
                height: 4px; border-radius: 2px;
            }
            QSlider::handle:horizontal:hover {
                background: #ffb060;
                width: 18px; height: 18px; margin: -7px 0;
            }
        """)
        self.ffmpeg_path = ffmpeg_path
        self.payload = dict(payload)
        self.reply = None
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self.refresh_preview)
        self._road_v_ratio  = float(payload.get("road_vfov", 60))  / max(1.0, float(payload.get("road_hfov", 90)))
        self._cabin_v_ratio = float(payload.get("cabin_vfov", 80)) / max(1.0, float(payload.get("cabin_hfov", 120)))

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 16)
        root.setSpacing(14)

        # ── TITRE ──────────────────────────────────────────────
        hdr = QHBoxLayout(); hdr.setSpacing(12)
        title = QLabel("Validation du cadrage")
        title.setStyleSheet(f"color:{C['text_hi']}; font-size:16px; font-weight:700; font-family:'{UI_FONT}',sans-serif;")
        subtitle = QLabel("Ajuste les angles  ·  Espace = valider  ·  Flèches = route  ·  Alt+Flèches = PiP")
        subtitle.setStyleSheet(f"color:{C['text_mid']}; font-size:11px; font-family:'{UI_FONT}',sans-serif;")
        hdr.addWidget(title); hdr.addSpacing(12); hdr.addWidget(subtitle); hdr.addStretch()
        root.addLayout(hdr)

        # ── ZONE PREVIEW DUALE ─────────────────────────────────
        preview_row = QHBoxLayout(); preview_row.setSpacing(10)

        road_panel = QWidget()
        road_panel.setStyleSheet("background:rgba(255,255,255,4);border:1px solid rgba(255,255,255,12);border-radius:10px;")
        rpl = QVBoxLayout(road_panel); rpl.setContentsMargins(0,0,0,0); rpl.setSpacing(0)
        road_tag = QLabel("  ROUTE")
        road_tag.setStyleSheet(f"color:{C['text_lo']};font-size:9px;letter-spacing:2px;font-weight:700;"
                               f"font-family:'{UI_FONT}',sans-serif;padding:8px 12px 4px;background:transparent;")
        self.road_label = QLabel()
        self.road_label.setAlignment(Qt.AlignCenter)
        self.road_label.setMinimumSize(560, 315)
        self.road_label.setStyleSheet("background:transparent;border:none;")
        rpl.addWidget(road_tag); rpl.addWidget(self.road_label, 1)
        preview_row.addWidget(road_panel, 3)

        cabin_panel = QWidget()
        cabin_panel.setStyleSheet("background:rgba(255,255,255,4);border:1px solid rgba(246,136,31,25);border-radius:10px;")
        cpl = QVBoxLayout(cabin_panel); cpl.setContentsMargins(0,0,0,0); cpl.setSpacing(0)
        cabin_tag = QLabel("  HABITACLE (PiP)")
        cabin_tag.setStyleSheet(f"color:{ACCENT};font-size:9px;letter-spacing:2px;font-weight:700;"
                                f"font-family:'{UI_FONT}',sans-serif;padding:8px 12px 4px;background:transparent;")
        self.cabin_label = QLabel()
        self.cabin_label.setAlignment(Qt.AlignCenter)
        self.cabin_label.setMinimumSize(300, 170)
        self.cabin_label.setStyleSheet("background:transparent;border:none;")
        cpl.addWidget(cabin_tag); cpl.addWidget(self.cabin_label, 1)
        preview_row.addWidget(cabin_panel, 2)

        root.addLayout(preview_row, 1)

        # ── PRÉRÉGLAGES ────────────────────────────────────────
        preset_row = QHBoxLayout(); preset_row.setSpacing(8)
        lbl_pr = QLabel("Préréglage :")
        lbl_pr.setStyleSheet(f"color:{C['text_mid']};font-size:11px;font-family:'{UI_FONT}',sans-serif;")
        self.saved_presets = load_reframe_presets()
        self.preset_select = StyledComboBox()
        self.preset_select.addItem("— Sélectionner un préréglage —")
        for name in sorted(self.saved_presets.keys()):
            self.preset_select.addItem(name)
        self.preset_select.setFixedHeight(34)
        self.btn_save_preset  = self._ctrl_btn("Sauvegarder…")
        self.btn_apply_preset = self._ctrl_btn("Appliquer")
        preset_row.addWidget(lbl_pr); preset_row.addWidget(self.preset_select, 1)
        preset_row.addWidget(self.btn_apply_preset); preset_row.addWidget(self.btn_save_preset)
        root.addLayout(preset_row)

        # ── SLIDERS ────────────────────────────────────────────
        sliders_w = QWidget()
        sliders_w.setStyleSheet("background:rgba(255,255,255,5);border:1px solid rgba(255,255,255,10);border-radius:10px;")
        sg = QGridLayout(sliders_w)
        sg.setContentsMargins(16,12,16,12); sg.setHorizontalSpacing(20); sg.setVerticalSpacing(8)

        def mk_slider(lo, hi, val, step=1, page=20):
            s = QSlider(Qt.Horizontal)
            s.setRange(lo, hi); s.setSingleStep(step); s.setPageStep(page)
            s.setTracking(True); s.setValue(val); return s

        def iv(key, default, scale=10):
            return int(round(float(self.payload.get(key, default)) * scale))

        self.road_yaw    = mk_slider(-1800, 1800, iv("road_yaw",   0),   step=1, page=30)
        self.road_pitch  = mk_slider(-450,  450,  iv("road_pitch", -10), step=1, page=10)
        self.road_hfov   = mk_slider(300,   1500, iv("road_hfov",  90),  step=5, page=50)
        self.cabin_yaw   = mk_slider(-1800, 1800, iv("cabin_yaw",  180), step=1, page=30)
        self.cabin_pitch = mk_slider(-450,  450,  iv("cabin_pitch",-5),  step=1, page=10)
        self.cabin_hfov  = mk_slider(300,   1500, iv("cabin_hfov", 120), step=5, page=50)
        self.pip_width   = mk_slider(260,   720,  int(self.payload.get("pip_width", 480)), step=2, page=16)
        self.pip_position = StyledComboBox()
        self.pip_position.addItems(["top_left","top_right","bottom_left","bottom_right"])
        self.pip_position.setCurrentText(self.payload.get("pip_position","top_right"))
        self.pip_position.setFixedHeight(30)

        self._value_labels = {}

        road_items = [
            ("←→  Yaw route",   self.road_yaw,   "road_yaw"),
            ("↕   Pitch route", self.road_pitch, "road_pitch"),
            ("⊡   FOV route",   self.road_hfov,  "road_hfov"),
        ]
        cabin_items = [
            ("←→  Yaw PiP",   self.cabin_yaw,   "cabin_yaw"),
            ("↕   Pitch PiP", self.cabin_pitch, "cabin_pitch"),
            ("⊡   FOV PiP",   self.cabin_hfov,  "cabin_hfov"),
        ]

        for col, txt, color in [(0, "ROUTE", ACCENT), (3, "HABITACLE / PiP", C['blue'])]:
            lh = QLabel(txt)
            lh.setStyleSheet(f"color:{color};font-size:9px;letter-spacing:2px;font-weight:700;font-family:'{UI_FONT}',sans-serif;")
            sg.addWidget(lh, 0, col, 1, 3)

        for ri, (lbl_txt, slider, key) in enumerate(road_items, start=1):
            lbl = QLabel(lbl_txt); lbl.setStyleSheet(f"color:{C['text_mid']};font-size:11px;"); lbl.setFixedWidth(120)
            val = QLabel(""); val.setFixedWidth(54); val.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            val.setStyleSheet(f"color:{ACCENT};font-size:11px;font-weight:700;")
            self._value_labels[key] = val
            sg.addWidget(lbl, ri, 0); sg.addWidget(slider, ri, 1); sg.addWidget(val, ri, 2)

        for ri, (lbl_txt, slider, key) in enumerate(cabin_items, start=1):
            lbl = QLabel(lbl_txt); lbl.setStyleSheet(f"color:{C['text_mid']};font-size:11px;"); lbl.setFixedWidth(120)
            val = QLabel(""); val.setFixedWidth(54); val.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            val.setStyleSheet(f"color:{C['blue']};font-size:11px;font-weight:700;")
            self._value_labels[key] = val
            sg.addWidget(lbl, ri, 3); sg.addWidget(slider, ri, 4); sg.addWidget(val, ri, 5)

        lbl_pw = QLabel("⊞   Taille PiP"); lbl_pw.setStyleSheet(f"color:{C['text_mid']};font-size:11px;"); lbl_pw.setFixedWidth(120)
        val_pw = QLabel(""); val_pw.setFixedWidth(54); val_pw.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        val_pw.setStyleSheet(f"color:{C['blue']};font-size:11px;font-weight:700;")
        self._value_labels["pip_width"] = val_pw
        sg.addWidget(lbl_pw, 4, 3); sg.addWidget(self.pip_width, 4, 4); sg.addWidget(val_pw, 4, 5)

        lbl_pos = QLabel("📌  Position PiP"); lbl_pos.setStyleSheet(f"color:{C['text_mid']};font-size:11px;"); lbl_pos.setFixedWidth(120)
        sg.addWidget(lbl_pos, 5, 3); sg.addWidget(self.pip_position, 5, 4, 1, 2)

        sg.setColumnStretch(1, 1); sg.setColumnStretch(4, 1)
        root.addWidget(sliders_w)

        # ── BOUTONS ────────────────────────────────────────────
        btns = QHBoxLayout(); btns.setSpacing(8)
        btn_reset = self._ctrl_btn("↺  Réinitialiser")
        btn_skip  = self._ctrl_btn("Ignorer l'auto-cadrage")
        btn_ok = QPushButton("Valider et exporter")
        btn_ok.setObjectName("btn_launch_active"); btn_ok.setFixedHeight(40); btn_ok.setMinimumWidth(180)
        apply_button_icon(btn_ok, "check", color="#140c04", size=16)
        btns.addWidget(btn_reset); btns.addWidget(btn_skip); btns.addStretch(); btns.addWidget(btn_ok)
        root.addLayout(btns)

        # ── CONNEXIONS ─────────────────────────────────────────
        for s in [self.road_yaw, self.road_pitch, self.road_hfov,
                  self.cabin_yaw, self.cabin_pitch, self.cabin_hfov, self.pip_width]:
            s.valueChanged.connect(self._update_labels_and_schedule)
        self.pip_position.currentIndexChanged.connect(self._schedule)
        btn_reset.clicked.connect(self._reset_auto)
        btn_skip.clicked.connect(self._skip_auto)
        btn_ok.clicked.connect(self._accept_values)
        self.btn_save_preset.clicked.connect(self._save_preset)
        self.btn_apply_preset.clicked.connect(self._apply_selected_preset)
        self.preset_select.activated.connect(lambda *_: self._apply_selected_preset())
        self._update_labels_and_schedule()

    def _ctrl_btn(self, txt):
        b = QPushButton(txt); b.setObjectName("btn_ghost"); b.setFixedHeight(34); return b

    def _update_labels_and_schedule(self):
        vals = {
            "road_yaw":   f"{self.road_yaw.value()/10:.1f}°",
            "road_pitch": f"{self.road_pitch.value()/10:.1f}°",
            "road_hfov":  f"{self.road_hfov.value()/10:.1f}°",
            "cabin_yaw":  f"{self.cabin_yaw.value()/10:.1f}°",
            "cabin_pitch":f"{self.cabin_pitch.value()/10:.1f}°",
            "cabin_hfov": f"{self.cabin_hfov.value()/10:.1f}°",
            "pip_width":  f"{self.pip_width.value()} px",
        }
        for k, lbl in self._value_labels.items(): lbl.setText(vals.get(k, ""))
        self._schedule()

    def _schedule(self): self._render_timer.start(180)

    def _current_payload(self):
        d = dict(self.payload)
        d["road_yaw"]    = round(self.road_yaw.value()/10.0, 1)
        d["road_pitch"]  = round(self.road_pitch.value()/10.0, 1)
        d["road_hfov"]   = round(self.road_hfov.value()/10.0, 1)
        d["road_vfov"]   = round(max(20.0, min(120.0, d["road_hfov"] * self._road_v_ratio)), 1)
        d["cabin_yaw"]   = round(self.cabin_yaw.value()/10.0, 1)
        d["cabin_pitch"] = round(self.cabin_pitch.value()/10.0, 1)
        d["cabin_hfov"]  = round(self.cabin_hfov.value()/10.0, 1)
        d["cabin_vfov"]  = round(max(20.0, min(120.0, d["cabin_hfov"] * self._cabin_v_ratio)), 1)
        d["pip_width"]   = int(self.pip_width.value())
        d["pip_height"]  = max(180, int(self.pip_width.value() * 9/16))
        d["pip_position"]= self.pip_position.currentText()
        return d

    def refresh_preview(self):
        self._render_timer.stop()
        d = self._current_payload()
        vp = d.get("video_path",""); wd = d.get("work_dir","")
        ts = float(d.get("preview_timecode", 5.0)); ff = self.ffmpeg_path
        if not vp or not os.path.isfile(str(vp)): return
        import tempfile as _tf
        if not wd: wd = _tf.mkdtemp(prefix="msa_prev_")
        tag = int(time.time()*1000)
        road_out  = os.path.join(wd, f"prev_road_{tag}.jpg")
        cabin_out = os.path.join(wd, f"prev_cabin_{tag}.jpg")
        r_road = _render_frame(ff, vp, road_out,  d["road_yaw"],  d["road_pitch"],  d["road_hfov"],  d["road_vfov"],  ts, w=800, h=450)
        r_cabin= _render_frame(ff, vp, cabin_out, d["cabin_yaw"], d["cabin_pitch"], d["cabin_hfov"], d["cabin_vfov"], ts, w=480, h=270)
        if r_road.returncode == 0 and os.path.exists(road_out):
            pix = QPixmap(road_out)
            if not pix.isNull():
                self.road_label.setPixmap(pix.scaled(self.road_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.road_label.setText("Aperçu route indisponible")
        if r_cabin.returncode == 0 and os.path.exists(cabin_out):
            pix = QPixmap(cabin_out)
            if not pix.isNull():
                self.cabin_label.setPixmap(pix.scaled(self.cabin_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.cabin_label.setText("Aperçu habitacle indisponible")

    def resizeEvent(self, event):
        super().resizeEvent(event); self._schedule()

    def _preset_payload(self):
        return extract_reframe_preset_payload(self._current_payload())

    def _save_preset(self):
        dlg = TextEntryDialog("Sauvegarder un préréglage", "Nom du preset", parent=self)
        if dlg.exec_() != QDialog.Accepted:
            return
        name = dlg.text_value()
        if not name:
            return
        self.saved_presets[name] = self._preset_payload()
        if save_reframe_presets(self.saved_presets):
            if self.preset_select.findText(name) == -1: self.preset_select.addItem(name)
            self.preset_select.setCurrentText(name)

    def _apply_selected_preset(self):
        name = self.preset_select.currentText().strip()
        if not name or name.startswith("—"): return
        data = self.saved_presets.get(name)
        if not isinstance(data, dict): return
        def sv(slider, key, default, scale=10):
            slider.setValue(int(round(float(data.get(key, default)) * scale)))
        sv(self.road_yaw,    "road_yaw",    0);  sv(self.road_pitch,  "road_pitch",  -10)
        sv(self.road_hfov,   "road_hfov",   90); sv(self.cabin_yaw,   "cabin_yaw",   180)
        sv(self.cabin_pitch, "cabin_pitch", -5); sv(self.cabin_hfov,  "cabin_hfov",  120)
        self.pip_width.setValue(int(data.get("pip_width", self.pip_width.value())))
        if data.get("pip_position"): self.pip_position.setCurrentText(data["pip_position"])
        self._update_labels_and_schedule()

    def _reset_auto(self):
        def rv(slider, key, default, scale=10):
            slider.setValue(int(round(float(self.payload.get(key, default)) * scale)))
        rv(self.road_yaw,"road_yaw",0); rv(self.road_pitch,"road_pitch",-10); rv(self.road_hfov,"road_hfov",90)
        rv(self.cabin_yaw,"cabin_yaw",180); rv(self.cabin_pitch,"cabin_pitch",-5); rv(self.cabin_hfov,"cabin_hfov",120)
        self.pip_width.setValue(int(self.payload.get("pip_width",480)))
        self.pip_position.setCurrentText(self.payload.get("pip_position","top_right"))
        self._update_labels_and_schedule()

    def _skip_auto(self):
        self.reply = {"mode": "skip_auto"}; self.accept()

    def _accept_values(self):
        self.reply = self._current_payload(); self.reply["mode"] = "validate"; self.accept()

    def get_reply(self):
        if self.reply is None: self.reply = self._current_payload(); self.reply["mode"] = "validate"
        return self.reply

    def keyPressEvent(self, event):
        key = event.key(); mod = event.modifiers()
        step = 50 if mod & Qt.ShiftModifier else 10
        if key == Qt.Key_Space:   self._accept_values(); return
        if key == Qt.Key_R:       self._reset_auto(); return
        if key == Qt.Key_Left:
            t = self.cabin_yaw if mod & Qt.AltModifier else self.road_yaw; t.setValue(t.value()-step); return
        if key == Qt.Key_Right:
            t = self.cabin_yaw if mod & Qt.AltModifier else self.road_yaw; t.setValue(t.value()+step); return
        if key == Qt.Key_Up:
            t = self.cabin_pitch if mod & Qt.AltModifier else self.road_pitch; t.setValue(t.value()+step); return
        if key == Qt.Key_Down:
            t = self.cabin_pitch if mod & Qt.AltModifier else self.road_pitch; t.setValue(t.value()-step); return
        super().keyPressEvent(event)

    # Alias compat
    def schedule_preview(self): self._schedule()
    def accept_preview(self):   self._accept_values()
    def reset_auto(self):       self._reset_auto()


# ══════════════════════════════════════════════════════════════
#  DIALOG RÉGLAGES
# ══════════════════════════════════════════════════════════════
class SettingsDialog(QDialog):
    def __init__(self, preset, ffmpeg_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Réglages")
        self.setWindowIcon(app_icon())
        self.setMinimumSize(1040, 790)
        self.setStyleSheet(STYLESHEET)
        self.preset=dict(preset); self.ffmpeg_path=ffmpeg_path or ""
        self._update_worker = None
        self._postponed_update_version = str(self.preset.get("update_postponed_version", "") or "").strip()
        self.diag_state = {
            "ffmpeg_validated": bool(self.preset.get("ffmpeg_validated")),
            "ffmpeg_resolved_path": self.preset.get("ffmpeg_resolved_path", ""),
            "media_sdk_validated": bool(self.preset.get("media_sdk_validated")),
            "media_sdk_resolved_path": self.preset.get("media_sdk_resolved_path", ""),
            "insv_ready": False,
            "ffmpeg_status_text": "",
            "media_sdk_status_text": "",
            "insv_status_text": "",
        }
        self._build()
        self._apply_initial_geometry()

    def _build(self):
        root = QVBoxLayout(self)
        root.setSpacing(18)
        root.setContentsMargins(22, 22, 22, 22)

        header = QFrame()
        header.setObjectName("settings_header")
        header.setAttribute(Qt.WA_StyledBackground, True)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(8)
        eyebrow = QLabel("PRÉFÉRENCES")
        eyebrow.setObjectName("section_eyebrow")
        title = QLabel("Réglages")
        title.setObjectName("settings_title")
        subtitle = QLabel("Ajuste le cadrage, la sortie, l'encodage et l'environnement de travail de MSA Video Tool.")
        subtitle.setObjectName("settings_subtitle")
        subtitle.setWordWrap(True)
        header_layout.addWidget(eyebrow)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        root.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("settings_tabs")
        self.tabs.setDocumentMode(True)
        self.tabs.tabBar().setExpanding(False)
        self.tabs.tabBar().setDrawBase(False)
        self.tabs.addTab(self._build_camera_tab(), "Caméra")
        self.tabs.addTab(self._build_output_tab(), "Sortie")
        self.tabs.addTab(self._build_encoding_tab(), "Encodage")
        self.tabs.addTab(self._build_system_tab(), "Système")
        root.addWidget(self.tabs, 1)

        footer = QFrame()
        footer.setObjectName("settings_footer")
        footer.setAttribute(Qt.WA_StyledBackground, True)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(18, 16, 18, 16)
        footer_layout.setSpacing(14)
        hint = QLabel("Les changements sont pris en compte pour les prochains exports.")
        hint.setObjectName("settings_footer_hint")
        hint.setWordWrap(True)
        footer_layout.addWidget(hint, 1)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setObjectName("btn_ghost")
        btn_cancel.setFixedHeight(42)
        btn_cancel.setMinimumWidth(140)
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Enregistrer")
        btn_ok.setObjectName("btn_launch_active")
        btn_ok.setFixedHeight(42)
        btn_ok.setMinimumWidth(176)
        btn_ok.clicked.connect(self.accept)
        footer_layout.addWidget(btn_cancel)
        footer_layout.addWidget(btn_ok)
        root.addWidget(footer)

    def _make_settings_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(14)
        scroll.setWidget(page)
        return scroll, page_layout

    def _build_camera_tab(self):
        def sp(key, lo, hi, tip=""):
            s = QSpinBox()
            s.setRange(lo, hi)
            s.setValue(self.preset.get(key, 0))
            configure_spinbox(s)
            if tip:
                s.setToolTip(tip)
            return s

        self.ry = sp("road_yaw", -180, 180, "0° = face avant")
        self.rp = sp("road_pitch", -90, 90)
        self.rhf = sp("road_hfov", 30, 180, "90° recommandé")
        self.rvf = sp("road_vfov", 20, 120)
        self.cy = sp("cabin_yaw", -180, 180, "180° = face arrière")
        self.cp = sp("cabin_pitch", -90, 90)
        self.chf = sp("cabin_hfov", 30, 180)
        self.cvf = sp("cabin_vfov", 20, 120)
        self.auto_rf = ToggleSwitch(self.preset.get("auto_reframe", False))
        self.preview_rf = ToggleSwitch(self.preset.get("preview_before_render", True))
        self.auto_secs = QSpinBox()
        self.auto_secs.setRange(1, 8)
        self.auto_secs.setValue(self.preset.get("auto_analysis_seconds", 3))
        configure_spinbox(self.auto_secs)
        self.auto_samples = QSpinBox()
        self.auto_samples.setRange(1, 5)
        self.auto_samples.setValue(self.preset.get("auto_sample_count", 2))
        configure_spinbox(self.auto_samples)
        self.auto_step = QSpinBox()
        self.auto_step.setRange(15, 90)
        self.auto_step.setSingleStep(15)
        self.auto_step.setValue(self.preset.get("auto_cabin_search_step", 45))
        configure_spinbox(self.auto_step)

        scroll, root = self._make_settings_page()

        route_card, route_body = self._make_settings_card(
            "Vue route",
            "Réglage du cadrage principal utilisé pour la vue avant.",
            eyebrow="CAMÉRA",
            eyebrow_color=ACCENT,
        )
        self._add_field_row(route_body, "Yaw", self.ry)
        self._add_field_row(route_body, "Pitch", self.rp)
        self._add_field_row(route_body, "H-FOV", self.rhf)
        self._add_field_row(route_body, "V-FOV", self.rvf)
        root.addWidget(route_card)

        cabin_card, cabin_body = self._make_settings_card(
            "Vue habitacle",
            "Définis le cadrage arrière utilisé dans le PiP.",
            eyebrow="PIP",
            eyebrow_color=C["blue"],
        )
        self._add_field_row(cabin_body, "Yaw", self.cy)
        self._add_field_row(cabin_body, "Pitch", self.cp)
        self._add_field_row(cabin_body, "H-FOV", self.chf)
        self._add_field_row(cabin_body, "V-FOV", self.cvf)
        root.addWidget(cabin_card)

        auto_card, auto_body = self._make_settings_card(
            "Auto-cadrage",
            "Active l’analyse automatique et contrôle la validation du cadrage avant export.",
            eyebrow="ASSISTANCE",
            eyebrow_color=C["green"],
        )
        self._add_field_row(auto_body, "Auto-cadrage", self.auto_rf)
        self._add_field_row(auto_body, "Validation cadrage", self.preview_rf)
        self._add_field_row(auto_body, "Analyse (s)", self.auto_secs)
        self._add_field_row(auto_body, "Images test", self.auto_samples)
        self._add_field_row(auto_body, "Pas yaw", self.auto_step)
        root.addWidget(auto_card)
        root.addStretch()
        return scroll

    def _build_output_tab(self):
        output_preset_key = normalize_output_preset(
            self.preset.get("output_preset"),
            self.preset.get("output_width", 1920),
            self.preset.get("output_height", 1080),
        )
        self.ow = QSpinBox()
        self.ow.setRange(640, 7680)
        self.ow.setValue(self.preset["output_width"])
        configure_spinbox(self.ow)
        self.oh = QSpinBox()
        self.oh.setRange(360, 4320)
        self.oh.setValue(self.preset["output_height"])
        configure_spinbox(self.oh)
        self.output_resolution_preset = StyledComboBox()
        for preset_key, preset_label, _size in OUTPUT_RESOLUTION_PRESETS:
            self.output_resolution_preset.addItem(preset_label, preset_key)
        preset_idx = self.output_resolution_preset.findData(output_preset_key)
        self.output_resolution_preset.setCurrentIndex(max(0, preset_idx))
        self.output_fps = StyledComboBox()
        for fps_value, fps_label in OUTPUT_FPS_OPTIONS:
            self.output_fps.addItem(fps_label, fps_value)
        fps_idx = self.output_fps.findData(resolve_output_fps(self.preset))
        self.output_fps.setCurrentIndex(max(0, fps_idx))
        self.pw = QSpinBox()
        self.pw.setRange(160, 1920)
        self.pw.setValue(self.preset["pip_width"])
        configure_spinbox(self.pw)
        self.ph2 = QSpinBox()
        self.ph2.setRange(90, 1080)
        self.ph2.setValue(self.preset["pip_height"])
        configure_spinbox(self.ph2)
        self.pm = QSpinBox()
        self.pm.setRange(0, 200)
        self.pm.setValue(self.preset["pip_margin"])
        configure_spinbox(self.pm)
        self.pip_pos_cb = StyledComboBox()
        for pos_key, pos_label in [
            ("top_right", "Haut droite"),
            ("top_left", "Haut gauche"),
            ("bottom_right", "Bas droite"),
            ("bottom_left", "Bas gauche"),
        ]:
            self.pip_pos_cb.addItem(pos_label, pos_key)
        current_pip = self.preset.get("pip_position", "top_right")
        idx = self.pip_pos_cb.findData(current_pip)
        self.pip_pos_cb.setCurrentIndex(max(0, idx))
        self.date_cb = ToggleSwitch(self.preset.get("output_date_folder", True))
        self.prefix = QLineEdit(self.preset.get("output_prefix", "MSA"))
        self.prefix.setPlaceholderText("MSA")
        self.output_resolution_preset.currentIndexChanged.connect(self._apply_output_resolution_preset)
        self.ow.valueChanged.connect(self._sync_output_resolution_preset)
        self.oh.valueChanged.connect(self._sync_output_resolution_preset)

        scroll, root = self._make_settings_page()

        resolution_card, resolution_body = self._make_settings_card(
            "Résolution",
            "Paramètres de sortie du rendu final exporté.",
            eyebrow="SORTIE",
            eyebrow_color=ACCENT,
        )
        self._add_field_row(resolution_body, "Preset", self.output_resolution_preset)
        self._add_field_row(resolution_body, "Largeur", self.ow)
        self._add_field_row(resolution_body, "Hauteur", self.oh)
        self._add_field_row(resolution_body, "FPS sortie", self.output_fps)
        root.addWidget(resolution_card)

        pip_card, pip_body = self._make_settings_card(
            "PiP",
            "Contrôle la taille, la marge et la position de la vue habitacle.",
            eyebrow="COMPOSITION",
            eyebrow_color=C["blue"],
        )
        self._add_field_row(pip_body, "Largeur", self.pw)
        self._add_field_row(pip_body, "Hauteur", self.ph2)
        self._add_field_row(pip_body, "Marge", self.pm)
        self._add_field_row(pip_body, "Position", self.pip_pos_cb)
        root.addWidget(pip_card)

        organization_card, organization_body = self._make_settings_card(
            "Organisation",
            "Choisis comment les exports sont nommés et structurés.",
            eyebrow="FICHIERS",
            eyebrow_color=C["green"],
        )
        self._add_field_row(organization_body, "Sous-dossier date", self.date_cb)
        self._add_field_row(organization_body, "Préfixe", self.prefix)
        root.addWidget(organization_card)
        root.addStretch()
        return scroll

    def _apply_output_resolution_preset(self, *_):
        preset_key = str(self.output_resolution_preset.currentData() or "custom")
        size = OUTPUT_RESOLUTION_PRESET_MAP.get(preset_key)
        if not size:
            return
        width, height = size
        old_w = self.ow.blockSignals(True)
        old_h = self.oh.blockSignals(True)
        try:
            self.ow.setValue(width)
            self.oh.setValue(height)
        finally:
            self.ow.blockSignals(old_w)
            self.oh.blockSignals(old_h)
        self._sync_output_resolution_preset()

    def _sync_output_resolution_preset(self, *_):
        preset_key = match_output_resolution_preset(self.ow.value(), self.oh.value())
        idx = self.output_resolution_preset.findData(preset_key)
        if idx < 0:
            idx = 0
        old_state = self.output_resolution_preset.blockSignals(True)
        try:
            self.output_resolution_preset.setCurrentIndex(idx)
        finally:
            self.output_resolution_preset.blockSignals(old_state)

    def _build_encoding_tab(self):
        self.quality_mode = StyledComboBox()
        for mode in ["Rapide", "Équilibré", "Haute qualité", "Personnalisé"]:
            self.quality_mode.addItem(mode)
        self.quality_mode.setCurrentText(self.preset.get("quality_mode", "Équilibré"))
        self.crf = QSpinBox()
        self.crf.setRange(0, 51)
        self.crf.setValue(self.preset["crf"])
        configure_spinbox(self.crf)
        self.enc_p = StyledComboBox()
        for preset_name in ["ultrafast", "fast", "medium", "slow"]:
            self.enc_p.addItem(preset_name)
        self.enc_p.setCurrentText(self.preset.get("preset_encode", "fast"))
        self.bitrate = QLineEdit(self.preset.get("video_bitrate", "12M"))
        self.nvenc = ToggleSwitch(self.preset.get("use_nvenc", True))
        self.quality_mode.currentTextChanged.connect(self._apply_quality_mode)

        self.insv_mode = StyledComboBox()
        for mode_name in INSV_PROCESSING_MODES:
            self.insv_mode.addItem(mode_name)
        self.insv_mode.setCurrentText(resolve_insv_processing_mode(self.preset))
        self.insv_mode_hint = QLabel()
        self.insv_mode_hint.setWordWrap(True)
        self.insv_mode.currentTextChanged.connect(self._refresh_insv_mode_hint)
        self._refresh_insv_mode_hint(self.insv_mode.currentText())

        self.thumb = ToggleSwitch(self.preset.get("gen_thumbnail", True))
        self.openfolder = ToggleSwitch(self.preset.get("auto_open_output", True))
        self.wm_cb = ToggleSwitch(self.preset.get("add_watermark", False))
        self.wm_path = QLineEdit(self.preset.get("watermark_path", ""))
        self.wm_path.setPlaceholderText("Chemin PNG logo…")
        self.wm_opa = QSpinBox()
        self.wm_opa.setRange(10, 100)
        self.wm_opa.setValue(self.preset.get("watermark_opacity", 80))
        self.wm_opa.setSuffix("%")
        self.wm_opa.setButtonSymbols(QAbstractSpinBox.NoButtons)
        bwm = QPushButton("…")
        bwm.setObjectName("btn_ghost")
        bwm.setFixedSize(36, 34)
        bwm.clicked.connect(lambda: self._browse(self.wm_path, "Logo PNG"))
        wm_row = QHBoxLayout()
        wm_row.setSpacing(10)
        wm_row.addWidget(self.wm_path)
        wm_row.addWidget(bwm)

        scroll, root = self._make_settings_page()

        quality_card, quality_body = self._make_settings_card(
            "Qualité",
            "Pilote le profil d’encodage principal utilisé pour le rendu final.",
            eyebrow="ENCODAGE",
            eyebrow_color=ACCENT,
        )
        self._add_field_row(quality_body, "Mode", self.quality_mode)
        self._add_field_row(quality_body, "CRF", self.crf)
        self._add_field_row(quality_body, "Vitesse", self.enc_p)
        self._add_field_row(quality_body, "Bitrate", self.bitrate)
        self._add_field_row(quality_body, "NVENC GPU", self.nvenc)
        root.addWidget(quality_card)

        insv_card, insv_body = self._make_settings_card(
            "Traitement INSV",
            "Choisis la stratégie utilisée pour le stitching 360 avant recadrage.",
            eyebrow="360",
            eyebrow_color=C["green"],
        )
        self._add_field_row(insv_body, "Mode INSV", self.insv_mode)
        insv_body.addWidget(self.insv_mode_hint)
        root.addWidget(insv_card)

        export_card, export_body = self._make_settings_card(
            "Options & watermark",
            "Comportements après export et habillage graphique optionnel.",
            eyebrow="SORTIE",
            eyebrow_color=C["blue"],
        )
        self._add_field_row(export_body, "Miniature JPG", self.thumb)
        self._add_field_row(export_body, "Ouvrir dossier", self.openfolder)
        self._add_field_row(export_body, "Watermark", self.wm_cb)
        self._add_field_row(export_body, "Logo", wm_row)
        self._add_field_row(export_body, "Opacité", self.wm_opa)
        root.addWidget(export_card)
        root.addStretch()
        return scroll

    def _build_system_tab(self):
        sys_scroll, sys_root = self._make_settings_page()
        self.ff = QLineEdit(self.preset.get("ffmpeg_path", "") or self.ffmpeg_path)
        self.ff.setPlaceholderText("Auto-détecté / FFmpeg embarqué")
        self.sdk = QLineEdit(self.preset.get("media_sdk_path", ""))
        self.sdk.setPlaceholderText("Dossier SDK ou exécutable MediaSDKTest.exe")
        self.outd = QLineEdit(self.preset.get("output_dir", ""))
        self.outd.setPlaceholderText("Dossier de sortie")
        self.ff.textChanged.connect(self._on_ffmpeg_path_changed)
        self.sdk.textChanged.connect(self._on_sdk_path_changed)

        def brow_f(inp, title, flt="Tous (*.*)"):
            path, _ = QFileDialog.getOpenFileName(self, title, "", flt)
            if path:
                inp.setText(path)

        def brow_d(inp, title="Dossier"):
            path = QFileDialog.getExistingDirectory(self, title)
            if path:
                inp.setText(path)

        ff_row = QHBoxLayout()
        ff_row.setSpacing(10)
        ff_btn = QPushButton("…")
        ff_btn.setObjectName("btn_ghost")
        ff_btn.setFixedSize(36, 34)
        ff_btn.clicked.connect(lambda: brow_f(self.ff, "FFmpeg", "Exécutable (*.exe);;Tous (*.*)"))
        ff_row.addWidget(self.ff)
        ff_row.addWidget(ff_btn)

        sdk_row = QHBoxLayout()
        sdk_row.setSpacing(10)
        sdk_auto_btn = QPushButton("AUTO")
        sdk_auto_btn.setObjectName("btn_ghost")
        sdk_auto_btn.setFixedHeight(34)
        sdk_file_btn = QPushButton("EXE")
        sdk_file_btn.setObjectName("btn_ghost")
        sdk_file_btn.setFixedHeight(34)
        sdk_dir_btn = QPushButton("DIR")
        sdk_dir_btn.setObjectName("btn_ghost")
        sdk_dir_btn.setFixedHeight(34)
        sdk_auto_btn.clicked.connect(self._detect_sdk_clicked)
        sdk_file_btn.clicked.connect(lambda: brow_f(self.sdk, "Exécutable SDK", "Exécutable (*.exe);;Tous (*.*)"))
        sdk_dir_btn.clicked.connect(lambda: brow_d(self.sdk, "Dossier SDK"))
        sdk_row.addWidget(self.sdk)
        sdk_row.addWidget(sdk_auto_btn)
        sdk_row.addWidget(sdk_file_btn)
        sdk_row.addWidget(sdk_dir_btn)

        out_row = QHBoxLayout()
        out_row.setSpacing(10)
        out_btn = QPushButton("…")
        out_btn.setObjectName("btn_ghost")
        out_btn.setFixedSize(36, 34)
        out_btn.clicked.connect(lambda: brow_d(self.outd))
        out_row.addWidget(self.outd)
        out_row.addWidget(out_btn)

        self.theme_mode = StyledComboBox()
        for mode_key, mode_label in THEME_MODE_ITEMS:
            self.theme_mode.addItem(mode_label, mode_key)
        theme_index = self.theme_mode.findData(normalize_theme_mode(self.preset.get("theme_mode", "dark")))
        self.theme_mode.setCurrentIndex(max(0, theme_index))
        self.update_auto = ToggleSwitch(self.preset.get("update_auto_check", True))
        self.update_manifest = QLineEdit(self.preset.get("update_manifest_url", ""))
        self.update_manifest.setPlaceholderText("https://ton-domaine/update.json")
        self.update_version_label = QLabel(APP_VERSION)
        self.update_version_label.setStyleSheet(f"color:{C['text_hi']}; font-weight:700;")
        self.update_status = QLabel("Configure une URL manifeste pour activer les notifications de nouvelle version.")
        self.update_status.setWordWrap(True)
        self.update_status.setStyleSheet(f"color:{C['text_mid']}; font-size:11px; font-weight:600;")
        self.btn_check_updates = QPushButton("Vérifier les mises à jour")
        self.btn_check_updates.setObjectName("btn_ghost")
        self.btn_check_updates.clicked.connect(self._check_updates_clicked)

        self.delivery_enabled = ToggleSwitch(self.preset.get("delivery_enabled", False))
        self.delivery_mock = ToggleSwitch(self.preset.get("delivery_mock_mode", True))
        self.delivery_sender = QLineEdit(self.preset.get("delivery_sender_name", "Motorsport Academy"))
        self.delivery_sender.setPlaceholderText("Motorsport Academy")
        self.delivery_backend = QLineEdit(self.preset.get("delivery_backend_url", ""))
        self.delivery_backend.setPlaceholderText("https://ton-backend.exemple.com")
        self.delivery_api_key = QLineEdit(self.preset.get("delivery_api_key", ""))
        self.delivery_api_key.setEchoMode(QLineEdit.Password)
        self.delivery_api_key.setPlaceholderText("Clé API backend")
        self.delivery_ttl = QSpinBox()
        self.delivery_ttl.setRange(1, 30)
        self.delivery_ttl.setValue(int(self.preset.get("delivery_link_ttl_days", 7) or 7))
        configure_spinbox(self.delivery_ttl)
        self.delivery_email = ToggleSwitch(self.preset.get("delivery_send_email", True))
        self.delivery_sms = ToggleSwitch(self.preset.get("delivery_send_sms", False))

        appearance_card, appearance_body = self._make_settings_card(
            "Apparence",
            "Choisis le thème visuel utilisé par l'interface V1.1.",
            eyebrow="INTERFACE",
            eyebrow_color=ACCENT,
        )
        self._add_field_row(appearance_body, "Thème", self.theme_mode)
        sys_root.addWidget(appearance_card)

        update_card, update_body = self._make_settings_card(
            "Mises à jour",
            "Au lancement, l'application peut vérifier un manifeste JSON et proposer le téléchargement de la dernière version.",
            eyebrow="VERSION",
            eyebrow_color=C["blue"],
        )
        self._add_field_row(update_body, "Version installée", self.update_version_label)
        self._add_field_row(update_body, "Vérification auto", self.update_auto)
        self._add_field_row(update_body, "URL manifeste", self.update_manifest)
        update_body.addWidget(self.update_status)
        update_btn_row = QHBoxLayout()
        update_btn_row.setSpacing(10)
        update_btn_row.addWidget(self.btn_check_updates)
        update_btn_row.addStretch()
        update_body.addLayout(update_btn_row)
        sys_root.addWidget(update_card)

        runtime_card, runtime_body = self._make_settings_card(
            "Exécutables et sortie",
            "Définis les chemins utilisés par l'application. Le Media SDK peut être détecté automatiquement.",
            eyebrow="ENVIRONNEMENT",
            eyebrow_color=C["green"],
        )
        self._add_field_row(runtime_body, "FFmpeg", ff_row)
        self._add_field_row(runtime_body, "Media SDK", sdk_row)
        self._add_field_row(runtime_body, "Dossier de sortie", out_row)
        sys_root.addWidget(runtime_card)

        delivery_card, delivery_body = self._make_settings_card(
            "Livraison client",
            "Le même export peut être envoyé automatiquement à plusieurs clients après traitement.",
            eyebrow="CLIENTS",
            eyebrow_color=ACCENT,
        )
        self._add_field_row(delivery_body, "Envoi auto", self.delivery_enabled)
        self._add_field_row(delivery_body, "Mode simulation", self.delivery_mock)
        self._add_field_row(delivery_body, "Nom expéditeur", self.delivery_sender)
        self._add_field_row(delivery_body, "Backend Stream", self.delivery_backend)
        self._add_field_row(delivery_body, "Clé API", self.delivery_api_key)
        self._add_field_row(delivery_body, "Durée du lien", self.delivery_ttl, suffix="jours")
        self._add_field_row(delivery_body, "Email client", self.delivery_email)
        self._add_field_row(delivery_body, "SMS client", self.delivery_sms)
        sys_root.addWidget(delivery_card)

        self.ff_status = QLabel()
        self.sdk_status = QLabel()
        self.insv_status = QLabel()
        diagnostic_card, diagnostic_body = self._make_settings_card(
            "Diagnostic",
            "Valide FFmpeg et le SDK avant le premier export INSV.",
            eyebrow="SANTÉ",
            eyebrow_color=C["blue"],
        )
        status_grid_wrap = QWidget()
        status_grid = QGridLayout(status_grid_wrap)
        status_grid.setContentsMargins(0, 0, 0, 0)
        status_grid.setHorizontalSpacing(12)
        status_grid.setVerticalSpacing(10)
        status_grid.addWidget(self._field_label("Statut FFmpeg"), 0, 0)
        status_grid.addWidget(self.ff_status, 0, 1)
        status_grid.addWidget(self._field_label("Statut SDK"), 1, 0)
        status_grid.addWidget(self.sdk_status, 1, 1)
        status_grid.addWidget(self._field_label("Traitement INSV"), 2, 0)
        status_grid.addWidget(self.insv_status, 2, 1)
        status_grid.setColumnStretch(1, 1)
        diagnostic_body.addWidget(status_grid_wrap)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        self.btn_check_ff = QPushButton("Vérifier FFmpeg")
        self.btn_check_ff.setObjectName("btn_ghost")
        self.btn_check_ff.clicked.connect(self._check_ffmpeg_clicked)
        self.btn_check_sdk = QPushButton("Vérifier le SDK")
        self.btn_check_sdk.setObjectName("btn_ghost")
        self.btn_check_sdk.clicked.connect(self._check_sdk_clicked)
        btn_row.addWidget(self.btn_check_ff)
        btn_row.addWidget(self.btn_check_sdk)
        btn_row.addStretch()
        diagnostic_body.addLayout(btn_row)

        self.diag_log = QTextEdit()
        self.diag_log.setObjectName("log_view")
        self.diag_log.setReadOnly(True)
        self.diag_log.setMinimumHeight(220)
        self.diag_log.setPlaceholderText("Le diagnostic FFmpeg / SDK s'affichera ici.")
        diagnostic_body.addWidget(self.diag_log)
        sys_root.addWidget(diagnostic_card)
        self._refresh_diag_status_labels()
        sys_root.addStretch()
        return sys_scroll

    def _apply_quality_mode(self, mode):
        prof = QUALITY_PROFILES.get(mode, {})
        if not prof:
            return
        self.crf.setValue(int(prof.get("crf", self.crf.value())))
        self.enc_p.setCurrentText(prof.get("preset_encode", self.enc_p.currentText()))
        self.bitrate.setText(prof.get("video_bitrate", self.bitrate.text()))

    def _make_settings_card(self, title, subtitle="", eyebrow="", eyebrow_color=None):
        card = QFrame()
        card.setObjectName("settings_card")
        card.setAttribute(Qt.WA_StyledBackground, True)
        body = QVBoxLayout(card)
        body.setContentsMargins(18, 16, 18, 16)
        body.setSpacing(12)
        if eyebrow:
            eyebrow_lbl = QLabel(eyebrow)
            eyebrow_lbl.setObjectName("section_eyebrow")
            if eyebrow_color:
                eyebrow_lbl.setStyleSheet(
                    f"color:{eyebrow_color}; font-size:10px; font-weight:800; letter-spacing:2px; font-family:'{UI_FONT}',sans-serif;"
                )
            body.addWidget(eyebrow_lbl)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("section_title")
        body.addWidget(title_lbl)
        if subtitle:
            subtitle_lbl = QLabel(subtitle)
            subtitle_lbl.setObjectName("section_subtitle")
            subtitle_lbl.setWordWrap(True)
            body.addWidget(subtitle_lbl)
        return card, body

    def _field_label(self, text):
        label = QLabel(text)
        label.setObjectName("field_label")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        return label

    def _add_field_row(self, parent_layout, label_text, field, suffix=""):
        row = QWidget()
        row.setObjectName("settings_row")
        row.setAttribute(Qt.WA_StyledBackground, True)
        grid = QGridLayout(row)
        grid.setContentsMargins(16, 12, 16, 12)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(0)
        label = self._field_label(f"{label_text}")
        label.setMinimumWidth(186)
        grid.addWidget(label, 0, 0)
        if isinstance(field, ToggleSwitch):
            holder = QWidget()
            holder_layout = QHBoxLayout(holder)
            holder_layout.setContentsMargins(0, 0, 0, 0)
            holder_layout.addStretch()
            holder_layout.addWidget(field)
            grid.addWidget(holder, 0, 1)
        elif isinstance(field, QWidget):
            grid.addWidget(field, 0, 1)
        else:
            grid.addLayout(field, 0, 1)
        if suffix:
            suffix_lbl = QLabel(suffix)
            suffix_lbl.setObjectName("field_label")
            suffix_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            grid.addWidget(suffix_lbl, 0, 2)
        grid.setColumnStretch(1, 1)
        parent_layout.addWidget(row)

    def _apply_initial_geometry(self):
        apply_initial_window_size(
            self,
            width_ratio=0.9,
            height_ratio=0.92,
            min_width=1040,
            min_height=790,
            max_width=1360,
            max_height=980,
        )

    def _refresh_insv_mode_hint(self, mode):
        self.insv_mode_hint.setText(describe_insv_processing_mode(mode))
        self.insv_mode_hint.setStyleSheet(
            f"color:{C['text_mid']}; font-weight:600; font-family:'{UI_FONT}',sans-serif;"
        )

    def _hdr(self,layout,txt,color):
        lb=QLabel(txt)
        lb.setStyleSheet(f"color:{color};font-size:9px;letter-spacing:2px;font-weight:700;margin-top:6px;font-family:'{UI_FONT}',sans-serif;")
        layout.addRow(lb)

    def _browse(self,inp,t): p,_=QFileDialog.getOpenFileName(self,t); inp.setText(p) if p else None

    def _append_diag(self, lines):
        if isinstance(lines, str):
            lines = [lines]
        stamp = datetime.now().strftime("%H:%M:%S")
        for line in lines:
            self.diag_log.append(f"[{stamp}] {line}")
        sb = self.diag_log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_status_label(self, label, text, state):
        color = {
            "ok": C["green"],
            "warn": ACCENT,
            "error": C["red"],
        }.get(state, C["text_mid"])
        label.setText(text)
        label.setStyleSheet(f"color:{color}; font-weight:600; font-family:'{UI_FONT}',sans-serif;")

    def _sync_insv_ready_state(self):
        ready = bool(self.diag_state["ffmpeg_validated"] and self.diag_state["media_sdk_validated"])
        self.diag_state["insv_ready"] = ready
        if ready:
            self.diag_state["insv_status_text"] = "Prêt (FFmpeg + SDK)"
        elif self.ff.text().strip() or self.sdk.text().strip() or find_bundled_sdk_binary():
            self.diag_state["insv_status_text"] = "Validation FFmpeg + SDK requise"
        else:
            self.diag_state["insv_status_text"] = "Non configuré"

    def _refresh_diag_status_labels(self):
        self._sync_insv_ready_state()
        ff_txt = self.diag_state.get("ffmpeg_status_text") or ("Validé" if self.diag_state["ffmpeg_validated"] else ("Non testé" if (self.ff.text().strip() or self.ffmpeg_path) else "À détecter"))
        bundled_sdk_present = bool(find_bundled_sdk_binary())
        sdk_txt = self.diag_state.get("media_sdk_status_text") or (
            "Validé"
            if self.diag_state["media_sdk_validated"]
            else ("Non testé" if (self.sdk.text().strip() or bundled_sdk_present) else "Non configuré")
        )
        insv_txt = self.diag_state.get("insv_status_text") or "Validation FFmpeg + SDK requise"
        insv_state = "ok" if self.diag_state["insv_ready"] else ("warn" if (self.ff.text().strip() or self.sdk.text().strip() or bundled_sdk_present) else "error")
        self._set_status_label(self.ff_status, ff_txt, "ok" if self.diag_state["ffmpeg_validated"] else "warn")
        self._set_status_label(self.sdk_status, sdk_txt, "ok" if self.diag_state["media_sdk_validated"] else ("warn" if (self.sdk.text().strip() or bundled_sdk_present) else "error"))
        self._set_status_label(self.insv_status, insv_txt, insv_state)

    def _set_update_status(self, text, state="neutral"):
        color = {
            "ok": C["green"],
            "warn": ACCENT,
            "error": C["red"],
            "neutral": C["text_mid"],
        }.get(state, C["text_mid"])
        self.update_status.setText(text)
        self.update_status.setStyleSheet(
            f"color:{color}; font-size:11px; font-weight:600; font-family:'{UI_FONT}',sans-serif;"
        )

    def _check_updates_clicked(self):
        manifest_url = self.update_manifest.text().strip()
        if not manifest_url:
            show_info_message(
                self,
                "Mises à jour",
                "Renseigne d'abord l'URL d'un manifeste JSON de mise à jour.",
                icon_name="info",
                accent=False,
            )
            return
        if self._update_worker and self._update_worker.isRunning():
            return
        self.btn_check_updates.setEnabled(False)
        self._set_update_status("Vérification en cours…", "warn")
        self._update_worker = UpdateCheckWorker(APP_VERSION, manifest_url)
        self._update_worker.sig_done.connect(self._on_update_check_done)
        self._update_worker.finished.connect(self._on_update_check_finished)
        self._update_worker.start()

    def _on_update_check_done(self, result):
        if not result.get("ok"):
            self._set_update_status(result.get("error") or "Échec de vérification.", "error")
            show_info_message(
                self,
                "Mises à jour",
                result.get("error") or "Impossible de vérifier les mises à jour.",
                icon_name="alert",
                accent=True,
            )
            return
        latest = result.get("latest_version", "")
        if not result.get("has_update"):
            self._postponed_update_version = ""
            self._set_update_status(f"Version {APP_VERSION} déjà à jour.", "ok")
            show_info_message(
                self,
                "Mises à jour",
                f"Aucune nouvelle version disponible.\n\nVersion actuelle : {APP_VERSION}",
                icon_name="check",
                accent=False,
            )
            return
        download_url = result.get("download_url", "").strip()
        self._set_update_status(f"Version {latest} disponible.", "warn")
        if not download_url:
            show_info_message(
                self,
                "Mises à jour",
                "Une nouvelle version a été détectée, mais le manifeste ne fournit aucun lien de téléchargement.",
                icon_name="alert",
                accent=True,
            )
            return
        accepted = ask_confirmation(
            self,
            result.get("title") or "Nouvelle version disponible",
            build_update_prompt_message(APP_VERSION, latest, result.get("notes", "")),
            confirm_text="Télécharger",
            cancel_text="Plus tard",
            icon_name="info",
            accent=True,
        )
        if accepted:
            if open_external_url(download_url):
                self._postponed_update_version = ""
                self._set_update_status(f"Téléchargement lancé pour la version {latest}.", "ok")
            else:
                self._set_update_status("Lien détecté, mais impossible de l'ouvrir automatiquement.", "error")
                show_info_message(
                    self,
                    "Téléchargement impossible",
                    f"Ouvre ce lien manuellement :\n{download_url}",
                    icon_name="alert",
                    accent=True,
                )
        else:
            self._postponed_update_version = latest
            self._set_update_status(f"Version {latest} reportée pour plus tard.", "warn")

    def _on_update_check_finished(self):
        self.btn_check_updates.setEnabled(True)

    def _on_ffmpeg_path_changed(self, _text):
        self.diag_state["ffmpeg_validated"] = False
        self.diag_state["ffmpeg_resolved_path"] = ""
        self.diag_state["ffmpeg_status_text"] = ""
        self._refresh_diag_status_labels()

    def _on_sdk_path_changed(self, _text):
        self.diag_state["media_sdk_validated"] = False
        self.diag_state["media_sdk_resolved_path"] = ""
        self.diag_state["media_sdk_status_text"] = ""
        self._refresh_diag_status_labels()

    def _check_ffmpeg_clicked(self):
        diag = ffmpeg_diagnostic(self.ff.text().strip())
        self.diag_state["ffmpeg_validated"] = diag["ok"]
        self.diag_state["ffmpeg_resolved_path"] = diag.get("resolved_path", "") if diag["ok"] else ""
        self.diag_state["ffmpeg_status_text"] = diag["status"]
        self._set_status_label(self.ff_status, diag["status"], "ok" if diag["ok"] else "error")
        self._append_diag(diag["logs"])
        self._refresh_diag_status_labels()

    def _check_sdk_clicked(self):
        diag = sdk_diagnostic(self.sdk.text().strip())
        self.diag_state["media_sdk_validated"] = diag["ok"]
        self.diag_state["media_sdk_resolved_path"] = diag.get("resolved_path", "") if diag["ok"] else ""
        self.diag_state["media_sdk_status_text"] = "SDK embarqué détecté" if (diag["ok"] and not self.sdk.text().strip() and is_runtime_bundled_path(diag.get("resolved_path", ""))) else diag["status"]
        self._set_status_label(self.sdk_status, diag["status"], "ok" if diag["ok"] else "error")
        self._append_diag(diag["logs"])
        self._refresh_diag_status_labels()

    def _detect_sdk_clicked(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            diag = autodetect_media_sdk()
        finally:
            QApplication.restoreOverrideCursor()
        self._append_diag(diag["logs"])
        detected_path = diag.get("resolved_path", "").strip()
        if detected_path and not is_runtime_bundled_path(detected_path):
            self.sdk.setText(detected_path)
        self.diag_state["media_sdk_validated"] = diag["ok"]
        self.diag_state["media_sdk_resolved_path"] = detected_path if diag["ok"] else ""
        self.diag_state["media_sdk_status_text"] = "SDK embarqué détecté" if (diag["ok"] and not self.sdk.text().strip() and is_runtime_bundled_path(detected_path)) else diag["status"]
        self._set_status_label(self.sdk_status, diag["status"], "ok" if diag["ok"] else "error")
        self._refresh_diag_status_labels()

    def get_values(self):
        ff_path = self.ff.text().strip()
        sdk_path = self.sdk.text().strip()
        ff_changed = ff_path != self.preset.get("ffmpeg_path","").strip()
        sdk_changed = sdk_path != self.preset.get("media_sdk_path","").strip()
        diag_ff_ok = self.diag_state["ffmpeg_validated"] and not ff_changed
        diag_sdk_ok = self.diag_state["media_sdk_validated"] and not sdk_changed
        p={"road_yaw":self.ry.value(),"road_pitch":self.rp.value(),"road_roll":0,
           "road_hfov":self.rhf.value(),"road_vfov":self.rvf.value(),
           "cabin_yaw":self.cy.value(),"cabin_pitch":self.cp.value(),"cabin_roll":0,
           "cabin_hfov":self.chf.value(),"cabin_vfov":self.cvf.value(),
           "output_width":self.ow.value(),"output_height":self.oh.value(),
           "output_preset":self.output_resolution_preset.currentData() or "custom",
           "output_fps":int(self.output_fps.currentData() or 0),
           "pip_width":self.pw.value(),"pip_height":self.ph2.value(),"pip_margin":self.pm.value(),
           "pip_position":self.pip_pos_cb.currentData(),
           "auto_reframe":self.auto_rf.isChecked(),"preview_before_render":self.preview_rf.isChecked(),"auto_analysis_seconds":self.auto_secs.value(),
           "auto_sample_count":self.auto_samples.value(),"auto_cabin_search_step":self.auto_step.value(),
           "quality_mode":self.quality_mode.currentText(),"crf":self.crf.value(),"preset_encode":self.enc_p.currentText(),
           "insv_processing_mode":self.insv_mode.currentText(),
           "video_bitrate":self.bitrate.text().strip() or "12M","use_nvenc":self.nvenc.isChecked(),
           "separate_files":False,"output_date_folder":self.date_cb.isChecked(),
           "output_prefix":self.prefix.text().strip(),"gen_thumbnail":self.thumb.isChecked(),
           "auto_open_output":self.openfolder.isChecked(),"add_watermark":self.wm_cb.isChecked(),
           "watermark_path":self.wm_path.text().strip(),"watermark_opacity":self.wm_opa.value(),
           "delivery_enabled":self.delivery_enabled.isChecked(),
           "delivery_mock_mode":self.delivery_mock.isChecked(),
           "delivery_send_email":self.delivery_email.isChecked(),
           "delivery_send_sms":self.delivery_sms.isChecked(),
           "delivery_sender_name":self.delivery_sender.text().strip() or "Motorsport Academy",
           "delivery_backend_url":self.delivery_backend.text().strip(),
           "delivery_api_key":self.delivery_api_key.text().strip(),
           "delivery_link_ttl_days":self.delivery_ttl.value(),
           "theme_mode":self.theme_mode.currentData() or "dark",
           "update_auto_check":self.update_auto.isChecked(),
           "update_manifest_url":self.update_manifest.text().strip(),
           "update_postponed_version":self._postponed_update_version,
           "ffmpeg_validated":diag_ff_ok,
           "ffmpeg_resolved_path":self.diag_state["ffmpeg_resolved_path"] if diag_ff_ok else "",
           "media_sdk_validated":diag_sdk_ok,
           "media_sdk_resolved_path":(self.diag_state["media_sdk_resolved_path"] if (diag_sdk_ok and sdk_path) else ""),
           "media_sdk_path":sdk_path,"output_dir":self.outd.text().strip(),
           "ffmpeg_path":ff_path}
        return p, ff_path


# ══════════════════════════════════════════════════════════════
#  FOND ANIMÉ
# ══════════════════════════════════════════════════════════════
class BgWidget(QWidget):
    def paintEvent(self, e):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(C["bg"]))
        if CURRENT_THEME_MODE == "dark":
            g=QRadialGradient(self.width()*0.12, self.height()*0.06, self.width()*0.32)
            g.setColorAt(0, QColor(255, 122, 0, 18)); g.setColorAt(1, QColor(0,0,0,0))
            p.fillRect(self.rect(), QBrush(g))
            g2=QRadialGradient(self.width()*0.86, self.height()*0.88, self.width()*0.28)
            g2.setColorAt(0, QColor(255, 255, 255, 8)); g2.setColorAt(1, QColor(0,0,0,0))
            p.fillRect(self.rect(), QBrush(g2))
        else:
            g=QRadialGradient(self.width()*0.1, self.height()*0.08, self.width()*0.28)
            g.setColorAt(0, QColor(255, 122, 0, 12)); g.setColorAt(1, QColor(0,0,0,0))
            p.fillRect(self.rect(), QBrush(g))
            g2=QRadialGradient(self.width()*0.86, self.height()*0.9, self.width()*0.24)
            g2.setColorAt(0, QColor(21, 32, 43, 8)); g2.setColorAt(1, QColor(0,0,0,0))
            p.fillRect(self.rect(), QBrush(g2))
        p.end()

# ══════════════════════════════════════════════════════════════
#  BARRE DE STATUT BOTTOM (propre, non technique)
# ══════════════════════════════════════════════════════════════
class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("status_shell")
        self.setFixedHeight(ui_px(56))
        self.setAttribute(Qt.WA_StyledBackground, True)
        l = QHBoxLayout(self); l.setContentsMargins(ui_px(18), 0, ui_px(18), 0); l.setSpacing(ui_px(18))

        self._dot = QLabel("●")
        self._dot.setStyleSheet(f"color:{C['text_lo']}; font-size:{ui_font(10)}px; background:transparent;")

        self._msg = QLabel("Prêt")
        self._msg.setStyleSheet(
            f"color:{C['text_mid']}; font-size:{ui_font(12)}px; font-weight:600; "
            f"font-family:'{UI_FONT}',sans-serif; background:transparent;"
        )

        self._bar = QProgressBar()
        self._bar.setFixedHeight(ui_px(4))
        self._bar.setFixedWidth(ui_px(160))
        self._bar.setTextVisible(False)
        self._bar.setStyleSheet(
            f"QProgressBar{{background:{C['progress_bg']};border:none;border-radius:3px;}}"
            f"QProgressBar::chunk{{background:{ACCENT};border-radius:3px;}}"
        )
        self._bar.hide()

        self._stats = QLabel("")
        self._stats.setStyleSheet(
            f"color:{C['text_lo']}; font-size:{ui_font(11)}px; background:transparent; "
            f"font-family:'{UI_FONT}',sans-serif;"
        )

        self._brand = QLabel("© Motorsport Academy")
        self._brand.setStyleSheet(
            f"color:{C['text_lo']}; font-size:{ui_font(11)}px; background:transparent; "
            f"font-family:'{UI_FONT}',sans-serif;"
        )

        l.addWidget(self._dot)
        l.addWidget(self._msg)
        l.addWidget(self._bar)
        l.addStretch()
        l.addWidget(self._stats)
        l.addSpacing(ui_px(12))
        l.addWidget(self._brand)
        self._idle_state = None
        self._processing_state = None
        self._error_state = None

    def set_idle(self, done=0, total=0, avg_sec=None):
        state = (int(done or 0), int(total or 0), None if avg_sec is None else round(float(avg_sec), 1))
        if state == self._idle_state:
            return
        self._idle_state = state
        self._processing_state = None
        self._error_state = None
        self._dot.setStyleSheet(f"color:{C['green']}; font-size:{ui_font(10)}px; background:transparent;")
        if total > 0:
            self._msg.setText(f"{done} / {total} vidéos traitées avec succès")
        else:
            self._msg.setText("Prêt — importez des fichiers pour commencer")
        self._bar.hide()
        if avg_sec and avg_sec > 0:
            self._stats.setText(f"Moy. {avg_sec:.0f}s / vidéo")
        else:
            self._stats.setText("")

    def set_processing(self, current_name, pct_global, eta_txt=""):
        state = (str(current_name or ""), int(pct_global or 0), str(eta_txt or ""))
        if state == self._processing_state:
            return
        self._processing_state = state
        self._idle_state = None
        self._error_state = None
        self._dot.setStyleSheet(f"color:{ACCENT}; font-size:{ui_font(10)}px; background:transparent;")
        self._msg.setText(f"Traitement en cours — {current_name}")
        self._bar.show()
        self._bar.setValue(pct_global)
        self._stats.setText(f"Temps restant {eta_txt}" if eta_txt else "")

    def set_error(self, msg):
        state = str(msg or "")
        if state == self._error_state:
            return
        self._error_state = state
        self._idle_state = None
        self._processing_state = None
        self._dot.setStyleSheet(f"color:{C['red']}; font-size:{ui_font(10)}px; background:transparent;")
        self._msg.setText(f"Erreur — {msg}")
        self._bar.hide()
        self._stats.setText("")

# ══════════════════════════════════════════════════════════════
#  FENÊTRE PRINCIPALE
# ══════════════════════════════════════════════════════════════
class PipelineWindow(QMainWindow):
    PRESET_FILE = "pipeline_preset_v1_1_stream.json"

    def __init__(self):
        super().__init__()
        self.db     = Database()
        self.preset = self._load_preset()
        apply_theme_mode(self.preset.get("theme_mode", "dark"))
        self.setWindowIcon(app_icon())
        self.ffmpeg = find_ffmpeg(self.preset.get("ffmpeg_path",""))
        self._sw={}; self._rb={}; self._rfb={}; self._db_btn={}; self._dlv_btn={}; self._delivery_recipients={}; self._eta={}; self._elapsed_done={}; self._stage={}
        self._session_rows = []
        self._session_name_by_sid = {}
        self._table_done_count = 0
        self._table_total_count = 0
        self._launch_state_active = None
        self.manager  = None
        self._delivery_queue = []
        self._delivery_worker = None
        self._sdk_autodetect_worker = None
        self._update_worker = None
        self._preview_warmup_worker = None
        self._auto_import_timer = QTimer(self)
        self._auto_import_timer.setInterval(AUTO_IMPORT_SCAN_INTERVAL_MS)
        self._auto_import_timer.timeout.connect(self._poll_auto_import_sources)
        self._auto_import_seen_paths = set()
        self._auto_import_busy = False
        self._auto_import_input_dir = app_input_dir()
        self._auto_import_active_mount = ""
        self._preserve_window_state_on_setup = False
        self._theme_restore_geometry = None
        self._preview_warmup_timer = QTimer(self)
        self._preview_warmup_timer.setSingleShot(True)
        self._preview_warmup_timer.timeout.connect(self._maybe_warmup_preview_cache)
        self.log_dlg  = LogDialog(self)
        self._setup_ui()
        self._init_notifications()
        self._setup_shortcuts()
        self._check_ffmpeg()
        self._check_sdk()
        self._refresh_table()
        self._log(f"══  {APP_NAME} {APP_VERSION}  ══")
        self._init_auto_import()
        QTimer.singleShot(250, self._maybe_autodetect_sdk_on_startup)
        QTimer.singleShot(900, self._maybe_check_updates_on_startup)

    # ── SETUP ─────────────────────────────────────────────────
    def _setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1180, 760)
        if not getattr(self, "_preserve_window_state_on_setup", False):
            apply_initial_window_size(
                self,
                width_ratio=0.96,
                height_ratio=0.92,
                min_width=1180,
                min_height=760,
                max_width=1760,
                max_height=1160,
            )
        self.setStyleSheet(STYLESHEET)

        bg = BgWidget(); self.setCentralWidget(bg)
        root = QHBoxLayout(bg)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        root.addWidget(self._build_side_rail())

        content = QWidget()
        content.setObjectName("content_shell")
        content.setAttribute(Qt.WA_StyledBackground, True)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        content_layout.addWidget(self._build_header())
        content_layout.addWidget(self._build_overview_strip())
        content_layout.addWidget(self._build_table(), stretch=1)
        content_layout.addWidget(self._build_status_bar())
        root.addWidget(content, stretch=1)
        self._update_header_compact_mode()

    def _init_notifications(self):
        self.tray_icon = None
        try:
            if QSystemTrayIcon.isSystemTrayAvailable():
                icon = app_icon()
                if icon.isNull():
                    icon = self.style().standardIcon(QStyle.SP_MediaPlay)
                self.tray_icon = QSystemTrayIcon(icon, self)
                self.tray_icon.setToolTip(APP_NAME)
                self.tray_icon.show()
        except Exception:
            self.tray_icon = None

    def _play_chime(self):
        try:
            app = QApplication.instance()
            if app:
                app.beep()
        except Exception:
            pass
        if sys.platform == "darwin":
            for sound in [
                "/System/Library/Sounds/Glass.aiff",
                "/System/Library/Sounds/Hero.aiff",
                "/System/Library/Sounds/Ping.aiff",
            ]:
                try:
                    if os.path.exists(sound):
                        subprocess.Popen(["afplay", sound], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
                except Exception:
                    continue

    def _play_preview_chime(self):
        try:
            app = QApplication.instance()
            if app:
                app.beep()
        except Exception:
            pass
        if sys.platform == "darwin":
            try:
                sound = "/System/Library/Sounds/Submarine.aiff"
                if os.path.exists(sound):
                    subprocess.Popen(["afplay", sound], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

    def _notify_export_done(self, title, message):
        try:
            if self.tray_icon and self.tray_icon.supportsMessages():
                self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)
                return
        except Exception:
            pass
        if sys.platform == "darwin":
            try:
                script = f'display notification {json.dumps(message)} with title {json.dumps(title)}'
                subprocess.Popen(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass

    def _build_side_rail(self):
        rail = QWidget()
        rail.setObjectName("side_shell")
        rail.setAttribute(Qt.WA_StyledBackground, True)
        rail.setFixedWidth(ui_px(92))
        l = QVBoxLayout(rail)
        l.setContentsMargins(ui_px(12), ui_px(28), ui_px(12), ui_px(20))
        l.setSpacing(ui_px(16))

        logo_wrap = QWidget()
        logo_layout = QVBoxLayout(logo_wrap)
        logo_layout.setContentsMargins(0, ui_px(6), 0, ui_px(10))
        logo_layout.setSpacing(0)
        logo_icon = brand_logo_widget(ui_px(54), ui_px(24), color=C["logo_color"])
        logo_layout.addWidget(logo_icon)
        l.addWidget(logo_wrap, alignment=Qt.AlignCenter)

        l.addSpacing(ui_px(4))

        self.btn_cfg = self._tbtn("settings", "Réglages", self._open_settings)
        self.btn_log = self._tbtn("list", "Journal", self._open_logs)
        self.btn_clr = self._tbtn("trash", "Vider la liste", self._clear_all)
        self.btn_pause = self._tbtn("pause", "Pause / Reprise (Ctrl+P)", self._toggle_pause_resume)
        self.btn_stop = self._tbtn("stop", "Arrêter le batch (Ctrl+Shift+P)", self._stop_batch)

        for btn in [self.btn_cfg, self.btn_log, self.btn_clr]:
            l.addWidget(btn, alignment=Qt.AlignCenter)

        l.addStretch()

        for btn in [self.btn_pause, self.btn_stop]:
            l.addWidget(btn, alignment=Qt.AlignCenter)

        tag = QLabel("V1.1")
        tag.setStyleSheet(
            f"color:{C['text_lo']}; font-size:{ui_font(10)}px; font-weight:700; letter-spacing:1.6px; background:transparent;"
        )
        l.addWidget(tag, alignment=Qt.AlignCenter)
        return rail

    # ── HEADER ────────────────────────────────────────────────
    def _build_header(self):
        card = QFrame()
        card.setObjectName("hero_shell")
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setMinimumHeight(178)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(22)

        left = QVBoxLayout()
        left.setSpacing(10)

        eyebrow = QLabel("TABLEAU DE BORD")
        eyebrow.setObjectName("hero_eyebrow")
        self.hero_title = QLabel("Traitement Vidéo Motorsport Academy")
        self.hero_title.setObjectName("hero_title")
        self.hero_subtitle = QLabel("Interface de traitement, export et livraison des vidéos Motorsport Academy.")
        self.hero_subtitle.setObjectName("hero_subtitle")
        self.hero_subtitle.setWordWrap(True)

        chips = QHBoxLayout()
        chips.setSpacing(8)
        self.lbl_status = QLabel()
        self.lbl_ffmpeg = QLabel()
        self.lbl_sdk = QLabel()
        self.lbl_count = QLabel()
        for chip in [self.lbl_status, self.lbl_ffmpeg, self.lbl_sdk, self.lbl_count]:
            chip.setObjectName("chip_label")
            chips.addWidget(chip)
        chips.addStretch()

        left.addWidget(eyebrow)
        left.addWidget(self.hero_title)
        left.addWidget(self.hero_subtitle)
        left.addLayout(chips)

        right = QVBoxLayout()
        right.setSpacing(12)
        right.setAlignment(Qt.AlignTop)

        self.theme_toggle_shell = self._build_theme_toggle()
        self.btn_preset = self._ghost("compass", "Preset", self._apply_preset_to_selection)
        self.btn_import = self._ghost("plus", "Importer", self._import_files)
        self.btn_launch = QPushButton("LANCER")
        self.btn_launch.clicked.connect(self._launch_batch)
        self.btn_launch.setFixedHeight(ui_px(48))
        self.btn_launch.setMinimumWidth(ui_px(180))
        self.btn_launch.setAutoDefault(False)
        self.btn_launch.setDefault(False)
        self.btn_launch.setFlat(False)
        self.btn_launch.setAttribute(Qt.WA_StyledBackground, True)
        self.btn_launch.setIcon(QIcon())
        self._set_launch_state(False, clickable=True, force=True)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addWidget(self.theme_toggle_shell)
        actions.addWidget(self.btn_preset)
        actions.addWidget(self.btn_import)
        right.addLayout(actions)
        right.addStretch()
        right.addWidget(self.btn_launch, alignment=Qt.AlignRight)

        layout.addLayout(left, stretch=1)
        layout.addLayout(right)
        self._set_global_status("ready")
        self._set_chip_state(self.lbl_ffmpeg, "FFmpeg …", "neutral")
        self._set_chip_state(self.lbl_sdk, "INSV …", "neutral")
        self._set_chip_state(self.lbl_count, "0 fichier", "neutral")
        return card

    def _build_overview_strip(self):
        wrap = QWidget()
        row = QHBoxLayout(wrap)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(14)

        q_card, self.ov_queue_value, self.ov_queue_meta = self._make_summary_card("QUEUE", "0", "Aucune session")
        d_card, self.ov_delivery_value, self.ov_delivery_meta = self._make_summary_card("LIVRAISON", "Manuel", "Envoi après export désactivé")
        m_card, self.ov_mode_value, self.ov_mode_meta = self._make_summary_card("MODE INSV", resolve_insv_processing_mode(self.preset), describe_insv_processing_mode(resolve_insv_processing_mode(self.preset)))

        row.addWidget(q_card, 2)
        row.addWidget(d_card, 2)
        row.addWidget(m_card, 3)
        return wrap

    def _make_summary_card(self, label_text, value_text, meta_text):
        card = QFrame()
        card.setObjectName("summary_card")
        card.setAttribute(Qt.WA_StyledBackground, True)
        l = QVBoxLayout(card)
        l.setContentsMargins(ui_px(18), ui_px(16), ui_px(18), ui_px(16))
        l.setSpacing(ui_px(8))

        label = QLabel(label_text)
        label.setObjectName("summary_label")
        value = QLabel(value_text)
        value.setObjectName("summary_value")
        meta = QLabel(meta_text)
        meta.setStyleSheet(
            f"color:{C['text_mid']}; font-size:{ui_font(11)}px; font-weight:600; background:transparent;"
        )
        meta.setWordWrap(True)

        l.addWidget(label)
        l.addWidget(value)
        l.addWidget(meta)
        l.addStretch()
        return card, value, meta

    def _setup_shortcuts(self):
        shortcuts = [
            ("Space", self._launch_or_resume_shortcut),
            ("Ctrl+I", self._import_files),
            ("Ctrl+L", self._open_logs),
            ("Ctrl+,", self._open_settings),
            ("Delete", self._delete_selected_shortcut),
            ("Backspace", self._delete_selected_shortcut),
            ("Ctrl+Up", self._move_selected_up),
            ("Ctrl+Down", self._move_selected_down),
            ("Ctrl+P", self._toggle_pause_resume),
            ("Ctrl+Shift+P", self._stop_batch),
            ("F1", self._show_shortcuts_help),
        ]
        self._shortcuts = []
        for seq, fn in shortcuts:
            sc = QShortcut(QKeySequence(seq), self)
            sc.activated.connect(fn)
            self._shortcuts.append(sc)

    def _launch_or_resume_shortcut(self):
        if self.manager and self.manager.paused:
            self._toggle_pause_resume()
        else:
            self._launch_batch()

    def _selected_sid(self):
        row = self.table.currentRow()
        sessions = self._session_rows or self.db.get_all()
        if row < 0 or row >= len(sessions):
            return None
        return sessions[row][0]

    def _selected_sids(self):
        rows = sorted({idx.row() for idx in self.table.selectionModel().selectedRows()})
        sessions = self._session_rows or self.db.get_all()
        sids = []
        for row in rows:
            if 0 <= row < len(sessions):
                sids.append(sessions[row][0])
        return sids

    def _delete_selected_shortcut(self):
        sid = self._selected_sid()
        if sid is not None:
            self._delete_session(sid)

    def _move_selected_up(self):
        sid = self._selected_sid()
        if sid is None:
            return
        if self.manager and (self.manager.running or self.manager.paused):
            self._log(f"[{self._ts()}] ⚠ Réorganisation bloquée pendant le batch")
            return
        if self.db.move_session(sid, -1):
            self._refresh_table()
            row = max(0, self.table.currentRow()-1)
            self.table.selectRow(row)
            self._log(f"[{self._ts()}] ↑ Session déplacée")

    def _move_selected_down(self):
        sid = self._selected_sid()
        if sid is None:
            return
        if self.manager and (self.manager.running or self.manager.paused):
            self._log(f"[{self._ts()}] ⚠ Réorganisation bloquée pendant le batch")
            return
        if self.db.move_session(sid, 1):
            self._refresh_table()
            row = min(self.table.rowCount()-1, self.table.currentRow()+1)
            self.table.selectRow(row)
            self._log(f"[{self._ts()}] ↓ Session déplacée")

    def _toggle_pause_resume(self):
        if not self.manager:
            return
        if self.manager.running:
            self.manager.request_pause()
            self.btn_launch.setText("PAUSE APRÈS CET EXPORT")
            self.btn_launch.setIcon(QIcon())
            self.status_bar.set_processing("Pause demandée…", 0)
            self._log(f"[{self._ts()}] ⏸ Pause demandée après l'export en cours")
        elif self.manager.paused:
            self.manager.resume()
            self.btn_launch.setText("EN COURS…")
            self.btn_launch.setIcon(QIcon())
            self._set_global_status("processing")
            self._log(f"[{self._ts()}] ▶ Batch repris")

    def _stop_batch(self):
        if not self.manager or (not self.manager.running and not self.manager.paused):
            return
        if not ask_confirmation(
            self,
            "Arrêter l'export ?",
            "Le rendu en cours sera arrêté et le batch restant ne sera pas traité.",
            confirm_text="Arrêter",
            cancel_text="Annuler",
            icon_name="alert",
            accent=True,
        ):
            return
        try:
            self.manager.stop()
        except Exception:
            pass
        self.btn_launch.setText("LANCER")
        self._set_global_status("ready")
        self.status_bar.set_error("Export arrêté")
        self._log(f"[{self._ts()}] ⏹ Batch arrêté manuellement")
        self._refresh_table()

    def _show_shortcuts_help(self):
        txt = (
            "Fenêtre principale\n"
            "Espace : lancer le batch / reprendre\n"
            "Ctrl+I : importer des fichiers\n"
            "Ctrl+L : ouvrir le journal\n"
            "Ctrl+, : ouvrir les réglages\n"
            "Ctrl/Cmd + clic : sélectionner plusieurs sessions\n"
            "Delete / Backspace : supprimer la session sélectionnée\n"
            "Ctrl+↑ / Ctrl+↓ : déplacer la session sélectionnée\n"
            "Ctrl+P : pause / reprise du batch\n"
            "Ctrl+Shift+P : arrêter l'export en cours et le batch\n"
            "F1 : ouvrir cette aide\n\n"
            "Popup de recadrage\n"
            "Espace : valider\n"
            "R : réinitialiser l'auto-cadrage\n"
            "Flèches : ajuster le fond\n"
            "Alt + Flèches : ajuster le PiP\n"
            "Shift : déplacement plus large"
        )
        show_info_message(self, "Raccourcis clavier", txt, icon_name="info", accent=False)

    def _on_rows_reordered(self, ordered_ids):
        if self.manager and (self.manager.running or self.manager.paused):
            self._log(f"[{self._ts()}] ⚠ Réorganisation bloquée pendant le batch")
            self._refresh_table()
            return
        if self.db.set_order(ordered_ids):
            self._refresh_table()
            self._log(f"[{self._ts()}] ↕ File d'attente réorganisée")
        else:
            self._refresh_table()

    def _make_logo(self):
        return brand_logo_widget(ui_px(54), ui_px(24), color=C["logo_color"])

    def _tbtn(self, icon_name, tip, fn):
        b = QPushButton()
        b.setObjectName("btn_tool")
        b.setToolTip(tip)
        b.setFixedSize(ui_px(46), ui_px(46))
        apply_button_icon(b, icon_name, color=C["text_mid"], size=ui_px(16))
        b.clicked.connect(fn)
        return b

    def _ghost(self, icon_name, txt, fn):
        b = QPushButton(txt)
        b.setObjectName("btn_ghost")
        b.setFixedHeight(ui_px(42))
        apply_button_icon(b, icon_name, color=C["text_mid"], size=ui_px(16))
        b.clicked.connect(fn)
        return b

    def _build_theme_toggle(self):
        shell = QFrame()
        shell.setObjectName("theme_toggle_shell")
        shell.setAttribute(Qt.WA_StyledBackground, True)
        shell.setFixedHeight(ui_px(42))

        mode = normalize_theme_mode(self.preset.get("theme_mode", "dark"))
        row = QHBoxLayout(shell)
        row.setContentsMargins(ui_px(12), 0, ui_px(12), 0)
        row.setSpacing(ui_px(8))

        sun = icon_label("sun", color=ACCENT if mode == "light" else C["text_lo"], size=ui_px(15))
        sun.setObjectName("theme_toggle_icon")
        moon = icon_label("moon", color=ACCENT if mode == "dark" else C["text_lo"], size=ui_px(15))
        moon.setObjectName("theme_toggle_icon")

        self.theme_switch = ToggleSwitch(checked=(mode == "dark"), parent=shell)
        self.theme_switch.toggled.connect(self._toggle_theme_mode)

        row.addWidget(sun)
        row.addWidget(self.theme_switch)
        row.addWidget(moon)
        return shell

    def _set_chip_state(self, label, text, tone="neutral"):
        tones = {
            "neutral": (C["sand"], C["chip_bg"], C["chip_border"]),
            "success": (C["green"], "rgba(65,211,140,16)", "rgba(65,211,140,34)"),
            "warning": (ACCENT, "rgba(255,122,0,14)", "rgba(255,122,0,34)"),
            "error": (C["red"], "rgba(255,105,105,14)", "rgba(255,105,105,34)"),
            "processing": (C["blue"], "rgba(135,184,255,14)", "rgba(135,184,255,34)"),
        }
        fg, bg, border = tones.get(tone, tones["neutral"])
        label.setText(text)
        label.setAttribute(Qt.WA_StyledBackground, True)
        label.setMinimumHeight(ui_px(34))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            f"color:{fg}; background:{bg}; border:1px solid {border};"
            f"border-radius:{ui_radius(15)}px; padding:{ui_px(7)}px {ui_px(12)}px;"
            f"font-size:{ui_font(11)}px; font-weight:700;"
        )

    def _launch_button_style(self, active):
        radius = ui_radius(18)
        padding_x = ui_px(24)
        font_size = ui_font(13)
        if active:
            return f"""
QPushButton {{
    background-color: #ff8a1a;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #ffbe72, stop:0.52 #ff8a1a, stop:1 #e16400);
    color: #140c04;
    border: 1px solid rgba(255,244,230,48);
    border-radius: {radius}px;
    padding: 0 {padding_x}px;
    font-size: {font_size}px;
    font-weight: 800;
    letter-spacing: 1.5px;
}}
QPushButton:hover {{
    background-color: #ff9426;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #ffc98b, stop:1 #ff7a00);
}}
QPushButton:pressed {{
    background-color: #c86010;
    background: #c86010;
}}
QPushButton:disabled {{
    background-color: {C['launch_disabled_bg']};
    background: {C['launch_disabled_bg']};
    color: {C['launch_disabled_text']};
    border: 1px solid {C['launch_disabled_border']};
}}
"""
        return f"""
QPushButton {{
    background-color: {C['launch_inactive_bg']};
    background: {C['launch_inactive_bg']};
    color: {C['launch_inactive_text']};
    border: 1px solid {C['launch_inactive_border']};
    border-radius: {radius}px;
    padding: 0 {padding_x}px;
    font-size: {font_size}px;
    font-weight: 700;
    letter-spacing: 1.5px;
}}
QPushButton:hover {{
    background-color: {C['launch_inactive_bg']};
    background: {C['launch_inactive_bg']};
    color: {C['launch_inactive_text']};
    border: 1px solid {C['launch_inactive_border']};
}}
QPushButton:pressed {{
    background-color: {C['launch_inactive_bg']};
    background: {C['launch_inactive_bg']};
}}
QPushButton:disabled {{
    background-color: {C['launch_disabled_bg']};
    background: {C['launch_disabled_bg']};
    color: {C['launch_disabled_text']};
    border: 1px solid {C['launch_disabled_border']};
}}
"""

    def _toggle_theme_mode(self, checked):
        self._set_theme_mode("dark" if checked else "light")

    def _set_theme_mode(self, mode):
        mode = normalize_theme_mode(mode)
        previous = normalize_theme_mode(self.preset.get("theme_mode", "dark"))
        if mode == previous:
            return
        self._theme_restore_fullscreen = self.isFullScreen()
        self._theme_restore_maximized = (not self.isFullScreen()) and self.isMaximized()
        self._theme_restore_geometry = QRect(self.geometry())
        self.preset["theme_mode"] = mode
        self._save_preset()
        self._animate_theme_transition(mode)

    def _create_theme_transition_overlay(self):
        pixmap = self.grab()
        overlay = QWidget(self)
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        overlay.setAttribute(Qt.WA_StyledBackground, False)
        overlay.setGeometry(self.rect())

        layout = QVBoxLayout(overlay)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QLabel(overlay)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setGeometry(overlay.rect())
        layout.addWidget(label)

        opacity = QGraphicsOpacityEffect(overlay)
        opacity.setOpacity(1.0)
        overlay.setGraphicsEffect(opacity)

        blur = QGraphicsBlurEffect(label)
        blur.setBlurRadius(0.0)
        label.setGraphicsEffect(blur)

        overlay._snapshot_label = label
        overlay._opacity_effect = opacity
        overlay._blur_effect = blur
        overlay.show()
        overlay.raise_()
        return overlay

    def _animate_theme_transition(self, mode):
        mode = normalize_theme_mode(mode)
        try:
            if getattr(self, "_theme_transition_running", False):
                return
            self._theme_transition_running = True
            overlay = self._create_theme_transition_overlay()
            self._theme_overlay = overlay

            apply_theme_mode(mode)
            self._rebuild_after_theme_change()
            overlay.raise_()

            fade = QPropertyAnimation(overlay._opacity_effect, b"opacity", overlay)
            fade.setDuration(220)
            fade.setStartValue(1.0)
            fade.setEndValue(0.0)
            fade.setEasingCurve(QEasingCurve.OutCubic)
            self._theme_fade_out = fade

            blur_anim = QPropertyAnimation(overlay._blur_effect, b"blurRadius", overlay)
            blur_anim.setDuration(220)
            blur_anim.setStartValue(0.0)
            blur_anim.setEndValue(6.0)
            blur_anim.setEasingCurve(QEasingCurve.OutQuad)
            self._theme_blur_anim = blur_anim

            def _finish_fade():
                try:
                    overlay.hide()
                    overlay.deleteLater()
                finally:
                    self._theme_overlay = None
                    self._theme_transition_running = False

            fade.finished.connect(_finish_fade)
            fade.start()
            blur_anim.start()
        except Exception:
            self._theme_transition_running = False
            overlay = getattr(self, "_theme_overlay", None)
            if overlay is not None:
                try:
                    overlay.hide()
                    overlay.deleteLater()
                except Exception:
                    pass
                self._theme_overlay = None
            apply_theme_mode(mode)
            self._rebuild_after_theme_change()

    def _set_launch_state(self, active, clickable=True, force=False):
        active = bool(active)
        clickable = bool(clickable)
        if self._launch_state_active == active and not force and self.btn_launch.isEnabled() == clickable:
            return
        self._launch_state_active = active
        if active:
            self.btn_launch.setObjectName("btn_launch_active")
        else:
            self.btn_launch.setObjectName("btn_launch_inactive")
        self.btn_launch.setEnabled(clickable)
        self.btn_launch.setIcon(QIcon())
        self.btn_launch.setAutoDefault(False)
        self.btn_launch.setDefault(False)
        self.btn_launch.setFlat(False)
        self.btn_launch.setStyleSheet(self._launch_button_style(active))
        self.btn_launch.style().unpolish(self.btn_launch)
        self.btn_launch.style().polish(self.btn_launch)
        self.btn_launch.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        overlay = getattr(self, "_theme_overlay", None)
        if overlay is not None:
            overlay.setGeometry(self.rect())
        self._update_header_compact_mode()

    def _update_header_compact_mode(self):
        width = self.width()
        compact = width < 1440
        tighter = width < 1280
        self.lbl_count.setVisible(not compact)
        self.lbl_ffmpeg.setVisible(not tighter or width > 1180)
        self.lbl_sdk.setVisible(not tighter or width > 1220)
        self.hero_subtitle.setVisible(not tighter)
        self.theme_toggle_shell.setVisible(width >= 1080)
        self.btn_preset.setText("" if tighter else "Preset")
        self.btn_import.setText("" if tighter else "Importer")
        self.btn_launch.setMinimumWidth(ui_px(152 if tighter else 180))

    def _refresh_overview_cards(self):
        total = int(self._table_total_count or 0)
        done = int(self._table_done_count or 0)
        wait = max(0, total - done)
        self.ov_queue_value.setText(str(total))
        self.ov_queue_meta.setText(f"{wait} en attente · {done} terminé(s)")

        if self.preset.get("delivery_enabled"):
            delivery_value = "Automatique"
            delivery_meta = "Simulation Stream" if self.preset.get("delivery_mock_mode") else "Backend actif"
        else:
            delivery_value = "Manuel"
            delivery_meta = "Envoi client désactivé"
        self.ov_delivery_value.setText(delivery_value)
        self.ov_delivery_meta.setText(delivery_meta)

        insv_mode = resolve_insv_processing_mode(self.preset)
        self.ov_mode_value.setText(insv_mode)
        self.ov_mode_meta.setText(describe_insv_processing_mode(insv_mode))

    def _init_auto_import(self):
        self._auto_import_input_dir = app_input_dir(ensure=True)
        self._auto_import_timer.start()
        self._log(f"[{self._ts()}] 📥 Dossier input surveillé : {self._auto_import_input_dir}")
        QTimer.singleShot(800, self._poll_auto_import_sources)

    def _poll_auto_import_sources(self):
        if self._auto_import_busy:
            return
        self._auto_import_busy = True
        try:
            self._transfer_camera_media_to_input()
            self._import_new_files_from_input_dir()
        finally:
            self._auto_import_busy = False

    def _transfer_camera_media_to_input(self):
        mount_root = find_named_volume_mount(AUTO_IMPORT_VOLUME_NAME)
        if not mount_root:
            self._auto_import_active_mount = ""
            return
        if mount_root != self._auto_import_active_mount:
            self._auto_import_active_mount = mount_root
            self._log(f"[{self._ts()}] 📷 Volume détecté : {AUTO_IMPORT_VOLUME_NAME}")
        dcim_dir = find_dcim_dir(mount_root)
        if not dcim_dir or not iter_media_files(dcim_dir):
            return
        try:
            moved_files = move_media_tree_to_input(dcim_dir, self._auto_import_input_dir)
        except Exception as exc:
            self._log(f"[{self._ts()}] ⚠ Transfert automatique impossible — {exc}")
            return
        if moved_files:
            count = len(moved_files)
            label = "fichier" if count == 1 else "fichiers"
            self._log(f"[{self._ts()}] ⇢ {count} {label} déplacé(s) depuis DCIM vers input")

    def _import_new_files_from_input_dir(self):
        current_files = iter_media_files(self._auto_import_input_dir)
        current_keys = {normalized_path_key(path): path for path in current_files}
        removed_keys = self._auto_import_seen_paths - set(current_keys.keys())
        if removed_keys:
            self._auto_import_seen_paths.difference_update(removed_keys)
        new_files = [path for key, path in current_keys.items() if key not in self._auto_import_seen_paths]
        if not new_files:
            return
        if self.manager and (self.manager.running or self.manager.paused):
            return
        stable_files = [path for path in new_files if is_path_stable(path)]
        if not stable_files:
            return
        inserted_rows = self._import_files_from_drop(stable_files, quiet_if_processing=True, source_label="input")
        self._auto_import_seen_paths.update(normalized_path_key(path) for path in stable_files)
        if inserted_rows:
            self._log(f"[{self._ts()}] ✓ Import automatique depuis input terminé")

    # ── TABLE ─────────────────────────────────────────────────
    def _build_table(self):
        container = QWidget()
        container.setObjectName("table_shell")
        container.setAttribute(Qt.WA_StyledBackground, True)
        l = QVBoxLayout(container); l.setContentsMargins(14,14,14,14); l.setSpacing(0)

        self.table = QueueTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["", "FICHIER SOURCE", "LIVRAISON", "RECADRAGE", "STATUT", "", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet(
            f"QTableWidget{{background:transparent;border:none;border-radius:{ui_radius(14)}px;}}"
            "QTableWidget::item{background:transparent;border:none;}"
            f"QTableWidget::item:selected{{background:{C['table_select_bg']};}}"
            "QHeaderView{background:transparent;border:none;}"
            "QHeaderView::section{background:transparent;border:none;"
            f"border-bottom:1px solid {C['header_border_soft']};color:{C['text_lo']};"
            f"font-size:{ui_font(10)}px;letter-spacing:2px;font-weight:700;padding:0 {ui_px(14)}px;height:{ui_px(42)}px;}}"
        )

        hh = self.table.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hh.setSectionResizeMode(0, QHeaderView.Fixed)   # numéro
        hh.setSectionResizeMode(1, QHeaderView.Stretch)  # fichier
        hh.setSectionResizeMode(2, QHeaderView.Fixed)   # livraison
        hh.setSectionResizeMode(3, QHeaderView.Fixed)   # recadrage
        hh.setSectionResizeMode(4, QHeaderView.Fixed)   # statut
        hh.setSectionResizeMode(5, QHeaderView.Fixed)   # retry
        hh.setSectionResizeMode(6, QHeaderView.Fixed)   # delete
        self.table.setColumnWidth(0, ui_px(52))
        self.table.setColumnWidth(2, ui_px(270))
        self.table.setColumnWidth(3, ui_px(190))
        self.table.setColumnWidth(4, ui_px(300))
        self.table.setColumnWidth(5, ui_px(116))
        self.table.setColumnWidth(6, ui_px(48))
        self.table.verticalHeader().setDefaultSectionSize(ui_px(66))
        self.table.files_dropped.connect(self._import_files_from_drop)
        self.table.itemSelectionChanged.connect(self._schedule_preview_warmup)
        l.addWidget(self.table)
        return container

    # ── STATUS BAR ────────────────────────────────────────────
    def _build_status_bar(self):
        self.status_bar = StatusBar()
        return self.status_bar

    # ── REFRESH TABLE ─────────────────────────────────────────
    def _refresh_table(self):
        sessions = self.db.get_all()
        self._session_rows = list(sessions)
        self._session_name_by_sid = {row[0]: row[1] for row in sessions}
        old_widget_maps = [self._sw, self._rb, self._rfb, self._db_btn, self._dlv_btn]
        stale_widgets = []
        for widget_map in old_widget_maps:
            stale_widgets.extend(widget_map.values())
            widget_map.clear()

        self.table.setUpdatesEnabled(False)
        try:
            self.table.clearContents()
            self.table.setRowCount(len(sessions))

            for widget in stale_widgets:
                try:
                    widget.hide()
                    widget.setParent(None)
                    widget.deleteLater()
                except Exception:
                    pass

            for row, (sid, fname, _pax_json, delivery_recipients_json, delivery_status, delivery_result_json, reframe_name, reframe_payload_json, status, pct, err, out_json) in enumerate(sessions):
                try:
                    recipients = normalize_delivery_recipients(json.loads(delivery_recipients_json or "[]"))
                except Exception:
                    recipients = []
                self._delivery_recipients[sid] = recipients

                def set_item(col, text="", align=Qt.AlignLeft | Qt.AlignVCenter, color=None):
                    it = QTableWidgetItem(text)
                    it.setTextAlignment(align)
                    it.setBackground(QBrush(QColor(0, 0, 0, 0)))
                    it.setForeground(QBrush(QColor(color or C['text_hi'])))
                    self.table.setItem(row, col, it)
                    return it

                # Col 0 — numéro
                n = set_item(0, f"{row+1:02d}", Qt.AlignCenter, C["text_lo"])
                n.setData(Qt.UserRole, sid)

                # Col 1 — fichier
                set_item(1, fname)

                # Col 2 — livraison client
                dlv_btn = DeliveryRecipientsBtn()
                dlv_btn.clicked.connect(lambda _, s=sid: self._edit_delivery_recipients(s))
                dlv_btn.set_delivery(recipients, delivery_status)
                self._dlv_btn[sid] = dlv_btn
                self.table.setCellWidget(row, 2, dlv_btn)

                # Col 3 — preset recadrage
                rfb = ReframePresetBtn()
                rfb.clicked.connect(lambda _, s=sid: self._apply_preset_to_sessions([s]))
                rfb.set_preset(reframe_name)
                self._rfb[sid] = rfb
                self.table.setCellWidget(row, 3, rfb)

                # Col 4 — statut
                sw = StatusWidget(status)
                if status == Status.DONE and sid in self._elapsed_done:
                    extra_text = format_elapsed_label(self._elapsed_done.get(sid, 0))
                elif status == Status.PROCESSING:
                    extra_text = self._stage.get(sid, "")
                else:
                    extra_text = ""
                sw.set_status(status, pct, extra_text)
                self._sw[sid] = sw
                self.table.setCellWidget(row, 4, sw)

                # Col 5 — retry si erreur
                if status == Status.ERROR:
                    rb = QPushButton("Relancer")
                    rb.setObjectName("btn_retry")
                    rb.setToolTip(err)
                    apply_button_icon(rb, "retry", color=C["red"], size=ui_px(14))
                    rb.clicked.connect(lambda _, s=sid: self._retry(s))
                    self._rb[sid] = rb
                    self.table.setCellWidget(row, 5, rb)
                else:
                    set_item(5, "")

                # Col 6 — supprimer
                db_btn = QPushButton()
                db_btn.setObjectName("btn_del")
                db_btn.setToolTip("Supprimer de la liste")
                apply_button_icon(db_btn, "close", color=C["text_lo"], size=ui_px(14))
                db_btn.clicked.connect(lambda _, s=sid: self._delete_session(s))
                self._db_btn[sid] = db_btn
                self.table.setCellWidget(row, 6, db_btn)
        finally:
            self.table.setUpdatesEnabled(True)
            self.table.viewport().update()

        # Compteurs
        done   = sum(1 for s in sessions if s[8]==Status.DONE)
        errors = sum(1 for s in sessions if s[8]==Status.ERROR)
        wait   = sum(1 for s in sessions if s[8]==Status.WAITING)
        total  = len(sessions)
        self._table_done_count = done
        self._table_total_count = total
        file_label = "fichier" if total == 1 else "fichiers"
        self._set_chip_state(self.lbl_count, f"{total} {file_label} · {done} ✓ · {errors} ✕ · {wait} attente", "neutral")
        self._refresh_overview_cards()

        # État du bouton launch
        is_running = bool(self.manager and self.manager.running)
        not_processing = not is_running
        self._set_launch_state(total > 0 and not_processing, clickable=not is_running, force=True)

        # Status bar
        done_t, total_sec = self.db.get_stats_today()
        avg = total_sec/done_t if done_t > 0 else None
        if not (self.manager and self.manager.running):
            self.status_bar.set_idle(done, total, avg)
            self._schedule_preview_warmup()

    # ── ACTIONS ──────────────────────────────────────────────
    def _import_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Importer des vidéos", "",
            "Vidéos (*.mp4 *.mov *.insv *.mkv);;Tous (*.*)")
        if not files: return
        self._import_files_from_drop(files)

    def _import_files_from_drop(self, files, quiet_if_processing=False, source_label=""):
        valid_files = []
        seen = set()
        existing_keys = self.db.existing_filepath_keys()
        for path in files or []:
            if not path:
                continue
            norm = normalized_path_key(path)
            if norm in seen:
                continue
            seen.add(norm)
            if not os.path.isfile(path):
                continue
            if Path(path).suffix.lower() not in QUEUE_DROP_EXTENSIONS:
                continue
            if norm in existing_keys:
                continue
            valid_files.append(path)
        if not valid_files:
            return []
        if self.manager and (self.manager.running or self.manager.paused):
            if not quiet_if_processing:
                self._log(f"[{self._ts()}] ⚠ Import ignoré pendant un batch en cours")
            return []
        inserted_rows = self.db.add_sessions(valid_files)
        for sid, _filename, filepath in inserted_rows:
            self._delivery_recipients[sid] = []
            prefix = "＋"
            if source_label:
                prefix = f"＋ [{source_label}]"
            self._log(f"[{self._ts()}] {prefix} {Path(filepath).name}")
        if inserted_rows:
            imported_count = len(inserted_rows)
            label = "fichier" if imported_count == 1 else "fichiers"
            suffix = f" depuis {source_label}" if source_label else ""
            self._log(f"[{self._ts()}] {imported_count} {label} importé(s){suffix}.")
        self._refresh_table()
        return inserted_rows

    def _edit_delivery_recipients(self, sid):
        try:
            dlg = DeliveryRecipientsDialog(self._delivery_recipients.get(sid, []), self)
            if dlg.exec_() != QDialog.Accepted:
                return
            recipients = dlg.get_recipients()
            self._delivery_recipients[sid] = recipients
            self.db.update_session_delivery(
                sid,
                recipients_json=json.dumps(recipients, ensure_ascii=False),
                status="queued" if recipients and self.preset.get("delivery_enabled") else "",
                result_json="",
            )
            if sid in self._dlv_btn:
                self._dlv_btn[sid].set_delivery(recipients, "queued" if recipients and self.preset.get("delivery_enabled") else "")
            self._refresh_table()
            self._log(f"[{self._ts()}] ✉ Destinataires mis à jour : {summarize_delivery_recipients(recipients)}")
        except Exception as exc:
            self._log(f"[{self._ts()}] ⚠ Ouverture des destinataires en échec — {exc}")
            show_info_message(self, "Destinataires", f"Impossible d'ouvrir la fiche client.\n\n{exc}", icon_name="alert", accent=True)

    def _choose_reframe_preset(self, current_name=""):
        presets = load_reframe_presets()
        items = ["Popup automatique", DIRECT_360_LABEL]
        items.extend(name for name in sorted(presets.keys()) if name != DIRECT_360_LABEL)
        current_label = describe_reframe_preset(current_name)
        dlg = PresetChoiceDialog(items, current_label, self)
        if dlg.exec_() != QDialog.Accepted:
            return None
        choice = dlg.selected_value()
        apply_all = dlg.apply_to_all()
        if not choice or choice == "Popup automatique":
            return {"name": "", "payload": {}, "apply_all": apply_all}
        if choice == DIRECT_360_LABEL:
            return {
                "name": DIRECT_360_LABEL,
                "payload": {SESSION_OUTPUT_MODE_KEY: SESSION_OUTPUT_MODE_360},
                "apply_all": apply_all,
            }
        payload = extract_reframe_preset_payload(presets.get(choice, {}))
        if not payload:
            show_info_message(self, "Preset introuvable", "Le preset sélectionné est vide ou introuvable.", icon_name="alert", accent=True)
            return None
        return {"name": choice, "payload": payload, "apply_all": apply_all}

    def _apply_preset_to_sessions(self, session_ids):
        session_ids = [sid for sid in session_ids if sid is not None]
        if not session_ids:
            return
        current_name = ""
        sessions = {row[0]: row for row in (self._session_rows or self.db.get_all())}
        if len(session_ids) == 1 and session_ids[0] in sessions:
            current_name = sessions[session_ids[0]][6]
        selection = self._choose_reframe_preset(current_name)
        if selection is None:
            return
        if selection.get("apply_all"):
            session_ids = [row[0] for row in (self._session_rows or self.db.get_all())]
        payload_json = json.dumps(selection["payload"], ensure_ascii=False) if selection["payload"] else ""
        self.db.update_sessions_reframe(session_ids, selection["name"], payload_json)
        self._refresh_table()
        target_count = len(session_ids)
        action = selection["name"] or "Popup automatique"
        self._log(f"[{self._ts()}] 🧭 Preset recadrage appliqué à {target_count} session(s) : {action}")

    def _apply_preset_to_selection(self):
        sids = self._selected_sids()
        if not sids:
            sid = self._selected_sid()
            sids = [sid] if sid is not None else []
        if not sids:
            show_info_message(self, "Preset de recadrage", "Sélectionne au moins une session dans la queue.", icon_name="info", accent=False)
            return
        self._apply_preset_to_sessions(sids)

    def _delete_session(self, sid):
        cache_path = self.db.delete_session(sid)
        safe_unlink(cache_path)
        sessions = {row[0]: row for row in (self._session_rows or self.db.get_all())}
        session_name = sessions.get(sid, ("", ""))[1] if sid in sessions else ""
        safe_rmtree(session_preview_cache_dir(sid, session_name))
        self._delivery_queue = [queued_sid for queued_sid in self._delivery_queue if queued_sid != sid]
        for d in [self._sw, self._rb, self._rfb, self._db_btn, self._dlv_btn, self._delivery_recipients, self._eta, self._elapsed_done, self._stage]:
            d.pop(sid, None)
        self._log(f"[{self._ts()}] 🗑  Session supprimée")
        self._refresh_table()

    def _launch_batch(self):
        if self.manager and self.manager.paused:
            self._toggle_pause_resume()
            return
        pending = self.db.get_pending()
        if not pending:
            if self.db.get_all():
                show_info_message(
                    self,
                    "Aucune session en attente",
                    "Aucune session n'est prête à être lancée.\nRelance une session en erreur ou importe de nouveaux fichiers.",
                    icon_name="info",
                    accent=False,
                )
            else:
                show_info_message(
                    self,
                    "Queue vide",
                    "Importe au moins un média dans la queue avant de lancer le traitement.",
                    icon_name="info",
                    accent=False,
                )
            return
        if not self._ensure_output_dir_ready():
            return
        if not self.ffmpeg:
            show_info_message(
                self,
                "FFmpeg manquant",
                "FFmpeg introuvable.\n\nMac : brew install ffmpeg\nWindows : https://ffmpeg.org/download.html\n\nPuis configure le chemin dans Réglages.",
                icon_name="alert",
                accent=True,
            )
            return
        if not self._insv_batch_ready(pending):
            msg = (
                "Des fichiers INSV sont en attente mais le SDK n'est pas validé.\n\n"
                "Ouvre Réglages > Système puis lance :\n"
                "1. Vérifier FFmpeg\n"
                "2. Vérifier le SDK"
            )
            show_info_message(self, "Validation SDK requise", msg, icon_name="alert", accent=True)
            self._log(f"[{self._ts()}] ⚠ Export INSV bloqué — FFmpeg/SDK non validés")
            return

        self._set_launch_state(False)
        self.btn_launch.setText("EN COURS…")
        self.btn_launch.setIcon(QIcon())
        self.btn_launch.setObjectName("btn_launch_inactive")
        self.btn_launch.setEnabled(False)
        self.btn_launch.style().unpolish(self.btn_launch)
        self.btn_launch.style().polish(self.btn_launch)

        self._set_global_status("processing")
        self._log(f"[{self._ts()}] ══  Batch démarré — {len(pending)} session(s) ══")
        self.status_bar.set_processing("Initialisation…", 0)

        self.manager = BatchManager(self.db, self.preset, self.ffmpeg)
        self.manager.on_done = self._on_batch_done
        self.manager.start(pending, {
            'progress': self._on_progress,
            'status':   self._on_status,
            'stage':    self._on_stage,
            'log':      self._log,
            'error':    self._on_error,
            'done_one': self._on_done_one,
            'preview': self._on_preview_request,
            'eta': self._on_eta,
        })

    def _ensure_output_dir_ready(self):
        if str(self.preset.get("output_dir", "")).strip():
            return True
        chosen = QFileDialog.getExistingDirectory(self, "Choisir le dossier de sortie des exports")
        if not chosen:
            self._log(f"[{self._ts()}] ⚠ Export annulé — aucun dossier de sortie choisi")
            return False
        self.preset["output_dir"] = chosen
        self._save_preset()
        self._log(f"[{self._ts()}] 📁 Dossier de sortie : {chosen}")
        return True

    def _retry(self, sid):
        self.db.reset(sid)
        self._sw.pop(sid,None); self._rb.pop(sid,None); self._stage.pop(sid, None); self._eta.pop(sid, None)
        self._refresh_table()
        self._log(f"[{self._ts()}] ↺  Session #{sid} relancée")

    def _open_settings(self):
        dlg = SettingsDialog(self.preset, self.ffmpeg or "", self)
        if dlg.exec_() == QDialog.Accepted:
            previous_theme = normalize_theme_mode(self.preset.get("theme_mode", "dark"))
            p, ff = dlg.get_values()
            self.preset.update(p)
            self.ffmpeg = find_ffmpeg(ff)
            self.preset['ffmpeg_path'] = ff
            self._save_preset()
            new_theme = normalize_theme_mode(self.preset.get("theme_mode", "dark"))
            if new_theme != previous_theme:
                self._animate_theme_transition(new_theme)
            else:
                self._check_ffmpeg()
                self._check_sdk()
                self._refresh_table()
            self._log(f"[{self._ts()}] ✓  Réglages enregistrés.")
            self._maybe_start_delivery_worker()

    def _rebuild_after_theme_change(self):
        restore_fullscreen = bool(getattr(self, "_theme_restore_fullscreen", False))
        restore_maximized = bool(getattr(self, "_theme_restore_maximized", False))
        restore_geometry = QRect(getattr(self, "_theme_restore_geometry", self.geometry()))
        self._theme_restore_fullscreen = False
        self._theme_restore_maximized = False
        self._theme_restore_geometry = None
        selected_sids = set(self._selected_sids())
        old_log_text = ""
        old_log_visible = False
        if self.log_dlg is not None:
            try:
                old_log_text = self.log_dlg.log_box.toPlainText()
                old_log_visible = self.log_dlg.isVisible()
                self.log_dlg.hide()
                self.log_dlg.deleteLater()
            except Exception:
                old_log_text = ""
                old_log_visible = False
        self.log_dlg = LogDialog(self)
        if old_log_text:
            self.log_dlg.log_box.setPlainText(old_log_text)
        if old_log_visible:
            self.log_dlg.show()

        old_central = self.centralWidget()
        self._preserve_window_state_on_setup = True
        try:
            self._setup_ui()
        finally:
            self._preserve_window_state_on_setup = False
        if old_central is not None:
            old_central.deleteLater()
        self._check_ffmpeg()
        self._check_sdk()
        self._refresh_table()
        if restore_fullscreen:
            if not self.isFullScreen():
                QTimer.singleShot(0, self.showFullScreen)
        elif restore_maximized:
            if not self.isMaximized():
                QTimer.singleShot(0, self.showMaximized)
        else:
            self.setGeometry(restore_geometry)
        if selected_sids:
            for row, session in enumerate(self._session_rows):
                if session[0] in selected_sids:
                    self.table.selectRow(row)
                    break
        if self.manager and (self.manager.running or self.manager.paused):
            self._set_global_status("processing")
            if self.manager.paused:
                self.status_bar.set_processing("Batch en pause", 0)
                self.btn_launch.setText("REPRENDRE")
            else:
                self.status_bar.set_processing("Traitement en cours…", 0)
                self.btn_launch.setText("EN COURS…")
        self._log(f"[{self._ts()}] 🎨 Thème actif : {theme_display_name(self.preset.get('theme_mode'))}")

    def _open_logs(self):
        self.log_dlg.show(); self.log_dlg.raise_()

    def _clear_all(self):
        if not ask_confirmation(
            self,
            "Supprimer toutes les sessions ?",
            "Toute la queue sera vidée, ainsi que les aperçus et caches associés.",
            confirm_text="Supprimer",
            cancel_text="Annuler",
            icon_name="trash",
            accent=True,
        ):
            return
        sessions = list(self._session_rows or self.db.get_all())
        cache_paths = self.db.clear()
        for cache_path in cache_paths:
            safe_unlink(cache_path)
        for sid, fname, *_rest in sessions:
            safe_rmtree(session_preview_cache_dir(sid, fname))
        self._delivery_queue.clear()
        self._delivery_worker = None
        for d in [self._sw,self._rb,self._rfb,self._db_btn,self._dlv_btn,self._delivery_recipients,self._eta,self._elapsed_done,self._stage]:
            d.clear()
        self._refresh_table()
        self._log(f"[{self._ts()}] 🗑  Liste vidée.")

    def _delivery_job_from_sid(self, sid):
        sessions = {row[0]: row for row in (self._session_rows or self.db.get_all())}
        row = sessions.get(sid)
        if not row:
            return None
        try:
            recipients = normalize_delivery_recipients(json.loads(row[3] or "[]"))
        except Exception:
            recipients = []
        try:
            outputs = json.loads(row[11] or "[]")
        except Exception:
            outputs = []
        outputs = [path for path in outputs if path and os.path.exists(path)]
        return {
            "sid": sid,
            "name": row[1],
            "recipients": recipients,
            "outputs": outputs,
            "delivery_status": row[4],
        }

    def _queue_delivery_for_session(self, sid):
        if not self.preset.get("delivery_enabled"):
            return
        job = self._delivery_job_from_sid(sid)
        if not job or not job["recipients"] or not job["outputs"]:
            return
        if sid not in self._delivery_queue and not (self._delivery_worker and self._delivery_worker.sid == sid):
            self._delivery_queue.append(sid)
        self.db.update_session_delivery(sid, status="queued", result_json="")
        self._log(f"[{self._ts()}] ☁ Livraison planifiée : {job['name']} → {len(job['recipients'])} client(s)")
        self._refresh_table()

    def _maybe_start_delivery_worker(self):
        if not self.preset.get("delivery_enabled"):
            return
        if self._delivery_worker and self._delivery_worker.isRunning():
            return
        if self.manager and (self.manager.running or self.manager.paused):
            return
        while self._delivery_queue:
            sid = self._delivery_queue.pop(0)
            job = self._delivery_job_from_sid(sid)
            if not job or not job["recipients"] or not job["outputs"]:
                continue
            worker = DeliveryWorker(sid, job["name"], job["outputs"], job["recipients"], self.preset)
            worker.sig_log.connect(self._log)
            worker.sig_status.connect(self._on_delivery_status)
            worker.sig_done.connect(self._on_delivery_done)
            worker.sig_error.connect(self._on_delivery_error)
            worker.finished.connect(self._on_delivery_worker_finished)
            self._delivery_worker = worker
            worker.start()
            return

    def _on_delivery_status(self, sid, status):
        self.db.update_session_delivery(sid, status=status)
        self._refresh_table()

    def _on_delivery_done(self, sid, payload):
        result_json = json.dumps(payload or {}, ensure_ascii=False)
        self.db.update_session_delivery(sid, status="sent", result_json=result_json)
        sent_count = int((payload or {}).get("sent_count", 0) or 0)
        asset_count = len((payload or {}).get("assets", []) or [])
        self._log(f"[{self._ts()}] ✅ Livraison client envoyée : {asset_count} vidéo(s) · {sent_count} client(s)")
        self._notify_export_done("Livraison envoyée", f"{self._session_name_by_sid.get(sid, 'Vidéo')} · {sent_count} client(s)")
        self._refresh_table()

    def _on_delivery_error(self, sid, message):
        payload = {"error": str(message or "")}
        self.db.update_session_delivery(sid, status="error", result_json=json.dumps(payload, ensure_ascii=False))
        self._log(f"[{self._ts()}] ❌ Livraison client — {message}")
        self._refresh_table()

    def _on_delivery_worker_finished(self):
        self._delivery_worker = None
        self._maybe_start_delivery_worker()

    # ── CALLBACKS ─────────────────────────────────────────────
    def _on_progress(self, sid, pct):
        stage = self._stage.get(sid, "")
        if sid in self._sw:
            self._sw[sid].set_status(Status.PROCESSING, pct, stage)
        total = self._table_total_count
        if total > 0:
            done = self._table_done_count
            global_pct = int((done / total)*100)
            fname = self._session_name_by_sid.get(sid, "")
            current_name = f"{fname} · {stage}" if fname and stage else (fname or stage)
            self.status_bar.set_processing(current_name, global_pct, self._eta.get(sid, ""))

    def _on_stage(self, sid, stage_txt):
        stage = str(stage_txt or "")
        if stage:
            self._stage[sid] = stage
            if sid in self._sw:
                state = getattr(self._sw[sid], "_state", None)
                pct = int(state[1] or 0) if state and len(state) >= 2 else 0
                self._sw[sid].set_status(Status.PROCESSING, pct, stage)
        else:
            self._stage.pop(sid, None)
        fname = self._session_name_by_sid.get(sid, "")
        total = self._table_total_count
        if not stage:
            return
        if total > 0 and self.manager and self.manager.running:
            done = self._table_done_count
            global_pct = int((done / total)*100)
            current_name = f"{fname} · {stage}" if fname and stage else (fname or stage)
            self.status_bar.set_processing(current_name, global_pct, self._eta.get(sid, ""))

    def _on_eta(self, sid, eta_txt):
        self._eta[sid] = eta_txt or ""
        fname = self._session_name_by_sid.get(sid, "")
        stage = self._stage.get(sid, "")
        total = self._table_total_count
        if total > 0:
            done = self._table_done_count
            global_pct = int((done / total)*100)
            current_name = f"{fname} · {stage}" if fname and stage else (fname or stage)
            self.status_bar.set_processing(current_name, global_pct, self._eta.get(sid, ""))

    def _on_preview_request(self, worker, sid, data):
        self._play_preview_chime()
        dlg = ReframePreviewDialog(self.ffmpeg, data, self)
        dlg.setModal(True)
        dlg.exec_()
        worker.set_preview_reply(dlg.get_reply())

    def _on_status(self, sid, status):
        if status != Status.PROCESSING:
            self._stage.pop(sid, None)
        if sid in self._sw: self._sw[sid].set_status(status, extra_text=format_elapsed_label(self._elapsed_done.get(sid, 0)) if status == Status.DONE and sid in self._elapsed_done else "")
        if status in (Status.DONE, Status.ERROR):
            self._eta.pop(sid, None)
            self._refresh_table()

    def _on_error(self, sid, msg):
        self.status_bar.set_error(msg[:60])
        self._refresh_table()

    def _on_done_one(self, sid, elapsed):
        self.db.add_stat(elapsed)
        self._elapsed_done[sid] = elapsed
        sessions = self.db.get_all()
        done = next((s for s in sessions if s[0] == sid), None)
        if done:
            fname = done[1]
            try:
                outputs = json.loads(done[11] or "[]")
            except Exception:
                outputs = []
            extra = f" · {len(outputs)} fichier(s)" if outputs else ""
            self._play_chime()
            self._notify_export_done("Export terminé", f"{fname}{extra} · {format_elapsed_label(elapsed)}")
            if sid in self._sw:
                self._sw[sid].set_status(Status.DONE, extra_text=format_elapsed_label(elapsed))
            self._queue_delivery_for_session(sid)
            self._maybe_start_delivery_worker()

    def _on_batch_done(self):
        if self.manager:
            self.manager.paused = False
        self.btn_launch.setText("LANCER")
        self._set_global_status("ready")
        self._log(f"[{self._ts()}] ══  Batch terminé ══")
        self._refresh_table()
        sessions = self.db.get_all()
        done_count = sum(1 for s in sessions if s[8] == Status.DONE)
        err_count = sum(1 for s in sessions if s[8] == Status.ERROR)
        self._notify_export_done("Batch terminé", f"{done_count} export(s) terminés · {err_count} erreur(s)")
        self._maybe_start_delivery_worker()

    # ── UTILS ─────────────────────────────────────────────────
    def _check_ffmpeg(self):
        if self.ffmpeg:
            try:
                r=run_process([self.ffmpeg,"-version"],capture_output=True,text=True,timeout=5)
                v=r.stdout.split('\n')[0].split(' ')
                ver=v[2] if len(v)>2 else "?"
                self._set_chip_state(self.lbl_ffmpeg, f"FFmpeg {ver}", "success")
                self._refresh_table()
            except: self._ffmpeg_ko()
        else: self._ffmpeg_ko()

    def _ffmpeg_ko(self):
        self.ffmpeg=None
        self._set_chip_state(self.lbl_ffmpeg, "FFmpeg non trouvé", "warning")
        self._log(f"[{self._ts()}] ⚠  FFmpeg introuvable — configurez dans ⚙")
        self._refresh_table()

    def _check_sdk(self):
        diag = sdk_diagnostic(self.preset.get("media_sdk_resolved_path", "") or self.preset.get("media_sdk_path", ""))
        if diag.get("ok") and (self.preset.get("media_sdk_validated") or not self.preset.get("media_sdk_path", "").strip()):
            self._set_chip_state(self.lbl_sdk, "INSV prêt", "success")
            return
        if diag.get("ok"):
            self._set_chip_state(self.lbl_sdk, "SDK détecté · vérifier", "warning")
            return
        if not self.preset.get("media_sdk_path", "").strip():
            self._set_chip_state(self.lbl_sdk, "INSV non configuré", "warning")
            return
        self._set_chip_state(self.lbl_sdk, "SDK invalide", "error")

    def _schedule_preview_warmup(self):
        if self._preview_warmup_worker is not None:
            return
        if self.manager and (self.manager.running or self.manager.paused):
            return
        self._preview_warmup_timer.start(450)

    def _eligible_preview_warmup_session(self):
        if not self.preset.get("preview_before_render", True):
            return None
        if self.preset.get("auto_reframe"):
            return None
        sdk_diag = sdk_diagnostic(self.preset.get("media_sdk_resolved_path", "") or self.preset.get("media_sdk_path", ""))
        if not sdk_diag.get("ok"):
            return None

        preferred_ids = self._selected_sids() or ([self._selected_sid()] if self._selected_sid() is not None else [])
        sessions = self.db.get_pending()
        ordered = sorted(
            sessions,
            key=lambda row: (0 if row[0] in preferred_ids else 1, row[0]),
        )
        for row in ordered:
            sid, fname, fpath, _pj, reframe_name, reframe_payload_json = row
            if not str(fpath).lower().endswith(".insv"):
                continue
            try:
                payload = json.loads(reframe_payload_json or "{}")
            except Exception:
                payload = {}
            if resolve_session_output_mode(reframe_name, payload) == SESSION_OUTPUT_MODE_360:
                continue
            if extract_reframe_preset_payload(payload):
                continue
            preview_dir = session_preview_cache_dir(sid, fname)
            preview_meta_path = session_preview_cache_meta_path(sid, fname)
            try:
                with open(preview_meta_path, "r", encoding="utf-8") as f:
                    preview_meta = json.load(f)
            except Exception:
                preview_meta = {}
            cache_ok, _reason, _expected_meta, _image_path = validate_preview_cache(preview_dir, preview_meta, fpath, preset=self.preset)
            if not cache_ok:
                return {"sid": sid, "filename": fname, "filepath": fpath}
        return None

    def _maybe_warmup_preview_cache(self):
        if self._preview_warmup_worker is not None:
            return
        session = self._eligible_preview_warmup_session()
        if not session:
            return
        self._preview_warmup_worker = PreviewWarmupWorker(
            session["sid"],
            session["filename"],
            session["filepath"],
            self.preset,
        )
        self._preview_warmup_worker.sig_done.connect(self._on_preview_warmup_done)
        self._preview_warmup_worker.finished.connect(self._on_preview_warmup_finished)
        self._preview_warmup_worker.start()

    def _on_preview_warmup_done(self, result):
        if result.get("ok") and not result.get("cache_hit"):
            self._log(f"[{self._ts()}] ✓ Aperçu INSV préchargé : {result.get('filename','session')}")

    def _on_preview_warmup_finished(self):
        self._preview_warmup_worker = None
        if not (self.manager and (self.manager.running or self.manager.paused)):
            self._schedule_preview_warmup()

    def _should_autodetect_sdk_on_startup(self):
        if os.name != "nt":
            return False
        if self._sdk_autodetect_worker is not None:
            return False
        if find_bundled_sdk_binary():
            return False
        if str(self.preset.get("media_sdk_path", "")).strip():
            return False
        if str(self.preset.get("media_sdk_resolved_path", "")).strip():
            return False
        return not bool(self.preset.get("sdk_autodetect_attempted"))

    def _maybe_autodetect_sdk_on_startup(self):
        if not self._should_autodetect_sdk_on_startup():
            return
        self.preset["sdk_autodetect_attempted"] = True
        self._save_preset()
        self._log(f"[{self._ts()}] 🔎 Recherche automatique du Media SDK au premier démarrage…")
        self.status_bar.set_processing("Détection automatique du Media SDK", 0)
        self._sdk_autodetect_worker = SdkAutodetectWorker()
        self._sdk_autodetect_worker.sig_done.connect(self._on_startup_sdk_autodetect_done)
        self._sdk_autodetect_worker.finished.connect(self._on_startup_sdk_autodetect_finished)
        self._sdk_autodetect_worker.start()

    def _on_startup_sdk_autodetect_done(self, result):
        logs = result.get("logs") or []
        for line in logs:
            self._log(f"[{self._ts()}] {line}")

        resolved_path = str(result.get("resolved_path", "") or "").strip()
        if result.get("ok") and resolved_path:
            self.preset["media_sdk_path"] = resolved_path
            self.preset["media_sdk_resolved_path"] = resolved_path
            self.preset["media_sdk_validated"] = True
            self._save_preset()
            self._log(f"[{self._ts()}] ✓ Media SDK détecté automatiquement")
        else:
            self._log(f"[{self._ts()}] ⚠ Aucun Media SDK valide détecté automatiquement")

        self._check_sdk()
        self._refresh_table()
        self._schedule_preview_warmup()

    def _on_startup_sdk_autodetect_finished(self):
        self._sdk_autodetect_worker = None
        self._refresh_table()

    def _should_check_updates_on_startup(self):
        if self._update_worker is not None:
            return False
        if not bool(self.preset.get("update_auto_check", True)):
            return False
        return bool(str(self.preset.get("update_manifest_url", "") or "").strip())

    def _maybe_check_updates_on_startup(self):
        if not self._should_check_updates_on_startup():
            return
        manifest_url = str(self.preset.get("update_manifest_url", "") or "").strip()
        self._log(f"[{self._ts()}] 🔄 Vérification des mises à jour…")
        self._update_worker = UpdateCheckWorker(APP_VERSION, manifest_url)
        self._update_worker.sig_done.connect(self._on_update_check_done)
        self._update_worker.finished.connect(self._on_update_check_finished)
        self._update_worker.start()

    def _on_update_check_done(self, result):
        if not result.get("ok"):
            error_text = str(result.get("error") or "").strip()
            if error_text and not result.get("skipped"):
                self._log(f"[{self._ts()}] ⚠ Vérification des mises à jour impossible — {error_text}")
            return
        latest = str(result.get("latest_version", "") or "").strip()
        if not result.get("has_update"):
            self._log(f"[{self._ts()}] ✓ Application à jour ({APP_VERSION})")
            if self.preset.get("update_postponed_version"):
                self.preset["update_postponed_version"] = ""
                self._save_preset()
            return
        if not latest:
            return
        if latest == str(self.preset.get("update_postponed_version", "") or "").strip():
            self._log(f"[{self._ts()}] ℹ Mise à jour {latest} reportée pour plus tard")
            return
        download_url = str(result.get("download_url", "") or "").strip()
        if not download_url:
            self._log(f"[{self._ts()}] ⚠ Mise à jour {latest} détectée sans lien de téléchargement")
            return
        self._log(f"[{self._ts()}] ↑ Nouvelle version disponible : {latest}")
        accepted = ask_confirmation(
            self,
            result.get("title") or "Nouvelle version disponible",
            build_update_prompt_message(APP_VERSION, latest, result.get("notes", "")),
            confirm_text="Télécharger",
            cancel_text="Plus tard",
            icon_name="info",
            accent=True,
        )
        if accepted:
            if open_external_url(download_url):
                self._log(f"[{self._ts()}] ⇢ Téléchargement de la version {latest} lancé")
                self.preset["update_postponed_version"] = ""
            else:
                self._log(f"[{self._ts()}] ⚠ Impossible d'ouvrir le lien de mise à jour : {download_url}")
                show_info_message(
                    self,
                    "Téléchargement impossible",
                    f"Impossible d'ouvrir automatiquement le lien.\n\n{download_url}",
                    icon_name="alert",
                    accent=True,
                )
        else:
            self._log(f"[{self._ts()}] ⏳ Mise à jour {latest} reportée")
            self.preset["update_postponed_version"] = latest
        self._save_preset()

    def _on_update_check_finished(self):
        self._update_worker = None

    def _insv_batch_ready(self, pending=None):
        rows = pending if pending is not None else self.db.get_pending()
        has_insv = any(str(row[2]).lower().endswith(".insv") for row in rows)
        if not has_insv:
            return True
        diag = sdk_diagnostic(self.preset.get("media_sdk_resolved_path", "") or self.preset.get("media_sdk_path", ""))
        return bool(diag.get("ok"))

    def _set_global_status(self, state):
        if state=="ready":
            self._set_chip_state(self.lbl_status, "PRÊT", "success")
        else:
            self._set_chip_state(self.lbl_status, "TRAITEMENT", "processing")

    def _log(self, msg):
        self.log_dlg.append(msg)

    def _ts(self): return datetime.now().strftime("%H:%M:%S")

    def _load_preset(self):
        if os.path.exists(self.PRESET_FILE):
            try:
                with open(self.PRESET_FILE) as f:
                    m=dict(DEFAULT_PRESET); m.update(json.load(f)); return m
            except: pass
        return dict(DEFAULT_PRESET)

    def _save_preset(self):
        try:
            with open(self.PRESET_FILE,'w') as f: json.dump(self.preset,f,indent=2)
        except Exception as e:
            self._log(f"[{self._ts()}] ⚠  Sauvegarde : {e}")

# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")
    base_font = QFont(UI_FONT, 11 if IS_WINDOWS else 10)
    base_font.setWeight(QFont.Medium)
    app.setFont(base_font)
    icon = app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
    apply_theme_mode("dark")
    win=PipelineWindow()
    win.show()
    sys.exit(app.exec_())
