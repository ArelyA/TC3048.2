class Function(object):
  def __init__(self, funcId):
    """
    Creates a function object with attributes
    
    id -> String

    type -> String

    signature -> List

    vars -> Dict
    """
    self.id = funcId # String
    self.type = None # String
    self.signature = [] # List
    self.vars = {} # Dict
  def __repr__(self):
    signature = "None" if self.signature == None else self.signature
    type = "None" if self.type == None else "'" + self.type + "'"
    vars = ",\n\t       ".join("'" + key + "':" + repr(self.vars[key]) for key in self.vars)
    return "\n\tid: '" + self.id + "',\n\ttype: " + type + ",\n\tsignature: " + ", ".join(item for item in signature) + ",\n\tvars: {" + vars + '\n\t      }\n'
  def getType(self):
    return self.type
  def setType(self, funcType):
    self.type = funcType
  def getValue(self):
    return self.value
  def setValue(self, funcValue):
    self.value = funcValue

  def getSignature(self):
    return self.signature
  # def setSignature(self, funcSignature):
  #   self.signature = funcSignature

  def addParam(self, param):
    self.signature.append(param)
    #address = param
    #self.addVar(param, None, None, address) -> If incorporated, add function to detect unused variables
  
  def addVar(self, varId, varType, dim, varAddr):
    """
    Add Variable to vars dict.
    """
    self.vars[varId] = Variable(varId, varType, dim, varAddr)
  def getVar(self, varId):
    """
    Get Variable from dict by id.
    """
    return self.vars.get(varId, None)

class Variable(object):
  def __init__(self, varId, varType, dim, varAddr):
    self.id = varId # String
    self.type = varType # String
    self.dim = dim
    self.addr = varAddr # ???
    
  def __repr__(self):
    dim = "None" if self.dim == None else self.dim
    type = "None" if self.type == None else "'" + self.type + "'"
    return "{type: '" + type + "', dim: " + dim + ", addr: " + repr(id(self.addr)) + "}"
  def getType(self):
    return self.type
  def setType(self, varType):
    self.type = varType
  def getAddr(self):
    return self.addr
  def setAddr(self, varAddr):
    self.addr = varAddr