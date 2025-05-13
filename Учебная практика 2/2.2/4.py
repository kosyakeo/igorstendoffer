class Counter:
    def __init__(self, value=0):
        self.value = value
    def addition(self):
        self.value += 1
    def subtraction(self):
        self.value -= 1
c = Counter()
print(c.value)
c.addition()
c.addition()
print(c.value)
c.subtraction()
print(c.value)
c2 = Counter(5)
print(c2.value)