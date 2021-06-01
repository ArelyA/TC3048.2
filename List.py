from Quad import *
from collections import deque
class List(deque):
  """Doubly-linked-List extension adding name attribute and overraiding repr function"""
  def __init__(self, name, maxMem = 100):
    self.name = name
  def __repr__(self):
    lenC = len(max(self, key=len))
    return self.name + " \n" + "\n".join("{:^10}".format(idx) + item.reprQ(lenC) for idx, item in enumerate(self))
  def push(self, x):
    """
    Appends the element or elements at the end of the list
    """
    if(isinstance(x, str)):
      self.append(x)
    else:
      try:
        iterator = iter(x)
      except TypeError:
        # not iterable
        self.append(x)
      else:
        # iterable
        self.extend(x)