class Instruction:
    """Simple instructions representative of a RISC machine

    These instructions are mostly immutable -- once constructed,
    they will not be changed -- only displayed and executed
    """
    def __init__(self, t):      # default constructor
        self._temp = t          # every instruction has a register
    def get_temp(self):         #     which holds its answer
        return self._temp

class Print(Instruction):
    """A simple non-RISC output function to display a value"""
    def __str__(self):
        return "print T" + str(self._temp)
    def execute(self,temps,stack,pc,sp):
        print( temps[self._temp] )

class Initialize(Instruction):
    def __init__(self, t, value):
        super().__init__(t)
        self._temp = t
        self._value = value
    def __str__(self):
        return "T" + str(self._temp) + "=" + str(self._value)
    def execute(self, temps, stack, pc, sp):
        temps[self._temp] = self._value

class Load(Instruction):
    def __init__(self, t , off):
        super().__init__(t)
        self._temp = t
        self._offset = off
    def __str__(self):
        return "T"+ str(self._temp) + "= stack["+ str(self._offset) +  "]"
    def execute(self, temps, stack, pc, sp):
        temps[self._temp] = stack[sp + self._offset]

class Store(Instruction):
    def __init__(self,t , off):
        super().__init__(t)
        self._temp = t
        self._offset = off

    def __str__(self):
        return "stack["+ str(self._offset)+ "] = T"+ str(self._temp)

    def execute(self, temps, stack, pc, sp):
        stack[sp + self._offset] = temps[self._temp]

class Perform(Instruction):
    def __init__(self,t, operator, left, right):
        super().__init__(t)
        self._temp = t
        self._oper = left
        self._left = operator
        self._right = right

    def __str__(self):
        return "T" + str(self._temp) + "= (T" +  str(self._left) + str(self._oper)  + "T" + str(self._right) + ")"

    def execute(self, temps, stack, pc, sp):
        temps[int(self._temp)] = eval(str(temps[int(self._left)]) + self._oper + str(temps[int(self._right)]))
