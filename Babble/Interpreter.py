import json
import httplib2
import environ

def connect_to_service():
    # read from config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # get global location
    print(config['babble_home_url'])

    symbols_url = 'symbols/'

    httplib2.debuglevel = 1
    h = httplib2.Http('.cache')
    response, content = h.request(config['babble_home_url'] + symbols_url)
    print(dict(response.items()))  
    print(content)  


def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float

def eval(x, env = environ.standard_env()):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):      # variable reference
        return env[x]
    elif not isinstance(x, List):  # constant literal
        return x                
    elif x[0] == 'if':             # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # definition
        (_, var, exp) = x
        env[var] = eval(exp, env)
    else:                          # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

#program = "(begin (define r 10) (* pi (* r r)))"
#tokens = tokenize(program)
#print(tokens)

eval(parse("(define r 10)"))
print(eval(parse("(* pi (* r r))")))

