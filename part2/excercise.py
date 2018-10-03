
INTEGER, OP, EOF = 'INTEGER', 'OP', 'EOF'

class Token(object):
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token({type_}, {value})'.format(
            type_=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

# only parse
class Lexer(object):
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_token = None
        if len(self._text) > 0:
            self._current_char = self._text[self._pos]
        else:
            self._current_char = None
        self._queue = list()
 
    def _next(self):
        self._pos += 1
        if self._pos > len(self._text) -1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._next()

    def _integer(self):
        result = ''
        while self._current_char is not None and self._current_char.isdigit():
            result += self._current_char
            self._next()
        return int(result)

    def _is_operator(self, char):
        if char in ['+', '-', '*', '/']:
            return True
        return False


    def _next_token(self):
        if self._current_char is None:
            return Token(EOF, None)

        if self._current_char.isspace():
            self._skip_whitespace()
            return self._next_token()

        if self._current_char.isdigit():
            return Token(INTEGER, self._integer())

        # parse operator
        if self._is_operator(self._current_char):
            token = Token(OP, self._current_char)
            self._next()
            return token

        raise Exception("'{text}' is not accepted value".format(text=self._current_char))

    def scan(self):
        result = True

        if self._pos > len(self._text)-1:
            result = False

        self._current_token = self._next_token()

        return result

    def token(self):
        return self._current_token

# check token type and calculate
class Interpreter(object):
    def __init__(self, text):
        self._lexer = Lexer(text)
        self._require_type = INTEGER
        self._queue = list()

    def check(self, token_type):
        if self._lexer.token().type != token_type:
            return False

        return True

    def current_token(self):
        return self._lexer.token()

    def interpret(self):
        """interpret => INTEGER PLUS INTEGER"""
        #self._current_token = self.get_next_token()
        tokens = list()
        result = 0

        if self._lexer.scan() and self.check(INTEGER):
            result = self.current_token().value
        else:
            raise Exception("firt value should be integer")

        while self._lexer.scan() and self.current_token().type in [OP]:
            token = self.current_token()
            if self._lexer.scan() and self.check(INTEGER):
                if token.value == "+":
                    result += self.current_token().value
                elif token.value == "-":
                    result -= self.current_token().value
            else:
                raise Exception("opration is last value")

        return result


def main():
    while True:
        try:
            text = raw_input('calc> ')
            if text == '':
                continue
            if text == 'exit':
                print 'interpreter terminated'
                break
        except EOFError:
            break
        if not text:
            continue

        try:
            interpreter = Interpreter(text)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print e

if __name__ == '__main__':
    main()

# problem: '3+3j' also works
