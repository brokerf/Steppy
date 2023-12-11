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
    
class If:

    def __init__(self, field):
        self.test = field.test
        self.body = field.body
        self.orelse = field.orelse
        self.op = "If"
    
    def getOrElse(self):
        return self.orelse
    
    def getTest(self):
        return self.test