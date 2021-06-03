from lark import Transformer, v_args
from lark.indenter import Indenter
from cherry_compiler import *
from utils import *
from SemanticCube import *

class TreeIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

@v_args(meta=True)
class PassiveSyntax(Transformer):
  def __init__(self, compiler):
    self.compiler = compiler
    self.termL = ["*", "/"]
    self.expL = ["+", "-"]
    self.compS = ["<", "<=", ">", ">="]
    self.compC = [ "==", "!="]
    self.compL = self.compS + self.compC
    self.notOpL = ["not"]
    self.andOpL = ["and"] 
    self.orOpL = ["or"] 
    self.compaoFunctL = self.orOpL + self.andOpL
    self.cube = SemanticCube
    self.types = {'int': 'CTE_INT', 'float': 'CTE_FLOAT', 'string': 'CTE_STRING', 'file': 'CTE_FILE'}

  def skip(self):
    self.compiler.pushJump()
    self.compiler.addQuad("GOTO", "", "", "SKIP_FUNC "+str(self.compiler.idx))

  def string_func(self, string, meta):
    """Pushes string value into operandos and CTE_STRING type into tipos"""
    string = string[0]
    constAddr = self.compiler.addConst(string.value[1:-1], string.type)
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(string.type)
    return string

  def bool_func(self, boo, meta):
    """Pushes bool value into operandos and CTE_BOOL type into tipos"""
    boo = boo[0]
    constAddr = self.compiler.addConst(boo.value, boo.type)
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(boo.type)
    return boo
  
  def int_func(self, intV, meta):
    """Pushes int_func value into operandos and CTE_INT type into tipos"""
    intV = intV[0]
    constAddr = self.compiler.addConst(intV.value, intV.type)
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(intV.type)
    return intV
  
  def float_func(self, fl, meta):
    """Pushes float value into operandos and CTE_FLOAT type into tipos"""
    fl = fl[0]
    constAddr = self.compiler.addConst(fl.value, fl.type)
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(fl.type)
    return fl

  def file_func(self, fi, meta):
    """Pushes file value into operandos and CTE_FILE type into tipos"""
    fi = fi[0]
    constAddr = self.compiler.addConst(fi.value, fi.type)
    self.compiler.pushOperando(constAddr)
    self.compiler.pushTipo(fi.type)
    return fi

  def id_func(self, id, meta):
    """Pushes id into operandos and ID type into tipos"""
    id = id[0]
    self.compiler.pushOperando(id.value)
    self.compiler.pushTipo(id.type)
    return id

  def factor_paren(self, ch, meta):
    self.compiler.pushOperador('(')
  
  def factor_paren_end(self, ch, meta):
    self.compiler.popOperador()

  def term_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op

  def term_func(self, ch, meta):
    self.expression(self.termL)

  def not_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op
  
  def not_func(self, ch, meta):
    self.expression_not(self.notOpL)

  def and_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op
  
  def and_func(self, ch, meta):
    self.expression(self.andOpL)
  
  def or_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op

  def or_func(self, ch, meta):
    self.expression(self.orOpL)
  
  def exp_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op
  
  def exp_func(self, ch, meta):
    self.expression(self.expL)
  
  def comp_func_op(self, op, meta):
    op = op[0]
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op
  
  def comp_func(self, ch, meta):
    self.expression(self.compL)
    
  def expression_not(self, lst):
    try:

      operador = self.compiler.topOperador()

      if(operador in lst):

        line = self.compiler.lines.pop()

        oper = self.compiler.popOperador()

        leftT = self.compiler.popTipo()

        left = self.compiler.popOperando()


        if leftT == 'ID':
          leftVar = self.compiler.getVar(left)
          if leftVar != None:
            leftT = leftVar.getType()
            left = leftVar.getAddr()
            if leftT == None:
              leftT = 'CTE_BOOL'
              leftVar.setType(leftT)
          else:
            leftVar = self.compiler.getVarG(left)
            if leftVar == None:
              raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + left + ".")
            else:
              leftT = leftVar.getType()
              left = "G" + str(leftVar.getAddr())
              if leftT == None:
                leftT = 'CTE_BOOL'
                leftVar.setType(leftT)
          if len(leftVar.getDimensions()) > 0:
            raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: cannot perform " + operador + " operation on an iterative variable")
      
        
        if(self.cube[oper][leftT] != False):
          addr = self.expression_genQuad(oper, left, "")
          
          self.compiler.pushOperando(addr)
          self.compiler.pushTipo(self.cube[oper][leftT])
        else:
          raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: " + oper + " " + leftT)

    except IndexError:
      """print("Empty pile.")"""
    except Exception as e:
      print(e)

  def expression(self, lst):
    try:
      operador = self.compiler.topOperador()

      if(operador in lst):
        line = self.compiler.lines.pop()

        oper = self.compiler.popOperador()

        rightT = self.compiler.popTipo()
        leftT = self.compiler.popTipo()

        right = self.compiler.popOperando()
        left = self.compiler.popOperando()

        if leftT == 'ID':
          
          leftVar = self.compiler.getVar(left)
          
          if leftVar != None:
            leftT = leftVar.getType()
            left = leftVar.getAddr()
            leftT = "None" if leftT == None else leftT
          else:
            leftVar = self.compiler.getVarG(left)
            if leftVar == None:
              raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + left + ".")
            else:
              leftT = leftVar.getType()
              left = "G" + str(leftVar.getAddr())
              leftT = "None" if leftT == None else leftT
          if len(leftVar.getDimensions()) > 0:
            raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: cannot perform " + operador + " operation on iterative variables")
        
        if rightT == 'ID':
          rightVar = self.compiler.getVar(right)
          if rightVar != None:
            rightT = rightVar.getType()
            right = rightVar.getAddr()
            rightT = "None" if rightT == None else rightT
          else:
            rightVar = self.compiler.getVarG(right)
            if rightVar == None:
              raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + right + ".")
            else:
              rightT = rightVar.getType()
              right = "G" + str(rightVar.getAddr())
              rightT = "None" if rightT == None else rightT
          if len(rightVar.getDimensions()) > 0:
            raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: cannot perform " + operador + " operation on iterative variables")

        oper_cube = 'compS' if oper in self.compS else 'compC' if oper in self.compC else 'compao' if oper in self.compaoFunctL else oper
        
        if(self.cube[oper_cube][leftT][rightT] != False):

          addr = self.expression_genQuad(oper, left, right)

          self.compiler.pushOperando(addr)
          self.compiler.pushTipo(self.cube[oper_cube][leftT][rightT])
        else:
          raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: " + leftT + " " + oper + " " + rightT)

    except IndexError:
      """print("Empty pile.")"""

  def expression_genQuad(self, op, left, right):
    addr = self.compiler.getTemp()
    self.compiler.addQuad(op, left, right, addr)
    return addr
  
  # def addr_genQuad(self, op, left, right):
  #   addr = self.compiler.getTemp()
  #   self.compiler.addQuad(op, left, right, "(" + str(addr) + ")")
  #   return "(" + str(addr) + ")"
  
  def asign_item_index(self, ch, meta):
    line = meta.line
    
    # Check if index is a valid value
    idxT = self.compiler.popTipo()
    idx = self.compiler.popOperando()

    if idxT != 'CTE_INT':
      if idxT != 'ID':
        raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: index must be an integer")
      idxVar = self.compiler.getVar(idx)
      if idxVar != None:
        idxT = idxVar.getType()
        idx = idxVar.getAddr()
      else:
        idxVar = self.compiler.getVarG(idx)
        if idxVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + idx)
        else:
          idxT = idxVar.getType()
          idx = "G" + str(idxVar.getAddr())
      if idxT != 'CTE_INT':
        raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: index must be an integer")

    idT = self.compiler.popTipo()
    id = self.compiler.popOperando()
    if idT != 'ID':
      raise SyntaxError("Error at line " + str(line) + ".\n" + "Cannot access a literal")
    idVar = self.compiler.getVar(id)
    if idVar != None:
      if len(idVar.getDimensions()) == 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: identifier " + id + " does not match an iterative variable")
      self.compiler.pushOperando(self.getElem(idVar, idx, idVar.getDimensions()[0].sup, idVar.getDimensions()[0].offset))
    else:
      idVar = self.compiler.getVarG(id)
      if idVar == None:
        raise NameError("Error at line " + str(line) + ".\n" + "Cannot access unknown identifier " + id)
      else:
        if len(idVar.getDimensions()) == 0:
          raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: identifier " + id + " does not match an iterative variable")
      self.compiler.pushOperando(self.getElem(idVar, idx, idVar.getDimensions()[0].sup, idVar.getDimensions()[0].offset, "G"))
    self.compiler.pushTipo(idVar.getType())
    return ch
  
  # def func_it_asign(self):
  #   if self.compiler.topOperador() == "=":
  #     """"""
    
  def asign_item_func(self, ch, meta):
    line = self.compiler.lines.pop()
    if self.compiler.topOperador() != "=":
      raise SyntaxError("Error at line " + str(line) + ".\n" + "Cannot perform this operation")
    _ = self.compiler.popOperador()
    # RIGHT MUST NOT BE ITERATIVE
    rightT = self.compiler.popTipo()
    right = self.compiler.popOperando()
    if rightT == 'ID':
      rightVar = self.compiler.getVar(right)
      if rightVar != None:
        rightT = rightVar.getType()
        right = rightVar.getAddr()
      else:
        rightVar = self.compiler.getVarG(right)
        if rightVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + right + ".")
        else:
          rightT = rightVar.getType()
          right = "G" + str(rightVar.getAddr())
      if len(rightVar.getDimensions()) > 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Dimensions must match.")

    left = self.compiler.popOperando()
    leftT = self.compiler.popTipo()
    if leftT != rightT:
      raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: cannot asign " + rightT + " to " + leftT)
    self.compiler.addQuad('=', right, "", left)







  def def_func_name(self, funcName, meta):
    funcName = funcName[0]
    self.skip()
    self.compiler.addFunc(funcName.value)
    self.compiler.setFuncIp()
    # self.compiler.lines.append(meta.line)
    # self.compiler.addQuad("ERA", funcName.value, "", "")
    return funcName
  
  def def_func_param_func(self, param, meta):
    paramName = param[0]
    paramType = self.compiler.popOperando()
    paramT = self.compiler.popTipo()
    
    self.compiler.addParam(paramName)
    self.compiler.addVar(paramName, paramType)
    return param

  def cte_int(self, intV, meta):
    intV = intV[0]
    self.compiler.pushOperando(convert(intV.value, intV.type))
    self.compiler.pushTipo(intV.type)
  
  def type_opt(self, typeP, meta):
    self.compiler.pushOperando(self.types[typeP[0].value])
    self.compiler.pushTipo('TYPE')
    return typeP
  
  def def_func_param_it(self, ch, meta):
    line = meta.line
    idxVal = self.compiler.popOperando()
    idxType = self.compiler.popTipo()
    paramName = self.compiler.popOperando()
    paramVal =  self.compiler.popTipo()
    paramType = self.compiler.popOperando()
    paramT = self.compiler.popTipo()
    
    if idxType != 'CTE_INT':
      raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: size must be an integer")

    self.compiler.addParam(paramName)
    self.compiler.addVar(paramName, paramType, idxVal)
    self.compiler.getVar(paramName).addDimension(0, idxVal)
  
  def def_func_end(self, ch, meta):
    func = self.compiler.release()
    funcType = func.getType()
    signature = [func.getVar(elem) for elem in func.getSignature()]
    if len(signature) > 0:
      func.setSignature(signature)
    if funcType != None:
      dims = funcType[1]
      elems = sum(dim.sup for dim in dims) if dims != None else 1
      addr = self.compiler.addVar("1" + func.getName(), funcType[0], elems)
      if dims != None:
        self.compiler.getVar("1" + func.getName()).setDimensions(dims)
      func.setReturnAddr("G" + str(addr))
    self.compiler.addQuad("ENDFUNC", "", "", "")
    self.compiler.fill()
    
  def return_line(self, ch, meta):
    self.compiler.lines.append(meta.line)
    return ch

  def def_func_type(self, ch, meta):
    line = self.compiler.lines.pop()
    tipo = self.compiler.popTipo()
    operando = self.compiler.popOperando()
    if tipo != 'ID':
      self.compiler.setFuncTipo([tipo, None])
      self.compiler.addQuad("RETURN", "", "", operando)
    else:
      funcVar = self.compiler.getVar(operando)
      if funcVar != None:
        tipo = funcVar.getType()
        operando = funcVar.getAddr()
      else:
        funcVar = self.compiler.getVarG(operando)
        if funcVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + operando + ".")
        else:
          tipo = funcVar.getType()
          operando = "G" + str(funcVar.getAddr())
      if len(funcVar.getDimensions()) == 0:
        self.compiler.setFuncTipo([tipo, None])
        self.compiler.addQuad("RETURN", "", "", operando)
      else: # Array CONTINUE
        self.compiler.setFuncTipo([tipo, funcVar.getDimensions()])
        self.compiler.addQuad("RETURNSTART", "", "", "")
        for dim in funcVar.getDimensions():
          for idx in range(dim.sup):
            constAddr = self.compiler.addConst(idx, 'CTE_INT')
            arrElem = self.getElem(funcVar, constAddr, dim.sup, dim.offset)
        self.compiler.addQuad("RETURNEND", "", "", "")

  def id_simp(self, id, ch, meta):
    id = id[0]
    self.compiler.pushOperando(id.value)
    self.compiler.pushTipo(id.type)
    return id

  def getElem(self, var, idx, sup, off, context = None):
    """"""
    varAddr = "G" + str(var.getAddr()) if context != None else var.getAddr()
    self.compiler.addQuad('VER', idx, self.compiler.addConst(0, 'CTE_INT'), self.compiler.addConst(sup, 'CTE_INT'))
    addrElem = self.expression_genQuad('+', idx, self.compiler.addConst(varAddr, 'CTE_INT'))
    if off != 0:
      addrElem = self.expression_genQuad('*', addrElem, off)
    # addrElem = self.addr_genQuad('=', addrOff, "")
    return "(" + str(addrElem) + ")"

  def asign_it(self, varLeft, varRight, context = None):
    line = self.compiler.lines.pop()
    if varLeft.getType() == None:
      varLeft.setType(varRight.getType())
    if len(varLeft.getDimensions()) == 0:
      rightElem = "G" + str(varRight.getAddr()) if context != None else varRight.getAddr()
      self.compiler.addQuad("=", rightElem, "", varLeft.getAddr())
    else:
      for dim in varRight.getDimensions():
        for idx in range(dim.sup):
          constAddr = self.compiler.addConst(idx, 'CTE_INT')
          leftElem = self.getElem(varLeft, constAddr, dim.sup, dim.offset)
          rightElem = self.getElem(varRight, constAddr, dim.sup, dim.offset, context)
          self.compiler.addQuad('=', rightElem, "", leftElem)

  def asign_op(self, op, meta):
    op = op[0].value
    self.compiler.pushOperador(op)
    self.compiler.lines.append(meta.line)
    return op

  def asign_simp_func(self, ch, meta):
    line = self.compiler.lines.pop()
    if self.compiler.topOperador() != "=":
      raise SyntaxError("Error at line " + str(line) + ".\n" + "Cannot perform this operation")
    _ = self.compiler.popOperador()
    rightT = self.compiler.popTipo()
    leftT = self.compiler.popTipo()

    right = self.compiler.popOperando()
    left = self.compiler.popOperando()

    if leftT != 'ID':
      raise SyntaxError("Error at line " + str(line) + ".\n" + "Cannot assign to literal")
    
    if rightT != 'ID':
      addr = self.compiler.addVar(left, rightT)
      lVar = self.compiler.getVar(left)
      if len(lVar.getDimensions()) == 0:
        self.compiler.addQuad("=", right, "", addr)
      else:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Dimensions must match.")
    else:
      rVar = self.compiler.getVar(right)
      if rVar != None:
        lVar = self.compiler.getVar(left)
        if lVar == None:
          rDims = rVar.getDimensions()
          elems = sum(dim.sup for dim in rDims)
          if elems == 0:
            elems = 1
          addr = self.compiler.addVar(left, rVar.getType(), elems)
          lVar = self.compiler.getVar(left)
          if len(rDims) > 0:
            lVar.setDimensions(rDims)
          self.compiler.lines.append(line)
          self.asign_it(lVar, rVar)
        elif lVar.getDimensions() >= rVar.getDimensions():
          self.compiler.lines.append(line)
          self.asign_it(lVar, rVar)
        else:
          raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Dimensions must match.")
      else:
        rVar = self.compiler.getVarG(right)
        if rVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Name not found: Cannot assign unknown identifier.")

        lVar = self.compiler.getVar(left)
        if lVar == None:
          rDims = rVar.getDimensions()
          elems = sum(dim.sup for dim in rDims)
          if elems == 0:
            elems = 1
          addr = self.compiler.addVar(left, rVar.getType(), elems)
          lVar = self.compiler.getVar(left)
          if len(rDims) > 0:
            lVar.setDimensions(rDims)
          self.compiler.lines.append(line)
          self.asign_it(lVar, rVar)
        elif lVar.getDimensions() >= rVar.getDimensions():
          self.compiler.lines.append(line)
          self.asign_it(lVar, rVar, "G")
        else:
          raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Dimensions must match.")

  def var_it_fondo(self, ch, meta):
    self.compiler.pushOperando("[")
    self.compiler.pushTipo("[")
  
  def var_it_asign(self, ch, meta):
    """Only works for 1-D Arrays"""
    line = meta.line
  
    stackElem = Stack("array")
    tipo = None
    while(self.compiler.topOperando() != "["):
      elemT = self.compiler.popTipo()
      elem = self.compiler.popOperando()

      if elemT == 'ID':
        elemVar = self.compiler.getVar(elem)
        if elemVar != None:
          elemT = elemVar.getType()
          elem = elemVar.getAddr()
        else:
          elemVar = self.compiler.getVarG(elem)
          if elemVar == None:
            raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + elem + ".")
          else:
            elemT = elemVar.getType()
            elem = "G" + str(elemVar.getAddr())
        if len(elemVar.getDimensions()) > 0:
          raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Array element cannot be iterative.")

      if tipo == None:
        tipo = elemT
      else:
        if tipo != elemT:
          raise TypeError("Error at line " + str(line) + ".\n" + "Type-Mismatch: Elements must be of the same type.")
      stackElem.push(elem)
    
    self.compiler.popOperando()
    self.compiler.popTipo()
    try:
      op = self.compiler.topOperador()
    except:
      op = None
    if op != '=':
      elems = len(stackElem)
      arrId = self.compiler.addVarArr(tipo, elems)
      varArr = self.compiler.getVar(arrId)
      varArr.addDimension(0, elems)
      for dim in varArr.getDimensions():
        for idx in range(elems):
          elem = stackElem.pop()
          constAddr = self.compiler.addConst(idx, 'CTE_INT')
          arrElem = self.getElem(varArr, constAddr, dim.sup, dim.offset)
          self.compiler.addQuad('=', elem, "", arrElem)
      self.compiler.pushOperando(arrId)
      self.compiler.pushTipo('ID')
    else: 
      
      _ = self.compiler.popOperador()
      
      if self.compiler.topTipo() != 'ID':
        raise SyntaxError("Error at line " + str(line) + ".\n" + "Cannot assign to literal")
      _ = self.compiler.popTipo()
      varId = self.compiler.popOperando()
      varArr = self.compiler.getVar(varId)
      if varArr == None:
        elems = len(stackElem)
        addr = self.compiler.addVar(varId, tipo, elems)
        varArr = self.compiler.getVar(varId)
        varArr.addDimension(0, elems)
      if len(varArr.getDimensions()) == 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Dimensions must match.")
      elems = len(stackElem)
      for dim in varArr.getDimensions():
        for idx  in range(elems):
          elem = stackElem.pop()
          constAddr = self.compiler.addConst(idx, 'CTE_INT')
          arrElem = self.getElem(varArr, constAddr, dim.sup, dim.offset)
          self.compiler.addQuad('=', elem, "", arrElem)

  def put_fondo(self, ch, meta):
    self.compiler.lines.append(meta.line)
    self.compiler.pushOperando("(")
    self.compiler.pushTipo("(")
    return ch
  
  def print_func(self, ch, meta):
    line = self.compiler.lines.pop()
    stackElems = Stack("Print")
    while(self.compiler.topOperando() != "("):
      elem = self.compiler.popOperando()
      elemType = self.compiler.popTipo()
      
      if elemType != 'ID':
        stackElems.push(elem)
      else:
        # CHECAR SI ELEM EXISTE
        printVar = self.compiler.getVar(elem)
        if printVar != None:
          context = None
        else:
          printVar = self.compiler.getVarG(elem)
          if printVar == None:
            raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + elem + ".")
          else:
            context = "G"
        if len(printVar.getDimensions()) == 0:
          addr = "G" + str(printVar.getAddr()) if context == "G" else printVar.getAddr()
          stackElems.push(addr)
        else:
          stackElems.push("]")
          for dim in printVar.getDimensions():
            for idx in reversed(range(dim.sup)):
              constAddr = self.compiler.addConst(idx, 'CTE_INT')
              arrElem = self.getElem(printVar, constAddr, dim.sup, dim.offset, context)
              stackElems.push(arrElem)
          stackElems.push("[")
    self.compiler.popOperando()
    self.compiler.popTipo()
    while(not stackElems.empty()):
      self.compiler.addQuad("PRINT", "", "", str(stackElems.pop()))
    self.compiler.addQuad("PRINT", "", "", "\n")

  def if_func(self, ch, meta):
    line = meta.line
    condVal = self.compiler.popOperando()
    condType = self.compiler.popTipo()
    if condType == 'ID':
      condVar = self.compiler.getVar(condVal)
      if condVar != None:
        context = None
      else:
        condVar = self.compiler.getVarG(condVal)
        if condVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + condVar + ".")
        else:
          context = "G"
      if len(condVar.getDimensions()) == 0:
        condVal = "G" + str(condVar.getAddr()) if context == "G" else condVar.getAddr()
        condType = condVar.getType()
      else:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Condition cannot be an array.")
    if condType != 'CTE_BOOL':
      raise TypeError("Error at line " + str(line) + ".\n" + "Condition must be boolean.")
    self.compiler.pushJump()
    self.compiler.addQuad("GOTOF", condVal, "", "IFFALSE "+str(self.compiler.idx))
    return ch

  def else_func(self, ch, meta):
    self.compiler.pushJump()
    self.compiler.addQuad("GOTO", "", "", "IFEND "+str(self.compiler.idx))
    jump = self.compiler.popJump()
    self.compiler.fill()
    self.compiler.pushJump(jump)
    
  def endif(self, ch, meta):
    self.compiler.fill()
  
  def end_prog(self, ch, meta):
    self.compiler.addQuad("ENDPROG", "", "", "")

  def while_func(self, ch, meta):
    self.compiler.pushJump()

  def while_cond(self, ch, meta):
    line = meta.line
    condVal = self.compiler.popOperando()
    condType = self.compiler.popTipo()
    if condType == 'ID':
      condVar = self.compiler.getVar(condVal)
      if condVar != None:
        context = None
      else:
        condVar = self.compiler.getVarG(condVal)
        if condVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + condVar + ".")
        else:
          context = "G"
      if len(condVar.getDimensions()) == 0:
        condVal = "G" + str(condVar.getAddr()) if context == "G" else condVar.getAddr()
        condType = condVar.getType()
      else:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Condition cannot be an array.")
    if condType != 'CTE_BOOL':
      raise TypeError("Error at line " + str(line) + ".\n" + "Condition must be boolean.")
    self.compiler.pushJump()
    self.compiler.addQuad("GOTOF", condVal, "", "IFFALSE "+str(self.compiler.idx))
    return ch

  def while_end(self, ch, meta):
    end = self.compiler.popJump()
    cond = self.compiler.popJump()
    self.compiler.addQuad("GOTO", "", "", cond)
    self.compiler.fill(end)
  
  # def for_func(self, ch, meta):
  #   self.compiler.pushJump()

  def for_check(self, ch, meta):
    line = meta.line
    itVal = self.compiler.popOperando()
    itType = self.compiler.popTipo()

    if itType == 'RANGE':

      qtyVal = self.compiler.popOperando()
      qtyType = self.compiler.popTipo()
      finVal = self.compiler.popOperando()
      finType = self.compiler.popTipo()
      iniVal = self.compiler.popOperando()
      iniType = self.compiler.popTipo()

      idVal = self.compiler.popOperando()
      idType = self.compiler.popTipo()

      if idType != 'ID':
        raise TypeError("Error at line " + str(line) + ".\n" + "Cannot assing to literal")

      idAddr = self.compiler.addVar(idVal, 'CTE_INT')
      self.compiler.addQuad("=", iniVal, "", idAddr)
      self.compiler.pushJump() # PARA GOTO
      addrComp = self.expression_genQuad("<", idAddr, finVal)
      self.compiler.pushJump() # PARA LLENARLO
      self.compiler.addQuad("GOTOF", addrComp, "", "ENDFOR")
      self.compiler.pushOperando(idAddr)
      self.compiler.pushTipo('ADDR')
      self.compiler.pushOperando(qtyVal)
      self.compiler.pushTipo(qtyType)

    elif itType != 'ID':
      raise TypeError("Error at line " + str(line) + ".\n" + "Cannot iterate literal") 
    else:
      itVar = self.compiler.getVar(itVal)
      if itVar != None:
        context = None
      else:
        itVar = self.compiler.getVarG(itVal)
        if itVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + itVar + ".")
        else:
          context = "G"
      if len(itVar.getDimensions()) == 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Must be an array.")
      
      idVal = self.compiler.popOperando()
      idType = self.compiler.popTipo()
      
      if idType != 'ID':
        raise TypeError("Error at line " + str(line) + ".\n" + "Cannot assing to literal")
      idAddr = self.compiler.addVar(idVal, itVar.getType())
      
      addr = self.expression_genQuad("=", self.compiler.addConst(0, 'CTE_INT'), "")
      self.compiler.pushJump() # PARA GOTO
      dim = itVar.getDimensions()[0]
      addrComp = self.expression_genQuad("<", addr, self.compiler.addConst(dim.sup, 'CTE_INT'))
      self.compiler.pushJump() # PARA LLENARL GOTOF
      self.compiler.addQuad("GOTOF", addrComp, "", "ENDFOR")
      arrElem = self.getElem(itVar, addr, dim.sup, dim.offset, context)
      self.compiler.addQuad("=", arrElem, "", idAddr)
      self.compiler.pushOperando(addr)
      self.compiler.pushTipo('ADDR')
      self.compiler.pushOperando(self.compiler.addConst(1, 'CTE_INT'))
      self.compiler.pushTipo('CTE_INT')
      

  def for_end(self, ch, meta):
    sumQty = self.compiler.popOperando()
    self.compiler.popTipo()
    addr = self.compiler.popOperando()
    self.compiler.popTipo()
    tempAddr = self.expression_genQuad("+", sumQty, addr)
    self.compiler.addQuad("=", tempAddr, "", addr)
    end = self.compiler.popJump()
    cond = self.compiler.popJump()
    self.compiler.addQuad("GOTO", "", "", cond)
    self.compiler.fill(end)
  
  
  def range_tope(self, ch, meta):
    self.compiler.pushOperando("(")
    self.compiler.pushTipo("(")
    return ch

  def range_func(self, ch, meta):
    line = meta.line
    """"""
    stackElems = Stack("Range")
    while(self.compiler.topOperando() != "("):
      elem = self.compiler.popOperando()
      elemType = self.compiler.popTipo()

      if elemType != 'ID':
        if elemType != 'CTE_INT':
          raise TypeError("Error at line " + str(line) + ".\n" + "Range elements must be integers.")
        stackElems.push(elem)
      else:
        """"""
        elemVar = self.compiler.getVarG(elem)
        if elemVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier " + elemVar + ".")
        else:
          context = "G"
        if len(elemVar.getDimensions()) > 0:
          raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Range elements cannot be arrays.")
        if elemType != 'CTE_INT':
          raise TypeError("Error at line " + str(line) + ".\n" + "Range elements must be integers.")
        stackElems.push(elem)
      
    self.compiler.popOperando()
    self.compiler.popTipo()
    ini = 0
    qty = 1
    elems = len(stackElems)
    if elems == 1:
      qty = self.compiler.addConst(qty, 'CTE_INT')
      fin = stackElems.pop()
      ini = self.compiler.addConst(ini, 'CTE_INT')
      
    elif elems == 2:
      qty = self.compiler.addConst(qty, 'CTE_INT')
      fin = stackElems.pop()
      ini = stackElems.pop()
    else:
      qty = stackElems.pop()
      fin = stackElems.pop()
      ini = stackElems.pop()
    
    self.compiler.pushOperando(ini)
    self.compiler.pushTipo('CTE_INT')
    self.compiler.pushOperando(fin)
    self.compiler.pushTipo('CTE_INT')
    self.compiler.pushOperando(qty)
    self.compiler.pushTipo('CTE_INT')
    self.compiler.pushOperando('RANGE')
    self.compiler.pushTipo('RANGE')
    return ch

  def call_func_name(self, id, meta):
    """Pushes id into operandos and ID type into tipos"""
    line = meta.line
    id = id[0]
    if self.compiler.getFunc(id.value) != None:
      self.compiler.pushOperando(id.value)
      self.compiler.pushTipo(id.type)
      self.compiler.pushOperando("(")
      self.compiler.pushTipo("(")
    else:
      raise NameError("Error at line " + str(line) + ".\n" + "Unknown function name.")
    return id

  def call_func_param(self, id, meta):
    line = meta.line
    params = Stack("Params")
    while self.compiler.topOperando() != "(":
      param = [self.compiler.popOperando(), self.compiler.popTipo()]
      params.push(param)

    self.compiler.popOperando()
    self.compiler.popTipo()

    funcId = self.compiler.popOperando()
    self.compiler.popTipo()
    func = self.compiler.getFunc(funcId)

    signature = func.getSignature()

    if len(params) != len(signature):
      raise TypeError("Error at line " + str(line) + ".\n" + "Unknown function name and signature.")
    
    self.compiler.addQuad("ERA", funcId, "", "")

    for elem in signature:
      param = params.pop()
      paramId = param[0]
      paramType = param[1]

      if paramType == 'ID':
        paramVar = self.compiler.getVar(paramId)
        if paramVar == None:
          paramVar = self.compiler.getVarG(paramId)

        # CONTINUE

      self.compiler.addQuad("PARAM", "ADDR", "#", "")

    self.compiler.addQuad("GOSUB", funcId, "", "")

    return id
  
  def write_func(self, opts, meta):
    line = meta.line
    fileL = opts[0].value
    TypeL = opts[0].type
    fileR = opts[1].value
    TypeR = opts[1].type
    
    if TypeL == 'ID':
      fileLVar = self.compiler.getVar(fileL)
      if fileLVar == None:
        fileLVar = self.compiler.getVarG(fileL)
        if fileLVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier.")
      
      if fileLVar.getType() != 'CTE_FILE':
        raise TypeError("Error at line " + str(line) + ".\n" + "Value is not a filename.")
      if len(fileLVar.getDimensions()) != 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Arrays are not supported.")
      fileL = fileLVar.getAddr()
    else:
      fileL = self.compiler.addConst(fileL, 'CTE_FILE')

    if TypeR == 'ID':
      fileRVar = self.compiler.getVar(fileR)
      if fileRVar == None:
        fileRVar = self.compiler.getVarG(fileR)
        if fileRVar == None:
          raise NameError("Error at line " + str(line) + ".\n" + "Unknown identifier.")
      
      if fileRVar.getType() != 'CTE_FILE':
        raise TypeError("Error at line " + str(line) + ".\n" + "Value is not a filename.")
      if len(fileRVar.getDimensions()) != 0:
        raise TypeError("Error at line " + str(line) + ".\n" + "Dimension-Mismatch: Arrays are not supported.")
      fileR = fileRVar.getAddr()
    else:
      fileR = self.compiler.addConst(fileR, 'CTE_FILE')

    self.compiler.addQuad("WRITE", fileL, "", fileR)
    return opts