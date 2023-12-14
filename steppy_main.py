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
            clas = Assign(i)
            classes.append(clas)
        elif typ == ast.Expr:
            clas = Expression(i)
            classes.append(clas)
        elif typ == ast.If:
            clas = If(i)
            classes.append(clas)
    return classes

def IfElse(upper, middle, lower, ram, test, body, orelse):
    """ Evaluate an if-else statement """
    check_sucess = True
    if type(test) == ast.Name: #existence check i.e: if x: ...
        if not ram[test.id]:
            check_sucess = False
        else:
            lower[0] = lower[0].replace(test.id, str(ram[test.id]), 1)
            print_Steppy(upper, middle, lower)
    if type(test) == ast.Compare:
        if type(test.left) == ast.BoolOp:
            left = BoolOp(upper, middle, lower, ram, test.left)
        elif type(test.left) == ast.BinOp:
            left = BinOp(upper, middle, lower, ram, test.left.left, test.left.op, test.left.right)
        elif type(test.left) == ast.Name:
            left = ram[test.left.id]
            if ram[test.left.id]:
                lower[0] = lower[0].replace(test.left.id, str(left), 1)
                print_Steppy(upper, middle, lower)
        elif type(test.left) == ast.Constant:
            left = test.left.value

        for i in range(len(test.ops)):
            comp_var = test.comparators[i]
            if type(comp_var) == ast.Name:
                lower[0] = lower[0].replace(comp_var.id, ram[comp_var.id], 1)
                print_Steppy(upper, middle, lower)
                comp_var = ram[comp_var.id]
            elif type(comp_var) == ast.Constant:
                comp_var = comp_var.value
            elif type(comp_var) == ast.BinOp:
                comp_var = BinOp(upper, middle, lower, ram, comp_var.left, comp_var.op, comp_var.right)
            elif type(comp_var) == ast.BoolOp:
                comp_var = BoolOp(upper, middle, lower, ram, comp_var)
            op = test.ops[i]
            match type(op):
                case ast.Gt:
                    if left > comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.GtE:
                    if left >= comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.Lt:
                    if left < comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.LtE:
                    if left <= comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.Is:
                    if left is comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.IsNot:
                    if left is not comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.In:
                    if left in comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.IsNot:
                    if left is not comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.Eq:
                    if left == comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break
                case ast.NotEq:
                    if left != comp_var:
                        left = comp_var
                    else:
                        check_sucess = False
                        break

    if check_sucess: #check suceed originally
        line = ast.unparse(orelse[0])
        if type(orelse[0]) == ast.If:
            line = "el" + line
        else:
            line = "else:\n" + (" " * 4) + line
        lower[0] = lower[0].replace(lower[0][3:lower[0].find(":")], "True", 1)
        print_Steppy(upper, middle, lower)
        lower[0] = lower[0][0:lower[0].find(line) - 1]
        print_Steppy(upper, middle, lower)
        IfBody(upper, middle, lower, body, ram)
    else: #check failed
        line = ast.unparse(orelse[0])
        if type(orelse[0]) == ast.If:
            line = "el" + line
        else:
            line = "else:\n" + (" " * 4) + line
        lower[0] = lower[0].replace(lower[0][3:lower[0].find(":")], "False", 1)
        print_Steppy(upper, middle, lower)
        lower[0] = lower[0][lower[0].find(line):]
        print_Steppy(upper, middle, lower)
        IfBody(upper, middle, lower, orelse, ram)

def IfBody(upper, middle, lower, body, ram):
    """ Handle the body of the if-clause """

    lower[0] = ast.unparse(body[0]) + "\n"
    for x in range(len(body) - 1, 0, -1): # populate list with body of our if clause
        lower.insert(1, ast.unparse(body[x]) + "\n")
    print_Steppy(upper, middle, lower)
    for i in body:
        if type(i) == ast.Assign:
            if type(i.value) == ast.Constant:
                for x in i.targets:
                    ram[x.id] = i.value.value
            elif type(i.value) == tuple:
                for x in range(len(i.targets)):
                    ram[i.targets[x].id] = i.value[min(x, len(i.value))].value
            upper.append(lower[0])
            lower.pop(0)
            
        if type(i) == ast.BoolOp:
            BoolOp(upper, middle, lower, ram, i)
            
        elif type(i) == ast.BinOp:
            BinOp(upper, middle, lower, ram, i.left, i.op, i.right)
            lower[0] = lower[0].replace("(", "")
            lower[0] = lower[0].replace(")", "")
            line2 = ast.parse(lower[0])
            ram[line2.body[0].targets[0].id] = line2.body[0].value.value
            upper.append(lower[0])
            lower.pop(0)
            
        elif type(i) == ast.If:
            IfElse(upper, middle, lower, ram, i.test, i.body, i.orelse)
        elif type(i) == ast.Expr:
            middle.append(lower[0] + "\n")
            lower.pop(0)
            print_Steppy(upper, middle, lower) 
        #print_Steppy(upper, middle, lower)

def BoolOp(upper, middle, lower, ram, value):
    """ Evaluate a Bool Operation """        
    op = value.op
    values = value.values
    return_value = True #return value of the whole function
    for i in range(0, len(values) - 1):
        match type(values[i]):
            case ast.BoolOp:
                left = BoolOp(upper, middle, lower, ram, values[i])
            case ast.Name:
                left = ram[values[i].id]
                lower[0] = lower[0].replace(values[i].id, str(left), 1)
                print_Steppy(upper, middle, lower)
            case ast.Constant:
                left = values[i].value
        match type(values[i + 1]):
            case ast.BoolOp:
                right = BoolOp(upper, middle, lower, ram, values[i + 1])
            case ast.Name:
                right = ram[values[i + 1].id]
                lower[0] = lower[0].replace(values[i].id, str(right), 1)
                print_Steppy(upper, middle, lower)
            case ast.Constant:
                right = values[i + 1].value
        match type(op):
            case ast.And:
                return_value = return_value and (left and right)
            case ast.Or:
                return_value = return_value and (left or right)
    return return_value

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
            reader = open(str(os.getcwd() + "\\" + sys.argv[1]))
            text = reader.read()
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
            lower = []
            parsed = ast.parse(text)
            for i in parsed.body:
                lower.append(ast.unparse(i) + "\n")
            ram = dict() #construct a "RAM" to hold any vars we encounter
            #print(ast.dump(parsed, indent=4))
            print_Steppy(upper, middle, lower)
            for classes in constructClass(parsed):
                
                targets = classes.getTargets() if classes.op != "If" else None
                value = classes.getValue() if classes.op != "If" else None
                if classes.op == "Assign":
                    #print("ENTERING ASSIGN!")
                    if type(targets[0]) is ast.Tuple: #multiple variables in one line, iter over all of them and add to ram
                        for i in range(len(targets[0].elts)):
                            ram[targets[0].elts[i].id] = value.elts[i].value
                    else:
                        ram[targets[0].id] = value.value
                    upper.append(lower[0])
                    lower.pop(0)
                elif classes.op == "BinOp":
                    #print("ENTERING BinOP!")
                    BinOp(upper, middle, lower, ram, value.left, value.op, value.right)
                    lower[0] = lower[0].replace("(", "")
                    lower[0] = lower[0].replace(")", "")
                    line2 = ast.parse(lower[0])
                    ram[line2.body[0].targets[0].id] = line2.body[0].value.value
                    upper.append(lower[0])
                    lower.pop(0)
                elif classes.op == "Expression":
                    middle.append(lower[0] + "\n")
                    lower.pop(0)
                elif classes.op == "If":
                    test = classes.getTest()
                    body = classes.body
                    orelse = classes.getOrElse()
                    IfElse(upper, middle, lower, ram, test, body, orelse)
                else:
                    raise NotImplementedError
                print_Steppy(upper, middle, lower)