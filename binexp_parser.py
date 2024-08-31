#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])


class BinOpAstTester(unittest.TestCase):
    tests = [osjoin('testbench','arith_id'),osjoin('testbench','mult_id'), osjoin('testbench','combined')]

    def test_all(self):
        for all_tests in self.tests:
            ins = osjoin(all_tests, 'inputs')
            outs = osjoin(all_tests,'outputs')

            for fname in os.listdir(ins):
                input = osjoin(ins,fname)
                output = osjoin(outs,fname)

                with open(input) as f:
                    inp = f.read().split()
                with open(output) as f:
                    expected = f.read()
                with self.subTest(msg=f"Testing {fname}", inp=inp, expected=expected):
                    t = BinOpAst([i for i in inp])
                    t.simplify_binops()
                    out = t.prefix_str()
                    self.assertEqual(out, expected)


class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """

    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """

        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  ' * indent
        left = '\n  ' + ilvl + self.left.__str__(indent + 1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent + 1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """

        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'

    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        if self.right:
            if self.type == NodeType.operator:
                if self.right.val == '0':
                    self.val = self.left.val
                    self.type = NodeType.number
                    return self
                elif self.right.type == NodeType.number:
                    if self.left.val == '0':
                        self.val = self.right.val
                        self.type = NodeType.number
                        return self
                else:
                    return self.right.additive_identity()
        else:
            return

    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        if self.right:
            if self.type == NodeType.operator:
                if self.right.val == '1':
                    self.val = self.left.val
                    self.type = NodeType.number
                    return self
                elif self.right.type == NodeType.number:
                    if self.left.val == '1':
                        self.val = self.right.val
                        self.type = NodeType.number
                        return self
                else:
                    return self.right.multiplicative_identity()
        else:
            return

    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        # Optionally, IMPLEMENT ME! (I'm pretty easy)
        pass

    def constant_fold(self):
        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """
        # Optionally, IMPLEMENT ME! This is a bit more challenging. 
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()
        self.constant_fold()


if __name__ == "__main__":
    unittest.main()
    #test_str = "+ 2 * 5 + 7 * 7 1".split()
    #print(f"Input: {test_str}")
    #test = BinOpAst(test_str)
    #print(test)
    #print()
    #test.simplify_binops()
    #print(f"Output: {test.prefix_str()}")
