import bitstring as bs

def create_tree_root(value= bs.Bits(bin='0b'), parent= None): #Cria um nó que será a raiz de uma árvore, pois não tem parente nem valor
  return Node(value, parent)

#Espera 'value' do tipo bs.Bits na inicialização
class Node:
  def __init__(self, value, parent):
    self.value = value
    self.used = False #Indica se o código do nodo já está sendo utilizado como prefixo ou código o número máximo de vezes 
    self.using = False #Indica se algum código usado tem esse prefixo
    self.l_node = None #Filho à esquerda do nodo
    self.r_node = None #Filho à direita do nodo
    self.have_children = False #Indica se o nodo tem filhos
    self.parent = parent #Nodo pai do nodo atual
  

  #Cria os filhos à esquerda e à direita do nodo atual
  def create_children(self):
    self.l_node = Node(self.value + bs.Bits(bin='0b0'), self) #'0' para a esquerda
    self.r_node = Node(self.value + bs.Bits(bin='0b1'), self) #'1' para a direita
    self.have_children = True

  #Ação para indicar os nodos que não podem mais ser utilizados e se o prefixo está sendo utilizado
  def close_node(self):
    #Se n tiver filhos ou os filhos estão sendo utilizados, significa que o nodo está sendo utilizado ao máximo
    if (not self.have_children) or (self.l_node.used and self.r_node.used):
      self.used = True

    #Se tiver nodo pai, indica que seu prefixo está sendo utilizado pelo menos uma vez e chama essa mesma função no nodo pai
    if self.parent:
      self.using = True
      self.parent.close_node()

  #Faz a procura do nodo mais à esquerda de profundidade 'i' possível de gerar um código prefixo
  def search(self, i):
    #Se o nodo encontrado já está sendo utilizado, retorna False
    if self.used == True : return False

    #Se estou no último nodo, verifico se ele já é prefixo de outro código
    elif i == 0:
      if (self.using): return False
      else: return self
 
    else:
      if not self.have_children: self.create_children() #Se não tiver filhos, cria os filhos
      final_node = self.l_node.search(i - 1) #Faz a busca no nodo filho esquerdo
      if final_node == False: #Se a busca resultar em falha, faz a busca no filho direito
        final_node = self.r_node.search(i - 1)
      
      return final_node #Retorna o resultado da busca

#Função para criar uma árvore e gerar os códigos baseados nos seus tamanhos
def make_tree_code (list_symbols, lengths):
  tree_code = []
  list_symbols = sorted(list_symbols)

  root = create_tree_root()

  for x in lengths:
    node = root.search(x)
    tree_code.append(node.value)
    node.close_node()
    

  return {key: value for key, value in zip(list_symbols, tree_code)}, root
