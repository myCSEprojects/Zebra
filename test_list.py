from sim import *
from typechecking import typecheck
def test():
    x = Identifier(4, "x")
    if (evaluate(Seq([Declare(x, zArray(Int, [Int(1)]),zArray, False), array_append(Int(2), x), BinOp(Operator(0, "="),Variable('x'), Variable('x'))]))).elements[1] != Int(2):
        print("Basic evaluation of array_append failed")
        return -1
    if (evaluate(Seq([Declare(x, zArray(Int, [Int(1)]),zArray, False), array_append(Int(2), x), array_remove(Int(1),x)]))) != Int(2):
        print("Basic evaluation of array_remove failed")
        return -1
    if (evaluate(Seq([Declare(x, zArray(Int, [Int(1)]),zArray, False), array_append(Int(2), x), array_len(x)]))) != Int(2):
        print("Basic evaluation of array_len failed")
        return -1
    if (evaluate(Seq([Declare(x, zArray(Str, [Str("hi")]),zArray, False), array_insert(Int(0), Str("hello"),x), array_len(x)]))) != Int(2):
        print("Basic evaluation of array_insert failed")
        return -1
    if (evaluate(Seq([Declare(x, zArray(Int, [Int(1), Int(2),Int(3)]),zArray, False), array_append(Int(100), x), Slice(Variable("x"),Int(1),Int(3))]))).elements[0] != Int(2):
        print("Basic evaluation of array_slice failed")
        return -1
    try:
        ast = Seq([Declare(x, zArray(Str, [Str("hi")]),zArray, False), array_insert(Int(0), Int(1000),x), array_len(x)])
        typecheck(ast)
        evaluate(ast)
        print("Typechecking of array insert failed")
        return -1
    except:
        print("Caught error")
    print("All test cases passed")
    return 0
if (__name__ == "__main__"):
    test()
