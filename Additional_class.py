import decimal
from typing import overload

class Stack :
    '''Python implementation the stack'''
    
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return self.items == []
        
    def push(self,item):
        self.items.append(item)		
        
    def pop(self):
        return self.items.pop()
        
    def peek(self):
        return self.items[len(self.items)-1]
    
    def size(self):
        return len(self.items)

class Formula():
    def __init__(self,Expr:str) -> None:
        '''please input Infix Formula'''
        self.InputInfixFormula(Expr)
        if (self.__Postfixformula=="a x * b +"\
            or self.__Postfixformula=="x a * b +"):
            self.__invertformula="y b - a /"

        elif (self.__Postfixformula=="a x * b -"\
            or self.__Postfixformula=="x a * b -"):
            self.__invertformula="y b + a /"
    
    def __PrivateInfixToPostfix(self,expr:str):
        '''https://www.geeksforgeeks.org/convert-infix-expression-to-postfix-expression/'''
        result = []
        stack = []
        s=expr.split()
        for i in range(len(s)):
            c = s[i]
    
            # If the scanned character is an operand, add it to the output string.
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
                result.append(c)
            # If the scanned character is an ‘(‘, push it to the stack.
            elif c == '(':
                stack.append(c)
            # If the scanned character is an ‘)’, pop and add to the output string from the stack
            # until an ‘(‘ is encountered.
            elif c == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()  # Pop '('
            # If an operator is scanned
            else:
                while stack and (self.__prec(s[i]) < self.__prec(stack[-1]) or
                                (self.__prec(s[i]) == self.__prec(stack[-1]) and self.__associativity(s[i]) == 'L')):
                    result.append(stack.pop())
                stack.append(c)
    
        # Pop all the remaining elements from the stack
        while stack:
            result.append(stack.pop())
    
        return(' '.join(result))
    
    def __PrivateEval_Postfix(self,postfixExpr:str) -> float:
        operand_stack = Stack()
        tokenList = postfixExpr.split()
        for token in tokenList:
            # If the token is an operand, convert it from a string to an integer and push the value onto stack
            if token not in "abcdefghijklmnopqrstuvwxyz()+*-/":
                operand_stack.push(float(token))
            # If the token is an operator, *, /, +, or -, Pop the operandStack twice.     
            else:
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                # Perform the arithmetic operation.
                result = self.__evaluate(token,operand1,operand2)
                # Push the result back on the stack. 
                operand_stack.push(result)
        return round(operand_stack.pop(),7)

    def __PrivatePostfixToInfix(self,postfixExpr:str) -> str:
        '''postfix to infix conversion  
        https://www.geeksforgeeks.org/postfix-to-infix/'''
        s = [] 
        exp = postfixExpr.split()
        for i in exp:     
            
            # Push operands 
            if (self.__isOperand(i)) :         
                s.insert(0, i) 
                
            # We assume that input is a 
            # valid postfix and expect 
            # an operator. 
            else:
            
                op1 = s[0] 
                s.pop(0) 
                op2 = s[0] 
                s.pop(0) 
                s.insert(0, " ( " + op2+ ' ' + i + ' ' +
                                op1 + " ) ") 
                
        # There must be a single element in 
        # stack now which is the required 
        # infix. 
        return s[0]

    def __evaluate(self,op, op1:float, op2:float):
        if op == "*":
            return op1 * op2
        elif op == "/":
            return op1 / op2
        elif op == "+":
            return op1 + op2
        else:
            return op1 - op2

    def __isOperand(self,x:str):
        return ((x >= 'a' and x <= 'z') or
                (x >= 'A' and x <= 'Z')) 

    def __prec(self,c:str):
        if c == '^':
            return 3
        elif c == '/' or c == '*':
            return 2
        elif c == '+' or c == '-':
            return 1
        else:
            return -1
 
    def __associativity(self,c):
        if c == '^':
            return 'R'
        return 'L'  # Default to left-associative
    
    def __expr_preprocess(self,expr:str=None):
        if not expr:
            expr=self.__Postfixformula
        for i,j in self.__replacestack.items():
            expr=expr.replace(i,j)
        return expr

    def InputInfixFormula(self,Expr:str):
        # expr=Expr.lower()
        expr=Expr.replace('y','').replace('Y','').replace('=','').replace('X','x')
        expr=expr.split()
        Elements=[]
        for i in expr:
            Elements.append(i)
        englist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        index=0
        self.__replacestack={}
        for i,element in enumerate(Elements):
            if element not in "abcdefghijklmnopqrstuvwxyz()+*-/":
                self.__replacestack[englist[index]]=element
                Elements[i]=englist[index]
                index+=1
        Exprafterprocess=' '.join(Elements)
        self.__Postfixformula=self.__PrivateInfixToPostfix(Exprafterprocess)
        pass

    def evaluate(self,X:float):
        expr=self.__Postfixformula.replace('x',str(X))
        expr=self.__expr_preprocess(expr)
        return self.__PrivateEval_Postfix(expr)
    
    def OutputInfixformula(self):
        result = self.__PrivatePostfixToInfix(self.__Postfixformula)
        return self.__expr_preprocess(result)
    
    def verylimit_formulainvert_evaluate(self,Y:float):
        invertformula=self.__expr_preprocess(self.__invertformula).replace('y',str(Y))
        return self.__PrivateEval_Postfix(invertformula)
        
class formula_data():
    @overload
    def __init__(self,dataname:str,formula:list[float],default:float|None=None) -> None : ...
    @overload
    def __init__(self,dataname:str,formula:Formula,default:float|None=None,useable:bool=True) -> None : ...

    def __init__(self,dataname:str,formula:Formula,default:float|None=None,useable:bool=True) -> None:
        self.dataname=dataname
        if isinstance(formula,Formula):
            self.formula=formula
        elif isinstance(formula,list):
            self.formula=self.__formulacaculate(formula)
        else:
            raise TypeError("'formula' must be Formula or List type.")
        self.default=default
        self.useable=useable

    def __formulacaculate(self,parameters:list[float]) -> Formula:
        _decimal=max([len(float_to_str(i)) for i in parameters])
        try:
            a=(parameters[2]-parameters[3])/(parameters[0]-parameters[1])
        except ZeroDivisionError:
            a=0
        a=float_to_str(a,_decimal)
        try:
            b=parameters[2]-((parameters[2]-parameters[3])/(parameters[0]-parameters[1]))*parameters[0]
        except ZeroDivisionError:
            b=0
        b=float_to_str(b,_decimal)
        return Formula(f"y = {a} * x + {b}")

    def CreateFormula(self,parameters:list[float]) -> None:
        self.formula = self.__formulacaculate(parameters)

    def __getitem__(self, __key:str):
        if __key.lower()=='dataname':
            return self.dataname
        elif __key.lower()=='formula':
            return self.formula
        elif __key.lower()=='default':
            return self.default
        elif __key.lower()=='useable':
            return self.useable
        raise KeyError(__key)
    

class formula_file_processer():
    def __init__(self,filename:str) -> None:
        self.data={str():formula_data(None,Formula(""))}
        self.data.clear()
        self.__filename=filename

    def read(self):
        with open(self.__filename,'r',encoding='utf-8') as f:
            temp=f.readline()
            while temp:
                elements=temp.split(',')
                dataname=elements[0].removesuffix(" ")
                formula=Formula(elements[1])
                default=self.__readdefault(elements[2])
                useable=self.__readbool(elements[3])
                self.data[dataname]=formula_data(dataname,formula,default,useable)
                temp=f.readline()
    
    def checkDataname(self,dataname:str):
        if dataname.lower() in [i.lower() for i in self.data.keys()]:
            raise KeyError(f'Data {dataname} already in database.')
    
    def newData(self,dataname:str,formula:Formula,default:float|None,useable:bool=True):
        self.checkDataname(dataname)
        self.data[dataname]=formula_data(dataname,formula,default,useable)
    
    def __readbool(self,_str:str):
        if 'true' in _str.lower():
            return True
        return False
    
    def __readdefault(self,_any):
        try:
            return float(_any)
        except ValueError:
            return None

    def file_write(self):
        with open(self.__filename,'w',encoding='utf-8') as f:
            for i in self.data.values():
                f.write(f"{i.dataname} , y ={i.formula.OutputInfixformula()} , {str(i.default)} , {str(i.useable)}\n")



class float_to_str_class():
    def __init__(self) -> None:
        # create a new context for this task
        self.ctx = decimal.Context()

        # 20 digits should be enough for everyone :D
        self.ctx.prec = 8

    def float_to_str(self,f):
        """
        Convert the given float to a string,
        without resorting to scientific notation
        """
        d1 = self.ctx.create_decimal(repr(f))
        return format(d1, 'f')

_instance=float_to_str_class()
def float_to_str(f:float,decimal:int=8):
    _instance.ctx.prec = decimal
    return _instance.float_to_str(float(f))

if __name__=="__main__":
    testf=Formula("y = (  ( 2136.6000 * x )  + 109.67600 )")
    testf.verylimit_formulainvert_evaluate(2285)
    pass
    