from Quad import *
from collections import deque
class Memory(deque):
  """Doubly-linked-List extension adding name attribute and overraiding repr function"""
  def __init__(self, name, maxMem = 100):
    self.name = name
    self.counterMem = 0
    self.maxMem = maxMem
  def __repr__(self):
    return self.name + " \n[" + ",\n".join(str(id(item)) for item in self) + ']'
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
    def pop(self, index = 1):
      if(self.counterMem < self.maxMem):
        nextSlot = self[self.counterMem]
        self.counterMem += index
      else: raise MemoryError("No more available memory")
      return()