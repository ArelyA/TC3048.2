import logging
from lark import Lark, logger, exceptions
from pathlib import Path
from Function import Function
from cherry_transformer import *
from cherry_compiler import *
from Memory import *
from Quad import *
from List import *
from utils import *
from SemanticCube import *
import os
import sys
import dill 
logger.setLevel(logging.DEBUG)

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
    #self.compiler = Compiler()
    self.mem = 2000
    self.memTemp = 1000
    self.memConst = 1000
    self.memory = Memory('Memory', self.mem, self.memTemp, self.memConst)
    self.source = 'code.cherry'
    self.line = 0
    self.end = " "
    self.returnV = None
    self.isReturn = False
    self.crumbs = Stack('Crumbs')
    self.funcContext = Stack('Contexto')
    self.funcContext.push('Global')
    self.constantes = None
    self.funciones = None
    self.cuadruplos = List('Cuadruplos')
    self.compSizeL = ["<", "<=", ">", ">="]
    self.compContL = ["==", "!="] 
    self.exprOps = ["*", "/", "+", "-", "not", "and", "or"] + self.compSizeL + self.compContL
    self.createTempsFolder()

  def createTempsFolder(self):
    path = os.path.join(os.path.dirname(__file__) + "/", "tmp")
    try:
      os.mkdir(path)
    except OSError:
      """print ("Creation of the directory %s failed" % path)"""
    else:
      """print ("Successfully created the directory %s " % path)"""

  def deleteTempsFolder(self):
    path = os.path.join(os.path.dirname(__file__) + "/", "tmp")
    try:
      shutil.rmtree(path)
    except OSError as e:
      """print ("Deletion of the directory %s failed" % path)"""
    else:
      """print ("Successfully deleted the directory %s" % path)"""

  def compile(self):
    lexer = Lark.open('cherry.lark', parser='lalr', debug=False, propagate_positions=True, postlex=TreeIndenter())
    code = open(os.path.join(os.path.dirname(__file__), self.source)).read()
    
    try:
      compiler = Compiler(self.mem, self.memTemp, self.memConst)
      tree = lexer.parse(code)
      transformer = PassiveSyntax(compiler)
      transformer.transform(tree)
      compiler.compile(self.source[:-7])
      
    except exceptions.UnexpectedInput as e:
      print("Error at line " + str(e.line) + ".\nInvalid syntax.")
      raise e
    except exceptions.VisitError as e:
      raise e
    
  
  def openObj(self):
    filename = os.path.join(os.path.dirname(__file__) + '/', self.source[:-7] + '.pkl')
    with open(filename, 'rb') as file:
      self.constantes = dill.load(file)
      self.funciones = dill.load(file)
      while True:
        try:
            self.cuadruplos.push(dill.load(file))
        except EOFError:
            break
    #os.remove(filename)
  
  def addrContext(self, addr):
    temp = self.memory.memSize
    if addr >= temp:
      addr = addr + self.funciones[self.funcContext.top()].addrTemp
    else:
      addr = addr + self.funciones[self.funcContext.top()].addr
    return addr
  
  def getFilename(self, filename):
    try:
      index = filename.rindex('/')
      filename_temp = filename[index:]
    except:
      filename_temp = filename
    return filename_temp
  
  def readAddr(self, addr):
    """
    G# 
    
    addr = int(#)
    # --------

    (#) 
    
    addr = addrContext(self.memoria[int(#)])
    
    \# 
    
    addr = addrContext(#)
    """
    if isinstance(addr, str):
      
      if addr[0] == 'G':
        """
        G#
        """
        addr = int(addr[1:])
      elif addr[0] == '(':
        """
        (#)
        """
        addr = self.addrContext(self.memory[int(addr[1:-1])])
      else:
        """
         #
        """
        addr = self.addrContext(int(addr))
    
    return addr
  
  def retrieveSingle(self, val):
    """"""
    try:
      lVal = self.memory[self.readAddr(val)]
      lType = self.constantes[lVal]['type']
      lVal = convert(lVal, lType)
    except:
      lVal = self.memory[self.readAddr(val)]
      lType = None
    return lVal, lType

  def tempFile(self, filename):
    dir = os.path.dirname(__file__) + '/'
    fPathTemp = dir + "tmp" + self.getFilename(filename)
    fTemp = tempName(fPathTemp)
    copyFile(filename, fTemp)
    fAddr = self.addConst(fTemp, 'CTE_FILE')
    return fTemp
  
  def addConst(self, constId, constType):
    constVar = self.constantes.get(str(constId), None)
    
    if(constVar == None):
      constAddr = self.memory.popConst()
      self.constantes[str(constId)] = {"addr": constAddr, "type": constType}
      self.memory[constAddr] = convert(constId, constType)
    else:
      constAddr = constVar['addr']

    return constAddr

  def instrSwitch(self, op, left, right, dest):
    """"""
    if op == "=":
      """"""
      lAddr = self.readAddr(left)
      destAddr = self.readAddr(dest)
      self.memory[destAddr] = self.memory[lAddr]
      self.line += 1
    elif op in self.exprOps:
      if op == '*':
        """
        string int repeatStr
        """
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        destAddr = self.readAddr(dest)
        if lType == 'CTE_STRING':
          result = repeatStr(lVal, rVal)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
        self.line += 1
      elif op == '+':
        """
        file string appendStrtoFile
        file file appendFile
        """
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        destAddr = self.readAddr(dest)
        if lType == 'CTE_FILE':
          self.addConst(lVal, 'CTE_FILE')
          lValTemp = self.tempFile(lVal)
          if rType == 'CTE_STRING':
            appendStrtoFile(lValTemp, rVal)
            result = lValTemp
          else:
            self.addConst(rVal, 'CTE_FILE')
            appendFile(rVal, lValTemp)
            result = lValTemp
          self.line += 1
        else:
          result = evaluate(op, lVal, rVal)
          self.line += 1
        self.memory[destAddr] = result
        if self.isReturn:
          self.returnV = "(" + str(result) + ")"
      elif op == '-':
        """
        string string removeStrfromStr
        file string removeStrfromFile
        """
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        destAddr = self.readAddr(dest)
        if lType == 'CTE_STRING':
          result = removeStrfromStr(lVal, rVal)
        elif lType == 'CTE_FILE':
          self.addConst(lVal, 'CTE_FILE')
          lValTemp = self.tempFile(lVal)
          removeStrfromFile(lValTemp, rVal)
          result = lValTemp
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
        self.line += 1
      elif op in self.compSizeL:
        """
        str str compareString
        file file compareFilesSize
        """
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        destAddr = self.readAddr(dest)

        if lType == 'CTE_STRING':
          result = compareString(lVal, rVal, op)
        elif lType == 'CTE_FILE':
          self.addConst(lVal, 'CTE_FILE')
          self.addConst(rVal, 'CTE_FILE')
          result = compareFilesSize(lVal, rVal, op)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
        self.line += 1
      elif op in self.compContL:
        """
        file file compareFilesContent
        """
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        destAddr = self.readAddr(dest)
        if lType == 'CTE_FILE':
          self.addConst(lVal, 'CTE_FILE')
          result = compareFilesContent(lVal, rVal, op)
        else:
          result = evaluate(op, lVal, rVal)
        self.memory[destAddr] = result
        self.line += 1
      elif op == 'not':
        """
        bool evaluate
        """
        lVal, lType = self.retrieveSingle(left)
        destAddr = self.readAddr(dest)
        result = evaluate(op, lVal)
        self.memory[destAddr] = result
        self.line += 1
    elif op == 'VER':
      """
      VER, left, right, dest
      left = idx
      right = Linf
      dest = LSup
      """
      lVal, lType = self.retrieveSingle(left)
      rVal, rType = self.retrieveSingle(right)
      dVal, dType = self.retrieveSingle(dest)

      if lVal >= rVal and lVal < dVal:
        self.line += 1
        if self.isReturn:
          self.returnV = None
      else:
        print("Index out of range.")
        self.line = len(self.cuadruplos) - 1

    elif op == 'PRINT':
      """"""
      if dest == '[':
        print(dest, end = self.end)
        self.end = ","
      elif dest == ']':
        self.end = " "
        print(dest, end = self.end)
      elif dest == "\n":
        print("\n", end = "")
      else:
        dVal, dType = self.retrieveSingle(dest)
        if dType == 'CTE_FILE':
          printFile(dVal)
          print("", end = self.end)
        else:
          print(dVal, end = self.end)
      self.line += 1
    elif op == 'GOTO':
      """
      GOTO, , , dest
      """
      self.line = dest
    elif op == 'GOTOF':
      """
      GOTOF, left, , dest
      """
      lVal, lType = self.retrieveSingle(left)
      
      result = evaluate('==', lVal, False)

      if result:
        self.line = dest
      else:
        self.line += 1
    elif op == 'ERA':
      """
      self.funcContext.push(left)
      func = self.funciones[left]
      addr = self.memory.popAvail(0)
      tempAddr = self.memory.popTemp(0) - self.mem
      func.addr = addr
      func.addrTemp = addrTemp
      self.memory.popAvail(func.sizeA)
      self.memory.popTemp(func.sizeT)
      """
    elif op == 'PARAM':
      """
      func = self.funciones[self.funcContext.top()]
      # type, dims, addr
      param = func.getSignature()[right]
      paramType = param.getType()
      paramAddr = param.getAddr()
      paramDims = param.getDimensions()
      pVal = self.readAddr(paramAddr)
      currentContext = self.funcContext.pop()
      lVal = self.readAddr(left)
      self.funcContext.push(currentContext)
      if paramDims == None:
        self.memory[pVal] = self.memory[lVal]
      else:
        for idx in range(paramDims.sup):
          self.memory[pVal + idx] = self.memory[lVal + idx]
      """
    elif op == 'GOSUB':
      """
      self.crumbs.push(self.line + 1)
      self.line = self.funciones[self.funcContext.top()].getIp()
      """
    elif op == 'ENDFUNC':
      """
      func = self.funciones[self.funcContext.top()]
      self.memory.release(func.addr, func.addrTemp)
      self.funcContext.pop()
      self.line = self.crumbs.pop()
      """
    elif op == 'RETURN':
      """
      pasa valores de un contexto a otro
      busca var 1func e iguala contenidos
      """
      addr = self.readAddr(self.funciones[self.funcContext.top()].getReturnAddr())
      destAddr = self.readAddr(dest)
      self.memory[addr] = self.memory[destAddr]
      print("RETURN")
      self.line += 1
    elif op == 'RETURNSTART':
      """
      RETURN FOR ARRAY
      continua hasta llegar a RETURNEND
      pasa valores de un contexto a otro
      busca var 1func e iguala contenidos
      idx = 0
      """
      idx = 0
      self.isReturn = True
      addr = self.readAddr(self.funciones[self.funcContext.top()].getReturnAddr())
      while self.cuadruplos[self.line].op != "RETURNEND":
        print('RETURNSTART', self.cuadruplos[self.line].op)
        self.instrSwitch(self.cuadruplos[self.line].op, self.cuadruplos[self.line].left, self.cuadruplos[self.line].right, self.cuadruplos[self.line].dest)
        if self.ReturnV != None:
          self.memory[addr + idx] = self.memory[self.readAddr(self.returnV) + idx]
          idx += 1
      print('RETURNEND', self.cuadruplos[self.line].op)
      self.line += 1
      self.isReturn = False
    elif op == 'WRITE':
      """
      WRITE, left, , dest
      left = filenameIN
      dest = filenameOUT
      """
      filenameIN, lType = self.retrieveSingle(left)
      filenameOUT, dType = self.retrieveSingle(dest)
      copyFile(filenameIN, filenameOUT)
      self.line += 1
    elif op == 'READ':
      """
      READ, left, , dest
      left = type
      dest = dest
      """
    elif op == 'SIZE':
      """
      SIZE, left, , dest
      left = filename
      """
    elif op == 'LEN':
      """"""
    elif op == 'COUNT':
      """"""
    elif op == 'GETLINE':
      """"""
    elif op == 'GETWORD':
      """"""
    elif op == 'FIND':
      """"""
    elif op == 'SUBSTR':
      """"""
    elif op == 'CLEAN':
      """"""
    elif op == 'NORM':
      """"""
    elif op == 'APPEND':
      """"""
    else:
      print("Unknown instruction " + op)
      self.line = len(self.cuadruplos) - 1

  def restoreConstantes(self):
    self.memory.popConst(len(self.constantes))
    for constante in self.constantes:
        self.memory[self.constantes[constante]['addr']] = constante
  
  def restore(self):
    self.openObj()
    self.restoreConstantes()

  def run(self):
    if len(sys.argv) != 2:
      print("Was expecting 1 file to compile, received", len(sys.argv) - 1, ".")
    else:
      try:
        self.source = sys.argv[1]
        self.compile()
        self.restore()
        self.memory.popAvail(self.funciones[self.funcContext.top()].sizeA)
        self.memory.popTemp(self.funciones[self.funcContext.top()].sizeT)
        """"""
        print(self.cuadruplos)
        with open("quad_log.txt", 'w') as f:
            print(self.cuadruplos, file = f)
        
        with open("func_log.txt", 'w') as f:
            print(self.funciones, file = f)
        
        while self.cuadruplos[self.line].op != "ENDPROG":
          # print(self.line)
          
          self.instrSwitch(self.cuadruplos[self.line].op, self.cuadruplos[self.line].left, self.cuadruplos[self.line].right, self.cuadruplos[self.line].dest)
          with open("memory_log.txt", 'w') as f:
            print(self.memory, file = f)
        print("ENDPROG")
        # except Exception as e:
        #   print(e)
        #   with open("memory_log.txt", 'w') as f:
        #     print(self.memory, file = f)

      except Exception as e:
        print(e)
    self.deleteTempsFolder()
    # RUN


if __name__ == "__main__":
  machine = Machine()
  machine.run()
