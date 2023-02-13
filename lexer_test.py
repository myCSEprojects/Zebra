from lexer import *

def test_lexer():
    def lex(stg):
        sm = Stream(stg, 0)

        l = Lexer(sm)
        while True:
            a = l.next_token()
            if (a==EOF()):
                break
            print(a) 

    print("a = 53.9124 hey <<< !===<~~66&&|||")
    lex("a = 53.9124 hey <<< !===<~~66&&|||")
    print()
    print("a==2<<<3")
    lex("a==2<<<3")
    print()
    print("<><><<==")
    lex("<><><<==")
    

test_lexer()