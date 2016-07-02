#Token Types
INTEGER = 'INTEGER'
PLUS    = 'PLUS'
EOF     = 'EOF'
SUBTRACT = 'SUBTRACT'

class Token(object):
    def __init__(self, type, value):
        #Type is either: INTEGER, PLUS, EOF
        self.type = type
        #value is 0-9
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]
        
        while current_char == ' ':
            self.pos += 1
            current_char = text[self.pos]

        if current_char.isdigit():
            digit = ""
            while current_char.isdigit():
                digit += current_char
                
                if self.pos + 1 >= len(text):
                    break

                self.pos += 1
                current_char = text[self.pos]
                
            token = Token(INTEGER, int(digit))
            self.pos += 1
            return token
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        if current_char == '-':
            token = Token(SUBTRACT, current_char)
            self.pos += 1
            return token

        self.error()
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        if self.current_token.type == PLUS:
            op = self.current_token
            self.eat(PLUS)

        if self.current_token.type == SUBTRACT:
            op = self.current_token
            self.eat(SUBTRACT)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        if op.type == SUBTRACT:
            result = left.value - right.value
            
        return result
def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
