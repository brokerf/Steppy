import sys
import os
import ast
from pathlib import Path
from steppy_classes import *
to_text = False
fileName = ""
paused = False
def constructClass(module: ast.Module) -> list:
    """ Construct classes based on the body of our ast.module of the whole file 
    
        Assign each member its own class based on its type
    """
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
        elif typ == ast.UnaryOp:
            clas = UnaryOp(i)
            classes.append(clas)
        elif typ == ast.BinOp:
            clas = BinOp(i)
            classes.append(clas)
        elif typ == ast.Compare:
            clas = Compare(i)
            classes.append(clas)
        elif typ == ast.BoolOp:
            clas = BoolOpe(i)
            classes.append(clas)
    return classes

def IfElse(upper: list[str], middle: list[str], lower: list[str], ram: dict, test, body, orelse) -> None:
    """ Evaluate an if-else statement 
    
        Match type of the test that is to be perform and use an according function to handle it.\n
        Additionally either go into its if - Body if if - Statement evaluated to True or to its else - Body otherwise.
    """
    #line_value = lower[0]
    check_sucess = True
    if type(test) == ast.Name: #existence check i.e: if x: ...
        if not ram[test.id]:
            check_sucess = False
        else:
            lower[0] = lower[0].replace(test.id, str(ram[test.id]), 1)
            print_Steppy(upper, middle, lower)
    """ Construct both left and right values recursiverly if needed to compare them"""
    if type(test) == ast.Compare:
        check_sucess = handleCompare(upper, middle, lower, ram, Compare(test))
        """if type(test.left) == ast.BoolOp:
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
         Iterate over all variables in our testing operations
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
                        break"""
    if type(test) == ast.UnaryOp:
        check_sucess = handleUnaryOp(upper, middle, lower, ram, UnaryOp(test))
    orelse_str = ast.unparse(orelse)
    if type(orelse) == ast.If:
        orelse_str = "el" + orelse_str
    else:
        orelse_str = "else"
    lower[0] = lower[0].replace(lower[0][3:lower[0].find(":")], str(check_sucess), 1)
    #write whether the check suceeded or not
    print_Steppy(upper, middle, lower)
    if not check_sucess:
        lower[0] = lower[0][lower[0].index(orelse_str):]
    else:
        lower[0] = lower[0][:lower[0].index(orelse_str)]
    IfBody(upper, middle, lower, body if check_sucess else orelse, ram) #handle if - body

def IfBody(upper: list[str], middle: list[str], lower: list[str], body: list[str], ram: dict) -> None:
    """ Handle an if - statement 
        
        Get first member of lower as if - statement, work through its body and change the to-be-printed line accordingly
    """

    lower[0] = ast.unparse(body[0]) + "\n"
    for x in range(len(body) - 1, 0, -1): # populate list with body of our if clause
        lower.insert(1, ast.unparse(body[x]) + "\n")
    
    for i in body:
        print_Steppy(upper, middle, lower)
        last_line = ast.parse(upper[-1])
        #print(ast.dump(last_line, indent=4))
        #print(ast.dump(i, indent=4))
        #try:
        #    print(last_line.body[0].targets[0].id == i.targets[0].id)
        #except:
        #    pass
        if type(i) == ast.Assign:
            if type(i.value) == ast.Constant:
                for x in i.targets:
                    ram[x.id] = i.value.value
            elif type(i.value) == tuple:
                for x in range(len(i.targets)):
                    ram[i.targets[x].id] = i.value[min(x, len(i.value))].value
            if type(last_line.body[0]) == ast.Assign and last_line.body[0].targets[0].id == i.targets[0].id: #same operation on the same value
                upper.pop()
            upper.append(lower[0])
            lower.pop(0)
            
        if type(i) == ast.BoolOp:
            BoolOp(upper, middle, lower, ram, i)
           
        elif type(i) == ast.BinOp:
            BinOp(upper, middle, lower, ram, i.left, i.op, i.right)
            lower[0] = lower[0].replace("(", " ")
            lower[0] = lower[0].replace(")", " ")
            line2 = ast.parse(lower[0])
            ram[line2.body[0].targets[0].id] = line2.body[0].value.value
            upper.append(lower[0])
            lower.pop(0)
            
        elif type(i) == ast.If:
            IfElse(upper, middle, lower, ram, i.test, i.body, i.orelse)
        elif type(i) == ast.Expr:
            middle.append(lower[0] + "\n")
            lower.pop(0)

def handleCompare(upper, middle, lower, ram, compare) -> bool:
    "Handle ast.Compare by iterating over the ops attribute of the body and putting the end-result together"
    left = compare.getLeft()
    ops = compare.getOps()
    right = compare.getComparators()
    compare_sucess = True
    match type(left):
        case ast.BinOp:
            left = BinOp(upper, middle, lower, ram, left.left, left.op, left.right)
        case ast.UnaryOp:
            left = handleUnaryOp(upper, middle, lower, ram, UnaryOp(left))
        case ast.Constant:
            left = left.value
        case ast.BoolOp:
            left = BoolOp(upper, middle, lower, ram, left)
    left_value = left
    for i in range(len(ops)):
        operation = ops[i]
        right_value = right[i]
        compare_sucess &= compare_values(left_value, right_value, operation, upper, middle, lower, ram)
        left_value = right_value
    x = ast.unparse(compare)
    left_index = lower[0].index(x)
    right_index = left_index + len(x)
    if lower[0][left_index - 1] == "(" and lower[0][right_index + 1] == ")":
        left_index -= 1
        right_index += 1
    lower[0] = lower[0].replace(lower[0][left_index:right_index], str(compare_sucess))
    print_Steppy(upper, middle, lower)
    return compare_sucess

def compare_values(left, right, operation, upper, middle, lower, ram):
    """
    Helper function to compare 2 values in ast.Compare.
    """
    match type(right):
        case ast.BinOp:
            right = BinOp(upper, middle, lower, ram, right.left, right.op, right.right)
        case ast.Constant:
            right = right.value
        case ast.Name:
            right = ram[right.id]
    match type(operation):
        case ast.LtE:
            return left <= right
        case ast.Lt:
            return left < right
        case ast.Gt:
            return left > right
        case ast.GtE:
            return left >= right
        case ast.Eq:
            return left == right

def BoolOp(upper: list[str], middle: list[str], lower: list[str], ram: dict, value) -> bool:
    """ Evaluate a Bool Operation 
    
        Match values that are used in the bool - statement and apply according operation on value[i] and value[i + 1]. \n
        Concatenate all evaluations together into one singular value and return it.
    """        
    op = value.getOpe()
    values = value.getValues()
    return_value = True #return value of the whole function
    right = None
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
            case ast.UnaryOp:
                left = handleUnaryOp(upper, middle, lower, ram, UnaryOp(values[i]))
            case ast.Compare:
                left = handleCompare(upper, middle, lower, ram, Compare(values[i]))
        match type(values[i + 1]):
            case ast.BoolOp:
                right = BoolOp(upper, middle, lower, ram, values[i + 1])
            case ast.Name:
                right = ram[values[i + 1].id]
                lower[0] = lower[0].replace(values[i].id, str(right), 1)
                print_Steppy(upper, middle, lower)
            case ast.Constant:
                right = values[i + 1].value
            case ast.UnaryOp:
                right = handleUnaryOp(upper, middle, lower, ram, UnaryOp(values[i + 1]))
            case ast.Compare:
                right = handleCompare(upper, middle, lower, ram, Compare(values[i + 1]))
        x = ast.BoolOp(op, values=[ast.Constant(left), ast.Constant(right)])
        left_index = lower[0].index(ast.unparse(x))
        right_index = left_index + len(ast.unparse(x))
        
        if lower[0][left_index - 1] == "(" and lower[0][right_index + 1] == ")":
            left_index -= 1
            right_index += 1
        print("BoolOp", lower[0][left_index - 1:right_index + 1])
        match type(op):
            case ast.And:
                return_value = return_value and (left and right)
            case ast.Or:
                return_value = return_value and (left or right)
        lower[0] = lower[0].replace(lower[0][left_index:right_index], str(return_value))
        print_Steppy(upper, middle, lower)      
    return return_value

def BinOp(upper: list[str], middle: list[str], lower: list[str], ram: dict, left, op, right):
    """ Evaluate Binary Operations recursively 

        Evaluate a binary operation recursively and return its final value. \n
        Change the to-be printed lines accordingly aswell.
    
    """
    if type(left) == ast.BinOp:
        left = BinOp(upper, middle, lower, ram, left.left, left.op, left.right)
    elif type(left) == ast.Name:
        if left.id in ram:
            index = lower[0].find("=")
            if index >= 0:
                lower[0] = lower[0][:index] + lower[0][index:].replace(left.id, str(ram.get(left.id)), 1)
            else:
                lower[0] = lower[0].replace(left.id, str(ram.get(left.id)), 1)
            left = ram.get(left.id)    
            print_Steppy(upper, middle, lower)
        else:
            raise NameError
    elif type(left) == ast.Constant:
        left = left.value
    elif type(left) == ast.UnaryOp:
        left = handleUnaryOp(upper, middle, lower, ram, UnaryOp(left))

    if type(right) == ast.BinOp:
        right = BinOp(upper, middle, lower, ram, right.left, right.op, right.right)
    elif type(right) == ast.UnaryOp:
        right = handleUnaryOp(upper, middle, lower, ram, UnaryOp(right))
    elif type(right) == ast.Name:
        if right.id in ram:
            lower[0] = lower[0].replace(right.id, str(ram.get(right.id)), 1)
            right = ram[right.id]
            print_Steppy(upper, middle, lower)
        else:
            raise NameError
    elif type(right) == ast.Constant:
        right = right.value
    """ Perform the mathematical operation that is stored in node.op and return the result of left and right """
    if type(right) in [int, float, str] and type(left) in [int, float, str]:
        x = ast.BinOp(ast.Constant(left), op, ast.Constant(right))
        left_index = lower[0].index(ast.unparse(x))
        right_index = left_index + len(ast.unparse(x))
        if lower[0][left_index - 1] == "(" and lower[0][right_index] == ")":   #surrounded by brackets so remove them
            left_index -= 1
            right_index += 1
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

def print_Steppy(upper, middle, lower) -> None:
    """ Print current Steppy Status 
    
        Iterate through upper, middle, lower and print out its contents, each list separated by "##########"
    """
    text = ""
    for i in upper:
        if i[-1] != "\n":
            i += "\n" 
        text += i
    text += "#" * 10 + "\n"
    for i in middle: 
        if i[-1] != "\n":
            i += "\n" 
        text += i
    text += "#" * 10 + "\n"
    for i in lower: 
        if i[-1] != "\n":
            i += "\n" 
        text += i
    print(text + "\n")
    if to_text:
        file = open(str(os.getcwd()) + "\\" + fileName, "a")
        file.write("\n" + text + "\n")
        file.close()


def handleClasses(upper, middle, lower, ram, classes):
    op = classes.getOp()
    match op:
        case "Assign":
            handleAssign(upper, middle, lower, ram, classes)
        case "AugAssign":
            handleAugAssign(upper, middle, lower, ram, classes)
        case "BinOp":
            handleBinOp(upper, middle, lower, ram, classes)
        case "If":
            handleIf(upper, middle, lower, ram, classes)
        case "Expression":
            handleExpression(upper, middle, lower, ram, classes)
        case "UnaryOp":
            handleUnaryOp(upper, middle, lower, ram, classes)
        case "Compare":
            handleCompare(upper, middle, lower, ram, classes)
        case "BoolOp":
            BoolOp(upper, middle, lower, ram, classes)
        case _:
            raise NotImplementedError(f'Not Supported Class {op}')
        
def handleBinOp(upper, middle, lower, ram, classes):
    value = classes.getValue()
    BinOp(upper, middle, lower, ram, value.left, value.op, value.right)
    lower[0] = lower[0].replace("(", "")
    lower[0] = lower[0].replace(")", "")
    line2 = ast.parse(lower[0])
    ram[line2.body[0].targets[0].id] = line2.body[0].value.value
    upper.append(lower[0])
    lower.pop(0)

def handleExpression(upper, middle, lower, ram, classes):
    value = classes.getValue()
    if value.func.id == "print":
        x = ast.Module()
        x.body = value.args
        for arg in constructClass(x):
            handleClasses(upper, middle, lower, ram, arg)
        middle.append("'" + lower[0][6:lower[0].index(")")] + "'" +  "\n")
        lower.pop(0)
        print_Steppy(upper, middle, lower)

def handleAssign(upper, middle, lower, ram, classes):
    targets = classes.getTargets()
    value = classes.getValue()
    if type(targets[0]) is ast.Tuple: #multiple variables in one line, iter over all of them and add to ram
        for i in range(len(targets[0].elts)):
            ram[targets[0].elts[i].id] = value.elts[i].value
    elif type(value) == ast.List:
        new_list = []
        for x in value.elts:
            new_list.append(x.value)
        ram[targets[0].id] = new_list
    elif type(value) == ast.Compare:
        ram[targets[0].id] = handleCompare(upper, middle, lower, ram, Compare(value))
    elif type(value) == ast.UnaryOp:
        ram[targets[0].id] = handleUnaryOp(upper, middle, lower, ram, UnaryOp(value))
    elif type(value) == ast.Name:
        ram[targets[0].id] = ram[value.id]
    elif type(value) == ast.BoolOp:
        ram[targets[0].id] = BoolOp(upper, middle, lower, ram, BoolOpe(value))
    elif type(value) == ast.BinOp:
        ram[targets[0].id] == BinOp(upper, middle, lower, ram, value.left, value.op, value.right)
    elif type(value) == ast.Constant:
        ram[targets[0].id] = value.value
    upper.append(lower[0])
    lower.pop(0)
    print_Steppy(upper, middle, lower)

def handleAugAssign(upper, middle, lower, ram, classes):
    """ Convert an AugAssign into a regular Assign with var to be assigned to, as its left value i.e:\n
     x += 2 -> x = x + 2; x *= y + 2 -> x = x * (y + 2) """
    targets = classes.getTargets()
    new_line = ast.Assign([targets], ast.BinOp(targets, classes.getOpe(), classes.getValue()))
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

def handleIf(upper, middle, lower, ram, classes):
    test = classes.getTest()
    body = classes.getBody()
    orelse = classes.getOrElse()
    IfElse(upper, middle, lower, ram, test, body, orelse) 

def handleUnaryOp(upper: list[str], middle: list[str], lower: list[str], ram: dict, classes: UnaryOp):
    operand = classes.getOperand()
    op = classes.getOpe()
    string_repr = ""
    match type(operand):
        case ast.BinOp:
            operand = BinOp(upper, middle, lower, ram, operand.left, operand.op, operand.right)
        case ast.BoolOp:
            operand = BoolOp(upper, middle, lower, ram, BoolOpe(operand))
        case ast.Constant:
            operand = operand.value
        case ast.Name:
            operand = ram[operand.id]
        case ast.Compare:
            operand = handleCompare(upper, middle, lower, ram, Compare(operand))
        case ast.UnaryOp:
            operand = handleUnaryOp(upper, middle, lower, ram, UnaryOp(operand))
    string_repr += str(operand)
    match type(op):
        case ast.Not:
            operand = not operand
            string_repr = "not " + string_repr
        case ast.Invert:
            operand = ~ operand
            string_repr = "~ " + string_repr
        case ast.USub:
            operand *= -1
            string_repr = "-" + string_repr
    left_index = lower[0].rfind(string_repr)
    right_index = left_index + len(string_repr)
    if lower[0][left_index - 1] == "(" and lower[0][right_index + 1] == ")":
            left_index -= 1
            right_index += 1
    lower[0] = lower[0].replace(lower[0][left_index:right_index], str(operand))
    print_Steppy(upper, middle, lower)
    return operand

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("USAGE: py steppy_main.py [file name] [options] [args]")
        exit(1)
    else:
        if sys.argv[-1] == "-h" or sys.argv[-1] == "--help":
            print("This is the help message for Steppy - a step-through process for python programms.\n" + 
                        "Currently Steppy supports only python files.\n" + 
                        "Steppy supports 4 different options:" + 
                        "\n" + 
                        "\n" + 
                        "-v or --verbose: shows ast.dump of the whole file, useful when you want to see how the file structure looks.\n" +
                        "-h or --help: displays this message, you know how to use it.\n" + 
                        "-o or --output: writes the output in the terminal to a text file named <your file name>_stepped_through.txt. " +  
                        "Look in there for a more slowed down step through.\n" + 
                        "-s or --show: shows at the end the state of the values that python associates with each variable.\n" +
                        "\nThe syntax for steppy usage is: py steppy_main.py [options from above] [name of your file]\n" + 
                        "For example: py steppy_main.py my_file.py --output my_file_output -v\n" +
                        "This will make a text file with steppy process in it, aswell as show the ast Tree of said file.")
            exit(1)
        try:
            
            reader = Path(str(sys.argv[1])).open()
            #reader = open(str(os.getcwd() + "\\" + sys.argv[-1]))
            lines_solo = reader.readlines()
            reader = Path(str(sys.argv[1])).open()
            #reader = open(str(os.getcwd() + "\\" + sys.argv[-1]))
            text = reader.read()
            lines = ""
            for x in lines_solo:
                lines += x
        except FileNotFoundError: #no such file or wrong name
            print("ERROR: No such file " + sys.argv[1] + " found!")
            exit(0)
        else:
            # construct three list[<str>] each holding the current representation
            # of Steppy, what lines have been evaluated (upper), which lines will print (middle)
            # and which lines are to be evaluated (lower). Then change them over time.
            upper = []
            middle = []
            lower = []
            parsed = ast.parse(text)
            for i in parsed.body:
                lower.append(ast.unparse(i) + "\n")
            ram = dict() #construct a "RAM" to hold any vars we encounter
            if "-v" in sys.argv or "--verbose" in sys.argv:
                print("#" * 20 + "\n")
                print(ast.dump(parsed, indent=4) + "\n")
                print("#" * 20 + "\n")
            if "-o" in sys.argv or "--output" in sys.argv:
                try:
                    fileName = sys.argv[sys.argv.index("-o") + 1]
                except ValueError:
                    fileName = sys.argv[sys.argv.index("--output") + 1]
                if fileName[-4:] != ".txt": fileName += ".txt" #hardcoded to be a text file but could be altered later on
                file = open(str(os.getcwd() + "\\" + fileName), "w")
                file.write("Here is the step process of the file " + str(sys.argv[1]) + "\n")
                file.close()
                to_text = True
            if "-h" in sys.argv or "--help" in sys.argv:
                print("This is the help message for Steppy - a step-through process for python programms.\n" + 
                        "Currently Steppy supports only python files.\n" + 
                        "Steppy supports 4 different options:" + 
                        "\n" + 
                        "\n" + 
                        "-v or --verbose: shows ast.dump of the whole file, useful when you want to see how the file structure looks.\n" +
                        "-h or --help: displays this message, you know how to use it.\n" + 
                        "-o or --output: writes the output in the terminal to a text file named <your file name>_stepped_through.txt. " +  
                        "Look in there for a more slowed down step through.\n" + 
                        "-s or --show: shows at the end state of the values that python associates with each variable.\n" +
                        "\nThe syntax for steppy usage is: py steppy_main.py [name of your file] [options from above]\n" + 
                        "for example: py steppy_main.py my_file.py --output my_file_output -v\n" +
                        "This will make a text file with steppy process in it, aswell as show the ast Tree of said file.")
                exit(1)
            print_Steppy(upper, middle, lower)
            for classes in constructClass(parsed):
                handleClasses(upper, middle, lower, ram, classes)
                print_Steppy(upper, middle, lower)
            if "-s" in sys.argv or "--show" in sys.argv:
                print("+" + "-" * (len(str(ram)) + 3) + "+")
                print("| " + str(ram) + "  |")
                print("+" + "⁻" * (len(str(ram)) + 3) + "+")
            exit(1)