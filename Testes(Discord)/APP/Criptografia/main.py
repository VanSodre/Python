import rsa
from cryptography.fernet import Fernet
from sqlite3 import * 

conn = connect("banco_dados.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS dados (id INTEGER PRIMARY KEY, priva_key TEXT NOT NULL, key_encrypted BLOB, msg_encrypted BLOB);")

key = Fernet.generate_key()
fernet = Fernet(key)

usuario = input("Usuario: ")
senha = input("Senha: ")
encrypted_message = fernet.encrypt(senha.encode())

public_key, private_key = rsa.newkeys(1024)
encrypted_key = rsa.encrypt(key, public_key)

c.execute("INSERT INTO dados (priva_key, key_encrypted, msg_encrypted) VALUES (?, ?, ?)", (private_key.save_pkcs1("PEM"), encrypted_key, encrypted_message, ))
conn.commit()

c.execute("SELECT * FROM dados")
resultado = c.fetchone()
if resultado:
    priva_key = rsa.PrivateKey.load_pkcs1(resultado[1])
    key_decrypted = rsa.decrypt(resultado[2], priva_key)

    fernet1 = Fernet(key_decrypted)

    msg_decrypted = fernet1.decrypt(resultado[3]).decode()
    print(msg_decrypted)

    
    
    
    