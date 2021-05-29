from abc import ABC, abstractmethod

class Table(ABC):
  def __init__(self, elemId, addr, elemType = None):
    self.id = elemId # String
    self.type = elemType # String
    self.addr = addr # Int
    super().__init__()
    
  @abstractmethod
  def __repr__(self):
    pass

  def getType(self):
    return self.type

  def setType(self, elemType):
    self.type = elemType

class Function(Table):
  def __init__(self, funcId, addr, addrTemp):
    """
    Creates a Function object with attributes:
    
    id -> String

    type -> String

    addr -> Int

    addrTemp -> Int

    signature -> ["varID"]

    vars -> {"varId": Variable}
    """
    self.addrTemp = addrTemp
    self.signature = [] # List
    self.vars = {} # Dict
    # self.const = {} # Dict
    super().__init__(funcId, addr)

  def __repr__(self):
    signature = "None" if self.signature == None else self.signature
    type = "None" if self.type == None else "'" + self.type + "'"
    vars = ",\n\t       ".join("'" + key + "':" + repr(self.vars[key]) for key in self.vars)
    return "\n\tid: '" + self.id + "',\n\ttype: " + type + ",\n\tbaseAddress: " + str(self.addr) + ",\n\tbaseTempAddress: " + str(self.addrTemp) + ",\n\tsignature: " + ", ".join(item for item in signature) + ",\n\tvars: {" + vars + '\n\t      }\n'

  def getAddr(self):
    """
    Returns base address*

    * to be added to any Variable or Constant address to get the correct reference
    """
    return self.addr

  def getSignature(self):
    return self.signature

  def addParam(self, paramId):
    """
    Add parameter to signature list.
    """
    if paramId in self.signature:
      raise ValueError("Duplicate argument '" + paramId + "' in function definition")
    else:
      self.signature.append(paramId)
  
  def addVar(self, varId, varType, varAddr):
    """
    Add Variable to vars dict.
    """
    self.vars[varId] = Variable(varId, varType, varAddr)

  def getVar(self, varId):
    """
    Get Variable from dict by varId.
    """
    return self.vars.get(varId, None)

class Variable(Table):
  def __init__(self, varId, varType, varAddr):
    """
    Creates a Variable object with attributes:
    
    id -> String

    type -> String

    addr -> Int

    dims -> [Dimension]

    """
    self.dims = [] # List
    super().__init__(varId, varAddr, varType)
    
    
  def __repr__(self):
    #dims = "None" if self.dims == None else self.dims
    type = "None" if self.type == None else "'" + self.type + "'"
    return "{type: '" + type + "', dims: " + "->".join(str(dim) for dim in self.dims) + ", addr: " + str(self.addr) + "}"

  # def getType(self):
  #   return self.type

  # def setType(self, varType):
  #   self.type = varType

  def getAddr(self):
    """
    Returns local address
    """
    return self.addr
    
  def setAddr(self, varAddr):
    self.addr = varAddr

  def getDimensions(self):
    return self.dims
  
  def addDimension(self, inf, sup):
    """
    Current implementation for 1-D arrays
    """
    self.dims.append(Dimension(inf, sup))
    # if len(self.dim) > 1:
    #   for idx, dim in enumerate(self.dims.reverse()[1:]):
    #     nextOffset = self.dims[idx - 1].offset if self.dims[idx - 1].offset != 0 else 1
    #     self.dims[idx].offset = nextOffset * (self.dims[idx - 1].sup - self.dims[idx - 1].inf + 1)
    

class Dimension(object):
  def __init__(self, inf, sup, offset = 0):
    """
    Creates a Dimension object with attributes:

    inf -> Int

    sup -> Int

    offset -> Int
    """
    self.inf = inf
    self.sup = sup
    self.offset = offset

  def __repr__(self):
    return str(self.inf) + " - " + str(self.sup) + " | offset: " + str(self.offset)
  def __eq__(self, other):
    if self.__class__ != other.__class__:
      return False
    return self.__dict__ == other.__dict__

