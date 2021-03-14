import bitstring as bs
import tree as tr
import time
import sys

def main(_dir=''):
  file_name = input('Write your file name: ')

  try:
    bits_header = bs.Bits(filename= file_name, length= 8) #Lê os 2 primeiros bytes do arquivo

    padding = check_header(bits_header) #Retira as informações do header

    _list = bs.Bits(filename= file_name, offset= 8,  length= 256) #Lê os 256 bits que indicam os símbolos

    list_symbols = get_symbols(_list) #Extrai quais são os símbolos

    bits_lengths = bs.Bits(filename= file_name, offset= 264, length= len(list_symbols)*8) #Lê os tamanhos dos códigos

    lengths = get_lengths(bits_lengths) #Extrai os tamanhos dos códigos

    code, tree = tr.make_tree_code (list_symbols, lengths) #Recria os códigos através dos tamanhos através de uma árvore

    file_bin = bs.Bits(filename= file_name, offset= 264 + len(list_symbols)*8) #Lê o resto do arquivo (Isso não traz para a memória o arquivo todo de uma vez)

    #Se tiver sido passado um diretório de destino específico
    if _dir:
      file_name = file_name.split('\\')[-1].split('/')[-1]
      f_write = open(_dir + '/' + file_name[:-4], 'wb')

    else:
      f_write = open(file_name[:-4], 'wb')

    decode(file_bin, f_write, code, tree, padding)#Gera o texto a partir dos códigos

  except WrongHeader:
    print('Header do arquivo não condiz com o esperado.')
    return -1

  finally:
    f_write.close()

  print('Sucesso!')

#-------------------------------------------------------------------------------------------
#Verifica se os 4 primeiros bits são 0xF, e extrai o padding dos últimos 4
def check_header(header):

  if header[:-4] == bs.Bits(hex= '0xf'):
    return header[4:].uint

  else: raise WrongHeader

class WrongHeader(Exception):
  pass

#---------------------------------------------------------------------------------------------
#Extrai os símbolos presentes
def get_symbols(_list):

  int_little = list(_list.findall('0b1')) #inteiros dos símbolos lidos na byteordem 'litte'

  symbols = [(255-s).to_bytes(1, byteorder= 'big') for s in int_little] #símbolos presentes em bytes

  return symbols

#--------------------------------------------------------------------------------------------
#Cria um array de inteiros com os tamanhos existentes
def get_lengths(bits_lengths):

  lengths = []

  for b in bits_lengths.tobytes():
    lengths.append(b)

  return lengths

#-----------------------------------------------------------------------------------------
#Decodifica o texto comprimido utilizando uma árvore
def decode (file_bin, f_write, code, tree, padding):
  end = file_bin.len - padding #Id do final do arquivo
  #print(file_bin.bin)
  print('Decoding... (this may take a while)')
  time_start = time.time()

  #Dicionario com o codigo como chave e o símbolo como valor
  inv_dict_code = {_code: symbol for symbol, _code in code.items()}

  node = tree #Colocando o nó na raiz

  #Percorre todo o arquivo de leitura bit a bit
  for i in range(end):
    #Percorre árvore se 0 para a esquerda e se 1 para a direita.
    if file_bin[i]:
        node = node.r_node
    else: node = node.l_node

    #Quando o nodo não tem filho, pega o código do nodo, escreve o símbolo correspondente no arquivo e volta para a raiz.
    if not node.have_children:
      f_write.write(inv_dict_code[node.value])
      node = tree


  time_end = time.time()
  print('Demorou: {} segundos'.format(time_end - time_start))

if __name__ == "__main__":
  #Aceita um diretório como argumento
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else: main()