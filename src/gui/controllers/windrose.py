import numpy as np
from windrose import WindroseAxes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import QtWidgets

def create_windrose_in_frame(frame, speeds):
    clear_frame(frame)

    directions = list(range(0,360,72))
    
    prob = list(speeds) + [speeds[0]]
    dirs = list(directions) + [directions[0]]
    angles = np.deg2rad(dirs)
    
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111, projection='polar')

    ax.plot(angles, prob, 'k-', linewidth=2)
    ax.set_theta_zero_location('N')
    ax.set_rgrids([0.25, 0.5, 0.75, 1.0], angle=0, alpha=0.3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_ylim(0, speeds[0])
    
    canvas = FigureCanvas(fig)
    if frame.layout() is None:
        frame.setLayout(QtWidgets.QVBoxLayout())
    frame.layout().addWidget(canvas)
    
    return canvas, fig

def clear_frame(frame):
    if frame.layout():
        while frame.layout().count():
            child = frame.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()