import bitstring as bs

def main():
  file_name = input('Write your file name: ')

  try:
    f = open(file_name, 'rb')
    symbols, n_bytes = get_prob(f)
  
  except OSError as ose:
    print(ose)
    return -1

  finally:
    f.close()

  code = create_code(symbols)

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  lenghts = [value.len for key, value in sorted(code.items(),key= lambda x: x[0])]
  lenghts = b''.join(list(map(lambda x: x.to_bytes(1, byteorder= 'big'), lenghts)))

  symbols_being = bs.Bits(length= 256)

  for s in code:
    mask = bs.Bits(uint= 1, length= 256) << int.from_bytes(s, byteorder='big')
    symbols_being = symbols_being | mask

  #print(symbols_being.bin)
  print(len(lenghts))
  #print(map(lambda x: 255 - x, bs.Bits('0b100').findall('0b1', bytealigned=True)))

  try:
    f_write = open(file_name[:-4] + 'v2.b', 'wb')
    f_read = open(file_name, 'rb')

    f_write.write(header.tobytes())
    f_write.write(symbols_being.tobytes())
    f_write.write(lenghts)

    write_code(f_read, f_write, code)


  finally:
    f_write.close()
    f_read.close()

  print(len(code), len(symbols))
  print(n_bytes)


def get_prob(f):

  #bits = bs.Bits(filename = file_name)

  symbols = {} #Dicionario com os simbolos e probabilidades

  n_bytes = 0 #Contador dos bytes do arquivo

  byte = f.read(1)
  while byte:
    if byte in symbols.keys():
      symbols[byte] += 1
    else: symbols[byte] = 1

    n_bytes += 1
    byte = f.read(1)

  symbols = {key: value/n_bytes for key, value in symbols.items()} #Dividindo todos os valores pelo total

  return symbols, n_bytes

def create_code(symbols):

  code = {key: bs.Bits(bin='0b') for key in symbols.keys()}

  list_symbols = [[x] for x in symbols.keys()]

  #Ordenando uma lista com conjuntos de simbolos de menor a maior valores de probalilidades somados do conjunto
  list_symbols = sorted(list_symbols, key= lambda k: sum(map(lambda x: symbols[x], k)))

  for s in list_symbols[0]:
    code[s] += bs.Bits(bin='0b0')

  for s in list_symbols[1]:
    code[s] += bs.Bits(bin='0b1')

  while len(list_symbols) > 2:

    new = list_symbols[0] + list_symbols[1]
    list_symbols = list_symbols[2:]
    list_symbols.append(new)
    list_symbols = sorted(list_symbols, key= lambda k: sum(map(lambda x: symbols[x], k)))

    for s in list_symbols[0]:
      code[s] = bs.Bits(bin='0b0') + code[s]

    for s in list_symbols[1]:
      code[s] = bs.Bits(bin='0b1') + code[s]

  return code

def write_code (f_read, f_write, code):

  buffer = bs.Bits(bin='0b')
  byte = f_read.read(1)

  while byte:
      buffer += code[byte]
      if buffer.len % 8 == 0:
        buffer = bs.Bits(bin='0b')
      byte = f_read.read(1)
  
  print('Terminei o arquivo')

if __name__ == "__main__":
  main()