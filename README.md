
# Language specifications
1. Explcit Semicolon terminated lines.
2. Explicit denotion of new Scope using Braces.
3. Static typing against standard dynamic typing.
4. Seperate Type checking parser(Type check before execution).

## Data Types

`Int`: Integer data type representing whole numbers

`Float`: Floating point numbers stored in form of Fractions $(\dfrac{p}{q}:p, q \in Q)$.

`Bool`: Boolean data types representing `{'true', 'false'}`

`Str`: String datatype representing strings `{"Manish", "Sriman", "Siva", "Rajesh", "Balu"}`

`nil`: A datatype representing `None` type

---
## Operators

### Binary Arithematic Operators

1.  `+` : Addition operator 
    
    **Operands**: a (`Int|Float`), b (`Int|Float`)

    **Returns**: (`Float|Int`) - Sum of `Numbers` a and b

    The operator takes care of implicit `Int` to `Float` conversions in case of Numbers
    $$Int+Int \rightarrow Int$$
    $$Float+(Int|Float) \rightarrow Float$$
    $$(Float|Int)+Float \rightarrow Float$$

2.  `-` : Subtraction operator
    
    **Operands**: a (`Int|Float`), b (`Int|Float`)

    **Returns**: (`Float|Int`) - Difference of `Numbers` a and b

    The operator takes care of implicit `Int` to `Float` conversions in case of Numbers
    $$Int-Int \rightarrow Int$$
    $$Float-(Int|Float) \rightarrow Float$$
    $$(Float|Int)-Float \rightarrow Float$$


3.  `*` : Multiplication operator  
    
    **Operands**: a (`Int|Float`), b (`Int|Float`)

    **Returns**: (`Float|Int`) - Product of `Numbers` a and b

    The operator takes care of implicit `Int` to `Float` conversions in case of Numbers
    $$Int\*Int \rightarrow Int$$
    $$Float\*(Int|Float) \rightarrow Float$$
    $$(Float|Int)\*Float \rightarrow Float$$

4.  `/` : Division operator 

    **Operands**: a (`Int|Float`), b (`Int|Float`), $b \neq 0$

    **Returns**: (`Float`) - $\dfrac{a}{b(\neq0)} $

    $$(Float|Int)/(Float|Int) \rightarrow Float$$

    *Note:* The operator takes care of the Zero Division Error(**Runtime**) 

5.  `//` : Integer Division operator 

    **Operands**: a (`Int|Float`), b (`Int|Float`), $b \neq 0 $

    **Returns**: (`Int`) - $\lfloor\dfrac{a}{b(\neq 0)}\rfloor$

    $$(Float|Int)//(Float|Int) \rightarrow Int$$

    *Note:* The operator takes care of the Zero Division Error(**Runtime**) 

6.  `%` : Modulo operator 

    **Operands**: a (`Int`), b (`Int`), $b \ne 0$

    **Returns**: (`Int`) - a MOD b($\ne0$)

    $$(Int)\%(Int) \rightarrow Int$$
    *Note:* The operator takes care of the Zero Division Error(**Runtime**) 

### Binary Bitwise Operators

7.  `<<` : Left shift operator 

    **Operands**: a (`Int`), b (`Int`), $b \in I ^ {+}$

    **Returns**: (`Int`) - a << b $(\in I ^ {+})$

    $$(Int)<<(Int) \rightarrow Int$$
    *Note:* The operator takes care of the Negative left operand by raising exception.

8.  `>>` : Right shift operator 

    **Operands**: a (`Int`), b (`Int`), $b \in I ^ {+}$

    **Returns**: (`Int`) - a >> b $(\in I ^ {+})$

    $$(Int)>>(Int) \rightarrow Int$$
    *Note:* The operator takes care of the Negative left operand by raising exception.

9.  `&` : Bitwise AND operator 

    **Operands**: a (`Int`), b (`Int`)

    **Returns**: (`Int`) - a AND b

    $$(Int) \And (Int) \rightarrow Int$$

10. `|` : Bitwise OR operator 

    **Operands**: a (`Int`), b (`Int`)

    **Returns**: (`Int`) - a OR b

    $$(Int)|(Int) \rightarrow Int$$

### Binary Comparision Operators

11. `<=` : Less than or equals operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a $\leq $ b

    $$(Type) <= (Type) \rightarrow Bool$$

12. `<` : Less than operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a < b

    $$(Type) < (Type) \rightarrow Bool$$

13. `>` : Greater than operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a > b

    $$(Type) > (Type) \rightarrow Bool$$

14. `>=` : Greater than or equals operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a $\geq $ b

    $$(Type) >= (Type) \rightarrow Bool$$

15. `==` : Equality operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a = b

    $$(Type) == (Type) \rightarrow Bool$$

16. `!=` : not equals operator 

    *Note:* Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`Bool`) - a $\neq$ b

    $$(Type) != (Type) \rightarrow Bool$$

### Binary Logical Operators

17. `&&` : Logical AND operator 

    **Operands**: a (`Bool`), b (`Bool`)

    **Returns**: (`Bool`) - `true` if both *a* and *b* are true

    $$(Bool) \And\And (Bool) \rightarrow Bool$$

18. `||` : Logical OR operator 

    **Operands**: a (`Bool`), b (`Bool`)

    **Returns**: (`Bool`) - `true` if either *a* or *b* is true

    $$(Bool) || (Bool) \rightarrow Bool$$

### Unary arithematic Operators

19. `-` : arithematic negation operator

    **Operands**: a (`Float|Int`)

    **Returns**: (`Float|Int`) - $-a$

    $$(Float) \rightarrow Float$$
    $$(Int) \rightarrow Int$$

### Unary Logical Operators

20. `-` : Logical negation operator

    **Operands**: a (`Bool`)

    **Returns**: (`Bool`) - NOT a 

    $$(Bool) \rightarrow Bool$$
 
### Assignment Operator

21.  `=` : Assignment operator
    
**Operands**: x (`Variable`), a (`AST`)

**Returns**: (`Float|Int|Bool|Str`) - returns the evaluated value of a

$$Variable=Int  \rightarrow  Int$$

$$Variable=Float  \rightarrow  Float$$

$$Variable=Bool  \rightarrow  Bool$$

$$Variable=Str  \rightarrow  Str$$

## Features 

1. **A print operation that prints values to screen(`PRINT()`)**

   `PRINT()` is used to perform the operation of printing the values to the screen. 
   
   The input to the print function is a list of AST's, we first evaluate the AST and print the value to the screen.
   
   We could also specify the delimiter between the printing values using the keyword `end` , the default delimiter is `" "`.
   
   Suppose we want to put `comma` as the delimiter then we put, `end=", "` 
   
 
2. **Sequential implementation(`Seq()`)**

   We provide the sequence of expressions which we want to execute, as a list. 
   
   Then evaluate each expression and return the value of the last evaluated expression.
   
3. **Truthy(`truthy()`)**

   `truthy(arg)` checks its argument `arg` and classify whether it corresponds to `True` or `False` 
   
   The values that corresponds to False are: 
   
   `Int(0)`, `Float(0)`, `empty dictionary`, `empty string`, `nil`, `False`, `empty list`
   
   Every value other than these correspond to `True`.
   
   
## Operator Precedence

The Operator Precedence from lowest to highest.
|&nbsp;&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Operators&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;Associates&nbsp;&nbsp;&nbsp;&nbsp; 
|------------|----------------|----
|assignment    |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Right
|logicalOr    |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\|\||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|logicalAnd    |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\&\&|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|Equality    |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;==&nbsp;&nbsp;&nbsp;!= |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|Comparison|&nbsp;&nbsp;>&nbsp;&nbsp;&nbsp;>=&nbsp;&nbsp;&nbsp;<&nbsp;&nbsp;&nbsp;<=|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|add|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;+|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|mult|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;*|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|unary|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;-|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Right
## CFG of the parser
**The Context Free Grammar of our language:**
$$~program  \rightarrow  (declaration)^*~~ EOF$$
$$declaration  \rightarrow  vardec  ~~ | ~~ statement$$
$$statement  \rightarrow  expression ~ Statement ~ | ~ print ~ Statement ~ | ~ if ~ Statement ~ | ~ while ~ Statement ~ | ~ for ~ Statement$$
$$vardec \rightarrow  "var" ~~ identifier ~~ ( ~ "=" ~ expression) ~ ? ~ ";"$$
$$while ~ Statement  \rightarrow  "while" ~~ "(" ~~ expression ~~ ")" ~~ "\{" ~~ declaration ~~ "\}" ~~ $$
$$if ~ Statement  \rightarrow  "if" ~~ "(" ~~ expression ~~ ")" ~~ "\{" ~~ declaration ~~ "\}" ~~ ("else" ~~ "\{" ~~ declaration ~~ "\}")? ~~ $$
$$print ~ Statement  \rightarrow  "zout" ~ "("~ expression ~ ")" ~ ";"$$
$$for ~ Statement  \rightarrow  "for" ~ "("( ~ vardec ~ | ~ expression ~ Statement ~ | ~ ";") ~~ expression? ~~ ";" ~ expression? ~ ")" ~statement$$
$$expression ~ Statement  \rightarrow  expression ~~ ";"$$
$$expression \rightarrow  assignment$$
$$assignment  \rightarrow  identifier "="assignment ~~~ | ~~~ logicOr ~~~ $$
$$logicOr \rightarrow  logicAnd ~~ (~~ "||" ~~ logicAnd ~~ )^* ~~ $$
$$logicAnd \rightarrow  equality ~~ ( ~~ "\And\And" ~~ equality ~~ )^* ~~ $$
$$equality  \rightarrow  comparision ~~ ( ~ ( ~ "!=" ~ | ~ "==" ~ ) ~~ comparision)^* ~~ $$
$$comparision  \rightarrow  add(~ (~ ">"~ |~ ">="~ |~ "<"~ |~ "<="~ )~ add~ )^* ~~ $$
$$add  \rightarrow mult( ~ ("-" ~ | ~ "+") ~ mult)^* ~~ $$
$$mult \rightarrow unary( ~ ("/" ~ | ~ "\*") ~ unary)^* ~~ $$
$$unary  \rightarrow  ("!" ~ | ~ "-") ~ unary ~~ |~~ atom$$
$$atom  \rightarrow  Identifier ~~ | ~~ Int ~~ | ~~ Bool ~~ | ~~ String ~~ | ~~ Float ~~ | ~~ nil ~~ | ~~ "(" ~ expression ~ ")"$$



## Scoping
1. Referencing a variable in its initializer is not an error, but it resolves to variable in previous scope.

## Typechecking

1. It checks the features of every data type(Int, Float, Bool, Variable, Str, nil) is assigned correctly or not as it was mentioned earlier of which type they are.

2. For now, We are checking all the features like Binary Operators, Unary Operator, Variables, Declare, Slice, While loop, If loop,
   sequence, PRINT. We will add as the features come in.

3. As the while loop, if loop, PRINT are statements we returned 'nil'.
4. The slice returns str.
5. For checking the data type we are typechecking the value which is assigned to it. The variable datatype is Int if it is assigned Integer,
    and it is Str if the variable is assigned String.

To be done:
1. refactor code    
2. Comment code
3. Implement errors
4. Complete the test files
5. Implement the resolver pass
6. Update the for loop for scopes
7. Fixed the assignment typechecking bug
8. PRINT test cases not fixed