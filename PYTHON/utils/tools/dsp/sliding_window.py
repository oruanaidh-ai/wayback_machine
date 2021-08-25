import numpy as np

class SlidingWindow:

    def __init__(self, data, stride, width):
        self.stride = stride
        self.width = width
        self.pos = 0
        self.data = data

    def __iter__(self):
        while self.pos + self.width <= len(self.data):
            yield self.data[self.pos:self.pos + self.width]
            self.pos += self.stride

