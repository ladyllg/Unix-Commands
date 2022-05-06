Este é a implementação de um command line interface que executa alguns comandos básicos do sistema UNIX

- Um arquivo log é gerado em cada sessão
- Trata possiveis erros adequadamento
- Simula execução em background (&)

Implementado em ***Python 3.6.9*** 

""" COMANDOS """

pwd

mkdir [destination]
    Não cria multiplos subdiretorios
    Reconhece os identificadores (~), (..)

    Exemplos: 
        mkdir Linux
        mkdir ~/Linux
        mkdir pastaExistente/Linux

ls [destination]
    Caso pasta não especificada, lista os arquivos do diretorio atual
    Reconhece os identificadores (~), (..)
    Exemplos 
        ls ~
        ls .

cd [destination]
    Reconhece os identificadores (~), (/), (..)

cp [source] [destination]
    Não copia diretorios, apenas arquivos.
    Aceita renomar o arquivo que está sendo copiado (em seu novo diretorio)
    Reconhece os identificadores (~), (/), (..)
    
rm [-r] [destination]
    Para apagar uma pasta (vazia ou não), digitar a flag -r
    Consegue apagar multiplos arquivos
    Reconhece os identificadores (~), (/), (..)
    Exemplo 
        rm ~/ai.txt testes/textoqualquer.txt

mv [source] [destination]
    Não consegue mover diretórios
    Reconhece os identificadores (~), (/), (..)

cat [source]
    Pode criar um novo arquivo (ou sobrescrever um ja existente) quando utilizar ">"
    Reconhece os identificadores (~), (/), (..)
    Exemplos 
        cat > pastaexistente/teste.txt
        cat arquivo.py

help
    Lista os comandos que implementei

echo 
    Implementação mais básica do comando echo