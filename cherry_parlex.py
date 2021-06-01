import logging
from lark import Lark, logger, exceptions
from pathlib import Path
from cherry_transformer import *
from cherry_compiler import *
from Memory import *
from Quad import *
from utils import *
import os
import sys
import pickle
logger.setLevel(logging.DEBUG)

"""
For parent dir use

code = open(os.path.join(os.path.dirname(__file__), os.pardir, 'folder/code.cherry'))
"""
code = open(os.path.join(os.path.dirname(__file__), 'code.cherry')).read()
compiler = Compiler()
 # Contiene el compilador

l = Lark.open('cherry.lark', parser='lalr', debug=False, propagate_positions=True)
try:
  tree = l.parse(code)
  #print( tree )
  transformer = PassiveSyntax(compiler)
  transformer.transform(tree)
  print(compiler.operadores, compiler.operandos, compiler.tipos, compiler.funciones, compiler.cuadruplos, compiler.jumps, compiler.funcContext.top(), sep='\n')
  # for const in [compiler.constantes[idx] for idx in compiler.constantes]:
  #   print(compiler.memory[const['addr']], const['type'])
  with open("memory_log.txt", 'w') as f:
    print(compiler.memory, file = f)
except exceptions.UnexpectedInput as e:
  print("Error at line " + str(e.line) + ".\nInvalid syntax.")
except exceptions.VisitError as e:
  print(e.orig_exc)




# MVP
# Create Machine class
# Add Run method that receives file
# Add Start method for user input
# Compiler outputs a dict
"""
out = {
  constantes: compiler.constantes,
  funciones : compiler.funciones,
  cuadruplos : compiler.cuadruplos
}
"""

class Machine(object):
  def __init__(self):
    self.compiler = Compiler()
    self.mem = 2000
    self.memTemp = 1000
    self.memConst = 1000
    self.memory = Memory('Memory', self.mem, self.memTemp, self.memConst)
    self.source = 'code.cherry'
    self.line = 0
    self.funcContext = Stack('Contexto')
    self.funcContext.push('Global')
    self.constantes = None
    self.compSizeL = ["<", "<=", ">", ">="]
    self.compContL = ["==", "!="] 
    self.exprOps = ["*", "/", "+", "-", "not", "and", "or"] + self.compSizeL + self.compContL

  def compile(self):
    lexer = Lark.open('cherry.lark', parser='lalr', debug=False, propagate_positions=True)
    code = open(os.path.join(os.path.dirname(__file__), self.source)).read()
    try:
      tree = l.parse(code)
      transformer = PassiveSyntax(self.compiler)
      transformer.transform(tree)
      self.compiler.compile(self.source[:-7])
    except exceptions.UnexpectedInput as e:
      print("Error at line " + str(e.line) + ".\nInvalid syntax.")
    except exceptions.VisitError as e:
      print(e.orig_exc)
  
  def openObj(self):
    filename = os.path.join(os.path.dirname(__file__), self.source[:-7] + '.pkl')
    with open(filename, 'rb') as input:
      return pickle.load(input)
    #os.remove(filename)
  
  def readAddr(self, addr):
    """
    G# -> removes G self.memoria[int(#)]
    (#) -> removes (), then double access self.memoria[self.memoria[int(#)]]
    # -> self.memoria[#]
    """
  def retrieve(self, left, right, dest):
    lVal = readAddr(left)
    lType = self.constantes[lVal]['type']
    lVal = convert(lVal, lType)
    rVal = readAddr(right)
    rType = self.constantes[rVal]['type']
    rVal = convert(rVal, rType)
    destAddr = readAddr(dest)
    return lVal, lType, rVal, rType, destAddr
    
  def instrSwitch(self, op, left, right, dest):
    """"""
    if op == "=":
      """"""
      self.memory[dest] = self.memory[left]
    elif op in self.exprOps:
      if op == '*':
        """
        string int repeatStr
        """
        lVal, lType, rVal, rType, destAddr = self.retrieve(left, right, dest)
        if lType == 'CTE_STRING':
          result = repeatStr(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
      elif op == '+':
        """
        file string appendStrtoFile
        file file appendFile
        """
        lVal, lType, rVal, rType, destAddr = self.retrieve(left, right, dest)
        if lType == 'CTE_FILE':
          if rType == 'CTE_STRING':
            result = appendStrtoFile(lVal, rVal)
          else:
            result = appendFile(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
      elif op == '-':
        """
        string string removeStrfromStr
        file string removeStrfromFile
        """
        lVal, lType, rVal, rType, destAddr = self.retrieve(left, right, dest)
        if lType == 'CTE_STRING':
          result = removeStrfromStr(lVal, rVal)
        elif lType == 'CTE_FILE':
          result = removeStrfromFile(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
      elif op in self.compSizeL:
        """
        str str compareString
        file file compareFilesSize
        """
        lVal, lType, rVal, rType, destAddr = self.retrieve(left, right, dest)
        if lType == 'CTE_STRING':
          result = compareString(lVal, rVal)
        elif lType == 'CTE_FILE':
          result = compareFilesSize(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
      elif op in self.compContL:
        """
        file file compareFilesContent
        """
        lVal, lType, rVal, rType, destAddr = self.retrieve(left, right, dest)
        if lType == 'CTE_FILE':
          result = compareFilesContent(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
      elif op == 'not':
        """
        bool evaluate
        """
        lVal = readAddr(left)
        lType = self.constantes[lVal]['type']
        lVal = convert(lVal, lType)
        destAddr = readAddr(dest)
        result = evaluate(op, lVal)
        self.memory[destAddr] = result
    elif op == 'VER':
      """"""
    elif op == 'PRINT':
      """"""
    elif op == 'GOTO':
      """"""
    elif op == 'GOTOF':
      """"""
    elif op == 'ERA':
      """
      """
    elif op == 'PARAM':
      """"""
    elif op == 'GOSUB':
      """"""
    elif op == 'RETURN':
      """
      pasa valores de un contexto a otro
      busca var 1func e iguala contenidos
      """
    elif op == 'RETURNSTART':
      """
      RETURN FOR ARRAY
      continua hasta llegar a RETURNEND
      pasa valores de un contexto a otro
      busca var 1func e iguala contenidos
      """


  def run(self):
    if len(sys.argv) != 2:
      print("Was expecting 1 file to compile, received", len(sys.argv) - 1, ".")
    else:
      self.source = sys.argv[1]
      self.compile()
      pickleDict = self.openObj()
      # Llenar info de constantes
      self.constantes = pickleDict['constantes']
      for constante in self.constantes:
        self.memory[self.constantes[constante]['addr']] = constante
      """"""
      while pickleDict['cuadruplos'][self.line].op != "ENDPROG":
        self.instrSwitch(pickleDict['cuadruplos'][line].op, pickleDict['cuadruplos'][line].left, pickleDict['cuadruplos'][line].right, pickleDict['cuadruplos'][line].dest)
    # RUN


# if __name__ == "__main__":
#   machine = Machine()
#   machine.run()
