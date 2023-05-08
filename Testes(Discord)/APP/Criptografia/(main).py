import rsa
from cryptography.fernet import Fernet
from sqlite3 import *
from os import system

class Main:
    def __init__(self):
        self.conn = connect("chaves.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS dados (priva_key BLOB, key_encrypted BLOB, senha_encrypted BLOB, id INTEGER PRIMARY KEY);")
        
    def menu(self):
        r = False
        while r == False:  
            system("cls")
            try: 
                print("BEM VINDO")
                escolha = int(input("Suas opções são:\n[1] = Cadastro\n[2] = Ver senha\n[3] = Sair\n "))
                if escolha >= 4 or escolha <= 0:
                    print("Escolha inválida!")
                elif escolha == 1:  
                    input("Usuario: ")
                    senha = input("Senha: ")                  
                    self.criptografia(senha)                    
                elif escolha == 2:
                    id = int(input("Id: "))
                    self.descriptografar(id)
                elif escolha == 3:
                    r = True
                    break
            
            except ValueError:                
                print(f"Você digitou um caracter inválido!")            
        
            input("")
    
    def criptografia(self, senha:str):
        conn, c = self.conn, self.c
        
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        senha_encriptada = fernet.encrypt(senha.encode())
        
        public_key, private_key = rsa.newkeys(1024)
        encrypted_key = rsa.encrypt(key, public_key)
        
        c.execute("INSERT INTO dados (priva_key, key_encrypted, senha_encrypted) VALUES (?, ?, ?)", (private_key.save_pkcs1("PEM"), encrypted_key, senha_encriptada, ))
        conn.commit()
        
        c.execute("SELECT * FROM dados ORDER BY id DESC LIMIT 1")
        id = c.fetchone()
        if id:
            print(f"Você foi cadastrado com o id {id[3]}!")
    
    def descriptografar(self, id:int):
        c = self.c
        
        c.execute("SELECT * FROM dados WHERE id = ?", (id, ))
        consulta = c.fetchone()
        if consulta:
            priva_key = rsa.PrivateKey.load_pkcs1(consulta[0])
            key_decrypted = rsa.decrypt(consulta[1], priva_key)
            fernet = Fernet(key_decrypted)
            
            senha_decrypted = fernet.decrypt(consulta[2]).decode()
            print(f"A senha do id: {id} é {senha_decrypted}!")
        else:
            print("Id não encontrado!")
            

if __name__ == "__main__":
    obj = Main()
    obj.menu()