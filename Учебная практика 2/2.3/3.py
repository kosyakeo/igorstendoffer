class Calculation:
    def __init__(self):
        self.calculationLine = ""
    def SetCalculationLine(self, value):
        self.calculationLine = value
    def SetLastSymbolCalculationLine(self, symbol):
        self.calculationLine += symbol
    def GetCalculationLine(self):
        return self.calculationLine
    def GetLastSymbol(self):
        return self.calculationLine[-1] if self.calculationLine else ""
    def DeleteLastSymbol(self):
        if self.calculationLine:
            self.calculationLine = self.calculationLine[:-1]
calc = Calculation()
calc.SetCalculationLine("4252")
print(calc.GetCalculationLine())
calc.SetLastSymbolCalculationLine("-")
print(calc.GetCalculationLine())
print(calc.GetLastSymbol())
calc.DeleteLastSymbol()
print(calc.GetCalculationLine())