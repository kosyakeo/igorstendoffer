class Test:
    def __init__(self, a=10, b=20):
        self.a = a
        self.b = b
    def __del__(self):
        print(f"Удален: a={self.a}, b={self.b}")
x = Test(1, 2)
y = Test()
del x
