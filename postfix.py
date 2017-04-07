# Copyright (C) 2016 Mario Iannotta <info@marioiannotta.com>
#!/usr/bin/python

import sys

import math
import string
import copy
import curses

operators = {
    "+": 2,
    "-": 2,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
    "root": 2,
    "^": 2,
    "log": 2,
    "sqrt": 1,
    "fact": 1,
    "ln": 1,
    "Log": 1,
    "abs": 1,
    "sin": 1,
    "cos": 1,
    "tan": 1
}

def is_float(x):

    try:
        a = float(x)

    except ValueError:
        return False

    else:
        return True

def is_int(x):

    try:
        a = float(x)
        b = int(a)

    except ValueError:
        return False

    else:
        return a == b

def leaf(item):
    return [item, [], []]

def get_token_list(string):
    return list(string.split(" "))

def is_token_a_number(token): # controlla se il token e float, int, e, pi
    return is_int(token) or is_float(token) or token == "e" or token == "pi"

def is_a_binary_operator(token):
    return operators[token] == 2

def is_an_unary_operator(token):
    return operators[token] == 1

def counter_decrease_for_token(token):

    if is_token_a_number(token):
        return 0

    elif is_a_binary_operator(token):
        return -2

    elif is_an_unary_operator(token):
        return -1

    return None

def is_token_list_valid(token_list):

    counter = 0

    if not token_list:
        return True

    for token in token_list:

        if not is_token_a_number(token) and not is_an_operator(token):
            return False

        counter += counter_decrease_for_token(token)

        if counter < 0:
            return None

        counter += 1

    return counter == 1

def is_an_operator(item):

    operators_keys = operators.keys()

    if item in operators_keys:
        return True

    return False

def evaluate_item(item):

    if item == "pi":
        return math.pi

    elif item == "e":
        return math.e

    else:
        return float(item)

def evaluate_unary_expression(fx, a):

    a = evaluate_item(a)

    if fx == "sqrt":

        if a < 0:
            return None

        return math.sqrt(a)

    elif fx == "fact":

        return math.factorial(a)

    elif fx == "ln":

        if a <= 0:
            return None

        return math.log(a)

    elif fx == "Log":

        if a <= 0:
            return None

        return math.log10(a)

    elif fx == "abs":

        return abs(a)

    elif fx == "sin":

        return math.sin(a)

    elif fx == "cos":

        return math.cos(a)

    elif fx == "tan":

        return math.tan(a)

    else:

        print("Unexpected operator")
        return None

def evaluate_binary_expression(fx, a, b):

    a = evaluate_item(a)
    b = evaluate_item(b)

    if fx == "+":

        return a + b

    elif fx == "-":

        return a - b

    elif fx == "*":

        return a * b

    elif fx == "/":

        if b != 0:
            return a / b
        else:
            return None

    elif fx == "//":

        if b == 0:
            return None

        return a // b

    elif fx == "%":

        if b == 0:
            return None

        return a % b

    elif fx == "root":

        if a < 0:
            return None

        return a**(1/b)

    elif fx == "^":

        return a**b

    elif fx == "log":

        if a <= 0:
            return None

        return math.log(b, a)

    else:

        print("Unexpected operator")
        return None

def get_syntax_tree(token_list):

    tree = []

    for token in token_list:

        if is_an_operator(token):

            dx = []
            sx = []

            if is_an_unary_operator(token):
                dx = tree.pop()

            elif is_a_binary_operator(token):
                dx = tree.pop()
                sx = tree.pop()

            tree.append([token, dx, sx])

        elif is_token_a_number(token):
            tree.append(leaf(token))

    return tree[0]

def is_a_leaf(item):

    if len(item) != 3:
        return False

    if len(item[1]) == 3 and len(item[2]) == 3:
        return not is_an_operator(item[1][0]) and not is_an_operator(item[2][0])

    else:
        return not is_an_operator(item[1][0])

def print_tree(tree):

    print(get_tree_description(copy.deepcopy(tree)))

def get_tree_description(tree):

    if not is_an_operator(tree[0]):
        return tree[0]

    if is_a_leaf(tree):
        return get_leaf_description(tree)

    else:
        if len(tree[1]) > 0:
            tree[1] = leaf(get_tree_description(tree[1]))

        if len(tree[2]) > 0:
            tree[2] = leaf(get_tree_description(tree[2]))

    return get_tree_description(tree)

def get_leaf_description(leaf):

    if len(leaf) != 3:
        return ""

    if is_a_binary_operator(leaf[0]) and not is_an_operator(leaf[1][0]) and not is_an_operator(leaf[2][0]):

        if leaf[0] == 'log' or leaf[0] == 'root':
            return  leaf[0] + "(" + leaf[2][0] + "," + leaf[1][0] + ")"
        else:
            return "(" + leaf[2][0] + leaf[0] + leaf[1][0] + ")"

    elif is_an_unary_operator(leaf[0]) and not is_an_operator(leaf[1][0]):
        return leaf[0] + "(" + leaf[1][0] + ")"

def evaluate_tree(tree):
    return evaluate_tree_rc(copy.deepcopy(tree))[0]

def evaluate_tree_rc(tree):

    if not is_an_operator(tree[0]):
        return leaf(tree[0])

    if is_a_leaf(tree):
        return leaf(evaluate_leaf(tree))
    else:
        if len(tree[1]) > 0:
            tree[1] = evaluate_tree_rc(tree[1])
        if len(tree[2]) > 0:
            tree[2] = evaluate_tree_rc(tree[2])

    return evaluate_tree_rc(tree)

def evaluate_leaf(leaf):

    if len(leaf) != 3:
        return ""

    if is_a_binary_operator(leaf[0]) and not is_an_operator(leaf[1][0]) and not is_an_operator(leaf[2][0]):
        return evaluate_binary_expression(leaf[0], leaf[2][0], leaf[1][0])

    elif is_an_unary_operator(leaf[0]) and not is_an_operator(leaf[1][0]):
        return evaluate_unary_expression(leaf[0], leaf[1][0])

def get_depth(tree):

    if len(tree) <= 2:
        return 0

    return max(get_depth(tree[1]), get_depth(tree[2])) + 1

def print_tree_structure(leaf):

    tree_depth = get_depth(tree)
    depth_map = get_depth_map(tree)

    tree_structure = ""

    for i in range(0, tree_depth):

        n = 2**i
        for j in range(0, n):

            number_empty_spaces = 2**(tree_depth-i)

            if j == 0:
                number_empty_spaces /= 2

            next_string = ""
            if depth_map[i][n-j-1] != []:
                if is_an_operator(depth_map[i]):
                    next_string = depth_map[i]
                else:
                    next_string = depth_map[i][n-j-1]

            tree_structure += get_empty_spaces(number_empty_spaces, len(next_string))+next_string

        tree_structure += "\n\n"

    print(tree_structure)

def get_depth_map(tree):

    depth = get_depth(tree)
    depth_indexes_list = get_depth_indexes_list(tree)
    depth_map = []

    if depth > 0:
        depth_map.append(tree[0])

    if depth > 1:
        depth_map.append(get_children(tree))

    for depth_indexes in depth_indexes_list:

        children = []

        for depth_index in depth_indexes:

            children += get_children_with_indexes(tree, depth_index)

        depth_map.append(children)

    return depth_map

def get_depth_indexes_list(tree):
    
    depth = get_depth(tree)
    depth_indexes_list = [[[]]]
    
    for i in range(1, depth - 1):
        
        prev_items = depth_indexes_list[i-1]
        
        if len(prev_items) == 0:
            
            depth_indexes_list.append([[1], [2]])
    
        else:

            tmp_list = []
            for j in range(0, len(prev_items)):
                
                left_indexes_list = prev_items[j] + [1]
                right_indexes_list = prev_items[j] + [2]
                
                tmp_list.append(left_indexes_list)
                tmp_list.append(right_indexes_list)

            depth_indexes_list.append(tmp_list)

    return depth_indexes_list

def get_children_with_indexes(tree, indexes):

    for index in indexes:
        if index < len(tree):
            tree = tree[index]

    if len(tree) == 3:
        return get_children(tree[1]) + get_children(tree[2])

    return [[], [], [], []]

def get_children(tree):

    children = []

    if len(tree) == 0:
        children = [[], []]

    else:

        if len(tree) >= 1 and len(tree[1]) > 0:
            children.append(tree[1][0])
        else:
            children.append([])

        if len(tree) >= 2 and len(tree[2]) > 0:
            children.append(tree[2][0])
        else:
            children.append([])

    return children

def get_empty_spaces(number, next_string_lenght):

    empty_spaces = ""
    for i in range(0, number - next_string_lenght):
        empty_spaces += " "

    return empty_spaces

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("\nInvalid syntax - usage: python ./postfix.py \"your expression here\"\n")
    
    else:
    
        str_expr = sys.argv[1]

        token_list = get_token_list(str_expr)
        is_valid = is_token_list_valid(token_list)

        print("\nEvaluating >> " + str_expr + "\n")

        if is_valid:
            print("Is valid")
        else:
            print("Is not valid.\n")
            raise SystemExit, 0

        tree = get_syntax_tree(token_list)

        print("\nraw tree:")
        print(tree)

        print("\nformatted tree:")
        print_tree(tree)

        print("\nresult:")
        print(evaluate_tree(tree))

        print("\ndepth:")
        print(get_depth(tree))

        print("\ntree structure")
        print_tree_structure(tree)

        print("\n")
