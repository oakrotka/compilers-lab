from typing import Generator


# abstract classes
class Node(object):
    pass

class Statement(Node):
    def __init__(self, line):
        self.line = line

class Value(Node):
    pass  # required attributes: value

class BinExpr(Node):
    def __init__(self, line, op, left, right) -> None:
        self.line = line
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
    def __init__(self, line, value: T, next_node=None) -> None:
        self.line = line
        self.arg = value
        self.next_node = next_node
        self.len = next_node.len + 1 if next_node is not None else 1

class Block(LinkedList):
    def __init__(self, line, statement: Statement, rest=None) -> None:
        self.line = line
        self.arg = statement
        self.next_node = rest
        self.len = rest.len + 1 if rest is not None else 1

class IntNum(Value):
    def __init__(self, line, value) -> None:
        self.line = line
        self.value = value

class FloatNum(Value):
    def __init__(self, line, value) -> None:
        self.line = line
        self.value = value

class String(Value):
    def __init__(self, line, value) -> None:
        self.line = line
        self.value = value

class Variable(Value):
    def __init__(self, line, name) -> None:
        self.line = line
        self.value = name

class Range(Node):
    def __init__(self, line, low, high) -> None:
        self.line = line
        self.low = low
        self.high = high

class Index(Node):
    def __init__(self, line, x, y=None) -> None:
        self.line = line
        self.x = x
        self.y = y

class Ref(Node):
    def __init__(self, line, name, indexer: Index) -> None:
        self.line = line
        self.name = name
        self.indexer = indexer

class RelExpr(BinExpr):
    pass

class NumExpr(BinExpr):
    pass

class MatExpr(BinExpr):
    pass

class UnExpr(Node):
    def __init__(self, line, op, value) -> None:
        self.line = line
        self.op = op
        self.value = value

class Assignment(Statement, BinExpr):
    def __init__(self, line, op, assignee, value) -> None:
        self.line = line
        self.op = op
        self.left = assignee
        self.right = value

class Conditional(Statement):
    def __init__(self, line, cond, true_block, false_block=None) -> None:
        self.line = line
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

class WhileLoop(Statement):
    def __init__(self, line, cond, block) -> None:
        self.line = line
        self.cond = cond
        self.block = block

class ForLoop(Statement):
    def __init__(self, line, name, range_expr: Range, block) -> None:
        self.line = line
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
    def __init__(self, line, varlist: Varlist) -> None:
        self.line = line
        self.args = varlist

class Vector(LinkedList):
    def __init__(self, line, row: Varlist, rest=None) -> None:
        self.line = line
        self.arg = row
        self.next_node = rest
        self.len = rest.len + 1 if rest is not None else 1

class FunctionCall(Node):
    def __init__(self, line, name, arg) -> None:
        self.line = line
        self.name = name
        self.arg = arg


class Error(Node):
    def __init__(self) -> None:
        self.line = line
        pass
