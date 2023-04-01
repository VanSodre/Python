class Matematica:
    '''
    Este é um módulo  que calcula o delta e a raiz quadrada para calcular equações de 2 grau, segue abaixo um exemplo de como usar:
    a = int(input("Digite o coeficiente a:"))
    b = int(input("Digite o coeficiente b:"))
    c = int(input("Digite o coeficiente c:"))
    calculo = Matematica(a, b, c)
    print(calculo.baskara())
    O valor de a, b e c deve ser um inteiro
    '''
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def delta(self):
        de = self.b**2 - 4 * self.a * self.c
        return de
    
    def v_a(self, n):
        if n < 0:
            return n * -1
        else:
            return n
    
    def sqrt(self, delta):
        return delta ** 0.5   
    
    def baskara(self):
        delta = self.delta()
        if delta <= -1:
            x1 = (-self.b + self.sqrt(self.v_a(self.delta())) * 1j) / (2 * self.a)
            x2 = (-self.b - self.sqrt(self.v_a(self.delta())) * 1j) / (2 * self.a)
            print(f"x1 = {str(x1)} x2 = {str(x2)}")
        elif delta >= 1:
            r1 = (-self.b + self.sqrt(delta)) / (2 * self.a)
            r2 = (-self.b - self.sqrt(delta)) / (2 * self.a)
            print(f"x1 = {str(r1)} x2 = {str(r2)}")

if __name__ == "__main__":
    a = int(input("Digite o coeficiente a:"))
    b = int(input("Digite o coeficiente b:"))
    c = int(input("Digite o coeficiente c:"))
    calculo = Matematica(a=a, b=b, c=c)
    calculo.baskara()
