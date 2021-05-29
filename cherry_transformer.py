from lark import Transformer, v_args
from cherry_compiler import *
from utils import *
from SemanticCube import *

@v_args(inline=True)
class PassiveSyntax(Transformer):
  def __init__(self, compiler):
    self.compiler = compiler
    self.termL = ["*", "/"]
    self.expL = ["+", "-"]
    self.compL = ["<", "<=", ">", ">=", "==", "!="]
    self.notOpL = ["not"]
    self.andOpL = ["and"] 
    self.orOpL = ["or"] 
    self.compaoFunctL = self.orOpL + self.andOpL
    self.cube = SemanticCube
  
  def string_func(self, string):
    """Pushes string value to operandos and CTE_STRING type to tipos"""
    self.compiler.pushOperando(string.value)
    self.compiler.pushTipo(string.type)
    return string

  def bool_func(self, boo):
    """Pushes bool value to operandos and CTE_BOOL type to tipos"""
    constAddr = self.compiler.addConst(boo.value, convert(boo.value, boo.type))
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(boo.type)
    return boo
  
  def int_func(self, intV):
    """Pushes int_func value to operandos and CTE_INT type to tipos"""
    constAddr = self.compiler.addConst(intV.value, convert(intV.value, intV.type))
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(intV.type)
    return intV
  
  def float_func(self, fl):
    """Pushes float value to operandos and CTE_FLOAT type to tipos"""
    constAddr = self.compiler.addConst(fl.value, convert(fl.value, fl.type))
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(fl.type)
    return fl

  def file_func(self, fi):
    """Pushes file value to operandos and CTE_FILE type to tipos"""
    constAddr = self.compiler.addConst(fi.value, convert(fi.value, fi.type))
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(fi.type)
    return fi

  def id_func(self, id):
    self.compiler.pushOperando(id.value)
    self.compiler.pushTipo(id.type)
    return id

  def factor_paren(self):
    self.compiler.pushOperador('(')
  
  def factor_paren_end(self):
    self.compiler.popOperador()

  def term_func_op(self, op):
    self.compiler.pushOperador(op)
    return op

  def term_func(self):
    self.expression(self.termL)

  def not_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def not_func(self):
    self.expression_not(self.notOpL)

  def and_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def and_func(self):
    self.expression(self.andOpL)
  
  def or_func_op(self, op):
    self.compiler.pushOperador(op)
    return op

  def or_func(self):
    self.expression(self.orOpL)
  
  def exp_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def exp_func(self):
    self.expression(self.expL)
  
  def comp_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def comp_func(self):
    self.expression(self.compL)
    
  def expression_not(self, lst):
    try:
      operador = self.compiler.topOperador()

      if(operador in lst):

        oper = self.compiler.popOperador()

        leftT = self.compiler.popTipo()

        left = self.compiler.popOperando()
        
        if(self.cube[oper][leftT] != False):
          addr = self.expression_genQuad(oper, left, "")
          
          self.compiler.pushOperando(addr)
          self.compiler.pushTipo(self.cube[oper][leftT])
        else:
          raise TypeError("Type-Mismatch: " + oper + " " + leftT)

    except IndexError:
      """print("Empty pile.")"""

  def expression(self, lst):
    try:
      operador = self.compiler.topOperador()

      if(operador in lst):

        oper = self.compiler.popOperador()

        rightT = self.compiler.popTipo()
        leftT = self.compiler.popTipo()

        right = self.compiler.popOperando()
        left = self.compiler.popOperando()

        oper_cube = 'comp' if oper in self.compL else 'compao' if oper in self.compaoFunctL else oper

        if(self.cube[oper_cube][leftT][rightT] != False):

          addr = self.expression_genQuad(oper, left, right)

          self.compiler.pushOperando(addr)
          self.compiler.pushTipo(self.cube[oper_cube][leftT][rightT])
        else:
          raise TypeError("Type-Mismatch: " + leftT + " " + oper + " " + rightT)

    except IndexError:
      """print("Empty pile.")"""

  def expression_genQuad(self, op, left, right):
    addr = self.compiler.getTemp()
    self.compiler.addQuad(op, left, right, addr)
    return addr
  
  def addr_genQuad(self, op, left, right):
    addr = self.compiler.getTemp()
    self.compiler.addQuad(op, left, right, "(" + str(addr) + ")")
    return "(" + str(addr) + ")"

  # def def_func_name(self, funcName):
  #   self.compiler.addFunc(funcName)
  #   return funcName
  
  # def def_func_param(self, paramName):
  #   self.compiler.addParam(paramName)
  #   return paramName
  
  # def def_func_type(self):
  #   self.compiler.setTipo(self.compiler.topTipo())

  def id_simp(self, id):
    self.compiler.pushOperando(id.value)
    self.compiler.pushTipo(id.type)
    return id
  def getElem(self, var, pos):
    """"""
    self.compiler.addQuad('ver', pos, 0, var.getDimensions()[0].sup)
    addrOff = self.expression_genQuad('+', pos, var.getAddr())
    addrElem = self.addr_genQuad('=', addrOff, "")
    return addrElem

  def asign_it(self, varLeft, varRight):
    for idx in range(varRight.getDimensions()[0].sup):
      constAddr = self.compiler.addConst(idx, convert(idx, 'CTE_INT'))
      leftElem = self.getElem(varLeft, constAddr)
      rightElem = self.getElem(varRight, constAddr)
      #constAddr = self.compiler.addConst(elem, convert(elem, varLeft.getType()))
      self.compiler.addQuad('=', rightElem, "", leftElem)

  def asign_simp_func(self):
    rightT = self.compiler.popTipo()
    leftT = self.compiler.popTipo()

    right = self.compiler.popOperando()
    left = self.compiler.popOperando()

    rVar = None
    #lVar = None

    if rightT == 'ID':
      rVar = self.compiler.getVar(right)
      if rVar == None:
        rVar = self.compiler.getVarG(right)
        if rVar == None:
          raise NameError("Name not found")
        else:
          right = "G" + str(rVar.getAddr())
      else:
        right = rVar.getAddr()
      rightT = rVar.getType()

    if leftT == 'ID':
      lVar = self.compiler.getVarG(left)
      if lVar == None:
        addr = self.compiler.addVar(left, rightT)
        if rVar != None:
          rDims = rVar.getDimensions()
          if len(rDims) > 0:
            lVar = self.compiler.getVar(left)
            lVar.addDimension(rDims[0].inf, rDims[0].sup)
            self.asign_it(lVar, rVar)
            return
      else:
        addr = "G" + str(lVar.getAddr())
        if rVar != None:
          if rVar.getDimensions() == lVar.getDimensions():
            self.asign_it(lVar, rVar)
            return
      self.compiler.addQuad("=", right, "", addr)
    else:
      raise SyntaxError("Cannot assign to literal")

  def var_it_fondo(self):
    if self.compiler.topTipo() != 'ID':
      self.compiler.pushOperando(self.compiler.addVarTemp())
      self.compiler.pushTipo('ID')
    self.compiler.pushOperando("[")
    self.compiler.pushTipo("[")
  
  def var_it_asign(self):
    stackElem = Stack("array")
    tipo = None
    while(self.compiler.topOperando() != "["):
      if tipo == None:
        tipo = self.compiler.popTipo()
      else:
        if tipo != self.compiler.popTipo():
          raise TypeError("Type-Mismatch: Elements must be of the same type.")
      stackElem.push(self.compiler.popOperando())
    self.compiler.popOperando()
    self.compiler.popTipo()
    if self.compiler.popTipo() == 'ID':
      # TODO 
      # REVISAR SI EXISTE LOCAL
      # REVISAR SI EXISTE GLOBAL
      # REVISAR QUE SEA IT
      varId = self.compiler.popOperando()
      var = self.compiler.getVar(varId)
      if var == None:
        var = self.compiler.getVarG(varId)
        if var == None: # No es global
          _ = self.compiler.addVar(varId, tipo)
          var = self.compiler.getVar(varId)
      
      upper = len(stackElem)
      var.addDimension(0, upper)
      for idx, elem in enumerate(stackElem):
        constAddr = self.compiler.addConst(idx, convert(idx, 'CTE_INT'))
        self.compiler.addQuad('ver', constAddr, 0, upper)
        addrOff = self.expression_genQuad('+', constAddr, var.getAddr())
        addrElem = self.addr_genQuad('=', addrOff, "")
        constAddr = self.compiler.addConst(elem, convert(elem, tipo))
        self.compiler.addQuad('=', constAddr, "", addrElem)
      self.compiler.pushOperando(varId)
    else:
      raise SyntaxError("Cannot assign to literal")
  
  
