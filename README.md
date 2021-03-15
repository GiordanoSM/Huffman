# Informações
Autor: Giordano Süffert Monteiro
Versão Python: 3.7.1
Executado pela linha de comando

# Execução de encoder.py

## Argumentos

Possível passagem de parâmetro na hora de execução indicando o nome da pasta de destino do resultado do programa (diretório já deve existir). Caso não passe nada, será criado o arquivo sem a extensão .bin no mesmo diretório do arquivo que será lido .

Será pedido o nome do arquivo a ser codificado. Incluir o caminho até ele a partir do diretório atual.

Exemplo:
  >python3 encoder.py bin
  >Write your file name: arquivos/fonte0.txt

## Resultado

O arquivo resultante terá o mesmo nome do arquivo lido, e estará ou no mesmo diretório que ele, ou em outro caso tenha sido especificado na chamada do programa.

Exemplo: 
  bin/fonte0.txt.bin

## Obs:

Não trata casos de exceção como (FileNotFound). Ocorrerá a exceção padrão da linguagem.

# Execução de decoder.py

## Argumentos

Possível passagem de parâmetro na hora de execução indicando o nome da pasta de destino do resultado do programa (diretório já deve existir). Caso não passe nada, será criado o arquivo sem a extensão .bin no mesmo diretório do arquivo que será lido (espera-se um .bin gerado pelo encoder.py).

Será pedido o nome do arquivo a ser decodificado. Incluir o caminho até ele a partir do diretório atual.

Exemplo:
  >python3 decoder.py results
  >Write your file name: bin/fonte0.txt.bin

## Resultado

O arquivo resultante terá o mesmo nome do arquivo lido, retirando as últimas 4 letras (tirando o .bin) e estará ou no mesmo diretório que ele, ou em outro caso tenha sido especificado na chamada do programa.

Exemplo: 
  results/fonte0.txt

## Obs:

Não trata casos de exceção como (FileNotFound). Ocorrerá a exceção padrão da linguagem.