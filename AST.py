from typing import Generator


# abstract classes
class Node(object):
    pass

class Statement(Node):
    pass

class Value(Node):
    pass  # required attributes: value

class BinExpr(Node):
    def __init__(self, op, left, right) -> None:
        if type(op) != str: op = op.val
        self.op = op
        self.left = left
        self.right = right

class LinkedList[T](Node):
    # required attributes: arg, next_node
    def iter(self) -> Generator[T]:
        cursor = self
        while cursor is not None:
            yield cursor.arg
            cursor = cursor.next_node

    def unwind(self) -> list[T]:
        return list(self.iter())

# actual classes
class Varlist[T](LinkedList):
    def __init__(self, value: T, next_node=None) -> None:
        self.arg = value
        self.next_node = next_node

class Block(LinkedList):
    def __init__(self, statement: Statement, rest=None) -> None:
        self.arg = statement
        self.next_node = rest

class IntNum(Value):
    def __init__(self, value) -> None:
        self.value = value

class FloatNum(Value):
    def __init__(self, value) -> None:
        self.value = value

class String(Value):
    def __init__(self, value) -> None:
        self.value = value

class Variable(Value):
    def __init__(self, name) -> None:
        self.value = name

class Range(Node):
    def __init__(self, low, high) -> None:
        self.low = low
        self.high = high

class Index(Node):
    def __init__(self, x, y=None) -> None:
        self.x = x
        self.y = y

class Ref(Node):
    def __init__(self, name, indexer: Index) -> None:
        self.name = name
        self.indexer = indexer

class RelExpr(BinExpr):
    pass

class NumExpr(BinExpr):
    pass

class UnExpr(Node):
    def __init__(self, op, value) -> None:
        self.op = op
        self.value = value

class Assignment(Statement, BinExpr):
    def __init__(self, op, assignee, value) -> None:
        self.op = op
        self.left = assignee
        self.right = value

class Conditional(Statement):
    def __init__(self, cond, true_block, false_block=None) -> None:
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

class WhileLoop(Statement):
    def __init__(self, cond, block) -> None:
        self.cond = cond
        self.block = block

class ForLoop(Statement):
    def __init__(self, name, range_expr: Range, block) -> None:
        self.name = name
        self.range_expr = range_expr
        self.block = block

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class ReturnStatement(Statement):
    pass

class PrintStatement(Statement):
    def __init__(self, varlist: Varlist) -> None:
        self.args = varlist

class Vector(LinkedList):
    def __init__(self, row: Varlist, rest=None) -> None:
        self.arg = row
        self.next_node = rest

class FunctionCall(Node):
    def __init__(self, name, arg) -> None:
        self.name = name
        self.arg = arg


class Error(Node):
    def __init__(self) -> None:
        pass
