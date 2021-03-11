import bitstring as bs
import tree as tr
import time
import sys

def main(_dir=''):
  file_name = input('Write your file name: ')

  try:
    bits_header = bs.Bits(filename= file_name, length= 8)

    padding = check_header(bits_header)

    _list = bs.Bits(filename= file_name, offset= 8,  length= 256)

    list_symbols = get_symbols(_list)

    bits_lengths = bs.Bits(filename= file_name, offset= 264, length= len(list_symbols)*8)

    lengths = get_lengths(bits_lengths)

    code, tree = tr.make_tree_code (list_symbols, lengths)

    print(code)

    file_bin = bs.Bits(filename= file_name, offset= 264 + len(list_symbols)*8) #Isso nao traz pra memoria

    if _dir:
      file_name = file_name.split('\\')[-1].split('/')[-1]
      f_write = open(_dir + '/' + file_name[:-4], 'wb')
    else:
      f_write = open(file_name[:-4], 'wb')

    decode(file_bin, f_write, code, tree, padding)

  except WrongHeader:
    print('Header do arquivo não condiz com o esperado.')
    return -1

  finally:
    f_write.close()

  print('Sucesso!')

#-------------------------------------------------------------------------------------------

def check_header(header):

  if header[:-4] == bs.Bits(hex= '0xf'):
    return header[4:].uint

  else: raise WrongHeader

class WrongHeader(Exception):
  pass

#---------------------------------------------------------------------------------------------

def get_symbols(_list):

  int_little = list(_list.findall('0b1')) #inteiros dos simbolos com bits lidos na ordem contraria

  symbols = [(255-s).to_bytes(1, byteorder= 'big') for s in int_little] #simbolos presentes em bytes

  return symbols

#--------------------------------------------------------------------------------------------

def get_lengths(bits_lengths):

  lengths = []

  for b in bits_lengths.tobytes():
    lengths.append(b)

  return lengths

#-----------------------------------------------------------------------------------------

def decode (file_bin, f_write, code, tree, padding):
  end = file_bin.len - padding
  #print(file_bin.bin)
  print('Decoding... (this may take a while)')
  time_start = time.time()

  inv_dict_code = {_code: symbol for symbol, _code in code.items()}

  node = tree

  for i in range(end):
    if file_bin[i]:
        node = node.r_node
    else: node = node.l_node

    if not node.have_children:
      f_write.write(inv_dict_code[node.value])
      node = tree

    #print("{}, {}".format(node.value, i))

  time_end = time.time()
  print('Demorou: {} segundos'.format(time_end - time_start))

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else: main()