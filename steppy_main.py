import sys
import os
import ast
from steppy_classes import *

def constructClass(module: ast.Module) -> list:
    """ Construct a class based on the ast.class it represents """
    classes = []
    for i in module.body:
        typ = type(i)
        if typ == ast.Assign:
            Class = Assign(i)
            classes.append(Class)
        elif typ == ast.Expr:
            Class = Expression(i)
            classes.append(Class)
    return classes
"""
def step_through_line(Class, upper: list, middle: list, lower: list):
    for i in Class:
        value = i.getValues()
        targets = i.getTargets()
        if i is not None:
            for x in targets:
"""

def BinOp(upper, middle, lower, ram, left, op, right):
    """ Evaluate Binary Operations recursively """
    if type(left) == ast.BinOp:
        left = BinOp(upper, middle, lower, ram, left.left, left.op, left.right)
    elif type(left) == ast.Name:
        if left.id in ram:
            lower[0] = lower[0].replace(left.id, str(ram.get(left.id)), 1)
            left = ram.get(left.id)
            print_Steppy(upper, middle, lower)
        else:
            raise NameError
    elif type(left) == ast.Constant:
        left = left.value

    if type(right) == ast.BinOp:
        right = BinOp(upper, middle, lower, ram, right.left, right.op, right.right)
    elif type(right) == ast.Name:
        if right.id in ram:
            lower[0] = lower[0].replace(right.id, str(ram.get(right.id)), 1)
            print_Steppy(upper, middle, lower)
        else:
            raise NameError
    elif type(right) == ast.Constant:
        right = right.value
    if type(right) in [int, float] and type(left) in [int, float]:
        left_index = lower[0].index(str(left))
        right_index = lower[0].index(str(right)) + len(str(right))
        if type(op) == ast.Add:
            lower[0] = lower[0].replace(lower[0][left_index:right_index], str(left + right), 1)
            print_Steppy(upper, middle, lower)
            return left + right
        elif type(op) == ast.Div:
            lower[0] = lower[0].replace(lower[0][left_index:right_index], str(left / right), 1)
            print_Steppy(upper, middle, lower)
            return left / right
        elif type(op) == ast.Sub:
            lower[0] = lower[0].replace(lower[0][left_index:right_index], str(left - right), 1)
            print_Steppy(upper, middle, lower)
            return left - right
        elif type(op) == ast.Mult:
            lower[0] = lower[0].replace(lower[0][left_index:right_index], str(left * right), 1)
            print_Steppy(upper, middle, lower)
            return left * right

def print_Steppy(upper, middle, lower):
    """ Print current Steppy States """
    text = ""
    for i in upper: text += i
    text += "#" * 10 + "\n"
    for i in middle: text += i
    text += "#" * 10 + "\n"
    for i in lower: text += i
    print(text + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: py steppy_main.py [name of file to be stepped through]")
    else:
        try:
            reader = open(str(os.getcwd() + "\\" + sys.argv[1]))
            lines_solo = reader.readlines()
            lines = ""
            for x in lines_solo:
                lines += x
        except FileNotFoundError: #no such file or wrong name
            print("ERROR: No such file " + sys.argv[1] + " found!")
        else:
            # construct three list[<str>] which each hold the current representation
            # of Steppy, what lines have been evaluated (upper), which lines will print (middle)
            # and which lines are to be evaluated (lower). Then change them over time.
            
            upper = []
            middle = []
            lower = lines_solo 
            ram = dict() #construct a "RAM" to hold any vars we encounter

            #for x in lines_solo:
                #print(ast.dump(ast.parse(x), indent=8))    
            while len(lower) > 0:
                #print(len(lower))
                line = ast.parse(lower[0])
                #print(ast.dump(line, indent=8))
                line_classes = constructClass(line)
                for y in range(len(line_classes)):

                    Class = line_classes[y]
                    value = Class.getValue()
                    targets = Class.getTargets()
                    
                    # step through one line at a time and do necessary stuff
                    if Class.op == "Assign":
                        #print("ENTERING ASSIGN!")
                        if type(targets[0]) is ast.Tuple: #multiple variables in one line, iter over all of them and add to ram
                            for i in range(len(targets[0].elts)):
                                ram[targets[0].elts[i].id] = value.elts[i].value
                        else:
                            ram[targets[0].id] = value.value
                        upper.append(lower[0])
                        lower.pop(0)
                        #print(lower)
                    elif Class.op == "BinOp":
                        #print("ENTERING BinOP!")
                        BinOp(upper, middle, lower, ram, value.left, value.op, value.right)
                        lower[0] = lower[0].replace("(", "")
                        lower[0] = lower[0].replace(")", "")
                        line2 = ast.parse(lower[0])
                        ram[line2.body[0].targets[0].id] = line2.body[0].value.value
                        upper.append(lower[0])
                        lower.pop(0)
                    elif Class.op == "Expression":
                        middle.append(lower[0] + "\n")
                        lower.pop(0)
                    else:
                        raise NotImplementedError
                    print_Steppy(upper, middle, lower)
            print(ram)