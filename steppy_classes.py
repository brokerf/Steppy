import ast

"""
Assign each class its default Values\n
Each class has per default targets, values and op.\n
Targets is either Body.targets or None in case its doesnt have any targets.\n
Values represent the values which are substitued in the operations later on.\n
Op is a string containing the type of the class to be invoked when needed.\n
Field is the original ast.Class from which it came.\n 
"""


class Assign:

    def __init__(self, field):
        self.targets = field.targets
        self.value = field.value
        self.op = "Assign"
        """if type(field.value) == ast.BinOp:
            self.op = "BinOp"""
        self.field = field
    
    def getTargets(self):
        return self.targets
    
    def getValue(self):
        return self.value
    
    def getOp(self):
        return self.op
    
    def getField(self):
        return self.field

class Expression:
    
    def __init__(self, field):
        self.targets = None
        self.value = field.value
        self.op = "Expression"
        self.field = field

    def getTargets(self):
        return None

    def getValue(self):
        return self.value
    
    def getOp(self):
        return self.op
    
    def getField(self):
        return self.field
    
class Name:

    def __init__(self, field):
        self.id = field.id
        self.op = "Name"

    def getId(self):
        return self.id
    
    def getOp(self):
        return self.op

class If:

    def __init__(self, field):
        self.test = field.test
        self.body = field.body
        self.orelse = field.orelse
        self.op = "If"
        self.field = field

    def getBody(self):
        return self.body
    
    def getOrElse(self):
        return self.orelse
    
    def getTest(self):
        return self.test
    
    def getOp(self):
        return self.op
    
    def getField(self):
        return self.field
    
class AugAssign:

    def __init__(self, field):
        self.targets = field.target
        self.op = "AugAssign"
        self.value = field.value
        self.ope = field.op
        self.field = field
    
    def getTargets(self):
        return self.targets
    
    def getValue(self):
        return self.value
    
    def getOpe(self):
        return self.ope

    def getOp(self):
        return self.op
    
    def getField(self):
        return self.field
"""    
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
"""
class BinaryOp:

    def __init__(self, field):
        self.left = field.left
        self.right = field.right
        self.ope = field.op
        self.op = "BinOp"
        self.field = field

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
    def getOp(self):
        return self.op
    
    def getOpe(self):
        return self.ope
    
    def getField(self):
        return self.field

class UnaryOp:

    def __init__(self, field):
        self.operand = field.operand
        self.ope = field.op
        self.op = "UnaryOp"
        self.field = field

    def getOperand(self):
        return self.operand
    
    def getOp(self):
        return self.op
    
    def getOpe(self):
        return self.ope

    def getField(self):
        return self.field
    
class BoolOpe:

    def __init__(self, field):
        self.values = field.values
        self.op = "BoolOp"
        self.ope = field.op
        self.field = field

    def getValues(self):
        return self.values
    
    def getOp(self):
        return self.op
    
    def getOpe(self):
        return self.ope
    
    def getField(self):
        return self.field
    
class Compare:

    def __init__(self, field):
        self.left = field.left
        self.ops = field.ops
        self.comparators = field.comparators
        self.op = "Compare"
        
    def getLeft(self):
        return self.left
    
    def getOps(self):
        return self.ops
    
    def getComparators(self):
        return self.comparators
    
    def getOp(self):
        return self.op