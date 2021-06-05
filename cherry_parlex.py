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
    self.funcContext = Stack('ContextoFunc')
    self.memContext = Stack('ContextoMem')
    self.constantes = None
    self.funciones = None
    self.cuadruplos = List('Cuadruplos')
    self.compSizeL = ["<", "<=", ">", ">="]
    self.compContL = ["==", "!="] 
    self.exprOps = ["*", "/", "+", "-", "not", "and", "or"] + self.compSizeL + self.compContL
    self.createTempsFolder()

  
  def restoreConstantes(self):
    self.memory.popConst(len(self.constantes))
    for tipo in self.constantes:
      for constante in self.constantes[tipo]:
        self.memory[self.constantes[tipo][constante]] = constante
        self.memory.popConst()
  
  def restore(self):
    self.openObj()
    self.restoreConstantes()
    self.funcContext.push('Global')
    self.saveMemContext()
    func = self.funciones['Global']
    self.memory.popAvail(func.sizeA)
    self.memory.popTemp(func.sizeT)
  
  def saveMemContext(self):
    func = self.funciones[self.funcContext.top()]
    self.memContext.push((func.addr, func.addrTemp))
  
  def restoreMemContext(self):
    old = self.memContext.pop()
    self.memory.release(old[0], old[1])
  
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
      # print(tree.pretty())
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
      addr = addr + self.memContext.top()[1]
    else:
      addr = addr + self.memContext.top()[0]
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
        return addr
      elif addr[0] == '(':
        """
        (#)
        """
        try:
          addr = self.readAddr(self.memory[int(addr[1:-1])])
        except:
          addr = self.readAddr(addr[1:-1])
        
      else:
        """
         #
        """
        addr = int(addr)

    if addr >= self.memory.tempMemLimit:
      return addr
    addr = self.addrContext(addr)
    return addr
  
  def retrieveSingle(self, val):
    """"""
    lVal = self.memory[self.readAddr(val)]
    for lType in self.constantes:
      lValT = self.constantes[lType].get(lVal, None)
      if lValT != None:
        lVal = convert(lVal, lType)
        return lVal, lType
    
    return lVal, None

  def tempFile(self, filename):
    dir = os.path.dirname(__file__) + '/'
    fPathTemp = dir + "tmp" + self.getFilename(filename)
    fTemp = tempName(fPathTemp)
    copyFile(filename, fTemp)
    fAddr = self.addConst(fTemp, 'CTE_FILE')
    return fTemp
  
  def addConst(self, constId, constType):
    "Adds constant to constants dictionary"
    constVar = self.constantes[constType].get(str(constId), None)
    
    if(constVar == None):
      constAddr = self.memory.popConst()
      self.constantes[constType][str(constId)] = constAddr
      self.memory[constAddr] = constId
    else:
      constAddr = constVar

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
        context = None
        if isinstance(rVal, str) and rType in ['CTE_INT', 'CTE_FLOAT']:
          rVal = int(rVal[1:])
          context = "G"
      
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
        result = context + str(result) if context != None else result
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
      elif op == '/':
        lVal, lType = self.retrieveSingle(left)
        rVal, rType = self.retrieveSingle(right)
        if lVal == 0 or rVal == 0:
          raise ZeroDivisionError("Cannor perform a division by zero.")
        destAddr = self.readAddr(dest)
        result = evaluate(op, lVal, rVal)
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
        raise IndexError("Index out of range.")
        self.line = len(self.cuadruplos) - 1

    elif op == 'PRINT':
      """"""

      if dest == '[':
        print(dest, end = "")
        self.end = ""
      elif dest == ']':
        print(dest, end = " ")
        self.end = " "
      elif dest == ',':
        print(dest, end = " ")
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
      ERA, left, , 
      """
      self.funcContext.push(left)
      func = self.funciones[left]
      addr = self.memory.popAvail(0)
      addrTemp = self.memory.popTemp(0) - self.mem
      func.addr = addr
      func.addrTemp = addrTemp
      self.memory.popAvail(func.sizeA)
      self.memory.popTemp(func.sizeT)
      self.saveMemContext()
      self.line += 1
    elif op == 'PARAM':
      """
      PARAM, ADDR, #,
      """
      func = self.funciones[self.funcContext.top()]
      # type, dims, addr
      param = func.getSignature()[right]
      paramType = param.getType()
      paramAddr = param.getAddr()
      paramDims = param.getDimensions()
      pVal = self.readAddr(paramAddr)
      currentContext = self.memContext.pop()
      lVal = self.readAddr(left)
      self.memContext.push(currentContext)
      if len(paramDims) == 0:
        self.memory[pVal] = self.memory[lVal]
      else:
        for dim in paramDims:
          for idx in range(dim.sup):
            self.memory[pVal + idx] = self.memory[lVal + idx]
      self.line += 1
    elif op == 'GOSUB':
      """
      GOSUB, funcId
      """
      self.crumbs.push(self.line + 1)
      self.line = self.funciones[left].getIp()
    elif op == 'ENDFUNC':
      """
      """
      self.funcContext.pop()
      self.restoreMemContext()
      self.line = self.crumbs.pop()
    elif op == 'RETURN':
      """
      pasa valores de un contexto a otro
      """
      addr = self.readAddr(self.funciones[self.funcContext.top()].getReturnAddr())
      destAddr = self.readAddr(dest)
      self.memory[addr] = self.memory[destAddr]
      self.line += 1
    elif op == 'RETURNSTART':
      """
      RETURN FOR ARRAY
      continua hasta llegar a RETURNEND
      pasa valores de un contexto a otro
      """
      idx = 0
      self.isReturn = True
      addr = self.readAddr(self.funciones[self.funcContext.top()].getReturnAddr())
      self.line += 1
      while self.cuadruplos[self.line].op != "RETURNEND":
        self.instrSwitch(self.cuadruplos[self.line].op, self.cuadruplos[self.line].left, self.cuadruplos[self.line].right, self.cuadruplos[self.line].dest)
        if self.returnV != None:
          self.memory[addr + idx] = self.memory[self.readAddr(self.returnV) + idx]
          idx += 1
    elif op == 'RETURNEND':
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
      var = input()
      destAddr = self.readAddr(dest)
      self.addConst(var, left)
      self.memory[destAddr] = convert(var, left)
      self.line += 1
      """"""
    else:
      print("Unknown instruction " + op)
      self.line = len(self.cuadruplos) - 1

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
        with open("quad_log.txt", 'w') as f:
          print(self.cuadruplos, file = f)
        
        with open("constini_log.txt", 'w') as f:
          print(self.constantes, file = f)
        
        with open("func_log.txt", 'w') as f:
          print(self.funciones, file = f)
          
        while self.cuadruplos[self.line].op != "ENDPROG":
          self.instrSwitch(self.cuadruplos[self.line].op, self.cuadruplos[self.line].left, self.cuadruplos[self.line].right, self.cuadruplos[self.line].dest)
          with open("memory_log.txt", 'w') as f:
            print(self.memory, file = f)

      except Exception as e:
        print(e)
        with open("memory_log.txt", 'w') as f:
          print(self.memory, file = f)

      self.deleteTempsFolder()
      with open("const_log.txt", 'w') as f:
        print(self.constantes, file = f)
    # RUN


if __name__ == "__main__":
  machine = Machine()
  machine.run()
