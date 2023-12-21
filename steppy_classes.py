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
    
class AugAssign:

    def __init__(self, field):
        self.targets = field.target
        self.op = "AugAssign"
        self.value = field.value
        self.ope = field.op
    
    def getTargets(self):
        return self.targets
    
    def getValue(self):
        return self.value
    
    def getOp(self):
        return self.ope
    
class ForLoop:

    def __init__(self, field):
        self.target = field.target
        self.iter = field.iter
        self.body = field.body
        self.orelse = field.orelse
        self.op = "ForLoop"

    def getTargets(self):
        return self.target
    
    def getIter(self):
        return self.iter
    
    def getBody(self):
        return self.body
    
    def getOrElse(self):
        return self.orelse
    
    def getOp(self):
        return self.op