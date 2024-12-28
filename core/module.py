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

# Later wrap ModelManager in a PyTorch Lightning module

class ModelManager():
    def __init__(self):
        self.component_wrappers = []

    def __len__(self):
        return len(self.component_wrappers)
    
    def __iter__(self):
        for component in self.component_wrappers:
            yield component
    
    def add_component(self, component):
        self.component_wrappers.append(component)

    def save(self, filepath):
        """
        Saves the ModelManager to a pickle file.
        """
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)
        print(f"ModelManager saved to {filepath}")

    @staticmethod
    def load(filepath):
        """
        Loads a ModelManager from a pickle file.
        """
        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def forward(self):
        pass

    def __str__(self):
        representation = []
        for component in self.component_wrappers:
            representation.append(str(component))
        return "\n".join(representation)


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
            'ReLUWrapper': '#FFA500',  # Orange
            'LeakyReLUWrapper': '#FF4500',  # Dark Orange
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
        print(self.layer)   

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        return button

    def __str__(self):
        return str(self.layer)
    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

class Conv3dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        # Update the object's attributes with the dictionary
        self.__dict__.update(params)
        self.layer = nn.Conv3d(**params)

    def get_layer(self):
        return self.layer

    def get_widget(self):
        button = QtWidgets.QPushButton(self.name)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setStyleSheet(f"background-color: {self.get_color()}; color: white; border-radius: 5px;")
        return button

    def __str__(self):
        return str(self.layer)

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

# Pooling Layers

class MaxPool1dWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.MaxPool1d(**params)

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

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

# Padding Layers


# Non-linear Activations
class ReLUWrapper(Activation):
    def __init__(self, name, params):
        super().__init__(name)
        self.activation = nn.ReLU(**params)

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

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

class LeakyReLUWrapper(Activation):
    def __init__(self, name, params):
        super().__init__(name)
        self.activation = nn.LeakyReLU(**params)

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

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")
    
# Normalization Layers

# Recurrent Layers

# Transformer Layers

# Linear Layers

class LinearWrapper(Layer):
    def __init__(self, name, params):
        super().__init__(name)
        self.layer = nn.Linear(**params)

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

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

# Dropout Layers

# Sparse Layers

# Distance Functions

# Loss Functions

# Vision Layers

# Shuffle Layers

# DataParallel Layers (multi-GPU, distributed)

# Utilities

# Quantized Functions

# Lazy Modules Initialization


# Registry
WRAPPER_REGISTRY = {
    "Conv2d": Conv2dWrapper,
    "Conv3d": Conv3dWrapper,
    "MaxPool1d": MaxPool1dWrapper,
    "ReLU": ReLUWrapper,
    "LeakyReLU": LeakyReLUWrapper,
    "Linear": LinearWrapper,
}

