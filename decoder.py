import bitstring as bs
import tree as tr
import time

def main():
  file_name = input('Write your file name: ')

  try:
    bits_header = bs.Bits(filename= 'arquivos/' + file_name, length= 8)

    padding = check_header(bits_header)

    _list = bs.Bits(filename= 'arquivos/' + file_name, offset= 8,  length= 256)

    list_symbols = get_symbols(_list)

    bits_lengths = bs.Bits(filename= 'arquivos/' + file_name, offset= 264, length= len(list_symbols)*8)

    lengths = get_lengths(bits_lengths)

    code = tr.make_tree_code (list_symbols, lengths)

    file_bin = bs.Bits(filename= 'arquivos/' + file_name, offset= 264 + len(list_symbols)*8) #Isso nao traz pra memoria

    f_write = open('results/' + file_name[:-2], 'wb')

    decode(file_bin, f_write, code, padding)

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

def decode (file_bin, f_write, code, padding):
  current = 0
  end = file_bin.len - padding

  print('Deconding... (this may take a while)')
  time_start = time.time()

  while current < end:
    print('Current: {}, End: {}'.format(current, end))
    for key, value in code.items():
      if file_bin.startswith(value, start= current, end= end):
        f_write.write(key)
        current += value.len

  time_end = time.time()
  print('Demorou: {} segundos'.format(time_end - time_start))

if __name__ == "__main__":
  main()