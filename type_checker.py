import AST
from symbol_table import SymbolTable

import sys

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):       # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

class TypeChecker(NodeVisitor):
    symbols = SymbolTable()
    correct = True

    def fail(self, line, reason):
        self.correct = False
        print(f'Error (line {line}): {reason}', file=sys.stderr)

    def is_num(self, x):
        return x in ['int', 'float']

    def eq_or_empty(self, a, b):
        return None in [a, b] or a == b

    def visit_Varlist(self, node):
        subtype = self.visit(node.arg)[0]
        for val in node.iter():
            if val != node.arg:
                if subtype != self.visit(val)[0]:
                    subtype = None
        return ('vector', subtype, node.len)

    def visit_Block(self, node):
        for val in node.iter():
            if type(val) == AST.Block:
                self.symbols.push_scope('block')
                self.visit(val)
                self.symbols.pop_scope()
            else:
                self.visit(val)

    def visit_IntNum(self, node):
        return ('int',)
    def visit_FloatNum(self, node):
        return ('float',)
    def visit_String(self, node):
        return ('string',)

    def visit_Variable(self, node):
        var = self.symbols.get(node.value)
        if var is None:
            self.fail(node.line, f'variable {node.value} is not declared')
            return ('undefined',)
        return var

    def visit_Range(self, node):
        type1 = self.visit(node.low)[0]
        type2 = self.visit(node.high)[0]
        if type1 != 'int' or type2 != 'int':
            self.fail(node.line, 'both arguments to range must be integers')
        return ('range',)

    def visit_Index(self, node):
        type1 = self.visit(node.x)[0]

        if node.y is not None:
            type2 = self.visit(node.y)[0]
            if type1 != 'int' or type2 != 'int':
                self.fail(node.line, 'both arguments to range must be integers')
        else:
            if type1 != 'int':
                self.fail(node.line, 'index must be an integer')

        return ('index', 1 + (node.y is not None))

    def visit_Ref(self, node):
        type1 = self.symbols.get(node.name)
        n = self.visit(node.indexer)[1]
        if type1 is None:
            self.fail(node.line, f'undeclared variable {node.name}')
            return ('int',)
        elif not (n == 1 and type1[0] == 'vector' or n == 2 and type1[0] == 'matrix'):
            self.fail(node.line, f'cannot index {type0[0]} with {n} arguments')
        return (type1[1],)


    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)[0]
        type2 = self.visit(node.right)[0]
        if not self.is_num(type1) or not self.is_num(type2):
            self.fail(node.line, f'cannot compare values of type {type1} and {type2}')
        return ('int',)  # adding booleans is too much work

    def visit_NumExpr(self, node):
        type1 = self.visit(node.left)[0]
        type2 = self.visit(node.right)[0]
        if not self.is_num(type1) or not self.is_num(type2):
            self.fail(
                node.line,
                f'cannot perform {node.op} operation on values of type {type1} and {type2}'
            )
        return ('float' if 'float' in [type1, type2] else 'int',)

    def visit_MatExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if type1[0] != type2[0] or type1[0] not in ['vector', 'matrix']:
            self.fail(
                node.line,
                f'cannot perform {node.op} operation on values of type {type1[0]} and {type2[0]}'
            )
            return ('undefined',)

        def check_dims(n, m):
            if not self.eq_or_empty(n, m):
                self.fail(node.line, f'mismatched dimensions: {n} and {m}')

        check_dims(type1[2], type2[2])
        if type1[0] == 'matrix': check_dims(type1[3], type2[3])
        
        subtype = 'float' if 'float' in [type1[1], type2[1]] else 'int'
        n = type1[2] if type1[2] is not None else type2[2]

        if type1[0] == 'matrix':
            m = type1[3] if type1[3] is not None else type2[3]
            return ('matrix', subtype, n, m)
        else:
            return ('vector', subtype, n)


    def visit_UnExpr(self, node):
        if node.op == '-':
            type1 = self.visit(node.value)[0]
            if not self.is_num(type1):
                self.fail(node.line, f'cannot negate value of type {type1}')
        elif node.op == '\'':
            type1 = self.visit(node.value)
            if type1[0] == 'vector':
                return type1
            elif type1[0] == 'matrix':
                (_, subtype, n, m) = type1
                return ('matrix', subtype, m, n)
            else:
                self.fail(node.line, f'unsupported operator \' on type {type1}')
                return type1
        else:
            raise NotImplementedError

    def visit_Assignment(self, node):
        type1 = self.visit(node.right)
        if node.op == '=' and type(node.left) == str:
            self.symbols.put(node.left, type1)
        else:
            if type(node.left) == str:
                id = node.left
                expected = self.symbols.get(id)
            else:
                id = node.left.name
                expected = self.visit(node.left)

            if expected == None:
                self.fail(node.line, f'{id} is undeclared')
            elif not (self.is_num(type1[0]) and self.is_num(expected[0])):
                self.fail(
                    node.line,
                    f'cannot perform {node.op} operation on values of type '
                    f'{expected[0]} and {type1[0]}'
                )

    def visit_Conditional(self, node):
        if self.visit(node.cond) != ('int',):
            self.fail(node.line, f'condition of if statement must be of type int')

        self.symbols.push_scope('if')
        self.visit(node.true_block)
        if node.false_block != None: self.visit(node.false_block)
        self.symbols.pop_scope()

    def visit_WhileLoop(self, node):
        if self.visit(node.cond) != ('int',):
            self.fail(node.line, f'condition of if statement must be of type int')

        self.symbols.push_scope('while')
        self.visit(node.block)
        self.symbols.pop_scope()

    def visit_ForLoop(self, node):
        self.visit(node.range_expr)
        self.symbols.push_scope('for')
        self.symbols.put(node.name, ('int',))
        self.visit(node.block)
        self.symbols.pop_scope()

    def visit_BreakStatement(self, node):
        if 'while' not in self.symbols.scope_names or 'for' not in self.symbols.scope_names:
            self.fail(node.line, 'no loop to break out of')

    def visit_ContinueStatement(self, node):
        if 'while' not in self.symbols.scope_names or 'for' not in self.symbols.scope_names:
            self.fail(node.line, 'no loop to continue')

    def visit_ReturnStatement(self, node):
        pass

    def visit_PrintStatement(self, node):
        for val in node.args.iter():
            type1 = self.visit(val)[0]
            if type1 not in ['int', 'float', 'string']:
                self.fail(node.line, f'cannot print value of type {type1}')

    def visit_Vector(self, node):
        node = node.arg
        type1 = self.visit(node.arg)
        n = type1[2] if type1[0] == 'vector' else None

        for val in node.iter():
            type2 = self.visit(val) if val != node.arg else type1
            if type2[0] == 'matrix':
                self.fail(node.line, 'only 1 and 2-dimensional matrices are supported')
            elif type2[0] not in ['int', 'float', 'vector']:
                self.fail(node.line, f'invalid member of matrix: {type2[0]}')
            elif type2 != type1:
                if type1[0] == 'vector' and type2[0] == 'vector':
                    if n == None:
                        n = type2[2]
                    elif n != type2[2]:
                        self.fail(node.line, f'mismatched matrix row lengths: {n} and {type2[2]}')
                        continue

                repr1 = type1[0] if type1[0] != 'vector' else type1
                repr2 = type2[0] if type2[0] != 'vector' else type2
                self.fail(node.line, f'mismatched types in matrix: {repr1} and {repr2}')

        if type1[0] in ['int', 'float']:
            return ('vector', type1[0], node.len)
        else:
            (_, subtype, m) = type1
            return ('matrix', subtype, m, node.len)

    def visit_FunctionCall(self, node):
        type1 = self.visit(node.arg)[0]
        if type1 != 'int':
            self.fail(node.line, 'argument to function must be an int')
        n = node.arg.value if type(node.arg) == AST.IntNum else None
        return ('matrix', 'int', n, n)
