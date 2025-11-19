from typing import Generator, Self


# abstract classes
class Node(object):
    pass

class Statement(Node):
    pass

class Expr(Node):
    pass

class Value[T](Expr):
    def __init__(self, value: T) -> None:
        self.value = value

class BinExpr(Expr):
    def __init__(self, op: str, left: Expr, right: Expr) -> None:
        assert op in self.valid_operators
        self.op: str = op
        self.left: Expr = left
        self.right: Expr = right

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

class Block(LinkedList, Statement):
    def __init__(self, statement: Statement, rest: Self | None = None) -> None:
        self.arg = statement
        self.next_node = rest

class IntNum(Value[int]):
    pass

class FloatNum(Value[float]):
    pass

class String(Value[str]):
    pass

class Variable(Value[str]):
    pass

class Range(Node):
    def __init__(self, low: Expr, high: Expr) -> None:
        self.low = low
        self.high = high

class Index(Node):
    def __init__(self, x: Expr, y: Expr | None = None) -> None:
        self.x = x
        self.y = y

class Ref(Expr):
    def __init__(self, name: Variable, indexer: Index) -> None:
        self.name = name
        self.indexer = indexer

class RelExpr(BinExpr):
    valid_operators = ['<', '>', '<=', '>=', '!=', '==']

class NumExpr(BinExpr):
    valid_operators = ['+', '-', '*', '/', '.+', '.-', '.*', './']

class UnExpr(Expr):
    def __init__(self, op: str, value: Expr) -> None:
        assert op in ['\'', '-']
        self.op = op
        self.value = value

class Assignment(Statement):
    def __init__(self, op: str, assignee: Variable | Ref, value: Expr) -> None:
        assert op in ['=', '+=', '-=', '*=', '/=']
        self.op = op
        self.left = assignee
        self.right = value

class Conditional(Statement):
    def __init__(
        self, cond: Expr, true_stmt: Statement, false_stmt: Statement | None = None
    ) -> None:
        self.cond = cond
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

class WhileLoop(Statement):
    def __init__(self, cond: Expr, stmt: Statement) -> None:
        self.cond = cond
        self.stmt = stmt

class ForLoop(Statement):
    def __init__(self, name: Variable, range_expr: Range, stmt: Statement) -> None:
        self.name = name
        self.range_expr = range_expr
        self.stmt = stmt

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
    def __init__(self, row: Varlist, rest: Self | None = None) -> None:
        self.arg = row
        self.next_node = rest

class FunctionCall(Expr):
    def __init__(self, name: str, arg: Expr) -> None:
        self.name = name
        self.arg = arg


class Error(Node):
    def __init__(self) -> None:
        pass
