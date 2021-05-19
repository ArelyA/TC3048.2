class Function(object):
  def __init__(self, funcId, funcType, funcSignature):
    """
    Creates a function object with attributes
    
    id -> String

    type -> String

    signature -> List

    vars -> Dict
    """
    self.id = funcId # String
    self.type = funcType # String
    self.signature = funcSignature # List
    self.vars = {} # Dict
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
  def setSignature(self, funcSignature):
    self.signature = funcSignature
  def addVar(self, varId, varType, varValue):
    """
    Add Variable to vars dict.
    """
    self.vars[varId] = Variable(varId, varType, varValue)
  def getVar(self, varId):
    """
    Get Variable from dict by id.
    """
    return self.vars.get(varId, None)

class Variable(object):
  def __init__(self, varId, varType, varValue):
    self.id = varId # String
    self.type = varType # String
    self.value = varValue # ???
  def getType(self):
    return self.type
  def setType(self, varType):
    self.type = varType
  def getValue(self):
    return self.value
  def setValue(self, varValue):
    self.value = varValue