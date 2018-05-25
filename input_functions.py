import string


def validate(sentence):
    ops = ['|', '&', '>', '^', '~','=']
    chars = string.ascii_lowercase + string.ascii_uppercase + ''.join(list(map(str, range(10))))
    sentence = sentence.strip()
    # basic checks with whitespaces
    var = False
    last = ''
    for c in sentence:
        if c in chars:
            if last == ' ' and var is True:
                return False
            var = True
        elif c in ops:
            var = False
        elif c not in "() ":
            return False
        last = c
    #parentheeses, grammar
    parentheses = 0
    last = None
    sentence = "".join(sentence.split())
    for c in sentence:
        if c == '(':
            parentheses = parentheses + 1
            if last in [chars+')']:
                return False
            last = '('
        elif c == ')':
            parentheses = parentheses - 1
            if last in [str(ops)+'(']:
                return False
            last = ')'
        elif c in chars:
            if last == ')': return False
            if c.isnumeric():
                if last in [None, str(ops)+"()"]:
                    if c not in "01": return False
            last = c
        elif c in ops:
            if last in [None, str(ops)+"("] and c != '~': return False
            if last in [chars+")"] and c == '~': return False
            last = c
        if parentheses < 0: return False
    if last in ops: return False
    elif parentheses != 0: return False
    else: return sentence


def convert_to_rpn(sentence):
    ops = ['|', '&', '>', '^', '~','=']
    op_priorities = {'|': 1,'&': 2, '^': 1, '~': 3, '>': 0, '=': 0, '*': 2}
    chars = string.ascii_lowercase + string.ascii_uppercase + ''.join(list(map(str, range(10))))
    stack = []
    ready = []
    _vars = []
    var_buf = ''
    for c in sentence:
        if c in chars:
            var_buf += c
        else:
            if var_buf != '':
                if var_buf in "01":
                    ready.append(int(var_buf))
                else:
                    ready.append(var_buf)
                if var_buf not in _vars and var_buf not in "01":
                    _vars.append(var_buf)
                var_buf = ''
            if c in ops:
                while len(stack) > 0 and stack[len(stack)-1] in ops and op_priorities[stack[len(stack)-1]] >= op_priorities[c]:
                    ready.append(stack.pop())
                stack.append(c)
            elif c == '(': stack.append(c)
            elif c == ')':
                while stack[len(stack)-1] != '(':
                    ready.append(stack.pop())
                stack.pop()

    if var_buf != '':
        if var_buf not in _vars and var_buf not in "01":
            _vars.append(var_buf)
        if var_buf in "01":
            ready.append(int(var_buf))
        else:
            ready.append(var_buf)
    while len(stack) > 0:
        ready.append(stack.pop())
    return ready, _vars


def find_minterms(rpn, vars):
    from itertools import product
    combinations = list(product(range(2), repeat=len(vars)))
    table = []
    for i in range(0, len(combinations)):
        val = combinations[i]
        val_list = list(val)
        tmp_dict = dict(zip(vars,val_list))
        if evaluate_sentence(rpn,tmp_dict):
            result = 1
        else:
            result = 0
        table.append(result)
    return table


def evaluate_sentence(rpn, values):
    ops = ['|', '&', '>', '^', '~', '=']
    stack = []
    rpn = rpn[:]
    for elem in rpn:
        if elem in values.keys():
            rpn[rpn.index(elem)] = values[elem]
    for c in rpn:
        if c in ops and c != '~':
            x = stack.pop()
            y = stack.pop()
            if c == '|': stack.append(x or y)
            elif c == '&': stack.append(x and y)
            elif c == '^': stack.append(x ^ y)
            elif c == '>': stack.append((not y) or x)
            elif c == '=': stack.append(y == x)
        elif c == '~':
            x = stack.pop()
            stack.append(not x)
        else:
            stack.append(c)
    return stack.pop()
