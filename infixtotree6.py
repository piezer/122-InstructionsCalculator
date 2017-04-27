from peekable import Peekable, peek
from newsplit import new_split_iter
from exprtree import Value, Var, Oper,Cond, Func

def tree_assign(iterator):
    left = tree_conditional(iterator)
    if peek(iterator) == "=":
        oper = next(iterator)
        right = tree_assign(iterator)
        left = Oper(left,oper,right)
    return left

def tree_conditional(iterator):
    cond = tree_relational(iterator)
    if peek(iterator) == "?":
        next(iterator)
        true = tree_assign(iterator)
        next(iterator)
        false = tree_assign(iterator)
        cond= Cond(cond,true,false)
    return cond
def tree_relational(iterator):
    left = tree_sum(iterator)
    while(peek(iterator) == ">" or peek(iterator) == "<" or peek(iterator) == ">=" or peek(iterator)=="<=" or peek(iterator) =="=="or peek(iterator) == "!="):
        oper = next(iterator)
        right = tree_sum(iterator)
        left= Oper(left,oper,right)
    return left
def tree_sum(iterator):
    left = tree_product(iterator)
    while(peek(iterator) == "+" or peek(iterator) == "-"):
        oper = next(iterator)
        right = tree_product(iterator)
        left = Oper(left, oper, right)
    return left
def tree_product(iterator):
    left = tree_factor(iterator)
    while(peek(iterator)=="*" or peek(iterator) == "/" or peek(iterator) == "%"):
        oper = next(iterator)
        right = tree_factor(iterator)
        left = Oper(left,oper,right)
    return left
def tree_factor(iterator):
    if peek(iterator).isalpha():
        name = next(iterator)
        if peek(iterator) == "(":
            next(iterator)
            args = []
            arg = tree_assign(iterator)
            args.append(arg)
            while peek(iterator) == ",":
                arg = tree_assign(iterator)
                args.append(arg)
            next(iterator)
            return Func(name,args)
        return Var(name)
    elif peek(iterator).isdigit():
        return Value(next(iterator))
    elif peek(iterator) == '(':
        next(iterator)
        ans = tree_assign(iterator)
        next(iterator)
        return ans
def to_expr_tree( expr ):
    return tree_assign(Peekable((new_split_iter(expr))))
def define_func(iterator):
    next(iterator)
    name = next(iterator)
    next(iterator)
    parameters = [next(iterator)]
    while peek(iterator) is not ")":
        next(iterator)
        parameters.append(next(iterator))
    next(iterator)
    next(iterator)
    body = tree_assign(iterator)
    return name, parameters, body

if __name__ == "__main__":
    print (to_expr_tree("A = 5"))
    print (to_expr_tree("A = 2 + 3 * B - xyz"))
    print (to_expr_tree("x < 0 ? 0 - x : x"))
