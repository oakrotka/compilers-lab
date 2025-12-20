class SymbolTable(object):
    def __init__(self): # parent scope and symbol table name
        self.scopes = [{}]
        self.scope_names = ['global']

    def put(self, name: str, symbol):
        self.scopes[-1][name] = symbol

    def get(self, name: str):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def push_scope(self, scope_name):
        self.scopes.append({})
        self.scope_names.append(scope_name)

    def pop_scope(self):
        self.scopes.pop()
        self.scope_names.pop()
