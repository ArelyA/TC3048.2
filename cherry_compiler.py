from Stack import *
from Function import Function
from Quad import *
from Queue import *
from List import *
from Memory import *
from utils import convert
import dill 
import os

class Compiler(object):
  def __init__(self, mem = 2000, memTemp = 1000, memConst = 1000):
    
    self.operadores = Stack('Operadores')
    self.operandos = Stack('Operandos')
    self.tipos = Stack('Tipos')
    self.jumps = Stack('Jumps')
    self.funciones = {}
    self.funcContext = Stack('Contexto')
    self.cuadruplos = List('Cuadruplos')
    self.idx = 0
    self.lines = []
    self.mem = mem
    self.memTemp = memTemp
    self.memConst = memConst
    self.memory = Memory('Memory', self.mem, self.memTemp, self.memConst)
    self.constantes = {}
    self.reservadas = ["def", "read", "write", "print", "in", "for", "if", "else", "while", "len", "norm", "clean", "find", "range", "count", "size", "join", "append", "create", "delete"]
    self.addFunc('Global')

  def fill(self, jmp = None, idx = None):
    if jmp == None:
      jmp = self.popJump()
    if idx == None:
      idx = self.idx
    self.cuadruplos[jmp].dest = idx

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

  def pushJump(self, jmp = None):
    """Removes the next jump"""
    if jmp == None:
      jmp = self.idx
    self.jumps.push(jmp)

  def topJump(self):
    """Returns the next jump"""
    return self.jumps.top()
  
  def addConst(self, constId, constType):
    constVar = self.constantes.get(str(constId), None)
    
    if(constVar == None):
      constAddr = self.memory.popConst()
      self.constantes[str(constId)] = {"addr": constAddr, "type": constType}
      self.memory[constAddr] = convert(constId, constType)
    else:
      constAddr = constVar['addr']

    return constAddr
  
  def getFunc(self, funcId):
    return self.funciones.get(funcId, None)

  def addFunc(self, funcId):
    """Adds function to context and to funciones dict"""
    if funcId in self.reservadas:
      raise ValueError("Invalid method identifier")
    if(self.funciones.get(funcId, None) == None):
      self.funcContext.push(funcId)
      addr = self.memory.popAvail(0)
      tempAddr = self.memory.popTemp(0) - self.mem
      self.funciones[funcId] = Function(funcId, (0 if addr < 0 else addr), (0 if tempAddr < 0 else tempAddr))
    else:
      raise RuntimeError("Cannot define method more than once")
  
  def addParam(self, paramId):
    self.funciones[self.funcContext.top()].addParam(paramId)

  def setFuncTipo(self, funcType):
    if self.funcContext.top() == 'Global':
      raise SyntaxError("Return does not belong to a function.")
    currentType = self.funciones[self.funcContext.top()].getType()
    if currentType != None:
      if currentType != funcType:
        raise SyntaxError("Returns must be of the same type.")
    self.funciones[self.funcContext.top()].setType(funcType)
  
  def popAvail(self, index = 1):
    self.funciones[self.funcContext.top()].incrementA(index)
    return self.memory.popAvail(index)
  
  def popTemp(self, index = 1):
    self.funciones[self.funcContext.top()].incrementT(index)
    return self.memory.popTemp(index)
  
  def setFuncIp(self):
    self.funciones[self.funcContext.top()].setIp(self.idx)

  def release(self):
    """
    Releases memory used by function and removes it from current context
    """
    funcId = self.funcContext.top()
    func = self.funciones[funcId]
    self.memory.release(func.addr, func.addrTemp)
    self.funcContext.pop()
    return func
  
  def getContexto(self):
    return self.funcContext.top()

  def addVar(self, varId, varType, elem = 1):
    """Adds variable to var dict of the corresponding Function (according to funcContext)"""
    var = self.funciones[self.funcContext.top()].getVar(varId)
    if(var == None):
      varAddr = self.popAvail(elem) - self.funciones[self.funcContext.top()].addr # guarda direcciones locales
      self.funciones[self.funcContext.top()].addVar(varId, varType, varAddr, elem)
    elif var.getType() == None:
      var.setType(varType)
      varAddr = var.getAddr()
    elif var.getType() == varType:
      varAddr = var.getAddr()
    else:
      raise TypeError("Type-Mismatch: " + varType + " cannot be assigned to " +  var.getType())
    return varAddr
  
  def addVarArr(self, tipo, elems):
    """Adds variable to store ARRAYS"""
    varAddr = self.popTemp(elems) - self.funciones[self.funcContext.top()].addrTemp
    self.funciones[self.funcContext.top()].addVar(str(varAddr), tipo, varAddr, elems)
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
    return self.popTemp() - self.funciones[self.funcContext.top()].addrTemp

  def addQuad(self, op, left, right, addr):
    """Adds Quad to the cuadruplos list"""
    self.cuadruplos.append(Quad(op, left, right, addr))
    self.idx += 1
  
  def compile(self, name):
    filename = os.path.join(os.path.dirname(__file__) + '/', name + '.pkl')
    with open(filename, 'wb') as output:
      dill.dump(self.constantes, output, -1)
      dill.dump(self.funciones, output, -1)
      for quad in self.cuadruplos:
        dill.dump(quad, output, -1)