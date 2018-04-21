from programs.mprog import MProg
from python_parser import Parser, a, anyof, maybe, someof
import operator as op

__all__ = ['Calc']


class InterpreterError(Exception):
    pass


class Calc(MProg):
    def __init__(self):
        super(Calc, self).__init__()
        self.name = 'calc'

        self.un_ops = {
            '-': op.neg,
            '+': op.pos
        }
        self.bin_ops = {
            '*': op.mul,
            '/': op.truediv,
            '+': op.add,
            '-': op.sub
        }

        self.vars = {}

        self.tokens = (
            ('(\d*\.\d+)|(\d+\.\d*)', 'FLOAT'),
            ('\d+', 'INT'),
            ('\+', 'ADD'),
            ('-', 'SUB'),
            ('\*', 'MUL'),
            ('/', 'DIV'),
            ('\)', 'R_PAR'),
            ('\(', 'L_PAR'),
            ('\w+\s*=', 'SET'),
            ('\w+', 'NAME'),
            ('=', 'EQ'),
            ('|', 'PIPE')
        )

        self.grammar = {
            'FACTOR': anyof(
                'FLOAT', 'INT', 'NAME',
                a(anyof('ADD', 'SUB'), 'FACTOR'),
                a('L_PAR', 'EXPR', 'R_PAR')),
            'TERM': a('FACTOR', maybe(someof(anyof('DIV', 'MUL'), 'FACTOR'))),
            'DEFN': a('SET', 'EXPR'),
            'EXPR': a('TERM', maybe(someof(anyof('ADD', 'SUB'), 'TERM'))),
            'PROGRAM': anyof('EXPR', 'DEFN')
        }

        self.parser = Parser(self.tokens, self.grammar)

    def expr(self, items):
        result = self.visit(next(items))
        op = next(items, None)
        while op is not None:
            result = self.bin_ops[op.value](result, self.visit(next(items)))
            op = next(items, None)
        return result

    def term(self, items):
        return self.expr(items)

    def factor(self, items):
        item = next(items)
        if item.name == 'L_PAR':
            result = self.visit(next(items))
        elif item.name in ('ADD', 'SUB'):
            result = self.un_ops[item.value](self.visit(next(items)))
        elif item.name == 'NAME':
            if item.value not in self.vars:
                raise InterpreterError(
                    'Variable {} is not defined'.format(item.value))
            result = self.vars[item.value]
        else:
            result = float(item.value)
        next(items, None)
        return result

    def defn(self, items):
        name = next(items).value.split('=')[0].rstrip()
        self.vars[name] = self.visit(next(items))

    def skip(self, items):
        return self.visit(next(items))

    def visit(self, node):
        return getattr(self, node.name.lower(), self.skip)(iter(node.items))

    def run(self, player, args, mud):
        ast = self.parser.parse('PROGRAM', args)
        return str(self.visit(ast))
