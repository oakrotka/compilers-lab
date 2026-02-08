import AST
from exceptions import BreakException, ContinueException, ReturnValueException
from memory import MemoryStack, Memory
from visit import on, when

import operator as op
import sys

import numpy as np

sys.setrecursionlimit(10000)

simple_actions = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '==': op.eq,
    '!=': op.ne,
    '<=': op.le,
    '>=': op.ge,
    '<': op.lt,
    '>': op.gt,
}

def operator_action(operator, both_ints=False):
    division = op.floordiv if both_ints else op.truediv
    return simple_actions[operator] if operator != '/' else division

def are_both_ints(r1, r2):
    is_int = lambda x: type(x) == int or (
        hasattr(x, 'dtype') and np.issubdtype(x.dtype, np.integer)
    )
    return is_int(r1) and is_int(r2)

class Interpreter(object):
    memstack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        if type(node) == AST.Assignment: return

        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        subop = node.op[1] if node.op[0] == '.' else node.op
        action = operator_action(subop, are_both_ints(r1, r2))

        return action(r1, r2)

    @when(AST.Varlist)
    def visit(self, node):
        return [self.visit(x) for x in node.iter()]

    @when(AST.Block)
    def visit(self, node):
        if not node.is_child:
            self.memstack.push(Memory('block'))
        for statement in node.iter():
            self.visit(statement)
        if not node.is_child:
            self.memstack.pop()

    @when(AST.Value)
    def visit(self, node):
        if type(node) == AST.Variable: return
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memstack.get(node.value)

    @when(AST.Range)
    def visit(self, node):
        l = self.visit(node.low)
        r = self.visit(node.high)
        return range(l, r + 1)

    @when(AST.Index)
    def visit(self, node):
        l = self.visit(node.x)
        if node.y is None:
            return (l,)
        else:
            r = self.visit(node.y)
            return (l, r)

    @when(AST.Ref)
    def visit(self, node):
        idx = self.visit(node.indexer)
        mat = self.memstack.get(node.id())
        return mat[node.convert_idx(idx)]

    @when(AST.UnExpr)
    def visit(self, node):
        val = self.visit(node.value)
        if node.op == '\'':
            return val.T
        elif node.op == '-':
            return -val
        else:
            raise NotImplementedError

    @when(AST.Assignment)
    def visit(self, node):
        val = self.visit(node.right)
        if type(node.left) == str:  # set whole value, without indexing
            if node.op != '=':  # operator-assign
                prev = self.memstack.get(node.left)
                action = operator_action(node.op[0], are_both_ints(prev, val))
                val = action(prev, val)
            self.memstack.set(node.left, val)
        else:  # set index
            ref = node.left
            assert type(ref) == AST.Ref

            idx = self.visit(ref.indexer)
            mat = self.memstack.get(ref.id())

            if node.op != '=':
                action = operator_action(node.op[0], are_both_ints(mat[idx], val))
                val = action(mat[idx], val)

            mat[node.left.convert_idx(idx)] = val

    @when(AST.Conditional)
    def visit(self, node):
        # self.memstack.push(Memory('if')))
        if self.visit(node.cond):
            self.visit(node.true_block)
        elif node.false_block is not None:
            self.visit(node.false_block)
        # self.memstack.pop()

    @when(AST.WhileLoop)
    def visit(self, node):
        try:
            while self.visit(node.cond):
                self.memstack.push(Memory('while'))
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
                self.memstack.pop()
        except BreakException:
            self.memstack.pop()

    @when(AST.ForLoop)
    def visit(self, node):
        try:
            for i in self.visit(node.range_expr):
                self.memstack.push(Memory('for'))
                self.memstack.insert(node.name, i)
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
                self.memstack.pop()
        except BreakException:
            self.memstack.pop()

    @when(AST.BreakStatement)
    def visit(self, node):
        raise BreakException

    @when(AST.ContinueStatement)
    def visit(self, node):
        raise ContinueException

    @when(AST.ReturnStatement)
    def visit(self, node):
        val = self.visit(node.value)
        raise ReturnValueException(val)

    @when(AST.PrintStatement)
    def visit(self, node):
        args = self.visit(node.args)
        for arg in args[:-1]:
            print(arg, end=' ')
        print(args[-1])

    @when(AST.Vector)
    def visit(self, node):
        # not the fastest way to do this as it retraveses a linked list every time a vector/matrix
        # is instanciated, but it works

        contents = [self.visit(val) for val in node.iter()]
        # looks weird to do this, but this is actually totally reasonable behavior
        if len(contents) == 1: contents = contents[0]

        return np.array(contents)

    @when(AST.FunctionCall)
    def visit(self, node):
        arg = self.visit(node.arg)

        match node.name:
            case 'eye':
                assert len(arg) == 1
                return np.eye(arg[0])
            case 'ones':
                return np.ones(tuple(arg))
            case 'zeros':
                return np.zeros(tuple(arg))
