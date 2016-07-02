#Token Types
INTEGER  = 'INTEGER'
PLUS     = 'PLUS'
EOF      = 'EOF'
SUBTRACT = 'SUBTRACT'
MULT     = 'MULT'
DIV      = 'DIV'

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

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def integer(self):
        digit = ""
        while self.current_char is not None and self.current_char.isdigit():
            digit += self.current_char
            self.advance()
        return int(digit)

    def get_next_token(self):
        text = self.text

        while self.current_char is not None:
    
            if self.pos > len(text) - 1:
                return Token(EOF, None)
        
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                digit = self.integer()
                self.advance()
                token = Token(INTEGER, int(digit))
                return token
        
            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.advance()
                return token
            if self.current_char == '-':
                token = Token(SUBTRACT, self.current_char)
                self.advance()
                return token
            if self.current_char == '*':
                token = Token(MULT, self.current_char)
                self.advance()
                return token
            if self.current_char == '/':
                token = Token(DIV, self.current_char)
                self.advance()
                return token

            self.error()
            
        return Token(EOF, None)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value
            
    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, SUBTRACT, MULT, DIV):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == SUBTRACT:
                self.eat(SUBTRACT)
                result = result - self.term()
            elif token.type == MULT:
                self.eat(MULT)
                result = result * self.term()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.term()
                
        return result

    def error(self):
        raise Exception('Error parsing input')
    
def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
