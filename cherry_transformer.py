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
    
  def factor_paren(self):
    self.compiler.pushOperador('(')
  
  def factor_paren_end(self):
    self.compiler.popOperador()

  def string_func(self, string):
    """Pushes string value to operandos and CTE_STRING type to tipos"""
    self.compiler.pushOperando(string.value)
    self.compiler.pushTipo(string.type)
    return string

  def bool_func(self, boo):
    """Pushes bool value to operandos and CTE_BOOL type to tipos"""
    self.compiler.pushOperando(boo.value)
    self.compiler.pushTipo(boo.type)
    return boo
  
  def int_func(self, intV):
    """Pushes int_func value to operandos and CTE_INT type to tipos"""
    self.compiler.pushOperando(intV.value)
    self.compiler.pushTipo(intV.type)
    return intV
  
  def float_func(self, fl):
    """Pushes float value to operandos and CTE_FLOAT type to tipos"""
    self.compiler.pushOperando(fl.value)
    self.compiler.pushTipo(fl.type)
    return fl

  def file_func(self, fi):
    """Pushes file value to operandos and CTE_FILE type to tipos"""
    self.compiler.pushOperando(fi.value)
    self.compiler.pushTipo(fi.type)
    return fi

  def term_func_op(self, op):
    self.compiler.pushOperador(op)
    return op

  def term_func(self):
    self.expression(self.termL, evaluate)

  def not_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def not_func(self):
    self.expression_not(self.notOpL, evaluate)

  def and_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def and_func(self):
    self.expression(self.andOpL, evaluate)
  
  def or_func_op(self, op):
    self.compiler.pushOperador(op)
    return op

  def or_func(self):
    self.expression(self.orOpL, evaluate)
  
  def exp_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def exp_func(self):
    self.expression(self.expL, evaluate)
  
  def comp_func_op(self, op):
    self.compiler.pushOperador(op)
    return op
  
  def comp_func(self):
    print("compareee", self.compiler.operandos)
    self.expression(self.compL, evaluate)
    
  def expression_not(self, lst, func):
    try:
      operador = self.compiler.topOperador()

      if(operador in lst):

        oper = self.compiler.popOperador()

        leftT = self.compiler.popTipo()

        left = convert(self.compiler.popOperando(), leftT)
        
        if(self.cube[oper][leftT] != False):
          self.expression_genQuad(oper, left, "")
          value = func(oper, left)
          
          self.compiler.pushOperando(str(value)) # replace with ADDR
          self.compiler.pushTipo(self.cube[oper][leftT])
        else:
          raise TypeError("Type-Mismatch: " + oper + " " + leftT)

    except IndexError:
      print("Empty pile.")

  def expression(self, lst, func):
    try:
      operador = self.compiler.topOperador()

      if(operador in lst):

        oper = self.compiler.popOperador()

        rightT = self.compiler.popTipo()
        leftT = self.compiler.popTipo()

        right = convert(self.compiler.popOperando(), rightT)
        left = convert(self.compiler.popOperando(), leftT)

        oper_cube = 'comp' if oper in self.compL else 'compao' if oper in self.compaoFunctL else oper
        print(self.cube[oper_cube][leftT][rightT])
        print(oper_cube, oper, leftT, rightT)
        if(self.cube[oper_cube][leftT][rightT] != False):
          self.expression_genQuad(oper, left, right)
          value = func(oper, left, right)
          
          self.compiler.pushOperando(str(value)) # replace with ADDR
          self.compiler.pushTipo(self.cube[oper_cube][leftT][rightT])
        else:
          raise TypeError("Type-Mismatch: " + leftT + " " + oper + " " + rightT)

    except IndexError:
      print("Empty pile.")

  def expression_genQuad(self, op, left, right):
    self.compiler.addQuad(op, left, right)

  # def def_func_name(self, funcName):
  #   self.compiler.addFunc(funcName)
  #   return funcName
  
  # def def_func_param(self, paramName):
  #   self.compiler.addParam(paramName)
  #   return paramName
  
  # def def_func_type(self):
  #   self.compiler.setTipo(self.compiler.topTipo())

  def asign_simp_func(self, id, opt):
    self.compiler.addVar(id.value, self.compiler.topTipo(), None)
    self.compiler.addQuad('=', id.value, self.compiler.popOperando())
    
    return id, opt