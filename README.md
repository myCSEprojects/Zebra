
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

## Statically typed list

List contains elements of only single specified type.  
Can handle nested lists.  
The list operations supported are: `list_append`, `list_remove`, `list_insert`, `Slice`, `list_len`    

language syntax:   

`list_append` : `append(element, list_name);`  
`list_remove` : `remove(index, list_name);`  
`list_insert` : `insert(index, element, list_name);`  
`Slice` : `list_name[start:end]`  
`list_len` : `length(list_name)`

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

$$
\begin{align}
~program  &\rightarrow  (declaration)^*~~ EOF \\
declaration  &\rightarrow  vardec  ~~ | ~~ statement \\
statement  &\rightarrow  expression ~ Statement ~ | ~ print ~ Statement ~ | ~ if ~ Statement ~ | ~ while ~ Statement ~ \\
&| ~ for ~ Statement ~ | ~ block ~ | ~ list ~ remove ~ statement ~ | ~ list ~ append~statement ~ | ~ list ~ insert ~ statement \\
vardec &\rightarrow  ('const')? ~~ ('int'~|~'float'~|~'boolean'~|~'string') ~~ identifier ~~ ( ~ '=' ~ expression)? ~ ';' \\
&|~~ ('list')* ~~ ('int' ~ | ~ 'float' ~ | ~ 'boolean'~|~'string') ~~ identifier ~~ ( ~ '=' ~ expression) ~ ? ~ ';' \\
while~Statement  &\rightarrow  'while' ~~ '(' ~~ expression ~~ ')' ~~ ' \\{ ' ~~ declaration ~~ ' \\} ' ~~  \\
block ~ &\rightarrow '\\{' ~~ (declaration)^* ~~ '\\}'  \\
if ~ Statement  &\rightarrow  'if' ~~ '(' ~~ expression ~~ ')' ~~ '\\{' ~~ declaration ~~ '\\}' ~~ ('else' ~~ ((if~statement )~|~'\\{' ~~ declaration ~~ '\\}'))? ~~  \\
print ~ Statement  &\rightarrow  'zout' ~ '('~ expression ~ ')' ~ ';' \\
for ~ Statement  &\rightarrow  'for' ~~ '(' ~~ ( ~ vardec ~ | ~ expression ~ Statement ~ | ~ ';') ~~ expression? ~~ ';' ~ expression? ~ ')' ~statement \\
list ~ remove ~ statement & \rightarrow 'remove' ~~ '(' ~~ expression ~~ ',' ~~ Indentifier ~~ ')' ~~ ';' \\
list ~ append ~ statement & \rightarrow 'append' ~~ '(' ~~ expression ~~ ',' ~~ Indentifier ~~ ')' ~~ ';' \\
list ~ insert ~ statement & \rightarrow 'insert' ~~ '(' ~~ expression ~~ ',' ~~ expression ~~ ',' ~~ Indentifier ~~ ')' ~~ ';' \\
expression ~ Statement  &\rightarrow  expression ~~ ';' \\
expression &\rightarrow  assignment \\
assignment  &\rightarrow  identifier '='assignment ~~~ | ~~~ logicOr ~~~  \\
logicOr &\rightarrow  logicAnd ~~ (~~ '||' ~~ logicAnd ~~ )^* ~~  \\
logicAnd &\rightarrow  equality ~~ ( ~~ '\And\And' ~~ equality ~~ )^* ~~  \\
equality  &\rightarrow  comparision ~~ ( ~ ( ~ '!=' ~ | ~ '==' ~ ) ~~ comparision)^* ~~  \\
comparision  &\rightarrow  add( ~ ( ~ '>' ~ | ~ '>=' ~ | ~ '<' ~ | ~ '<=' ~ ) ~ add ~ )^* ~~  \\
add  &\rightarrow mult ~~ ( ~ ('-' ~ | ~ '+') ~ mult)^* ~~  \\
mult &\rightarrow unary ~~ ( ~ ('/' ~ | ~ '*' ~ | ~ '\\%' ) ~ unary)^\* \\
unary  &\rightarrow  ('!' ~ | ~ '-') ~ unary ~~ | ~~ atom ~~ | ~~ list ~ length\\
list ~ length & \rightarrow 'length' ~~ '(' ~~ Indentifier ~~ ')' \\
atom  &\rightarrow  Identifier ~~ | Identifier ~~ '(' ~~ (expression) ~~ * ~~ expression ~~ ')' ~~ \\
&|~~ Int ~~ | ~~ Bool ~~ | ~~ String ~~ | ~~ Float ~~ | ~~ nil ~~ | ~~ '(' ~ expression ~ ')' \\
\end{align}
$$


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

To be done and Updates:
1. refactor code    
2. Comment code
4. Complete the test files
5. Implement the resolver pass
6. Update the for loop for scopes
7. Fixed the assignment typechecking bug
8. PRINT test cases not fixed
9. Adding a synchronize method to the parser class.
10. Add Line number feature to the tokens
11. Open an issue for << operator
12. UNOP add exceptions
13. Removed the boolean typechecking in IF 
14. Removed the variable accessing errors in evaluation -> yet to add a resolver pass(but present in type checking)
15. Replacing the var in Declare class to a identifier token(Helps in raising the error)
16. Think of way to introduce tokens in Slice function
17. sep and end features to add in parser of zout
18. string_concat parser
19. line numbers for errors
# Errors

We report the Error type, its message and its line number.

We also perform error recovery in case of parsing and lexing to catch as many errors as possible.

## During parsing
We use panic mode error recovery for errors during parse errors.

When we encounter an error inside parsing we report the error, set the `isError` flag to `True` and synchronize the parser to the next statement or the end of file.

This prevents cascading of errors and is fast enough.

## Runtime Errors

We raise the Runtime errors and exit the program.
> **_Note_**: Add tokens to BINOP, UNOP, Declare, Slice
