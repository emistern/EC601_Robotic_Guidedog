class command():

    def __init__(self, code, name):
        
        self.code = code

        self.name = name

    def __str__(self):
        return str(self.name)

class Code():

    F = 1
    R = 2
    L = 3

class CommandSet():

    F = command(Code.F, "forward")
    R = command(Code.R, "right")
    L = command(Code.L, "left")

if __name__ == "__main__":

    print(CommandSet.F)
    c = CommandSet.F
    print(c.code == Code.F)