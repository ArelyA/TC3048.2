import os
import filecmp
import shutil
import operator
from io import StringIO
from html.parser import HTMLParser
from file_read_backwards import FileReadBackwards
import re

ops = { "or": operator.or_, "and": operator.and_, "not": operator.not_, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "==": operator.eq, "!=": operator.ne, "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

class MLStripper(HTMLParser):
  """ 
  Strips HTML tags
  
  source: https://stackoverflow.com/a/925630
  """
  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.text = StringIO()

  def handle_data(self, d):
    self.text.write(d)

  def get_data(self):
    return self.text.getvalue()

def strip_tags(html):
  """ 
  Strips HTML tags
  
  source: https://stackoverflow.com/a/925630
  """
  s = MLStripper()
  s.feed(html)
  return s.get_data()

def raw(text):
    """
    Returns a raw string representation of text

    source: https://code.activestate.com/recipes/65211-convert-a-string-into-a-raw-string/
    """
    escape_dict = {
      '\\a':'\a',
      '\\b':'\b',
      '\\c':'\c',
      '\\f':'\f',
      '\\n': '\n',
      '\\r':'\r',
      '\\t':'\t',
      '\\v':'\v',
      '\'':'\'',
      '\\"':'\"',
      '\\0':'\0',
      '\\1':'\1',
      '\\2':'\2',
      '\\3':'\3',
      '\\4':'\4',
      '\\5':'\5',
      '\\6':'\6',
      '\\7':'\7',
      '\\8':'\8',
      '\\9':'\9'
    }
    new_string = text.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
    return new_string

def convert(var, type):
  if(type == 'CTE_INT'):
    return int(float(var))
  elif(type == 'CTE_FLOAT'):
    return float(var)
  elif(type == 'CTE_BOOL'):
    return True if var == 'True' else False
  elif(type == 'CTE_FILE'):
    return var
  else: # CTE_FILE (filename) and CTE_STRING
    return raw(var)

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
  #return left.replace(right)
  return left.replace(right, "")

def _tempName(file, count = ""):
  """HELPER Generates temp name to avoid overwriting"""
  temp = "temp"
  filename, file_extension = os.path.splitext(file)
  try:
    index = filename.rindex('/')
    filename_temp = filename[:index+1] + temp + count + "_" + filename[index+1:] + file_extension
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
  return filename_temp

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
  shutil.copyfile(fileFrom, fileTo, follow_symlinks=False)

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

def printFile(filename):
  with open(filename) as file:
    for idx, line in enumerate(file):
      print(line)

def getLineBack(filename, pos):
  """Returns a specific line reading from end"""
  with FileReadBackwards(filename, encoding="utf-8") as file:
    for idx, line in enumerate(file):
      if idx == pos:
        return line
  raise EOFError("Element does not exist.")

def getLine(filename, pos):
  """Returns a specific line"""
  if pos < 0:
    return getLineBack(filename, pos * (-1) - 1)
  else:
    with open(filename) as file:
      for idx, line in enumerate(file):
        if idx == pos:
          return line
    raise EOFError("Element does not exist.")
  
def getWord(filename, pos):
  """
  Returns a specific word
  """
  filename_temp = tempName(filename)
  with open(filename) as file, open(filename_temp, "a+") as fout:
    for idx, line in enumerate(file):
      line = re.sub(r'\s+', "\n", line)
      line = re.sub(r'\s+', "\n", line)
      if line != "\n":
        print(line, file=fout)
  if pos < 0:
    return getLineBack(filename_temp, pos * (-1) - 1)
  else:
    return getLine(filename_temp, pos)
  
def countWords(filename):
  """"""
  total = 0
  with open(filename) as file:
    for idx, line in enumerate(file):
      (_, n) = re.subn(r'\S', " ", line)
      total += n
  return total

def countLines(filename):
  total = 0
  with open(filename) as file:
    for idx, line in enumerate(file):
      total += 1
  return total
