
INTEGER, OP, EOF, BRACKET_OPEN, BRACKET_CLOSE = 'INTEGER', 'OP', 'EOF', 'BRACKET_OPEN', 'BRACKET_CLOSE'

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


class Lexer(object):
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._current_token = None
        if len(self._text) > 0:
            self._current_char = self._text[self._pos]
        else:
            self._current_char = None

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

    def _is_operator(self):
        if self._current_char in ['+', '-', '*', '/']:
            return True
        return False

    def _is_bracket_open(self):
        if self._current_char == "(":
            return True
        return False

    def _is_bracket_close(self):
        if self._current_char == ")":
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
        if self._is_operator():
            token = Token(OP, self._current_char)
            self._next()
            return token

        # parse parenthese open
        if self._is_bracket_open():
            token = Token(BRACKET_OPEN, self._current_char)
            self._next()
            return token

        if self._is_bracket_close():
            token = Token(BRACKET_CLOSE, self._current_char)
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

    @property
    def current_token(self):
        return self._lexer.token()

    def eat(self, token_type):
        
        if self._lexer.token().type != token_type:
            raise Exception("token type not matching as expected")

        self._lexer.scan()

    def factor(self):
        """
        factor: BRACKET_OPEN{1} expr BRACKET_CLOSE{1}
        factor: INTEGER
        """
        if self.current_token.type == BRACKET_OPEN:
            self.eat(BRACKET_OPEN)
            value = self.expr()
            self.eat(BRACKET_CLOSE)
            return value
        else:
            value = self.current_token.value
            self.eat(INTEGER)
            return value

    def term(self):
        """
        term: factor ((MUL | DIV) factor)*
        """
        value = self.factor()
        while self.current_token.value in ['*', '/']:
            op = self.current_token.value
            self.eat(OP)
            if op == '*':
                value *= self.factor()
            elif op == '/':
                value /= self.factor()
        return value

    def expr(self):
        result = self.term()

        while self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.eat(OP)
            if op == '+':
                result += self.term()
            elif op == '-':
                result -= self.term()

        return result


    def interpret(self):
        """Aruthmetic expression parser / interpreter

        expr    : term ((PLUS | MINUS ) term)*
        term    : factor ((MUL | DIV ) factor)*
        factor  : BRACKET_OPEN{0,1} expr BRACKET_CLOSE{0,1}

        """
        try:
            self._lexer.scan()
            return self.expr()
        except Exception as e:
            raise e

        raise Exception("wrong syntax")


def main():
    while True:
        try:
            print "[info] interpreter starts. print type 'exit' to quit program"
            text = raw_input('calc> ')
            if text == 'exit':
                print '[info] interpreter terminated'
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
            print "[error]", e
            print "[info] print 'exit' to exit program"

if __name__ == '__main__':
    main()

