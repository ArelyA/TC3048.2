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
    #print(l)
    return "".join(["{:^", str(l),"}"]).format(self.op) +  " | " + "".join(["{:^", str(l),"}"]).format(str(self.left)) + " | " + "".join(["{:^", str(l),"}"]).format(str(self.right)) + " | " + "".join(["{:^", str(l),"}"]).format(str(self.dest))

  def __len__(self):
    return max(len(str(self.op)), len(str(self.left)), len(str(self.right)), len(str(self.dest)))
  