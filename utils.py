import os
import filecmp
import shutil
import operator

ops = { "or": operator.or_, "and": operator.and_, "not": operator.not_, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "==": operator.eq, "!=": operator.ne, "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

def convert(var, type):
  if(type == 'CTE_INT'):
    return int(float(var))
  elif(type == 'CTE_FLOAT'):
    return float(var)
  elif(type == 'CTE_BOOL'):
    return True if var == 'True' else False
  else: # CTE_FILE (filename) and CTE_STRING
    return str(var)

def compareFilesSize(left, right, op):
  """FILE FILE Compare sizes for >, >=, <, <="""
  return evaluate(os.path.getsize(left), os.path.getsize(right), op)

def compareFilesContent(left, right, op):
  """FILE FILE Compares file content similarity for ==, !="""
  if(op == '=='):
    return filecmp.cmp(left, right)
  else:
    return not filecmp.cmp(left, right)

def compareArray(left, right, op):
  """ARR ARR Compare array lengths for >, >=, <, <="""
  return evaluate(len(left), len(right), op)

def compareString(left, right, op):
  """STR STR Compare string lengths for >, >=, <, <="""
  return evaluate(len(left), len(right), op)

def removeStrfromStr(left, right):
  """STR STR Removes all occurrences of right string from left string"""
  return left.replace(right)

def _tempName(file, count = ""):
  """HELPER Generates temp name to avoid overwriting"""
  temp = "temp"
  filename, file_extension = os.path.splitext(file)
  try:
    index = filename.rindex('/')
    filename_temp = filename[:index] + temp + count + "_" + filename[index:] + file_extension
  except:
    filename_temp = temp + count + "_" + filename + file_extension
  return filename_temp
def tempName(file):
  """Generates temp name to avoid overwriting"""
  temp_count = 0
  filename_temp = _tempName(file)

  while os.path.isfile(filename_temp):
    #File does not exist
    temp_count += 1
    filename_temp = _tempName(file, str(temp_count))

def removeStrfromFile(file, string):
  """FILE STR Removes a string from a file. Original file is altered."""
  filename_temp = tempName(file)

  with open(file) as fin, open(filename_temp, "w+") as fout:
    for line in fin:
      line = line.replace(string, "")
      fout.write(line)
  
  copyFile(filename_temp, file)
  removeFile(filename_temp)

def copyFile(fileFrom, fileTo):
  """Copies one file to another"""
  shutil.copyfile(fileFrom, fileTo)

def appendFile(fileFrom, fileTo):
  """Appends one file to another"""
  with open(fileFrom) as fin, open(fileTo, "a+") as fout:
    for line in fin:
      fout.write(line)

def appendStrtoFile(file, string):
  """Appends a string to the end of a file"""
  with open(file, "a+") as fout:
    fout.write(string)

def repeatStr(string, integer):
  """Repeats a string integer times"""
  return "".join(string for i in range(integer))
  
def removeFile(file):
  """Deletes a file"""
  os.remove(file)

def evaluate(op, left, right=None):
  """
  When comparing 2 elements.

    Applies for all cases of or, and, not, most cases of ==, != (except files) and some cases of >, >=, <, <=

    * For string >, >=, <, <= use compareString

    * For array >, >=, <, <= use compareArray

    * For file >, >=, <, <= use compareFilesSize

    * For file ==, != use compareFilesContent
  """
  if(right != None):
    return ops[op](left, right)
  else:
    return ops[op](left)