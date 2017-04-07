# Postfix expression evaluator
Evaluate postfix expression with Python.

# What is a postfix expression?
tl;dr:
Instead of write (3 + 4) * 5 you write 3 4 + 5 *.

From wikipedia: _"A **postfix expression** AKA **reverse polish expression** is a mathematical notation in which every operator follows all of its operands, in contrast to Polish notation (PN), which puts the operator before its operands."_ 
[You can read more about it here here](https://en.wikipedia.org/wiki/Reverse_Polish_notation).

# Why
A postfix expression is easier to evaluate than a standard one because you haven't to consider parenthesis.

# How does the script works?
For a given string rappresenting a postfix expression, the script will calculate 
- the validity (if the expression is properly formatted)
- the raw tree
- the formatted tree
- the expression result
- the tree depth
- a visual rappresentation of the expression

# Example

Run the script with 
```
python ./postfix.py
```

The result should look like this
```
Evaluating >> 1 ln 2 + 3 * 4 sqrt 5 + cos - 6 4 * ln sqrt 4 + +

Is valid

raw tree:
`['+', ['+', ['4', [], []], ['sqrt', ['ln', ['*', ['4', [], []], ['6', [], []]], []], []]], ['-', ['cos', ['+', ['5', [], []], ['sqrt', ['4', [], []], []]], []], ['*', ['3', [], []], ['+', ['2', [], []], ['ln', ['1', [], []], []]]]]]`

formatted tree:
((((ln(1)+2)*3)-cos((sqrt(4)+5)))+(sqrt(ln((6*4)))+4))

result:
11.0288074333

depth:
6

tree structure             
                                +

               -                               +

       *             cos            sqrt               4

   +       3               +              ln

ln   2                sqrt   5               *

  1                       4                 6  4
  ```

# PS
This script is the very first thing I wrote with Python so pull requests are very welcome :)

# Info
If you like this git you can follow me here or on twitter [@MarioIannotta](http://www.twitter.com/marioiannotta)
