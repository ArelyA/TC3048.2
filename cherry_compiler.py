from Stack import *
from Function import Function
from Quad import *
from Queue import *
class Compiler(object):
  def __init__(self):
    """
    Initializes variables

    operadores -> Stack

    operandos -> Stack

    jumps -> Stack

    funciones -> Dict

    funcContext -> Stack

    cuadruplos -> List

    avail -> Queue
    """
    self.operadores = Stack()
    self.operandos = Stack()
    self.jumps = Stack()
    self.funciones = {}
    self.funcContext = Stack()
    self.cuadruplos = []
    self.avail = Queue()

  def popOperador(self):
    """Removes the next element in operador"""
    self.operadores.pop()

  def pushOperador(self):
    """Adds the next element in operador"""
    self.operadores.push()

  def topOperador(self):
    """Returns the next element in operador"""
    return self.operadores.top()

  def popOperando(self):
    """Removes the next element in operando"""
    self.operandos.pop()
  
  def pushOperando(self):
    """Removes the next element in operando"""
    self.operandos.push()

  def topOperando(self):
    """Returns the next element in operando"""
    return self.operandos.top()

  def popJump(self):
    """Removes the next jump"""
    self.jumps.pop()

  def pushJump(self):
    """Removes the next jump"""
    self.jumps.push()

  def topJump(self):
    """Returns the next jump"""
    return self.jumps.top()

  def getAvail(self):
    """Returns the next available memory slot"""
    return self.avail.pop()

  def addFunc(self, funcId, funcType, funcSignature):
    """Adds function to context and to funciones dict"""
    self.funcContext.push(funcId)
    self.funciones[funcId] = Function(funcId, funcType, funcSignature)

  def addVar(self, varId, varType, varValue):
    """Adds variable to var dict of the corresponding Function (according to funcContext)"""
    self.funciones[self.funcContext.top()].addVar(varId, varType, varValue)

  def addQuad(self, op, left, right, dest):
    """Adds Quad to the cuadruplos list"""
    self.cuadruplos.append(Quad(op, left, right, dest))