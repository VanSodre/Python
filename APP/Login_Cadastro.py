from sqlite3 import *
import getpass
from os import system
from time import *
from hashlib import *
from googletrans import *

class Sistema:
    def __init__(self, nome_database:str="banco_dados_login", nome_tabela:str="tabela_dados") -> None:
        self.nome_database = nome_database
        self.nome_tabela = nome_tabela   
        if len(self.nome_database.strip()) == 0 or len(self.nome_tabela.strip()) == 0:
            self.nome_database = "banco_dados_login"
            self.nome_tabela = "tabela_dados"  
            
        self.conn = connect(f"{self.nome_database}.db")
        self.c = self.conn.cursor()
            
        self.__tabela()
        
    def __tabela(self):
        c = self.c
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.nome_tabela} (usuario TEXT, senha TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")
        c.execute(f"CREATE TABLE IF NOT EXISTS tabela_senhas (senha TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")
        
    def __titulo(self, nome_titulo:str):
        input("")
        system("cls")
        print("\033[01;34m-"*42)
        print(nome_titulo.center(42))
        print("\033[01;34m-\033[m"*42)      
        
    def __criptografia(self, *args:str):
        cripto_hash = []
        for entrada in args:
            entrada_bytes = entrada.encode("utf-8")
            hash_object = sha256(entrada_bytes)
            cripto_hash.append(hash_object.hexdigest())
            
        return cripto_hash
    
    def __mostrar_senhas(self, id):
        c = self.c
        c.execute(f"SELECT * FROM tabela_senhas WHERE id=?", (id, ))
        mostrar = c.fetchone()
        if mostrar is not None:
            print(f"Sua senha é: {mostrar[0]}")   
            
    def fechar_conexao(self):
        c = self.c
        conn = self.c
        c.close()
        conn.close()       
    
    def login(self):
        c = self.c
        self.__titulo("LOGIN")
        usuario = str(input("Digite o nome de usuario: "))
        senha = str(input("Digite a sua senha: "))
        id =  int(input("Digite o id fornecido no cadastro: "))
        dados = self.__criptografia(usuario, senha)
        c.execute(f"SELECT * FROM {self.nome_tabela} WHERE usuario=? AND senha=? AND id=?", (dados[0], dados[1], id,))
        result = c.fetchone()
        if result is not None:
            print("Login bem sucedido.")
            self.__mostrar_senhas(id)
            
    
    def cadastro(self):
        c = self.c
        conn = self.conn
        self.__titulo("CADASTRO")
        usuario = str(input("Digite o nome de usuario a ser cadastrado: "))
        senha = getpass.getpass("Digite a senha a ser cadastrada: ")
        dados = self.__criptografia(usuario, senha)
        if len(usuario.strip()) >= 8 and len(str(senha).strip()) >= 8:
            c.execute(f"INSERT INTO {self.nome_tabela} (usuario, senha) VALUES (?, ?)", (dados[0], dados[1], ))
            c.execute("INSERT INTO tabela_senhas (senha) VALUES (?)", (senha, ))
            conn.commit()
            c.execute(f"SELECT * FROM {self.nome_tabela} ORDER BY id DESC LIMIT 1")
            ultimo_id = c.fetchone()
            if ultimo_id:
                print(f"O nome:{usuario}\nE senha:{senha}\nFoi cadastrado com o id:{ultimo_id[2]}")
                     
 
j = Sistema()
j.cadastro()
j.login()
j.fechar_conexao()
