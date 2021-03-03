import bitstring as bs

def create_tree_root(value= bs.Bits(bin='0b'), parent= None):
  return Node(value, parent)

'''
class BinTree:
  def __init__(self):
    self.l_node = Node(bs.Bits(bin='0b0'), self)
    self.r_node = Node(bs.Bits(bin='0b1'), self)
  
  def close_node(self):
    pass
'''

#Espera value do tipo bs.Bits
class Node:
  def __init__(self, value, parent):
    self.value = value
    self.used = False
    self.l_node = None
    self.r_node = None
    self.have_children = False
    self.parent = parent
  
  def create_children(self):
    self.l_node = Node(self.value + bs.Bits(bin='0b0'), self)
    self.r_node = Node(self.value + bs.Bits(bin='0b1'), self)
    self.have_children = True

  def close_node(self):
    if (not self.have_children) or (self.l_node.used and self.r_node.used):
      self.used = True
      self.parent.close_node()

