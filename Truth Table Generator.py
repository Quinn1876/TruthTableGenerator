#################################
## Name: Truth Table Generator
##
## Auth: Quinn Hodges
#################################

import pprint as pp

class Proposition:
  def __init__(self, type_, label=None, prop1=None, prop2=None):
    if type_ == 'atomic' and (not prop1 is None or not prop2 is None):
      raise InvalidPropError
    if type_ != 'atomic' and prop1 is None and not prop2 is None:
      raise InvalidPropError

    self.type = type_
    self.label = label
    self.prop1: Proposition = prop1
    self.prop2: Proposition = prop2

    self.propTypes = {
      'atomic': lambda a, b: self.label,
      'NOT': Proposition.notText,
      'OR': Proposition.orText,
      'AND': Proposition.andText,
      'INFERS': Proposition.inferenceText,
      'IMPLIES': Proposition.implicationText,
      'IFAOIF': Proposition.ifAndOnlyIfText,
    }

  def __str__(self):
    return self.propTypes.get(self.type, lambda a, b: '')(str(self.prop1), str(self.prop2))

  @classmethod
  def orText(cls, a, b):
    return "(%s \/ %s)" % (a,b)

  @classmethod
  def andText(cls, a, b):
    return "(%s /\ %s)" % (a,b)

  @classmethod
  def notText(cls, a, b):
    return f"(~{a})"

  @classmethod
  def implicationText(cls, a, b):
    return f"({a} ==> {b})"

  @classmethod
  def inferenceText(cls, a, b):
    return "(%s <== %s)" % (a,b)

  @classmethod
  def ifAndOnlyIfText(cls, a, b):
    return "(%s <==> %s)" % (a,b)

class InvalidPropError(Exception):
  pass

class TruthTable:
    def __init__(self):
        self.table = [[], []]
        self.numAtomics = 0
        self.aProps = (n for n in range(65, 123))

    def appendProposition(self, type_, **kwargs):
      if type_ == 'atomic':
        self.table[0].append(Proposition('atomic', label=chr(int(next(self.aProps)))))
        self.table[0].append(Proposition('NOT', prop1=self.table[0][len(self.table[0]) - 1]))
        self.numAtomics += 1
      else:
        self.table[0].append(Proposition(type_, **kwargs))

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
            print('%d: %s' % (i + 1, str(self.table[0][i])))
        print("#" * 10)

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

        self.appendProposition("OR", prop1=self.table[0][int(x[0]) - 1], prop2=self.table[0][int(x[1]) - 1])
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


        self.appendProposition( "AND", prop1=self.table[0][int(x[0]) - 1], prop2=self.table[0][int(x[1]) - 1])

        print("Propositions Updated")
        self.printPropositions()
        return 0

    def NOT(self):
        print("Please select the proposition that you would like to negate")
        self.printPropositions()
        ui = input()

        if len(ui) != 1 or not self.validateInput(ui):
            return -1

        self.appendProposition("NOT", prop1=self.table[0][ui-1])

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


        self.appendProposition("IMPLIES", prop1=self.table[0][int(x[0])-1], prop2=self.table[0][int(x[1])-1])

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


        self.appendProposition("INFERS",prop1=self.table[0][int(x[0]) - 1], prop2=self.table[0][int(x[1]) - 1])

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


        self.appendProposition("IFAOIF", prop1=self.table[0][int(x[0]) - 1], prop2=self.table[int(x[1]) - 1])

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
        rows = 0
        for col in range(len(self.table[0])):
            if self.table[0][col].type == "atomic":
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
        if prop.type == "atomic":
            return self.table[1][col]
        else:
            a = self.evaluate( int(prop.prop1) )
            if (type(prop.prop2) == str):
                b = self.evaluate( int(prop.prop2) )
            c = []

            if prop.type == "OR":
                for i in range(len(a)):
                    if bool(a[i]) or bool(b[i]):
                        c.append(1)
                    else:
                        c.append(0)

            elif prop.type == "AND":
                for i in range(len(a)):
                    if bool(a[i]) and bool(b[i]):
                        c.append(1)
                    else:
                        c.append(0)

            elif prop.type == "NOT":
                for i in range(len(a)):
                    if bool(a[i]):
                        c.append(0)
                    else:
                        c.append(1)
            elif prop.type == "IMPLIES":
                for i in range(len(a)):
                    if bool(a[i]):
                        c.append(b[i])
                    else:
                        c.append(1)

            elif prop.type == "INFERS":
                for i in range(len(a)):
                    if bool(b[i]):
                        c.append(a[i])
                    else:
                        c.append(1)

            elif prop.type == "IFAOIF":
                for i in range(len(a)):
                    if int(a[i]) == int(b[i]):
                        c.append(1)
                    else:
                        c.append(0)
            return c





############# WELCOME MESSAGE #####################################
ttable = TruthTable()

while True:
    ui = input("How many atomic propositions would you like?")
    try:
        x = int(ui)
        break
    except:
        continue
print("x = %d" % x)
for i in range(x):
  ttable.appendProposition('atomic')

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


