# Introduction  
Zebra is a programming language designed to be easy to read and write. 
Zebra includes features such as variables, data types (e.g. integers, floats, strings, bool), conditional statements (e.g. if/else), loops (e.g. for,while), functions, lists, arrays, etc.
It is a new addition to the world of programming languages. This is a very friendly language and an excellent one for the beginners.  

# Language Features
## Comments 
Comment lines using `@`.   
Example: 
`@ Hello world` 

## Keywords
`if, else, while, for, zout, array, append, remove, length, insert, func, slice, index, end, sep, pop`.   
These are the keywords in the language and are not supposed to be used as identifiers. Otherthan these anything can be used as an identifier.

## Semicolons 
Use semicolons to indicate the end of an expression.  
Example:
`int a = 5;`  
## DataTypes 
### Integer 
`int` is used to define objects of type integer.  
Example: 
`int a = 5;` 
### Float 
`float` is used to define objects of type float.  
Example:
`float a = 1.5;` 
### String 
`string` is used to define objects of type string.   
Example:
`string a = "zebra";` 
### Boolean 
`boolean` is used to define objects of type bool.   
Example: 
`bool a = "true";`   
Right side of the assignment can contain any valid datatype, the language evaluate it to `True` or `False` based on its value.   
Integer 0, Float 0, Empty string, and nil are evaluate to `False`, and rest others are evaluated to `True`.

### Constant
`const` is used to define objects of constant type, that is, once defined they cannot be modified.  
Example: 
`const int a = 10;` 

### Array
`array` is used to define a container that contains values of only specified type.  
Syntax:   
```
"array" datatype identifier = [datatype object, datatype object,....]
```
Example: 
```
array int a = [10,5,6];
array string b = ["Hi","Hello","Namasthe"];
```
## Print statement
### zout 
Print statement in zebra look like: 
```
zout(1,2,3,sep =',',end = '\n');
zout(100);
```
`sep` : To indicate the seperation factor between multiple print objects  
`end` : To specify the end of line  

## Control Structures  
### If-else  
If-else conditional statements in zebra look like:   
```
if (i ==1 )   
{
  zout(i);
}
else if (j == 11)
{
	zout(j);
}
else
{
  zout(k);
} 
```  
### For
For loop in zebra look like:   
```
for(int i =0;i<10; i=i+1 ){
	zout(i);
}
```
### While
While loop in zebra look like:  
```
int i = 1;
while(i < 10){
     zout(i);
     i = i + 1;
}
``` 
## Functions
Functions in zebra are defined as:  
Syntax: 
```
"func" returnDatatype identifier(dataType identifier, dataType identifier,....)
{
    -------------
    -------------
    -------------
    return identifier;
}
```
```
func int fib(int num){
    int x=1+num;
    return x;
}
```
Functions are called as:  
Syntax:
```
returnDataType identifier = identifier(parameter);
```
```
int z = fib(142);
```
## Array operations
### Append
`append` is used to append an element at the last of the array.   
Syntax:
```
append(element,identifier)
```
Example: 
```
array int a = [10,5,6];
append(2,a);

result:
[10,5,6,2]
```
### Pop
`pop` is used to pop an element from the end of the array if the array is not empty.  
Syntax:
```
pop(identifier)
```
Example: 
```
array int a = [10,5,6];
pop(a);

result:
[10,5]
Pops out 6 from the end. 
```
### Remove
`remove` is used to remove an element at the specified index.  
Syntax:
```
remove(index,identifier)
```
Example: 
```
array int a = [10,5,6];
remove(1,a);

result:
[10,6]
Removes an element from the array `a` at index 1
```
### Insert
`insert` is used to insert an element at the specified index.  
Syntax:
```
insert(index,element,identifier)
```
Example: 
```
array int a = [10,5,6];
insert(1,100,a);

result:
[10,100,5,6]
Inserts the element 100 element into the array `a` at index 1
```
### Length
`length` is used to find the size of the array.  
Syntax:
```
length(identifier)
```
Example: 
```
array int a = [10,5,6];
length(a);

result:
3
Gives the length of the array `a`.
```
### Slice
`slice` is used to get the elements of a array within a specified range.  
Syntax:
```
slice identifier start:end
```
Example: 
```
array int a = [10,5,6];
zout(slice a 0:2);

result:
[10,5]
Returns the elements between index 0(inclusive) and 2(exclusive) of the array `a`.
```
### Index
`index` is used to get the element of a array with a specified index.  
Syntax:
```
index identifier index_number
```
Example:
``` 
array int a = [10,5,6];
zout(index a 1);

result:
5
Returns the element at index 1 of `a`.
```  
## Classes 

### Feature Update
1. Added a feature to create classes (without support for inheritance and static methods).
```
class className{
    Variable declarations + Function declarations
}
```

Example: 

```
class ll{
    int value;
    ll next;

    func boolean init(int value){
        this.value = value;
        return true;
    }
}
```

2. Ability to create instances of classes.
```
className varName = className(params);
```
> *Note:* The process of instantiation automatically calls the function named `"init"`(if present). Whatever the function might return, it discards it and returns an object instance. But when called explicitly like `instanceObject.init(params)`, its return value would be as expected.

3.Setters:
```
instanceName.fieldName = fieldValue;
```
> *Note:* We can only Declare a field of an instance inside the class, but we can only modify its value outside the class. We can not modify a function declaration of the scope outside of the class.
4. Getters:
```
@ Getting a field  
instanceName.fieldName;  
@ Getting a method  
instanceName.methodName();
```
> *Note:* Assigning an instance variable to a variable does not create a copy, but the variable points to the value of the variable. 
> Example:
```
className a = className(params);
className b = a; @ Here b points to the same value pointed by a   
```
## Errors
The possible errors are: `TokenError, typeCheckError, RuntimeError, ParseError, resolveError`  
### typeCheckError: 
Arises when operations are performed on objects of conflicting types.  
Examples: 
```
int a=5; 
string b="Hi";
int c=a+b;
```
### RuntimeError: 
Arises when the program crashes or produces a wrong output.   
Examples: 
```
array index out of bounds
cannot divide with zero
```
### TokenError: 
Arises when an expected token isn't provided.   
Example: 
```
int a=10 
raises a token error "Expected a ';'"
```
### ParseError: 
Arises when the declaration or syntax is not consistent with the language specifications.   
Examples: 
```
Expected an identifier
Cannot use Keywords as Identifiers
Cannot declare a array as const.
Expected data type.
Dimensions of the given array and initializer array do not match
```
### resolveError: 
Arises when the redeclarations occur and when the variables could not be resolved.  
Examples: 
```
Redeclaring already declared variable x
Could not resolve the variable x
```


