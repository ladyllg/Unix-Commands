import datetime
import errno
from pathlib import Path
import shutil
import logging
import os

""" Função auxiliar para a implementação do comando cd. """
def generate_abs_path(current_path_args, new_path_args):
    if len(current_path_args) < len(new_path_args):
        for arg in new_path_args[len(current_path_args):]:
            current_path_args.append(arg)
    if len(current_path_args) > len(new_path_args):
        for arg in new_path_args:
            current_path_args.append(arg)
    else:
        current_path_args = []
        for arg in new_path_args:
            current_path_args.append(arg)
    
    return current_path_args

""" Função que retorna o caminho absoluto do diretorio atual. """
def psh_pwd(current_path):
    # A classe Path é ultilizada para retorna o diretorio raiz do usuário
    print(current_path.replace("~",str(Path.home())))

""" Função que executa o comando mkdir. 
    Não aceita opções, logo o comando implementado não cria multiplos subdiretórios
"""
def psh_mkdir(command, current_path):
    # Criando o caminho absoluto do diretorio atual
    abs_current_path = current_path.replace("~",str(Path.home()))

    # Mudando para o diretorio atual
    os.chdir(abs_current_path)

    # Lidando com o identificador ~ caso exista
    if "~" in command:
        command = command.replace("~", str(Path.home()))

    # Extraindo o nome do novo diretorio
    target_name_dir = command.split("/")[-1]

    # Gerando o caminho absoluto p o diretorio pai da nova pasta 
    abs_target_path = str(Path(command).resolve()).replace(target_name_dir,"").replace(" ","")
    
    try:
        # Por fim, muda para o diretorio pai desejado
        os.chdir(abs_target_path)

        # Cria a nova pasta com ajuda da lib pathlib
        Path(target_name_dir).mkdir()        
    except Exception as e:
        logging.error(e)
        print(e)

""" Função que executa o comando ls mais básico. 
    Para funcionar corretamente é possivel chamar apenas o comando ou informar o diretório desejado
    Não aceita opções
"""
def psh_ls(current_path, path):
    # Criando caminho absoluto
    abs_current_path = current_path.replace("~",str(Path.home()))
    abs_desired_path = path.replace("~", str(Path.home()))  
    
    # Primeiro, muda para o diretorio atual
    os.chdir(abs_current_path)

    # Verificando se um diretorio foi especificado
    if abs_desired_path != "":
        p = Path(abs_desired_path.replace(" ",""))
    else:
        p = Path(abs_current_path)
    
    # Se caminho for um diretorio, lista os arquivos
    if p.is_dir():
        files_dict = []
        for x in p.iterdir():
            if not x.name.startswith('.'):
                files_dict.append(x.name)

        print('   '.join(files_dict))
    else:
        print("[Errno 20] Not a directory: ", str(p))
        logging.error("[Errno 20] Not a directory: " + str(p))

""" Função que executa o comando cd 
    Nessa implementação os diretórios não sao acessados literalmente, mas sim a string de referencia
    vai sendo atualizado. 
    Reconhece os identificadores (~), (/), (..)
"""
def psh_cd(current_path, new_path):
    # Criando o caminho absoluto da pasta atual
    current_path = current_path.replace("~", str(Path.home()))

    # Caso diretorio desejado é o root, apenas retorna ~
    if new_path == '~':
        return new_path
    if new_path == '/':
        return new_path

    # Criando o caminho absoluto da pasta desejada 
    new_path = new_path.replace("~", str(Path.home())).replace(" ","")

    # Criando listas para cada caminho absoluto
    new_path_args = new_path.split("/")
    current_path_args = current_path.split("/")
       


    if new_path == '..':
        return "/".join(current_path_args[:-1]).replace(str(Path.home()), "~")
    else: 
        # Um caminho relativo foi especificado
        # Se len(current_path_args) < len(new_path_args), significa que vamos DESCER a árvore de diretorios
        # Se len(current_path_args) > len(new_path_args), significa que vamos SUBIR a árvore de diretorios

        # Função generate_abs_path vai retornar uma lista que concatena as arrays, gerando 
        # o novo caminho para onde deve-se seguir
        current_path_args = generate_abs_path(current_path_args, new_path_args)
    
    # Verificando se o novo caminho existe
    abs_current_path = "/".join(current_path_args)
    path_aux = Path(abs_current_path).resolve()
    if path_aux.exists():
        return str(path_aux).replace(str(Path.home()), "~")
    else:
        print("cd: no such file or directory: {}".format(new_path))
        logging.error("cd: no such file or directory: {}".format(new_path))
        return current_path.replace(str(Path.home()), "~")

""" Função que executa o comando mv 
    Basicamente chama as funções implementadas de copiar e remover arquivos
    Não move diretorios, apenas arquivos!
"""
def psh_mv(current_path,command):
    try:
        if psh_cp(current_path, command):
            args = command.split(" ")
            psh_rm(args[0],current_path) # Delete o arquivo original q foi copiada para a nova pasta
    except Exception as e:
        pass

""" Função que executa o comando rm 
    Aceita apenas a flag '-r' !    
"""
def psh_rm(command, current_path):
    current_path_args = current_path.replace("~", str(Path.home())).split("/")
    abs_current_path = current_path.replace("~", str(Path.home()))
    args = command.split(" ")
    files = []
    flags = []

    # Primeiro, muda para o diretorio atual
    os.chdir(abs_current_path)

    # Seperando em listas o parametro -r caso exista, e o nomes dos arquivos/diretorios a serem removidos
    for arg in args:
        if arg == '-r':
            flags.append(arg)
        else:
            files.append(arg)

    # Removendo diretórios
    if "-r" in flags:        
        for file in files:
            # Criando o caminho absoluto para o diretorio
            path_dir = file.replace("~", str(Path.home()))
            abs_path_dir = str(Path(path_dir).resolve())
            try:
                try:
                    file_path = Path(abs_path_dir)
                    file_path.rmdir() # Passa o caminho absoluto da pasta para Path() e o remove
                except OSError: 
                    shutil.rmtree(file_path) # Usa a lib para remover a arvore de arquivos da pasta nao vazia
                except Exception as e:
                    print(e)
                    logging.error(e)
            except Exception as e: # Erro FileNotFoundError
                print(e)
                logging.error(e) 
    else:
        # Removendo arquivos
        for file in files:
            path_file = file.replace("~", str(Path.home()))
            abs_path_file = str(Path(path_file).resolve())
            print("excluindo ", path_file)
            try:
                file_path = Path(abs_path_file)
                file_path.unlink() # Passa o caminho absoluto do arquivo para Path() e o remove
            except Exception as e:
                print(e)
                logging.error(e)

""" Função que executa o comando cat 
    Aceita o comando ">" para criar um novo arquivo de texto num diretorio existente 
"""
def psh_cat(command, current_path):
    abs_current_path = current_path.replace("~", str(Path.home()))
    
    # Primeiro, muda para o diretorio atual
    os.chdir(abs_current_path)

    # Cria novo arquivo  
    if ">" in command:        
        desired_path = command.replace("> ","")
        # Criando o caminho absoluto do novo arquivo
        abs_desired_path = desired_path.replace("~", str(Path.home())).replace(" ","")    
        
        # Extraindo o nome do novo arquivo
        file_name = str(abs_desired_path).split("/")[-1]

        # Criando caminho absoluto do diretorio pai 
        abs_dir_desired_path = str(Path(abs_desired_path).resolve()).replace(file_name, "")        
        try:
            os.chdir(abs_dir_desired_path) # Muda para o diretorio pai
            try:
                if not Path(file_name).exists():            
                    f = open(str(file_name), "x") # Cria novo arquivo com o nome desejado
                else:
                    f = open(str(file_name), "w") # Caso arquivo ja existe, sobrescreve

                lines = []
                while True:                
                    try:
                        inp = input()
                        lines.append(inp)
                    except EOFError:
                        break
                for line in lines:
                    f.write(line+"\n")
                f.close()                 
            except Exception as e:
                logging.error(e)
                print(e) 
        except Exception as e:
            print(e)
    else:
        # Cat modo leitura
        files = command.split(" ")
        for file_path in files:            
            abs_desired_path = file_path.replace("~", str(Path.home()))  # Define o caminho absoluto para o arquivo      
            p = Path(abs_desired_path) # Cria um Path para o caminho desejado
            if not p.is_dir():
                try:        
                    # Abre arquivo
                    with p.open() as f:
                        lines = f.readlines()
                        for line in lines:
                            print(line.replace("\n", ""))
                except Exception as e:
                    print("[Errno 2] No such file or directory: " + abs_desired_path)
                    logging.error("[Errno 2] No such file or directory: " + abs_desired_path)
            else:
                print("cat: ", abs_desired_path+": Is a directory")  
                logging.error(abs_desired_path+": Is a directory") 
     
def psh_help(current_path):
    print("""psh: implementação de alguns comandos básicos do sistema UNIX
            pwd
            mkdir [destination]
            ls [destination]
            cd [destination]
            mv [source] [destination]
            rm [-r] [destination]
            cat [source]
            cp [source] [destination]
            echo "[message]"

            Para mais detalhes, ler o arquivo README.md
            """)

""" Função auxiliar para executar o comando cp """
def handle_root(path):
    if "~" in path:
        return path.replace("~",str(Path.home()))
    return path

""" Função para executar o comando cp
    Não copia pastas! Ou seja, não reconhece a flag "-r"
    Tem a possibilidade de renomar o arquivo q esta sendo copiado
"""
def psh_cp(current_path, command):
    files = command.split(" ") # Separa os caminhos especificados
    current_path = handle_root(current_path)

    if len(files) == 1:
        # Lidando com argumento invalido
        print("cp: missing destination file operand after "+files[0])
        logging.error("cp: missing destination file operand after "+files[0])
    else:
        try:
            file_path = files[0] # Arquivo source
            target_dir = files[1] # Diretorio de destino

            os.chdir(current_path) # Muda para o diretorio atual q está o shell

            # Caso caminho seja um diretorio, a função finaliza
            if os.path.isdir(file_path): # Passa o caminho relativo
                raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), file_path)              
            
            
            file_name = file_path.split("/")[-1] # Extraindo o nome do arquivo que vai ser copiado
            file_dir = handle_root(file_path) # Criando o caminho absoluto para o diretorio que vai ser copiado

            # Abrindo arquivo e criando outro temporario igual
            file_pointer = open(file_dir, 'r')
            temp_file = file_pointer.read()
            file_pointer.close()
            
            # Verifica se o target_dir é um diretorio
            if(os.path.isdir(handle_root(target_dir))):
                file_name = file_name.split("/")[-1]
                target_dir = handle_root(target_dir)

            # Caso nao seja, indica que deseja-se renomear o arquivo
            else:
                file_name = target_dir.split("/")[-1] # Pega o ultimo argumento do target_dir
                target_dir = target_dir.replace(file_name, "") # Extraindo o diretorio pai 
            
            os.chdir(target_dir)  # Muda para o diretorio pai onde deseja-se colar o arquivo

            # Abrindo um novo arquivo e escrevendo os dados
            file_pointer = open(file_name, 'w') 
            file_pointer.write(temp_file)
            file_pointer.close()

            return True
        except Exception as e:
            print(e)
            logging.error(e)
            return False

""" Função para executar o comando echo mais básico """
def psd_echo(text):
    print(text)

def commands(inp, current_path):
    if "cd " in inp[:3]:
        current_path = psh_cd(current_path, inp[3:])
    elif inp == "help":
        psh_help(current_path)
    elif "ls" in inp[:3]:
        psh_ls(current_path, inp[3:])
    elif inp == "pwd":
        psh_pwd(current_path)
    elif inp[:3] == "rm ":
        psh_rm(inp[3:], current_path)
    elif inp[:4] == "cat ":
        psh_cat(inp[4:], current_path)
    elif inp[:6] == "mkdir ":
        psh_mkdir(inp[6:], current_path)
    elif inp[:3] == "cp ":
        psh_cp(current_path, inp[3:])
    elif inp[:3] == "mv ":
        psh_mv(current_path, inp[3:])
    return current_path

def main():    
    current_path = str(Path.cwd())
    current_path = current_path.replace(str(Path().home()), "~")

    log_time = datetime.datetime.now().strftime("%H%M%S")
    LOG_FILENAME = str("log_session"+log_time)
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format=FORMAT)

    print(""" ~ Bem vindo ao meu CMD. Para listas os comandos implementados digite 'help'""")
    while True:
        inp = input(current_path + " $ ")        
        logging.info('{}'.format(inp))

        if inp == "exit":
            break 
        if " & " in inp:
            for cmd in inp.split(" & "):                
                current_path = commands(cmd, current_path)
        else:
            current_path = commands(inp, current_path)

if '__main__' == __name__:
    main()