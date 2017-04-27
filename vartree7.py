class VarTree:
    class Node:
        __slots__ = "_value","_var",  "_left", "_right"
        def __init__(self, left,var, value,right):
            self._left = left
            self._var = var
            self._value = value
            self._right = right
    def __init__(self):
        self._root = None
    def _search(self, here, var):
        if here is None:
            return 0
        elif here._var == var:
            return here._value
        elif var < here._var:
            return self._search(here._left, var)
        elif var > here._var:
            return self._search(here._right, var)

    def _insert(self, here, var, value):
        if here is None:
            return self.Node(None, var, value, None)
        elif var == here._var:
            return self.Node(here._left, var, value, here._right)
        elif var < here._var:
            return self.Node(self._insert(here._left, var,  value),here._var, here._value, here._right)
        elif var > here._var:
            return self.Node(here._left, here._var, here._value, self._insert(here._right,var,value))
                
    def assign(self, var, value):
        self._root = self._insert(self._root, var, value)
        
    def lookup(self, var):
        return self._search(self._root, var)
    def _rec_tuples(self, here):
        if here is None:
            return ''
        else:
            return (self._rec_tuples(here._left), here._var, here._value, self._rec_tuples(here._right))
    def __str__(self):
        tuples = self._rec_tuples(self._root)
        return str(tuples).replace("'', ","").replace(", ''","")
    def is_empty(self):
        if self._root is None:
            return True
        else:
            return False
    def _rec_size(self,here):
        if here is None:
            return 0
        else:
            return 1 + self._rec_size(here._left) + self._rec_size(here._right)
    def __len__(self):
        return self._rec_size(self._root)


if __name__ == "__main__":
    V = VarTree()
    V.assign("one",5)
    print(V)
    V.assign("two",4)
    print(V)
    V.assign("three",6)
    print(V)
    V.assign("a",34)
    print(V)
    print(V.lookup("three"))
    print(len(V))