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
    self.using = False #Indica se algum codigo esta usando esse prefixo
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

    if self.parent:
      self.using = True
      self.parent.close_node()

  def search(self, i):
    if self.used == True : return False

    elif i == 0:
      if (self.using): return False
      else: return self
    
    else:
      if not self.have_children: self.create_children()
      final_node = self.l_node.search(i - 1)
      if final_node == False:
        final_node = self.r_node.search(i - 1)
      
      return final_node


def make_tree_code (list_symbols, lengths):
  tree_code = []
  list_symbols = sorted(list_symbols)

  root = create_tree_root()

  for x in lengths:
    node = root.search(x)
    tree_code.append(node.value)
    node.close_node()
    

  return {key: value for key, value in zip(list_symbols, tree_code)}, root
