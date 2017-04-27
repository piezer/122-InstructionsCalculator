from linkedlist import LinkedList
from vartree import VarTree

def eval_postfix(tree,expr):
    stack = LinkedList()
    for x in expr:
        if x.isalnum():
            stack.push(str(x))
        elif x == '=':
            val = stack.pop()
            var = stack.pop()
            tree.assign(var,val)
            stack.push(val)
        else:
            right = stack.pop()
            left = stack.pop()
            if right.isalpha():
                right = tree.lookup(right)
            if left.isalpha():
                left = tree.lookup(left)
            answer = eval(left + x + right)
            stack.push(str(answer))
    answer=stack.pop()
    if answer.isalpha():
        answer = tree.lookup(answer)
    return answer