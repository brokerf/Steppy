import sys
import os
import ast
from pathlib import Path
from steppy_classes import *
to_text = False
text_name = ""
def constructClass(module: ast.Module) -> list:
    """ Construct a classes based on the body of our ast.module of the whole file """
    classes = []
    #breakdown here
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
        elif typ == ast.AugAssign:
            clas = AugAssign(i)
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
    """ Construct both left and right values recursiverly if needed to compare them"""
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
        """ Iterate over all variables in our testing operations"""
        for i in range(len(test.ops)):
            comp_var = test.comparators[i] #assignment of testig variable
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
            op = test.ops[i] #match operation to be made
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
    lower[0] = lower[0].replace(lower[0][3:lower[0].rfind(":")], str(check_sucess), 1) #write whether the check suceeded or not
    print_Steppy(upper, middle, lower)
    if len(orelse) > 0:
        line = ast.unparse(orelse[0])
        if type(orelse[0]) == ast.If:
            line = "el" + line
        else:
            line = "else:\n" + (" " * 4) + line
        if check_sucess: #if check suceed we remove the orelse portion else we remove the body of the if statement
            lower[0] = lower[0][0:lower[0].find(line) - 1]
        else:
            lower[0] = lower[0][lower[0].find(line):]
            #print_Steppy(upper, middle, lower)
    IfBody(upper, middle, lower, body if check_sucess else orelse, ram) #handle if - body

def IfBody(upper, middle, lower, body, ram):
    """ Handle the body of the If - statement """

    lower[0] = ast.unparse(body[0]) + "\n"
    for x in range(len(body) - 1, 0, -1): # populate list with body of our if clause
        lower.insert(1, ast.unparse(body[x]) + "\n")
    #print_Steppy(upper, middle, lower)
    for i in body:
        print_Steppy(upper, middle, lower)
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
            index = lower[0].find("=")
            if index >= 0:
                lower[0] = lower[0][:index] + lower[0][index:].replace(left.id, str(ram.get(left.id)), 1)
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
    """ Perform the mathematical operation that is stored in node.op and return the result of left and right"""
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
    """ Print current Steppy Status """
    text = ""
    for i in upper: text += i
    text += "#" * 10 + "\n"
    for i in middle: text += i
    text += "#" * 10 + "\n"
    for i in lower: text += i
    print(text + "\n")
    if to_text:
        file = open(str(os.getcwd()) + "\\" + text_name, "a")
        file.write("\n" + text + "\n")
        file.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: py steppy_main.py [name of file to be stepped through]")
    else:
        try:
            reader = Path(str(sys.argv[-1])).open()
            #reader = open(str(os.getcwd() + "\\" + sys.argv[-1]))
            lines_solo = reader.readlines()
            reader = Path(str(sys.argv[-1])).open()
            #reader = open(str(os.getcwd() + "\\" + sys.argv[-1]))
            text = reader.read()
            lines = ""
            for x in lines_solo:
                lines += x
        except FileNotFoundError: #no such file or wrong name
            print("ERROR: No such file " + sys.argv[-1] + " found!")
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
            if "-v" in sys.orig_argv or "--verbose" in sys.orig_argv:
                print("#" * 20 + "\n")
                print(ast.dump(parsed, indent=4) + "\n")
                print("#" * 20 + "\n")
            if "-t" in sys.orig_argv or "--text" in sys.orig_argv:
                text_name = str(sys.argv[-1]) + "_stepped_through.txt"
                text_file = open(str(os.getcwd() + "\\" + text_name), "w")
                text_file.write("Here is the step process of the file " + sys.argv[-1] + "\n")
                text_file.close()
                to_text = True
            if "-h" in sys.orig_argv or "--help" in sys.orig_argv:
                print("This is the help message for Steppy - a step-through process for python programms.\n" + 
                        "Currently Steppy supports only python files.\n" + 
                        "Steppy supports 3 different options:" + 
                        "\n" + 
                        "\n" + 
                        "-v or --verbose: shows ast.dump of the whole file, useful when you want to see how the file structure looks.\n" +
                        "-h or --help: displays this message, you know how to use it.\n" + 
                        "-t or --text: writes the output in the terminal to a text file named <your file name>_stepped_through.txt. " +  
                        "Look in there for a more slowed down step through.\n" + 
                        "\nThe syntax for steppy usage is: py steppy_main.py [options from above] [name of your file]\n" + 
                        "for example: py steppy_main.py --text -v my_file.py\n" +
                        "This will make a text file with steppy process in it, aswell as show the ast Tree of said file.")
                exit(1)
            print_Steppy(upper, middle, lower)
            for classes in constructClass(parsed):
                
                targets = classes.getTargets() if classes.op != "If" else None
                value = classes.getValue() if classes.op != "If" else None
                if classes.op == "Assign":
                    
                    if type(targets[0]) is ast.Tuple: #multiple variables in one line, iter over all of them and add to ram
                        for i in range(len(targets[0].elts)):
                            ram[targets[0].elts[i].id] = value.elts[i].value
                    elif type(value) == ast.List:
                        new_list = []
                        for x in value.elts:
                            new_list.append(x.value)
                        ram[targets[0].id] = new_list
                    else:    
                        ram[targets[0].id] = value.value
                    upper.append(lower[0])
                    lower.pop(0)
                elif classes.op == "BinOp":
                    """ We encountered a BinOp, evaluate that and strip the line in lower from all <(>,<)> accurances"""
                    BinOp(upper, middle, lower, ram, value.left, value.op, value.right)
                    lower[0] = lower[0].replace("(", "")
                    lower[0] = lower[0].replace(")", "")
                    line2 = ast.parse(lower[0])
                    ram[line2.body[0].targets[0].id] = line2.body[0].value.value
                    upper.append(lower[0])
                    lower.pop(0)
                elif classes.op == "Expression":
                    #TODO: add actual expression handlng, for now it just puts it in the middle part
                    middle.append(lower[0])
                    lower.pop(0)
                elif classes.op == "If":
                    """ We encountered an if statement, queue if - handling"""
                    test = classes.getTest()
                    body = classes.body
                    orelse = classes.getOrElse()
                    IfElse(upper, middle, lower, ram, test, body, orelse)
                elif classes.op == "AugAssign":
                    """ Convert an AugAssign into a regular Assign with var to be assigned to, as its left value i.e: """
                    """ x += 2 -> x = x + 2; x *= y + 2 -> x = x * (y + 2)"""
                    new_line = ast.Assign([targets], ast.BinOp(targets, classes.getOp(), classes.getValue()))
                    new_line.lineno = 0
                    new_line.col_offset = 0
                    lower[0] = ast.unparse(new_line) + "\n" #replace the line to be printed with our new formed line
                    print_Steppy(upper, middle, lower)
                    """ Convert the right of new_line into a BinOp so that we can process it and assign the value to the var"""
                    new_value = BinOp(upper, middle, lower, ram, new_line.value.left, new_line.value.op, new_line.value.right)
                    ram[targets.id] = new_value
                    lower[0] = lower[0].replace(")", " ")
                    lower[0] = lower[0].replace("(", " ")
                    upper.append(lower[0])
                    lower.pop(0)
                else:
                    #Fail State
                    raise NotImplementedError
                print_Steppy(upper, middle, lower)
            #print(ram)
            