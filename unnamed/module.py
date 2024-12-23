import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets


# Later wrap ModelManager in a PyTorch Lightning module

class ModelManager():
    def __init__(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def forward(self):
        pass

    def backward(self):
        pass

    def train(self):
        pass

    def eval(self):
        pass

    def predict(self):
        pass

    def to_string(self):
        pass

class Component(ABC):
    def __init__(self, component_name):
        super().__init__()
        self.component_name = component_name

    # Allows each component to be visualized differently
    @abstractmethod
    def display_component_widget(self):
        pass 

    @abstractmethod
    def to_string(self):
        pass

class Layer(Component):
    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def get_layer(self):
        pass

    @abstractmethod
    def forward(self):
        pass



class Conv2D_wrapper(Layer):
    def __init__(self, params):
        super().__init__("Conv2d")
        self.layer = nn.Conv2d(**params)

    def get_layer(self):
        return self.layer

    def display_component_widget(self):
        pass

    def to_string(self):
        return self.layer

    def forward(self):
        raise NotImplementedError("Forward logic not implemented yet.")

