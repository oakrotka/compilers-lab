from operator import add
import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def tprefix(indent):
    print('|  ' * indent, end='')

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.LinkedList)
    def printTree(self, indent=0):
        for node in self.iter():
            node.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        tprefix(indent)
        print('VECTOR')
        for node in self.iter():
            node.printTree(indent+1)

    @addToClass(AST.Value)
    def printTree(self, indent=0):
        tprefix(indent)
        print(self.value)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        tprefix(indent)
        print(self.op)

        indent += 1
        if type(self.left) == str:
            tprefix(indent)
            print(self.left)
        else:
            self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        tprefix(indent)
        print('RANGE')

        indent += 1
        self.low.printTree(indent)
        self.high.printTree(indent)

    @addToClass(AST.Index)
    def printTree(self, indent=0):
        self.x.printTree(indent)
        if self.y is not None:
            self.y.printTree(indent)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        tprefix(indent)
        print('REF')

        indent += 1
        if type(self.name) == str:
            tprefix(indent)
            print(self.name)
        else:
            self.name.printTree(indent)
        self.indexer.printTree(indent)

    @addToClass(AST.UnExpr)
    def printTree(self, indent=0):
        tprefix(indent)
        print(self.op)
        self.value.printTree(indent+1)

    @addToClass(AST.Conditional)
    def printTree(self, indent=0):
        tprefix(indent)
        print('IF')
        self.cond.printTree(indent+1)

        tprefix(indent)
        print('THEN')
        self.true_block.printTree(indent+1)

        if self.false_block is not None:
            tprefix(indent)
            print('ELSE')
            self.false_block.printTree(indent+1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        tprefix(indent)
        print('WHILE')

        indent += 1
        self.cond.printTree(indent)
        self.block.printTree(indent)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        tprefix(indent)
        print('FOR')

        indent += 1
        tprefix(indent)
        print(self.name)
        self.range_expr.printTree(indent)
        self.block.printTree(indent)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        tprefix(indent)
        print('BREAK')

    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        tprefix(indent)
        print('CONTINUE')

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent=0):
        tprefix(indent)
        print('RETURN')

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        tprefix(indent)
        print('PRINT')
        self.args.printTree(indent+1)

    @addToClass(AST.FunctionCall)
    def printTree(self, indent=0):
        tprefix(indent)
        print(self.name)
        self.arg.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body
