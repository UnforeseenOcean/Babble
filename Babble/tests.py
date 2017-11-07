import unittest

class Test_tests(unittest.TestCase):
    def test_parse(self):
        program = "(begin (define r 10) (* pi (* r r)))"

        parse(program)

    #def test_eval(self):
    #    program = "(begin (define r 10) (* pi (* r r)))"

    #    parse(program)

    #    eval(parse(program)) # test what's printed out with 314.1592653589793

if __name__ == '__main__':
    unittest.main()
