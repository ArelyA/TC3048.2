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

    avail -> Queue
    """
    self.operadores = Stack('Operadores')
    self.operandos = Stack('Operandos')
    self.tipos = Stack('Tipos')
    self.jumps = Stack('Jumps')
    self.funciones = {}
    self.funcContext = Stack('Contexto')
    self.cuadruplos = List('Cuadruplos')
    self.memoriaTotal = 100
    self.avail = Memory('Avail', self.memoriaTotal)
    self.avail.push([object() for i in range(self.memoriaTotal)])
    print(self.avail)
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

  def getAvail(self):
    """Returns the next available memory slot"""
    return self.avail.pop()

  def addFunc(self, funcId):
    """Adds function to context and to funciones dict"""
    if(self.funciones.get(funcId, None) == None):
      self.funcContext.push(funcId)
      self.funciones[funcId] = Function(funcId)
    else:
      raise RuntimeError("Cannot define method more than once")
  
  def addParam(self, paramId):
    self.funciones[self.funcContext.top()].addParam(paramId)

  # def setFuncTipo(self, )
  # def getVar(self, varId):
  #   self.funciones[self.funcContext.top()].get(varId, None)

  def addVar(self, varId, varType, dim):
    """Adds variable to var dict of the corresponding Function (according to funcContext)"""
    # if(self.funciones[self.funcContext.top()].get(varId, None) == None):
    #   self.funciones[self.funcContext.top()].addVar(varId, varType, dim, varAddr)
    # else:
    #   self.funciones[self.funcContext.top()]
    self.funciones[self.funcContext.top()].addVar(varId, varType, dim, self.avail.pop())

    #return varAddr

  def addQuad(self, op, left, right):
    """Adds Quad to the cuadruplos list"""
    if(op != '='):
      self.cuadruplos.append(Quad(op, left, right, self.avail.pop()))
    else:
      self.cuadruplos.append(Quad(op, right, '', self.funciones[self.funcContext.top()].getVar(left).getAddr()))
      self.pushOperando(self.funciones[self.funcContext.top()].getVar(left).getAddr())