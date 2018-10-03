
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

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

    def error(self):
        raise Exception('Error input parsing')

    def _next_token(self):
        text = self._text

        if self._pos > len(text)-1:
            return Token(EOF, None)

        current_char = text[self._pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self._pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self._pos += 1
            return token

        self.error()

    def scan(self):
        text = self._text
        result = True

        if self._pos > len(text)-1:
            result = False

        self._current_token = self._next_token()

        return result

    def token(self):
        return self._current_token

# check token type and calculate
class Interpreter(object):
    def __init__(self, text):
        self._lexer = Lexer(text)

    def eat(self, token_type):
        try:
            if self._lexer.scan():
                if self._lexer.token().type == token_type:
                    return self._lexer.token()
                else:
                    raise Exception('Error input parsing')
        except Exception as e:
            raise e

    def interpret(self):
        """interpret => INTEGER PLUS INTEGER"""
        #self._current_token = self.get_next_token()

        try:
            left = self.eat(INTEGER)

            op = self.eat(PLUS)

            right = self.eat(INTEGER)
        except Exception as e:
            raise e

        result = left.value + right.value
        return result

def main():
    while True:
        try:
            text = raw_input('calc> ')
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
