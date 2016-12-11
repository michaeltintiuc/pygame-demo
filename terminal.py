from commands import *


class Terminal:
    def __init__(self, engine=None):
        self.run = False
        self.input = ''
        self.engine = engine
        self.commands = Commands(self)

    def init(self):
        if not self.run:
            self.input = raw_input('Terminal initiated\n>> ')
        else:
            self.input = raw_input('>> ')

        while not self.input:
            self.input = raw_input('>> ')

        self.input = self.input.lower().split()
        self.run = True

    def run_cmd(self):
        if self.input[0] in self.commands.list:
            return getattr(self.commands, self.input[0])()
        else:
            print 'Command not found. Use "help"\n'
