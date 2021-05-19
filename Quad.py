class Quad(object):

  def __init__(self, op, left, right, dest):
    """
    Creates quad dict with contents
    
    OP | LEFT | RIGHT | DEST
    """
    self.op = op
    self.left = left
    self.right = right
    self.dest = dest
  