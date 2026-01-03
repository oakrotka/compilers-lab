
class Memory:
    def __init__(self, name):
        self.name = name
        self.vars = {}

    def has_key(self, name):  # variable name
        return name in self.vars

    def get(self, name):
        return self.vars[name]

    def set(self, name, value):
        self.vars[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.mem = [Memory('global') if memory is None else memory]

    def get(self, name):
        for mem in reversed(self.mem):
            if mem.has_key(name):
                return mem.get(name)

    def insert(self, name, value):
        self.mem[-1].set(name, value)

    def set(self, name, value):
        for mem in reversed(self.mem):
            if mem.has_key(name):
                mem.set(name, value)
        self.mem[-1].set(name, value)

    def push(self, memory):
        self.mem.append(memory)

    def pop(self):
        self.mem.pop()
