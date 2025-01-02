import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat
from pyqtgraph.opengl import GLViewWidget, GLGridItem, GLImageItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from pyqtgraph import ColorMap
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pickle
import numpy as np
import os


class Component(ABC):
    def __init__(self, name):
        super().__init__()
        self.name = name

    # Allows each component to be visualized differently
    @abstractmethod
    def get_widget(self):
        pass 

    @abstractmethod
    def __str__(self):
        pass
    
    def get_color(self):
        """Return a specific color for the layer type."""
        layer_colors = {
            'Conv2dWrapper': '#007FFF',  # Blue
            'Conv3dWrapper': '#003F7F',  # Dark Blue
            'MaxPool1dWrapper': '#00BF7F',  # Green
            'MaxPool2dWrapper': '#00BF7F',  # Green
            'AdaptiveAvgPool2dWrapper': '#00BF7F',  # Green
            'ReLUWrapper': '#FFA500',  # Orange
            'LeakyReLUWrapper': '#FF4500',  # Dark Orange
            'BatchNorm2dWrapper': '#FFD700',  # Yellow
            'LinearWrapper': '#800080',  # Purple
        }
        return layer_colors.get(self.__class__.__name__, '#808080')  # Default gray

class Layer(Component):
    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def get_layer(self):
        pass

    @abstractmethod
    def forward(self):
        pass
    
class Activation(Component):
    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def get_layer(self):
        pass

    @abstractmethod
    def forward(self):
        pass

# Convolution Layers
class Conv2dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name, )
        # Update the object's attributes with the dictionary
        self.__dict__.update(params)
        self.layer = nn.Conv2d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        return button

    def __str__(self):
        return str(self.layer)
    
    def forward(self, x):
        return self.layer(x)
        

class Conv3dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        # Update the object's attributes with the dictionary # TODO: Check if this is necessary, or use self.params
        self.__dict__.update(params)
        self.layer = nn.Conv3d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

# Pooling Layers

class MaxPool1dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.MaxPool1d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.7
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

class MaxPool2dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.MaxPool2d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.7
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

class AdaptiveAvgPool2dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.AdaptiveAvgPool2d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.7
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

# Padding Layers


# Non-linear Activations
class ReLUWrapper(Activation):
    def __init__(self, name, params):
        super().__init__(name)
        self.activation = nn.ReLU(**params)
        self.params = params

    def get_layer(self):
        return self.activation

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.5
        return button

    def __str__(self):
        return str(self.activation)

    def forward(self, x):
        return self.activation(x)

class LeakyReLUWrapper(Activation):
    def __init__(self, name, params):
        super().__init__(name)
        self.activation = nn.LeakyReLU(**params)
        self.params = params

    def get_layer(self):
        return self.activation

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.5
        return button

    def __str__(self):
        return str(self.activation)

    def forward(self, x):
        return self.activation(x)
    
# Normalization Layers

class BatchNorm2dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.BatchNorm2d(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.7
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

# Recurrent Layers

# Transformer Layers

# Linear Layers

class LinearWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.Linear(**params)
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.8
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)

# Dropout Layers

# Sparse Layers

# Distance Functions

# Loss Functions

# Vision Layers

# Shuffle Layers

# DataParallel Layers (multi-GPU, distributed)

# Utilities

class FlattenWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.Flatten()
        self.params = params

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        button.scaling_factor = 0.4
        return button

    def __str__(self):
        # TODo: Check if this is correct
        return str(self.layer)

    def forward(self, x):
        return self.layer(x)


# Quantized Functions

# Lazy Modules Initialization


# Registry
# Mapping layer (raw) names to the corresponding wrapper classes
WRAPPER_REGISTRY = {
    "Conv2d": Conv2dWrapper,
    "Conv3d": Conv3dWrapper,
    "MaxPool1d": MaxPool1dWrapper,
    "MaxPool2d": MaxPool2dWrapper,
    "AdaptiveAvgPool2d": AdaptiveAvgPool2dWrapper,
    "ReLU": ReLUWrapper,
    "LeakyReLU": LeakyReLUWrapper,
    "BatchNorm2d": BatchNorm2dWrapper,
    "Linear": LinearWrapper,
    "Flatten": FlattenWrapper,
}

