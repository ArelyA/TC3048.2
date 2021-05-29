from Stack import *
from Function import Function
from Quad import *
from Queue import *
from List import *
from Memory import *
class Compiler(object):
  def __init__(self):
    """
    Initializes variables

    operadores -> Stack

    operandos -> Stack
    
    tipos -> Stack

    jumps -> Stack

    funciones -> Dict

    funcContext -> Stack

    cuadruplos -> List

    memory -> Memory
    """
    self.operadores = Stack('Operadores')
    self.operandos = Stack('Operandos')
    self.tipos = Stack('Tipos')
    self.jumps = Stack('Jumps')
    self.funciones = {}
    self.funcContext = Stack('Contexto')
    self.cuadruplos = List('Cuadruplos')

    """ PASAR A MACHINE """
    self.mem = 2000
    self.memTemp = 1000
    self.memConst = 1000
    self.memory = Memory('Memory', self.mem, self.memTemp, self.memConst)
    """ HASTA AQUI """

    #self.memory.push([object() for i in range(len(self.memory))])
    # constantes
    self.constantes = {}
    self.reservadas = ["def", "read", "write", "print", "in", "for", "if", "else", "while", "len", "unigrams", "bigrams", "ngrams", "norm", "clean", "find", "substr", "range", "tokenize", "set", "count", "size"]
    self.addFunc('Global')

  def popOperador(self):
    """Removes the next element in operador"""
    return self.operadores.pop()

  def pushOperador(self, op):
    """Adds the next element in operador"""
    self.operadores.push(op)

  def topOperador(self):
    """Returns the next element in operador"""
    return self.operadores.top()

  def popOperando(self):
    """Removes the next element in operando"""
    return self.operandos.pop()
  
  def pushOperando(self, op):
    """Removes the next element in operando"""
    self.operandos.push(op)

  def topOperando(self):
    """Returns the next element in operando"""
    return self.operandos.top()
  
  def popTipo(self):
    """Removes the next element in tipos"""
    return self.tipos.pop()

  def pushTipo(self, op):
    """Adds the next element in tipos"""
    self.tipos.push(op)

  def topTipo(self):
    """Returns the next element in tipos"""
    return self.tipos.top()

  def popJump(self):
    """Removes the next jump"""
    return self.jumps.pop()

  def pushJump(self, jmp):
    """Removes the next jump"""
    self.jumps.push(jmp)

  def topJump(self):
    """Returns the next jump"""
    return self.jumps.top()
  
  def addConst(self, constId, constVal):
    constAddr = self.constantes.get(constId, None)
    if(constAddr == None):
      constAddr = self.memory.popConst()
      self.constantes[constId] = constAddr
      self.memory[constAddr] = constVal
    return constAddr

  def addFunc(self, funcId):
    """Adds function to context and to funciones dict"""
    if funcId in self.reservadas:
      raise ValueError("Invalid method identifier")
    if(self.funciones.get(funcId, None) == None):
      self.funcContext.push(funcId)
      addr = self.memory.popAvail() - self.memory.memSize
      tempAddr = self.memory.popTemp() - self.memory.tempSize
      self.funciones[funcId] = Function(funcId, (0 if addr < 0 else addr), (0 if tempAddr < self.memory.maxMemLimit else tempAddr))
    else:
      raise RuntimeError("Cannot define method more than once")
  
  def addParam(self, paramId):
    self.funciones[self.funcContext.top()].addParam(paramId)

  def setFuncTipo(self, funcType):
    self.funciones[self.funcContext.top()].setType(funcType)
  # def getVar(self, varId):
  #   self.funciones[self.funcContext.top()].get(varId, None)

  def addVar(self, varId, varType):
    """Adds variable to var dict of the corresponding Function (according to funcContext)"""
    var = self.funciones[self.funcContext.top()].getVar(varId)
    if(var == None):
      varAddr = self.memory.popAvail() - self.funciones[self.funcContext.top()].addr # guarda direcciones locales
      self.funciones[self.funcContext.top()].addVar(varId, varType, varAddr)
    elif var.getType() == None:
      var.setType(varType)
      varAddr = var.getAddr()
    elif var.getType() == varType:
      varAddr = var.getAddr()
    else:
      raise TypeError("Type-Mismatch: " + varType + " cannot be assigned to " +  var.getType())
    return varAddr
  
  def addVarTemp(self):
    """Adds variable to store ARRAYS"""
    varAddr = self.memory.popTemp() - self.funciones[self.funcContext.top()].addrTemp
    self.funciones[self.funcContext.top()].addVar(str(varAddr), None, varAddr)
    return str(varAddr)

  def getVar(self, varId):
    """Gets variable from var dict of the corresponding Function (according to funcContext)"""
    return self.funciones[self.funcContext.top()].getVar(varId)

  def getVarG(self, varId):
    """Gets variable from var dict of the global context"""
    if self.funcContext.top() == "Global":
      return None
    return self.funciones["Global"].getVar(varId)
  
  def getTemp(self):
    return self.memory.popTemp() - self.funciones[self.funcContext.top()].addrTemp

  def addQuad(self, op, left, right, addr):
    """Adds Quad to the cuadruplos list"""
    self.cuadruplos.append(Quad(op, left, right, addr))
    # if(op != '='):
    #   self.cuadruplos.append(Quad(op, left, right, addr))
    # else:
    #   self.cuadruplos.append(Quad(op, right, '', left))
    #   self.pushOperando(self.funciones[self.funcContext.top()].getVar(left).getAddr())