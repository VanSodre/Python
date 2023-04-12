from sqlite3 import *
from getpass import getpass
from os import system
class Sistem:     
    def __init__(self, nome_banco:str, nome_tabela:str):
        self.nome_banco = nome_banco
        self.nome_tabela = nome_tabela
        if len(self.nome_banco.strip()) == 0 or "<>\/:" in self.nome_banco or len(self.nome_tabela.strip()) == 0 or "<>\/:" in self.nome_tabela:
            self.nome_banco = "NONE" 
            self.nome_tabela = "NONE"   
            
        self.tabela() 
        
    def nome_bonito(self, nome_funcao:str):
        if len(nome_funcao.strip()) >= 1:
            system("cls")
            print("-"*42)
            print(nome_funcao.center(42))
            print("-"*42)        
        
    def tabela(self):
        conn = connect(f"{self.nome_banco}.db")
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.nome_tabela} (usuario TEXT, senha TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")    

    def cadastro(self):
        self.nome_bonito("CADASTRO")
        conn = connect(f"{self.nome_banco}.db")
        c = conn.cursor()
        usuario = input("Digite o nome de usuario a ser cadastrado: ")
        senha = getpass("Digite a senha a ser cadastrada: ")
        if len(usuario.strip()) >= 8 and len(senha.strip()) >= 8:
            c.execute(f"SELECT * FROM {self.nome_tabela} WHERE usuario=? AND senha=?", (usuario, senha,))
            r = c.fetchone()
            if r is None:
                c.execute(f"INSERT INTO {self.nome_tabela} (usuario, senha) VALUES (?, ?)", (usuario, senha, ))
                conn.commit()
                c.execute(f"SELECT * FROM {self.nome_tabela} ORDER BY id DESC LIMIT 1")
                ultimo_id = c.fetchone()
                if ultimo_id:
                    print(f"O nome:{ultimo_id[0]}\nE senha:{ultimo_id[1]}\nFoi cadastrado com o id:{ultimo_id[2]}")        
                c.close()
                conn.close()
            else:
                print("Nome de usuario ou senha já existentes")
            self.result = True
        elif usuario == "Anonimus" and senha == "2009":
            print("Você acessou a área confidencial\nNesta área você pode ver todos os dados..")
            if input("Deseja ver todos os dados [S/N]?").upper()[0] == "S":
                c.execute(f"SELECT * FROM {self.nome_tabela}")
                for row in c.fetchall():
                    print(f"Nome:{row[0]}|Senha: {row[1]}|Id: {row[2]}")
                self.result = True
            else:
                self.result = True
        else:
            print("Nome de usuario ou senha muito curtos.\nTente mas tarde...")
            self.result = False            
        input("")
        
    def login(self):     
        self.nome_bonito("LOGIN")
        if self.result:  
            conn = connect(f"{self.nome_banco}.db")
            c = conn.cursor()
            usuario = input("Digite o seu nome de usuario para fazer login: ")
            senha = getpass("Digite a sua senha para fazer login: ")
            id = int(input("Digite o seu id para fazer login: "))
            if len(usuario.strip()) >= 8 and len(senha.strip()) >= 8 and len(str(id).strip()) >= 1:
                c.execute(f"SELECT * FROM {self.nome_tabela} WHERE usuario=? AND senha=? AND id=?", (usuario, senha, id, ))
                r = c.fetchone()
                if r is not None:
                    print("Login bem sucedido...")
                    print(f"Os seu dados são:\nNome: {r[0]}\nSenha: {r[1]}\nId: {r[2]}")
                else:
                    print("Falha no login\nVerifique se o nome de usuario, sennha ou id estão corretos e tente mas tarde...")
            else:
                print("Nome de usuario, senha ou id muito curtos.\nTente mas tarde...")
        input("")        
if __name__ == "__main__":
    sistema = Sistem("banco_dados", "login_cadastro")
    sistema.cadastro()
    sistema.login()
    



        
