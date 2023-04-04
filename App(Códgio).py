from hashlib import *
from random import *
from PYTHON.baskara import Matematica
import os
class App:
    '''
    Precisa antes criar os arquvios chamados: App(lista_dados).txt e o arquivo App(lista_hash).txt
    Exemplo de como usar: <nome_variavel> = App(), <nome_variavel>.menu()
    '''
    def __init__(self):
        pass
    
    def nome(self, nome):
        os.system("cls")
        print("-"*42)
        print(str(nome).center(42))
        print("-"*42)

    def menu(self):
        while True:
            try:
                self.nome("MENU")
                opcoes = input("\033[01;37m[1] Jogo de adivinhar\n[2] Calculadora de equações de 2 grau\n[3] Sair\n")
                if opcoes == "1":
                    self.nome("Jogo de adivinhar")
                    self.dificuldade = int(input("[1] Fácil\n[2] Médio\n[3] Difícil\n[4] Impossivel\n"))
                    self.nome(f"DIFICULDADE {self.dificuldade}")
                    self.jogador_numero = input("Em que número estou pensando? ")
                    self.pontos()
                    input("")
                elif opcoes == "2":
                    self.nome("CALCULADORA DE EQUAÇÕES")
                    a = int(input("\033[01;37mCoeficiente a:"))
                    b = int(input("Coeficiente b:"))
                    c = int(input("Coeficiente c:"))
                    calculo = Matematica(a, b, c)
                    calculo.baskara()
                    input("")
                elif opcoes == "3":
                    print("\033[01;32mTchau.\033[m")
                    break                
            except Exception as erro:
                print(f"\033[01;31;43mErro: {erro}\033[m")
                if input("Deseja voltar ao menu?[S/N] ").upper()[0] == "N":
                    break

    def verificar(self):
        numero = md5(str(self.jogador_numero).encode()).hexdigest()
        with open("App(lista_hash).txt", "r", encoding="utf-8") as lista:
            lista_hash = lista.read()
        if numero in lista_hash:
            return True
        else:
            return False

    def gerar_numeros(self):
        if self.dificuldade == 1:
            numero = randint(1, 10)
        if self.dificuldade == 2:
            numero = randint(5, 20)
        if self.dificuldade == 3:
            numero = randint(10, 40)
        if self.dificuldade == 4:
            numero = randint(20, 100)
        with open("App(lista_hash).txt", "w") as escrever:
            escrever.write(md5(str(numero).encode()).hexdigest())
        
        return numero
        
    def pontos(self):
        if self.verificar():
            with open("App(lista_dados).txt", "r") as t:
                p = int(t.read().split(":")[1])
            p += 1
            with open("App(lista_dados).txt", "w") as t:
                t.write(f"p:{p}\n")
            print("Parabéns, você acertou!")
        else:
            print(f"Que pena, eu estava pensando em {self.gerar_numeros()}")

if __name__ == "__main__":
    j = App()
    j.menu()

