from abc import ABCMeta,abstractmethod
from vartree import VarTree
from machine import Initialize,Load, Store,Perform

numRegister = 0
numVariables = -1

class ExprTree(metaclass=ABCMeta):
    """Abstract class for expression"""
    def __str__(self):
        return ' '.join( str(x) for x in iter(self) )

    #   All of the derived class mus implement these functions
    @abstractmethod
    def __iter__(self):
        """an inorder iterator for this tree node, for display"""
        pass
    @abstractmethod
    def postfix(self):
        """a post-order iterator to create a postfix expression"""
        pass
    @abstractmethod
    def evaluate(self, variables,functions):
        """evaluate using the existing variables"""
        pass

class Var(ExprTree):
    """A variable leaf"""
    def __init__(self, n):
        self._name = n
    def __iter__(self):
        yield self._name
    def postfix(self):
        yield self._name
    def evaluate(self, variables,functions):
        return variables.lookup(self._name)
    def comp(self, variables, functions):
        varNum = variables.lookup(self._name)
        global numRegister
        numRegister += 1
        program.code.append(Load(numRegister,varNum))

class Func(ExprTree):
    def __init__(self,n,args):
        self._name = n
        self._args = args
    def __iter__(self):
        yield self._name
        yield "("
        if len(self._args) > 0:
            yield self._args[0]
            for i in range(1,len(self._args)):
                yield ","
                yield self._args[i]
        yield ")"
    def postfix(self):
        pass
    def evaluate(self, variables,functions):
        temp = VarTree()
        [params,body] = functions.lookup(self._name)
        for i in range(len(params)):
            par = params[i]
            parVal = self._args[i].evaluate(variables,functions)
            temp.assign(par,parVal)
        return body.evaluate(temp,functions)

class Value(ExprTree):
    """A value leaf"""
    def __init__(self, v):
        self._value = v
    def __iter__(self):
        yield self._value
    def postfix(self):
        yield self._value
    def evaluate(self, variables,functions):
        return self._value
    def comp(self,variables,program):
        global numRegister
        numRegister +=1
        program.code.append(Initialize(numRegister,self._value))
class Oper(ExprTree):
    def __init__(self, left, op, right):
        self._oper = op
        self._left = left
        self._right = right
    def __iter__(self):
        yield "("
        yield from iter(self._left)
        yield self._oper
        yield from iter(self._right)
        yield ")"
    def postfix(self):
        yield from self._left.postfix()
        yield from self._right.postfix()
        yield self._oper
    def evaluate(self, variables,functions):
        if self._oper == '=':
            variables.assign(str(self._left), int(self._right.evaluate(variables)))
            return self._left.evaluate(variables,functions)
        else:
            left = self._left.evaluate(variables,functions)
            right = self._right.evaluate(variables,functions)
            return eval(str(left) + self._oper +str(right))
    def comp(self, variables, program):
        if self._oper =="=":
            self._right.comp(variables,program)
            global numVariables
            numVariables +=1
            variables.assign(str(self._left), numVariables)
            program.code.append(Store(numRegister, numVariables))
        else:
            self._left.comp(variables, program)
            lefttemp = numRegister
            self._right.comp(variables,program)
            righttemp = numRegister
            global numRegister
            numRegister+=1
            program.code.append(Perform(numRegister, lefttemp, self._oper, righttemp))
        
class Cond(ExprTree):
    def __init__(self, cond, true, false):
        self._true = true
        self._conditional = cond
        self._false = false
    def __iter__(self):
        yield "("
        yield from self._conditional
        yield "?"
        yield from self._true
        yield ":"
        yield from self._false
        yield ")"
    def postfix(self):
        pass
    def evaluate(self,variables,functions):
        if self._conditional.evaluate(variables,functions):
            return self._true.evaluate(variables,functions)
        else:
            return self._false.evaluate(variables,functions)
    
if __name__ == '__main__':
    V = VarTree()
    VA = Var("A")
    Sum = Oper(Value(2),'+',Value(3))
    A = Oper(VA,'=',Sum)
    print( "Infix iteration: ", list(A) )
    print( "String version ", A )
    print( "Postfix iteration: ", list(A.postfix() ))
    print( "Execution: ", A.evaluate(V) )
    print( "Afterwards, A = ", VA.evaluate(V) )

    # If A == 5, return A+2 else return 3
    CondTest = Cond(Oper(VA,'==',Value(5)),Oper(VA,'+',Value(2)),Value(3))
    print( CondTest,'-->',CondTest.evaluate(V) )

#Output:
#Infix iteration:  ['(', 'A', '=', '(', 2, '+', 3, ')', ')']
#String version  ( A = ( 2 + 3 ) )
#Postfix iteration:  ['A', 2, 3, '+', '=']
#Execution:  5
#Afterwards, A =  5
#( ( A == 5 ) ? ( A + 2 ) : 3 ) --> 7
