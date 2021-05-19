import logging
from lark import Lark, logger
from pathlib import Path
from cherry_transformer import *
from cherry_compiler import *

logger.setLevel(logging.DEBUG)

compiler = Compiler()
transformer = PassiveSyntax(compiler) # Contiene el compilador

l = Lark.open('cherry.lark', parser='lalr', debug=False, transformer= transformer)

print( l.parse("""a = -2""") ) 