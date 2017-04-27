from infixtotree import to_expr_tree
#from evalpostfix import evalpostfix

class LinkedList:
    class Node:
        __slots__ = "_value","_next"

        def __init__(self, val, forward):
            self._value = val
            self._next = forward
            
    def __init__(self):
        self._head = None
        self._size = 0
    def __len__(self):
        return self._size
    def is_empty(self):
        return self._size==0

    def push(self, val):
        self._head = self.Node(val, self._head)
        self._size+=1
    def pop(self):
        current = self._head
        if self.is_empty():
            raise Exception('Stack is Empty')
        self._head = self._head._next
        self._size-=1
        return current._value
    def top(self):
        current=self._head
        if self.is_empty():
            raise Exception('Stack is Empty')
        return current._value
    def __iter__(self):
        current = self._head
        while current is not None:
            yield str(current._value)
            current = current._next
    def __str__(self):
        toReturn =''
        current=self._head
        for i in range(self._size):
            toReturn+=(str(current._value)+' ')
            current = current._next
        return toReturn
            

if __name__ == "__main__":
    cheese = LinkedList()
    print(cheese.is_empty())
    #print(cheese.pop())
    cheese.push(1)
    cheese.push(2)
    cheese.push(3)
    print(cheese.is_empty())
    print(cheese.top())
    print(cheese)
    for i in range(3):
        print(cheese.pop())
        print(cheese)
    print(cheese.is_empty())
    #print(cheese.top())