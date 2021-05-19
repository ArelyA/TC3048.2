from lark import Transformer, v_args
from cherry_compiler import *

@v_args(inline=True)
class PassiveSyntax(Transformer):
  def __init__(self, compiler):
    self.compiler = compiler
  def factor_func(self, op, var):
    print(op, var)
    return op, var
  def asign_simp_func(self, id, op, opt):
    print(id, op, opt)
    return id, op, opt