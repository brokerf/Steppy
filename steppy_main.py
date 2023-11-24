import sys
import os
import ast

class Assign:

    def __init__(self, field):
        self.targets = field.targets
        self.op = "Assign"
    
    def getTargets(self):
        return self.targets

class Expression:
    
    def __init__(self, field):
        self.value = field.value
        self.op = "Expression"


def constructClass(body):
    """ Construct a Class based on the ast.body"""
    steps = []
    for i in body.body:
        typ = type(i)
        if typ == ast.Assign:
            f = Assign(i)
        elif typ == ast.Expr:
            f = Expression(i)
        steps.append(f)
    return steps    


if __name__ == "__main__":
    """print(os.getcwd())
    if len(sys.argv) < 2:
        print("USAGE: py steppy_main.py + [name of file to be stepped through]")
    else:
        try:
            reader = open(str(os.getcwd() + "\\" +  sys.argv[1]))
        finally:
            print(reader.readlines())"""
    if len(sys.argv) < 2:
        print("USAGE: py steppy_main.py [name of file to be stepped through]")
    else:
        try:
            reader = open(str(os.getcwd() + "\\" + sys.argv[1]))
        finally:
            mainbody = ast.parse(reader.read())
            print(ast.dump(mainbody, indent=8))
            steps = constructClass(mainbody)
            print(steps)
            print(0)