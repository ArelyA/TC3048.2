from Quad import *
from collections import deque
class Memory(deque):
  """Doubly-linked-List extension adding name attribute and overraiding repr function"""
  def __init__(self, name, maxMem = 2000, tempMem = 1000, constMem = 1000):
    # Name
    self.name = name
    # Sizes
    self.memSize = maxMem
    self.tempSize = tempMem
    self.constSize = constMem
    self.size = self.memSize + self.tempSize + self.constSize
    # Counters
    self.counterMem = 0
    self.counterTemp = self.memSize
    self.counterConst = self.memSize + self.tempSize
    # Limits
    self.maxMemLimit = self.memSize
    self.tempMemLimit = self.tempSize  + self.memSize
    self.constMemLimit = self.size
    
    
    self.push([None for i in range(self.size)])
    #object()

  def __repr__(self):
    #return self.name + " \n[" + ",\n".join(str(item) if item != None else 'None' for item in self) + ']'
    return self.name + " \n[" + ",\n".join(str(id_item) + ": " + str(item) if item != None else str(id_item) + ": " + 'None' for id_item, item in enumerate(self)) + ']'

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

  def popAvail(self, index = 1):
    """
    Returns next available memory slot
    """
    if(self.counterMem < self.maxMemLimit):
      nextSlot = self.counterMem
      self.counterMem += index
      return nextSlot
    else: raise MemoryError("Out of memory")

  def popTemp(self, index = 1):
    """
    Returns next available temporal memory slot
    """
    if(self.counterTemp < self.tempMemLimit):
      nextSlot = self.counterTemp
      self.counterTemp += index
      return nextSlot
    else: raise MemoryError("Out of temporals memory")

  def popConst(self, index = 1):
    """
    Returns next available temporal memory slot
    """
    if(self.counterConst < self.constMemLimit):
      nextSlot = self.counterConst
      self.counterConst += index
      return nextSlot
    else: raise MemoryError("Out of constants memory")

  def release(self, mem, temp):
    self.counterMem = mem
    self.counterTemp = temp