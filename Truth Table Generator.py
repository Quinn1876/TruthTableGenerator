#################################
## Name: Truth Table Generator
##
## Auth: Quinn Hodges
#################################

import pprint as pp

class TruthTable:
    aProps = ['q', 'p', 'r', 'm', 'n', 's', 't']

    def __init__(self):
        self.table = [[], []]
        self.numAtomics = 0

    def appendAtomic(self, num):
        for i in range(num):
            self.table[0].append([self.aProps[i], 'atomic'])
        for i in range(num):
            self.appendCompound(self.notText(self.mapIndexToName(i)), "NOT", i+1)
        self.numAtomics += num

    def appendCompound(self, string, Type, prop1, prop2=None):

        self.table[0].append([string, Type, str(int(prop1) - 1), str(int(prop2) - 1) if prop2 is not None else None])

    def mapIndexToName(self, index1, index2=None):
        if index2 is not None:
            return [ self.table[0][int(index1) - 1][0], self.table[0][int(index2) - 1][0] ]
        else:
            return self.table[0][int(index1) - 1][0]

    def validateInput(self, *inputs):
        for i in inputs:
            if int(i) - 1 not in range(len(self.table[0])):
                return False
        return True

    def printPropositions(self):
        print("#" * 10)
        for i in range(len(self.table[0])):
            print('%d: %s' % (i + 1, self.table[0][i][0]))
        print("#" * 10)

    @staticmethod
    def orText(a, b):
        return "(%s \/ %s)" % (a,b)

    @staticmethod
    def andText(a, b):
        return "(%s /\ %s)" % (a,b)

    @staticmethod
    def notText(a):
        return "(~%s)" % a

    @staticmethod
    def implicationText(a, b):
         return "(%s ==> %s)" % (a,b)

    @staticmethod
    def inferenceText(a, b):
        return "(%s <== %s)" % (a,b)

    @staticmethod
    def ifAndOnlyIfText(a, b):
        return "(%s <==> %s)" % (a,b)

    def OR(self):
        print("""
Please select the first and second proposition for your or statement:
(Write your selection in terms '1,2')
              """)

        self.printPropositions()
        ui = input()
        try:
            x = ui.split(',')
            if len(x) != 2 or not self.validateInput(*x):
                raise Exception
        except:
            return -1

        self.appendCompound(TruthTable.orText(*self.mapIndexToName(*x)), "OR", int(x[0]), int(x[1]))
        print("Propositions Updated")
        self.printPropositions()
        return 0



    def AND(self):
        print("""
Please select the first and second proposition for your and statement:
(Write your selection in terms '1,2')
              """)
        self.printPropositions()
        ui = input()

        x = ui.split(',')
        if len(x) != 2 or not self.validateInput(*x):
            return -1


        self.appendCompound(TruthTable.andText(*self.mapIndexToName(*x)), "AND", int(x[0]), int(x[1]))

        print("Propositions Updated")
        self.printPropositions()
        return 0

    def NOT(self):
        print("Please select the proposition that you would like to negate")
        self.printPropositions()
        ui = input()

        if len(ui) != 1 or not self.validateInput(ui):
            return -1

        self.appendCompound(self.notText(self.mapIndexToName(ui)), "NOT", ui)

        print("Propositions Updated")
        self.printPropositions()
        return 0



    def IMPLIES(self):
        print("""
Please select the first and second proposition for your implication:
(Write your selection in terms '1,2')
              """)
        self.printPropositions()
        ui = input()

        x = ui.split(',')
        if len(x) != 2 or not self.validateInput(*x):
            return -1


        self.appendCompound(TruthTable.implicationText(*self.mapIndexToName(*x)), "IMPLIES", int(x[0]), int(x[1]))

        print("Propositions Updated")
        self.printPropositions()
        return 0

    def INFERS(self):
        print("""
Please select the first and second proposition for your inference:
(Write your selection in terms '1,2')
              """)
        self.printPropositions()
        ui = input()

        x = ui.split(',')
        if len(x) != 2 or not self.validateInput(*x):
            return -1


        self.appendCompound(TruthTable.inferenceText(*self.mapIndexToName(*x)), "INFERS", int(x[0]), int(x[1]))

        print("Propositions Updated")
        self.printPropositions()
        return 0

    def IFAOIF(self):
        print("""
Please select the first and second proposition for your \"if and only if\" statement:
(Write your selection in terms '1,2')
              """)
        self.printPropositions()
        ui = input()

        x = ui.split(',')
        if len(x) != 2 or not self.validateInput(*x):
            return -1


        self.appendCompound(TruthTable.ifAndOnlyIfText(*self.mapIndexToName(*x)), "IFAOIF", int(x[0]), int(x[1]))

        print("Propositions Updated")
        self.printPropositions()
        return 0

    def SONEDEFAULT(self):
        pass

    def EVALUATE(self):
        self.evaluateTable()

    switch1 = {
    '1' : OR,
    '2' : AND,
    '3' : NOT,
    '4' : IMPLIES,
    '5' : INFERS,
    '6' : IFAOIF,
    '7' : EVALUATE,
    'default' : SONEDEFAULT
    }

    def evaluateTable(self):
        self.table[1] = []
        rows = 1
        for col in range(len(self.table[0])):
            if self.table[0][col][1] == "atomic":
                self.table[1].append(([1 for i in range((1 << self.numAtomics)//(1<< col+1))] + [0 for i in range((1 << self.numAtomics)//(1<< col+1))]) * (1<<col))
                rows += 1

            else:
                self.table[1].append(self.evaluate(col))



        self.printPropositions()
        print(' | '.join([str(self.table[0][i][0]) for i in range(len(self.table[0]))]))
        print('---'.join(['-' * len(str(self.table[0][i][0])) for i in range(len(self.table[0]))]))

        for i in range(1 << self.numAtomics):
            print(' | '.join([(str(self.table[1][j][i]) + ' ' * (len(self.table[0][j][0]) - 1))  for j in range(len(self.table[1]))]))


    def evaluate(self, col):
        prop = self.table[0][col]
        if prop[1] == "atomic":
            return self.table[1][col]
        else:
            a = self.evaluate( int(prop[2]) )
            if (type(prop[3]) == str):
                b = self.evaluate( int(prop[3]) )
            c = []

            if prop[1] == "OR":
                for i in range(len(a)):
                    if bool(a[i]) or bool(b[i]):
                        c.append(1)
                    else:
                        c.append(0)

            elif prop[1] == "AND":
                for i in range(len(a)):
                    if bool(a[i]) and bool(b[i]):
                        c.append(1)
                    else:
                        c.append(0)

            elif prop[1] == "NOT":
                for i in range(len(a)):
                    if bool(a[i]):
                        c.append(0)
                    else:
                        c.append(1)
            elif prop[1] == "IMPLIES":
                for i in range(len(a)):
                    if bool(a[i]):
                        c.append(b[i])
                    else:
                        c.append(1)

            elif prop[1] == "INFERS":
                for i in range(len(a)):
                    if bool(b[i]):
                        c.append(a[i])
                    else:
                        c.append(1)

            elif prop[1] == "IFAOIF":
                for i in range(len(a)):
                    if int(a[i]) == int(b[i]):
                        c.append(1)
                    else:
                        c.append(0)
            return c





############# WELCOME MESSAGE #####################################
ttable = TruthTable()

while True:
    ui = input("How many atomic propositions would you like(1-7)?")
    try:
        x = int(ui)
        if (x in range(1, 8)):
            break
    except:
        continue
print("x = %d" % x)
ttable.appendAtomic(x)

##################### MAIN LOOP ##################################
while True:
    print("""
          Which composite propositions would you like?
          1 OR
          2 AND
          3 NOT
          4 IMPLIES
          5 INFERS
          6 IF AND ONLY IF
          7 Evaluate
          8 END
          """)
    ui = input()
    if ui in ttable.switch1.keys():
        ttable.switch1[ui](ttable)
    else:
        break


