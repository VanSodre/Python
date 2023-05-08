from sqlite3 import *
from time import *
from os import system
from main import Sistema

class Connect:
    
    def __init__(self, nome_database:str, nome_tabela:str):
        self.nome_database = nome_database
        self.nome_tabela = nome_tabela
        if nome_database == "" and nome_tabela == "":
            self.nome_database = "banco"
            self.nome_tabela = "tabela"
            
        self.conn = connect(f"{self.nome_database}.db")
        self.c = self.conn.cursor()
        c = self.c
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.nome_tabela} (usuario TEXT, senha TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

    def verificar_cadastro(self, usuario:str, senha:str):
        c = self.c
        if len(usuario.strip()) >= 8 and len(senha.strip()) >= 8:
            c.execute(f"SELECT * FROM {self.nome_tabela} WHERE usuario=? AND senha=?", (usuario, senha))            
            registros = c.fetchall()
            if len(registros) == 0:
                return True  
            else:
                return False
        else:
            return False
        
    def verificar_outros(self, usuario:str, senha:str, id:int):
        c = self.c
        if len(usuario) >= 8 and len(senha) >= 8 and len(str(id)) >= 1:
            c.execute(f"SELECT * FROM {self.nome_tabela} WHERE usuario=? AND senha=? AND id=?", (usuario, senha, id))            
            registros = c.fetchall()
            if registros:
                return True  
            else:
                return False
        else:
            return False        
    
class SistemaPrincipal(Connect):
    """Como usar:
    obj = SistemaPrincipal("<nome_banco_dados>", "<nome_tabela>")
    obj.menu()"""
    print("\033[01;37m")
    def __titulo(self, nome_titulo:str):
        system("cls")
        print("-"*42)
        print(nome_titulo.center(42))
        print("-"*42)
    
    def menu(self):
        r = False
        while r == False:  
            system("cls")
            try: 
                print("BEM VINDO")
                escolha = int(input("Suas opções são:\n[1] = Cadastro\n[2] = Login\n[3] = Ver dados\n[4] = Atualizar dados\n[5] = Apagar dados\n[6] = Sair\n "))
                if escolha >= 7 or escolha <= 0:
                    print("Escolha inválida!")
                elif escolha == 1:
                    self.cadastro()                    
                elif escolha == 2:
                    self.login()
                elif escolha == 3:
                    self.mostrar_dados()
                elif escolha == 4:
                    self.atualizar_dados()
                elif escolha == 5:
                    self.apagar_dados()
                elif escolha == 6:
                    r = True
                    break
                
            except ValueError:                
                print(f"Você digitou um caracter inválido!")
                
            
            input("")
    
    def cadastro(self):
        teste = Sistema()
        self.__titulo("CADASTRO")
        c, conn = self.c, self.conn
        usuario = str(input("Digite seu nome de usurio: ")).strip()
        senha = str(input("Digite a senha a ser cadastrada: ")).strip()
        if self.verificar_cadastro(usuario, senha):
            print("Cadastro bem sucedido..")
            usuario_e = teste.criptografar(usuario)
            senha_e = teste.criptografar(senha)
            c.execute(f"INSERT INTO {self.nome_tabela} (usuario, senha) VALUES (?, ?)", (usuario_e, senha_e, )) 
            conn.commit()
            c.execute(f"SELECT * FROM {self.nome_tabela} ORDER BY id DESC LIMIT 1")
            ultimo_id = c.fetchone()
            if ultimo_id:
                print(f"Você foi cadastrado com o id:{ultimo_id[2]}\nGuarde esse id, pois vai ser usado na hora do cadastro..")
        else:
            print("Falha no cadastro\nPossiveis falhas:\nVocÊ digitou um nome de usuario ou senha muito curtos, os nome de usuairo ou senha devem possuir pelo menos 8 caracteres\nOutro erro pode ser que o o nome de usuario ou senha já estão cadastrados!")
            if input("Deseja ser redirecionado ao login [S/N]? ").strip().upper()[0] == "S":
                self.login()      
        
    def login(self):
        self.__titulo("LOGIN")
        usuario = str(input("Digite o seu nome de usuario para fazer login: ")).strip()
        senha = str(input("Digite a sua senha para fazer login: ")).strip()
        id = int(input("Digite o seu id em que os dados inseridos acima foram cadastrados: "))
        if self.verificar_outros(usuario, senha, id):
            print("Login bem sucedido!")
        else:
            print("Falha no login!")
    
    def atualizar_dados(self):        
        self.__titulo("ATUALIZAR DADOS")
        c, conn = self.c,self.conn
        usuario = str(input("Digite o seu nome de usuario a ser atualizado: "))
        senha = str(input("Digite a sua senha a ser atualizada: "))
        id = int(input("Digite o seu id em que os dados inseridos acima foram cadastrados: "))
        if self.verificar_outros(usuario, senha, id):
            self.__titulo("NOVOS DADOS")
            novo_usuario = str(input("Digite o novo nome de usuario: ")).strip()
            novo_senha = str(input("Digite a nova senha: ")).strip()
            c.execute(f"UPDATE {self.nome_tabela} SET usuario=?, senha=? WHERE id=?", (novo_usuario, novo_senha, id))
            conn.commit()
            print("Dados atualizados com sucesso!")
        else:
            print("Dados inválidos")
    
    def apagar_dados(self):      
        self.__titulo("APAGAR DADOS")  
        c, conn = self.c,self.conn
        usuario = str(input("Digite o seu nome de usuario a ser apagado: "))
        senha = str(input("Digite a sua senha a senha a ser apagada: "))
        id = int(input("Digite o seu id em que os dados inseridos acima foram cadastrados: "))
        if self.verificar_outros(usuario, senha, id):
            c.execute(f"DELETE FROM {self.nome_tabela} WHERE id=?", (id,))
            conn.commit()
            print("Dados apagados com sucesso!")
        else:
            print("Dados inválidos")
    
    def mostrar_dados(self):
        self.__titulo("VER DADOS")
        c = self.c
        id = int(input("Digite o id dos dados que deseja ver: "))
        c.execute(f"SELECT * FROM {self.nome_tabela} WHERE id=?", (id, ))
        result = c.fetchone()
        if result is not None:
            print(f"Seus dados são:\nNome:{result[0]}\nSenha:{result[1]}\nId:{result[2]}")
            
        else:
            print("Ocorreu um erro\nTente mas tarde...")
            
    print("\033[01;37m\033[m")

if __name__ == "__main__":    
    obj = SistemaPrincipal("", "")
    obj.menu()


