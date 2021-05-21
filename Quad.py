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
  def reprQ(self, l):
    return "{:^4}".format(self.op) +  " | " + "".join(["{:^", str(l),"}"]).format(self.left) + " | " + "".join(["{:^", str(l),"}"]).format(self.right) + " | " + "{:^10}".format(id(self.dest))
  def __len__(self):
    return max(len(str(self.left)), len(str(self.right)))
  