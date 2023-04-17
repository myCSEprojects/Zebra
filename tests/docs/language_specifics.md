# Language Specification
Zebra is a high-level programming language that emphasizes explicit scoping, static typing, and ease of use. It has a small set of data types and a concise set of operators. This document provides the specifications for the Zebra programming language.
<br>

## Basic Syntax
The basic syntax of Zebra includes semicolon terminated lines and explicit denotion of new scope using braces. This means that all statements end with a semicolon `;` and the code block enclosed in braces `{}` is used to denote a new scope.
<br>
>Zebra is a statically typed language, which means that variables must be explicitly typed and checked for correctness at compile-time. <br>

## Data Types

`int`: integer data type representing whole numbers

`float`: floating point numbers stored in form of Fractions $(\dfrac{p}{q}:p, q \in Q)$.

`boolean`: Boolean data types representing `{'true', 'false'}`

`Str`: String datatype representing strings `{"Manish", "Sriman", "Siva", "Rajesh", "Balu"}`

`nil`: A datatype representing `None` type

---

## Operators

### Binary Arithematic Operators

1.  `+` : Addition operator

    **Operands**: a (`int|float`), b (`int|float`)

    **Returns**: (`float|int`) - Sum of `Numbers` a and b

    The operator takes care of implicit `int` to `float` conversions in case of Numbers
    $$int+int \rightarrow int$$
    $$float+(int|float) \rightarrow float$$
    $$(float|int)+float \rightarrow float$$

2.  `-` : Subtraction operator

    **Operands**: a (`int|float`), b (`int|float`)

    **Returns**: (`float|int`) - Difference of `Numbers` a and b

    The operator takes care of implicit `int` to `float` conversions in case of Numbers
    $$int-int \rightarrow int$$
    $$float-(int|float) \rightarrow float$$
    $$(float|int)-float \rightarrow float$$

3.  `*` : Multiplication operator

    **Operands**: a (`int|float`), b (`int|float`)

    **Returns**: (`float|int`) - Product of `Numbers` a and b

    The operator takes care of implicit `int` to `float` conversions in case of Numbers

    $$int\*int \rightarrow int$$
    $$float\*(int|float) \rightarrow float$$
    $$(float|int)\*float \rightarrow float$$

4.  `/` : Division operator

    **Operands**: a (`int|float`), b (`int|float`), $b \neq 0$

    **Returns**: (`float`) - $\dfrac{a}{b(\neq0)} $

    $$(float|int)/(float|int) \rightarrow float$$

    _Note:_ The operator takes care of the Zero Division Error(**Runtime**)

5.  `//` : integer Division operator

    **Operands**: a (`int|float`), b (`int|float`), $b \neq 0 $

    **Returns**: (`int`) - $\lfloor\dfrac{a}{b(\neq 0)}\rfloor$

    $$(float|int)//(float|int) \rightarrow int$$

    _Note:_ The operator takes care of the Zero Division Error(**Runtime**)

6.  `%` : Modulo operator

    **Operands**: a (`int`), b (`int`), $b \ne 0$

    **Returns**: (`int`) - a MOD b($\ne0$)

    $$(int)\%(int) \rightarrow int$$
    _Note:_ The operator takes care of the Zero Division Error(**Runtime**)

7.  `^` : Exponentiation operator

    **Operands**: a (`int|float`), b(`int|float`)

    **Returns**: (`int|float`) - $a^{b}$

    $$(float|int)^{(float|int)} \rightarrow (float|int)$$

### Binary Bitwise Operators

8.  `<<` : Left shift operator

    **Operands**: a (`int`), b (`int`), $b \in I ^ {+}$

    **Returns**: (`int`) - a << b $(\in I ^ {+})$

    $$(int)<<(int) \rightarrow int$$
    _Note:_ The operator takes care of the Negative left operand by raising exception.

9.  `>>` : Right shift operator

    **Operands**: a (`int`), b (`int`), $b \in I ^ {+}$

    **Returns**: (`int`) - a >> b $(\in I ^ {+})$

    $$(int)>>(int) \rightarrow int$$
    _Note:_ The operator takes care of the Negative left operand by raising exception.

10. `&` : Bitwise AND operator

    **Operands**: a (`int`), b (`int`)

    **Returns**: (`int`) - a AND b


    $$(int) \And (int) \rightarrow int$$

11. `|` : Bitwise OR operator

    **Operands**: a (`int`), b (`int`)

    **Returns**: (`int`) - a OR b

    $$(int)|(int) \rightarrow int$$

### Binary Comparision Operators

12. `<=` : Less than or equals operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a $\leq $ b

    $$(Type) <= (Type) \rightarrow boolean$$

13. `<` : Less than operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a < b

    $$(Type) < (Type) \rightarrow boolean$$

14. `>` : Greater than operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a > b

    $$(Type) > (Type) \rightarrow boolean$$

15. `>=` : Greater than or equals operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a >= b

    $$(Type) >= (Type) \rightarrow boolean$$

16. `==` : Equality operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a = b

    $$(Type) == (Type) \rightarrow boolean$$

17. `!=` : not equals operator

    _Note:_ Both the operands must be explicitly of the same type.

    **Operands**: a (`Type`), b (`Type`)

    **Returns**: (`boolean`) - a $\neq$ b

    $$(Type) != (Type) \rightarrow boolean$$

### Binary Logical Operators

18. `&&` : Logical AND operator

    **Operands**: a (`boolean`), b (`boolean`)

    **Returns**: (`boolean`) - `true` if both _a_ and _b_ are true

    $$(boolean) \And\And (boolean) \rightarrow boolean$$

19. `||` : Logical OR operator

    **Operands**: a (`boolean`), b (`boolean`)

    **Returns**: (`boolean`) - `true` if either _a_ or _b_ is true

    $$(boolean) || (boolean) \rightarrow boolean$$

### Unary arithematic Operators

20. `-` : arithematic negation operator

    **Operands**: a (`float|int`)

    **Returns**: (`float|int`) - $-a$

    $$(float) \rightarrow float$$
    $$(int) \rightarrow int$$

### Unary Logical Operators

21. `~` : Logical negation operator

    **Operands**: a (`boolean`)

    **Returns**: (`boolean`) - NOT a

    $$(boolean) \rightarrow boolean$$

### Assignment Operator

22. `=` : Assignment operator

**Operands**: x (`Variable`), a (`AST`)

**Returns**: (`float|int|boolean|Str`) - returns the evaluated value of a

$$Variable=int  \rightarrow  int$$

$$Variable=float  \rightarrow  float$$

$$Variable=boolean  \rightarrow  boolean$$

$$Variable=Str  \rightarrow  Str$$  

## Operator Precedence

Zebra follows the follwing operator precedence (from low to high).
|&nbsp;&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Operators&nbsp;&nbsp;&nbsp;&nbsp;| &nbsp;&nbsp;&nbsp;&nbsp;Associates&nbsp;&nbsp;&nbsp;&nbsp;
|------------|----------------|----
|assignment |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Right
|logicalOr |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\|\||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|logicalAnd |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\&\&|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|Equality |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;==&nbsp;&nbsp;&nbsp;!= |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Left
|Comparison|&nbsp;&nbsp;>&nbsp;&nbsp;&nbsp;>=&nbsp;&nbsp;&nbsp;<&nbsp;&nbsp;&nbsp;<=|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|add|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;+|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|mult|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;\*|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Left
|unary|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;-|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Right

<br>

## Language Features:  

### if statements :  
`if` statements in Zebra are conditional statements, where the branches of code are conditionally executed. According to the value of the boolean expression evaluated, conditional execution of the branches is followed.  

$$
\begin{align}
if ~ Statement  &\rightarrow  'if' ~~ '(' ~~ expression ~~ ')' ~~ '\\{' ~~ declaration ~~ '\\}' ~~ ('else' ~~ ((if~statement )~|~'\\{' ~~ declaration ~~ '\\}')) ~~  \\
\end{align}
$$  


### for statements:
`for` statements in Zebra are loops, where the loop is iterated over the sequence.  

$$
\begin{align}
for ~ Statement  &\rightarrow  'for' ~~ '(' ~~ ( ~ vardec ~ | ~ expression ~ Statement ~ | ~ ';') ~~ expression? ~~ ';' ~ expression? ~ ')' ~block \\
\end{align}
$$  

In the above grammer for the `for` loop, the content present inside the brackets represents the iterative sequence. The sequence is checked, and the block (branch of code) is evaluated.  
  
### while statements:  
while statement in Zebra is a loop which is executed based on condition mentioned in the expression.

$$
\begin{align}
while~Statement  &\rightarrow  'while' ~~ '(' ~~ expression ~~ ')' ~~ ' \\{ ' ~~ block ~~ ' \\} ' ~~  \\
\end{align}
$$  

Similar to the `for` loop, `while` loop check the condition expression (comes out to be a `boolean`, and enters the block if the condition evaluates to be `true`.
### print statement:
The print statement is used to display the given object on the output screen.  

$$
\begin{align}
print ~ Statement  &\rightarrow  'zout' ~ '(' **obj** ')' ~ ';' \\
\end{align}
$$  
> **_obj_** in the above denotes a sequence of objects.  
  
### functions:  
Zebra supports user-defined functions.  
>Zebra follows **Lexical Scoping**  
  
**Declarations:**  
Declarations of functions in Zebra follow the definition of `implicit declaration`, meaning, the function once declared, will not be vanished, and will remain declared throughout its scope(including its children scopes).
The declaration of a function follows the below format:  

$$
\begin{align}
  functionDeclaration &\rightarrow  'func' ~~ ~~  returnType  ~~  functionName ~~ '(' ~~ ( dataType ~~ ~~ Identifier ',' )^* ~~ , ~~ datatype ~~ ~~ Identifier ~~ ')'   ' \\{'  ~~ block ~~ ' \\}'    ';'\\
\end{align}
$$  
  
  
  
**Function Calls:**  
The decalred functions are called by the user in their corresponding scopes. A function call in zebra follows the below format:  

$$
\begin{align}
functionName  '('  ~~ ((obj/identifier',')^* ~~  ~~(Identifier/obj)~~) ? ')'  ';'
\end{align}
$$  

  
### String operations:
**slicing:** Slicing of strings can be done using the `slice` based on the indices of string characters. Zero indexing is followed. This operation returns a string.  

_string_.slice[_startIndex_:_endIndex_]  
 
>Note : The start index character will be included in the sliced string, while the end index will not be inlcuded.
  
**length:**  
  
### Lists:      

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
&|~~ Int ~~ | ~~ Bool ~~ | ~~ String ~~ | ~~ Float ~~ | ~~ nil ~~ | ~~ '(' ~ expression ~ ')' ~~ | ~~ '['(expression',')(expression)?']' ~~ \\
&| ~ 'slice' ~~ expression ~~ expression:expression\\
\end{align}
$$
