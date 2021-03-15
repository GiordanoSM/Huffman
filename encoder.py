import bitstring as bs
import tree as tr
import time
import sys
import os

def main(_dir=''):
  file_name = input('Write your file name: ')

  try:
    f = open(file_name, 'rb')
    symbols, n_bytes = get_prob(f) #Gera as probabilidades dos símbolos

  finally:
    f.close()

  code = create_code(symbols) #Cria os códigos de huffman

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  lengths = [value.len for key, value in sorted(code.items(),key= lambda x: x[0])] #Tamanhos dos códigos na ordem dos símbolos

  symbols_being = bs.Bits(length= 256) #256bits para indicar quais dos 256 simbolos existem (1 se existe e 0 se não)

  code, tree = tr.make_tree_code(code.keys(), lengths) #Gerando o código a ser utilizado

  #Para cada código, gerar o valor em 'symbols_being'
  for s in code:
    mask = bs.Bits(uint= 1, length= 256) << int.from_bytes(s, byteorder='big')
    symbols_being = symbols_being | mask

  print('Número de símbolos: {}'.format(len(lengths)))

  lengths = b''.join(list(map(lambda x: x.to_bytes(1, byteorder= 'big'), lengths))) #Tamanhos dos códigos em bytes para ser escrito no arquivo

  try:
    #Se tiver sido passado um diretório de destino específico
    if _dir:
      file_n = file_name.split('\\')[-1].split('/')[-1]
      f_write = open(_dir + '/' + file_n + '.bin', 'wb') #Extensão .bin
      file_n = _dir + '/' + file_n + '.bin'

    else: 
      f_write = open(file_name + '.bin', 'wb')
      file_n = file_name + '.bin'

    f_write.write(header.tobytes()) #Escreve o header no arquivo (0xF0), poderiormente 0 será o tamanho do padding final
    f_write.write(symbols_being.tobytes()) #Escreve a sequência de existência dos símbolos
    f_write.write(lengths) #Escreve os tamanhos dos códigos na ordem lexicográfica de seus símbolos

    f_read_bits = bs.Bits(filename= file_name) #Abre o arquivo para leitura

    padding = write_code(f_read_bits, f_write, code) #Escreve texto codificado

    f_write.seek(0)
    f_write.write((header[:4] + padding).tobytes()) #Insere a quantidade final de padding no cabeçalho

  finally:
    f_write.close()

  #compress_info()

  print('Tamanho do arquivo original em bytes: {}'.format(n_bytes))
  print('Tamanho do arquivo comprimido em bytes: {}'.format(os.path.getsize(file_n)))
  #print(code)
  #print(bs.Bits(filename= file_n).bin, padding)

#--------------------------------------------------------------------
#Gera um dicionário com os símbolos e suas probabilidades
def get_prob(f):

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

#-------------------------------------------------------------------------------------------------
#Gera o código de huffman
def create_code(symbols):

  code = {key: bs.Bits(bin='0b') for key in symbols.keys()}

  list_symbols = [[x] for x in symbols.keys()]

  #Ordenando uma lista com conjuntos de simbolos de menor a maior valores de probalilidades somados do conjunto
  list_symbols = sorted(list_symbols, key= lambda k: sum(map(lambda x: symbols[x], k)))

  #0 para o símbolo de menor probabilidade
  for s in list_symbols[0]:
    code[s] += bs.Bits(bin='0b0')

  #1 para o segundo símbolo de menor probabilidade
  for s in list_symbols[1]:
    code[s] += bs.Bits(bin='0b1')

  #Supõe que existem mais de 2 símbolos inicialmente
  while len(list_symbols) > 2:

    new = list_symbols[0] + list_symbols[1] #Cria novo símbolo como a junção dos dois com menor probabilidade
    list_symbols = list_symbols[2:] #Tira os dois primeiros símbolos
    list_symbols.append(new) #Coloca novo símbolo
    list_symbols = sorted(list_symbols, key= lambda k: sum(map(lambda x: symbols[x], k))) #Ordena pela probabilidade com o novo símbolo combinado

    for s in list_symbols[0]:
      code[s] = bs.Bits(bin='0b0') + code[s]

    for s in list_symbols[1]:
      code[s] = bs.Bits(bin='0b1') + code[s]

  return code #Dicionário com os simbolos e seus códigos

#------------------------------------------------------------------
#Escreve o texto codificado no arquivo
def write_code (f_read_bits, f_write, code):


  start = time.time()
  buffer = bs.Bits(bin='0b')
  cur_position = 0 #Posição no arquivo de leitura a partir do inicio
 
  print('Enconding... (this may take a while)')

  #Pega cada 8 bits e transforma em 1 byte
  byte = f_read_bits[cur_position: cur_position + 8].tobytes()

  #Percorre todos os bytes do arquivo
  while byte:
    buffer += code[byte]
    if buffer.len % 8 == 0: #A cada múltiplo de 8 bits de código gerado, escreve no arquivo e esvazia o buffer
      buffer.tofile(f_write)
      buffer = bs.Bits(bin='0b')

    cur_position += 8
    byte = f_read_bits[cur_position: cur_position + 8].tobytes()

  buffer.tofile(f_write) #Coloca o resto do código gerado no arquivo

  #print(buffer, buffer.len)

  end = time.time()
  print('Demorou: {} segundos'.format(end - start))

  #Retorna o padding utilizado na última adição ao arquivo
  if buffer.len % 8 == 0:
    padding = 0
  else: padding = 8 - (buffer.len % 8)

  return bs.Bits(int= padding, length= 4)

if __name__ == "__main__":
  #Aceita argumento com o diretório
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else: main()