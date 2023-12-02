import ast
class Assign:

    def __init__(self, field):
        self.targets = field.targets
        self.value = field.value
        self.op = "Assign"
        if type(field.value) == ast.BinOp:
            self.op = "BinOp"
    
    def getTargets(self):
        return self.targets
    
    def getValue(self):
        return self.value

class Expression:
    
    def __init__(self, field):
        self.targets = None
        self.value = field.value
        self.op = "Expression"

    def getTargets(self):
        return None

    def getValue(self):
        return self.value