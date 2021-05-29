import logging
from lark import Lark, logger
from pathlib import Path
from cherry_transformer import *
from cherry_compiler import *
import os

logger.setLevel(logging.DEBUG)

"""
For parent dir use

code = open(os.path.join(os.path.dirname(__file__), os.pardir, 'folder/code.cherry'))
"""
code = open(os.path.join(os.path.dirname(__file__), 'code.cherry')).read()
compiler = Compiler()
transformer = PassiveSyntax(compiler) # Contiene el compilador

l = Lark.open('cherry.lark', parser='lalr', debug=False, transformer= transformer)
tree = l.parse(code)
print( tree )

print(compiler.operadores, compiler.operandos, compiler.tipos, compiler.funciones, compiler.cuadruplos, sep='\n')
with open("memory_log.txt", 'w') as f:
  print(compiler.memory, file = f)
# MVP
# Create Machine class
# Add Run method that receives file
# Add Start method for user input
