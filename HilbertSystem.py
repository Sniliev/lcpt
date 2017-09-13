import re

class Formula:
    list_version = []
    string_version = ""
    for_every = []
    exist = []

    def __init__(self, string):
        self.string_version = string
        self.list_version = self.string_to_formula(string)

    def string_to_formula(self, string):
        result = []
        brackets = 0;
        inside_formula = ''
        formula = ''
        for letter in string:
            if(letter == '('):
                if(brackets > 0):
                    inside_formula += letter

                brackets += 1
                continue
            if(letter == ')'):
                brackets -= 1
                if(brackets == 0):
                    result.append(Formula(inside_formula))
                    flag = False
                    inside_formula = ""
                    continue
            
            if(brackets > 0):
                inside_formula += letter
                continue

            if(letter == '-'): continue
            if(letter == ' '): continue
            if(letter == '>'):
                if formula != '':
                    result.append(formula)
                result.append("->")
                formula = ''
                continue
            
            if(letter == 'v' or letter == '&' or letter == '!'):
                if formula != '':
                    result.append(formula)
                result.append(letter)
                formula = ''
                continue
        
            if(letter == '{'):
                if formula != '':
                    result.append(formula)
                formula = '{'
                continue

            if(letter == ']' ):
                result.append(formula + ']')
                formula = ''
                continue
            
            formula += letter
        if formula != '':
            result.append(formula)
        return result

    def __eq__(self, other):
        if isinstance(other, str):
                return self.string_version == other
        return self.string_version == other.string_version
    
    def __len__(self):
        return len(self.list_version)

def is_valid(inp):
    formula = inp.list_version
    for index, element in enumerate(formula):
        if(index == 0):
            if(element == "->" or element == 'v' or
                    element == "&" or element == ')'):
                return False
        if(index + 1 == len(formula)):
            if(element == "->" or element == 'v' or
                    element == "&" or element =='(' or element == '!'):
                return False
        if isinstance(element, Formula):
            if(not is_valid(element)): return False
            if(index > 0):
                pre = formula[index -1]
                if(isinstance(pre, Formula) or pre == ')'):
                    return False

        if(element == '('):
            if(index > 0):
                pre = formula[index - 1]
                if(isinstance(pre, Formula) or re.search('[a-zA-Z]', pre)):
                    return False
            suc = formula[index + 1]
            if(suc == "->" or suc == 'v' or suc == '&'):
                    return False

        if(element == ')'):
            if(index < len(formula) -1):
                suc = formula[index + 1]
                if(suc == "!" or isinstance(suc, Formula) or 
                    re.search('[a-zA-Z]', suc)):
                    return False
            pre = formula[index - 1]
            if(pre == "->" or pre == 'v' or pre == '&' or pre == '!'):
                return False

        if(element == "->" or element == 'v' or element == '&'):
            pre = formula[index - 1]
            suc = formula[index + 1]
            if( not ( isinstance(pre, Formula) or re.search('[a-zA-Z]', pre) or
                pre == ')')):
                return False
            if( not ( isinstance(suc, Formula) or re.search('[a-zA-Z]', suc) or
                pre == '(' or suc == '!')):
                return False

        if(element == '!'):
            if(index > 0):
                pre = formula[index -1]
                if(isinstance(pre, Formula) or pre == ')' or
                        re.search('[a-zA-Z]', pre)):
                    return False
            suc = formula[index +1]
            if(suc == ')' or suc == "->" or suc == 'v' or suc == '&'):
                return False
        try:
            if ("FE[" in element):
                if(index > 0):
                    pre = formula[index - 1]
                    if(isinstance(pre, Formula) or pre == ')'):
                        return False
                suc = formula[index + 1]
                if(suc == '->' or suc == 'v' or suc == '&' or suc == '!'):
                    return False
        except(TypeError):
           continue 
            
        if ("Ex[" in element):
            if(index > 0):
                pre = formula[index - 1]
                if(isinstance(pre, Formula) or pre == ')'):
                    return False
            suc = formula[index + 1]
            if(suc == '->' or suc == 'v' or suc == '&' or suc == '!'):
                return False

        if(not check_brackets(inp.string_version)): return False
    return True



def check_brackets(formula):
    a = list(formula)
    count = 0
    for letter in a:
        if(letter == '('):
            count+=1
        if(letter == ')'):
            count -=1
        if(count < 0):
            return False

    if(count == 0): return True
    return False



    

def is_correct(formula, formulas, type_of_logic):
    if is_in_formulas(formula, formulas): return True
    if is_axiom(formula, type_of_logic): return True
    if mp(formula, formulas): return True
    if is_gen(formula, formulas): return True
    if fixed_brackets(formula, formulas): return True
    return False

def is_in_formulas(formula, formulas):
    return (formulas.count(formula) > 0)

def is_axiom(formula, type_of_logic):
    if is_first_axiom(formula): return True
    if is_second_axiom(formula): return True
    if is_third_axiom(formula): return True
    if is_fourth_axiom(formula): return True
    if is_fifth_axiom(formula): return True
    if is_sixth_axiom(formula): return True
    if is_seventh_axiom(formula): return True
    if is_eight_axiom(formula): return True
    if (type_of_logic == 'i' or type_of_logic == 'c'):
        if is_eleventh_axiom(formula): return True
    if type_of_logic == 'c':
        if is_twelfth_axiom(formula): return True

    return False

def mp(formula, formulas):
    for ak in formulas:
        for aj in formulas:
            try:
                if(ak == '(' + aj.string_version + ')' + "->" + formula.string_version):
                    return True
                if(ak == aj.string_version + "->" + formula.string_version):
                    return True
            except(IndexError, AttributeError) as e:
                continue

    return False

def is_gen(formula, formulas):
    if len(formula) != 2: return False
    try:
        if "FE" not in formula.list_version[0] : return False
        for aj in formulas:
            if formula.list_version[1] == aj : return True
    except(TypeError, IndexError):
        return False
    return False

#"(A->B->C)->(A->B)->A->C"
def is_first_axiom(formula):
    try:
        if len(formula) != 7: return False 
        if len(formula.list_version[0]) != 5: return False
        if len(formula.list_version[2]) != 3: return False
        A = ((formula.list_version[0].list_version[0] == formula.list_version[2].list_version[0]) and
            (formula.list_version[0].list_version[0] == formula.list_version[4]))

        B = (formula.list_version[0].list_version[2] == formula.list_version[2].list_version[2])
        C = (formula.list_version[0].list_version[4] == formula.list_version[6])
        impl = "->"
        D = ((impl == formula.list_version[0].list_version[1]) and
                (impl == formula.list_version[0].list_version[3]) and
                (impl == formula.list_version[1]) and
                (impl ==formula.list_version[2].list_version[1]) and
                (impl == formula.list_version[3]) and
                (impl == formula.list_version[5]))

        if(A and B and C and D): return True

    except (IndexError, AttributeError) as e:
        return False

    return False

#"A->B->A"
def is_second_axiom(formula):
    if len(formula) != 5 : return False
    try:
        A = (formula.list_version[0] == formula.list_version[4])
        impl = "->"
        B = ((impl == formula.list_version[1]) and
                (impl == formula.list_version[3]))

        if(A and B): return True

    except (IndexError, AttributeError) as e:
        return False
    
    return False 

#"(A&B)->A, (A&B)->B"
def is_third_axiom(formula):
    try:
        if len(formula) != 3 : return False
        if len(formula.list_version[0]) !=3 : return False
        A = ((formula.list_version[0].list_version[0] == formula.list_version[2]) or
                (formula.list_version[0].list_version[2] == formula.list_version[2]))

        con = '&'
        impl = "->"
        B = ((con == formula.list_version[0].list_version[1]) and
                (impl == formula.list_version[1]))

        if(A and B): return True

    except (IndexError, AttributeError) as e:
        return False

    return False

#"A->B->(A&B)"
def is_fourth_axiom(formula):
    try:
        if len(formula) != 5 : return False
        if len(formula.list_version[4]) != 3 : return False
        
        A = ((formula.list_version[0] == formula.list_version[4].list_version[0]) and
                (formula.list_version[2] == formula.list_version[4].list_version[2]))
        con = '&'
        impl = "->"

        B = ((impl == formula.list_version[1]) and
                (impl == formula.list_version[3]) and
                (con == formula.list_version[4].list_version[1]))
        
        if(A and B): return True

    except (IndexError, AttributeError) as e:
        return False

    return False

#"A->(AvB), B->(AvB)"
def is_fifth_axiom(formula):
    try:
        if len(formula) != 3 : return False
        if len(formula.list_version[2]) != 3 : return False
        
        A = ((formula.list_version[0] == formula.list_version[2].list_version[0]) or
                (formula.list_version[0] == formula.list_version[2].list_version[2]))
        dis = 'v'
        impl = "->"

        B = ((impl == formula.list_version[1]) and
                (dis == formula.list_version[2].list_version[1]))
        
        if(A and B): return True

    except (IndexError, AttributeError) as e:
        return False

    return False


#"(A->C) -> (B->C) -> (AvB) -> C"
def is_sixth_axiom(formula):
    try:
        if len(formula) != 7 : return False
        if len(formula.list_version[0]) != 3 : return False
        if len(formula.list_version[2]) != 3 : return False
        if len(formula.list_version[4]) != 3 : return False
        
        A = (formula.list_version[0].list_version[0] == formula.list_version[4].list_version[0]) 
        B = (formula.list_version[2].list_version[0] == formula.list_version[4].list_version[2]) 
        C = ((formula.list_version[0].list_version[2] == formula.list_version[2].list_version[2]) and
                (formula.list_version[0].list_version[2] == formula.list_version[6]))

        impl = "->"
        dis = 'v'
        B = ((impl == formula.list_version[0].list_version[1]) and
                (impl == formula.list_version[1]) and
                (impl == formula.list_version[2].list_version[1]) and
                (impl == formula.list_version[3]) and
                (impl == formula.list_version[5]) and
                (dis == formula.list_version[4].list_version[1]))
        
        if(A and B): return True

    except (IndexError, AttributeError) as e:
        return False

    return False

#"FE[x]A -> A[x --> t]"
def is_seventh_axiom(formula):
    try:
        if len(formula) != 4 : return False
        if "FE" not in formula.list_version[0]: return False
        x = re.search(r"\[(\w+)\]", formula.list_version[0]).group(1)
        A = is_replaced(formula.list_version[1], formula.list_version[3], x)
        impl = "->"
        
        B = (impl == formula.list_version[2])
        if (A and B): return True

    except (IndexError, TypeError) as e:
        return False

    return False

def is_replaced(first_formula, second_formula, x):
    if(not len(first_formula) == len(second_formula)): return False
    flag = False
    t = ""
    if(isinstance(first_formula, str)):
        a = list(first_formula)
    if(isinstance(second_formula, str)):
        b = list(second_formula)
    if(isinstance(first_formula, Formula)):
        a = first_formula.list_version
    if(isinstance(second_formula, Formula)):
        b = second_formula.list_version

    for index, elem in enumerate(a):
        if(elem == x and (not flag)):
            t = b[index]
            flag = True
            continue
        if(elem == x):
            if(not b[index] == t):
                return False
            else: continue
        if(elem != b[index]):
            return False

    return True


#"FE[x](B->A) -> (B -> FE[x]A)"
def is_eight_axiom(formula):
    try:
        if len(formula) != 4 : return False
        if len(formula.list_version[1]) != 3 : return False
        if len(formula.list_version[3]) != 4 : return False
        if "FE" not in formula.list_version[0]: return False
        if "FE" not in formula.list_version[3].list_version[2]: return False

        A = (formula.list_version[1].list_version[0] == formula.list_version[3].list_version[0] and
                formula.list_version[1].list_version[2] == formula.list_version[3].list_version[3])

        impl = "->"
        B = (impl == formula.list_version[2] and 
                impl == formula.list_version[3].list_version[1])

        if (A and B) : return True
    except (IndexError, AttributeError) as e:
        return False

#"A[x --> t] -> Ex[x]A"
def is_ninth_axiom(formula):
    try:
        if len(formula) != 4 : return False
        if "Ex" not in formula.list_version[2]: return False
        x = re.search(r"\[(\w+)\]", formula.list_version[2]).group(1)
        A = (is_replaced(formula.list_version[3], formula.list_version[0], x))

        impl = "->"
        B = (impl == formula.list_version[1])

        if (A and B)  : return True
    except (IndexError, AttributeError) as e:
        return False

    return False

#"FE(x)(A->B) -> (Ex(x)A -> B)"
def is_tenth_axiom(formula):
    try:
        if len(formula) != 4 : return False
        if len(formula.list_version[1]) != 3 : return False
        if len(formula.list_version[3]) != 4 : return False
        if "FE" not in formula.list_version[0]: return False
        if "Ex" not in formula.list_version[3].list_version[0]: return False
        A = (formula.list_version[1].list_version[0] == formula.list_version[3].list_version[1] and
                formula.list_version[1].list_version[2] == formula.list_version[3].list_version[3])
        impl = "->"

        B = (impl == formula.list_version[2] and
                impl == formula.list_version[1].list_version[1] and
                impl == formula.list_version[3].list_version[2])

        if (A and B)  : return True
    except (IndexError, AttributeError) as e:
        return False

    return False

#"FALSE -> A
def is_eleventh_axiom(formula):
    try:
        A = (formula.list_version[0] == "FALSE")
        B = (formula.list_version[1] == "->")
        if(A and B):
            return True
    except(IndexError, AttributeError) as e:
        return False
    return False

#!!A -> A
def is_twelfth_axiom(formula):
    try:
        if len(formula)!=5 : return False
        A = (formula.list_version[0] == '!' and formula.list_version[1] == '!')
        B = (formula.list_version[3] == "->")
        C = (formula.list_version[2] == formula.list_version[4])
        if(A and B and C):
            return True
    except(IndexError, AttributeError) as e:
        return False
    return False



def fixed_brackets(formula, formulas):
    string = formula.string_version
    for f in formulas:
        if(removed_brackets(f.string_version, string)):
            return True

    for f in formulas:
        if(removed_brackets(string, f.string_version)):
            return True

    return False

def removed_brackets(old_formula, new_formula):
    a = list(old_formula)
    b = list(new_formula)
    if(len(a) - len(b) != 2): return False
    count = 0
    flag = False
    for index, letter in enumerate(a):
        if(letter  == ')'):
            if(((len(a) == index + 1) or (a[index + 1] == ')') and flag)):
                if(len(a) == index + 1):
                    if(letter != b[-1]): return True
                    return False
                return True
        if(letter == b[count]): 
            count += 1
            continue
        if(letter == '('):
            flag = True
            continue
    return False
def print_axioms(type_of_logic):
  print
  print "The axioms you can use are:"
  print "(A->B->C)->(A->B)->A->C"
  print "A->B->A"
  print "A->B->(A&B)"
  print "A->(AvB), B->(AvB)"
  print "(A->C) -> (B->C) -> (AvB) -> C"
  print "FE[x]A -> A[x --> t]"
  print "FE[x](B->A) -> (B -> FE[x]A)"
  print "A[x --> t] -> Ex[x]A"
  print "FE(x)(A->B) -> (Ex(x)A -> B)"
  if(type_of_logic == 'i' or type_of_logic == 'c'):
    print "FALSE -> A"
  if(type_of_logic == 'c'):
    print "!!A -> A"
  print 

print "Choose minimal,intensional or classical logic by typing m, i or c"
type_of_logic = raw_input()
print
print "Now enter the set Gamma of assumptions"
print "Type \"END\" when you're done"
formulas = []
while True:
    new_formula = raw_input()
    if(not is_valid(Formula(new_formula))):
        print "invalid formula"
        continue
    if new_formula == "END":
        break
    formulas.append(Formula(new_formula))

print 
print "Now start your proof"
print "Type \"QED\" when you're done"
print "Type \"axioms\" to see all the axioms"

while True:
    new_line = raw_input()
    if(new_line == "QED"):
        print "Your proof is finished"
        break
    if(new_line == "axioms"):
        print_axioms(type_of_logic)
        continue
    formula = Formula(new_line)
    if(not is_valid(formula)):
        print "invalid formula"
        continue
    result = is_correct(formula, formulas, type_of_logic)
    if(result):
        formulas.append(formula)
    else:
        print "incorrect formula"

print
for formula in formulas: print(formula.string_version)

#Two example proofs:
#(x->(x->x)->x)->(x->(x->x))->x->x
#w->(w->w)->w
#(w->(w->w))->w->w
#w->w->w
#w->(w->w_
#w->w
#
#
#!!A
#
#!!A->A
#A

