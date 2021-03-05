# Little Duck 2020
<div style="text-align: right"> by Arely Aceves Compean </div>

## *Contents*

* [Diagrams](#Diagrams)
* [Regular Expressions](Regular Expressions)
* [Grammar](#Grammar)
* [Code](#Code)
* [Test Cases](#Test Cases)
* [Compilation Results](#Compilation Results)

## Diagrams

![](C:\Users\Arely\Desktop\TEC\Compiladores\TC3048.2\Tarea3\LittleDuck.png)

## Regular Expressions

| Token         | Regex                                              |
| ------------- | -------------------------------------------------- |
| program       | ([a-z\*\|A-Z\*]+[0-9]\*_\*)+.exe                   |
| var           | ([a-z\*\|A-Z\*]+[0-9]\*_\*)+                       |
| id            | \d{8}                                              |
| Sym_Semicolon | ;                                                  |
| Sym_Dot       | .                                                  |
| Sym_Colon     | :                                                  |
| Type_int      | int                                                |
| Type_float    | float                                              |
| Sym_LCBracket | {                                                  |
| Sym_RCBracket | }                                                  |
| Sym_Equal     | =                                                  |
| Sym_Rel       | <>\|<\|>                                           |
| Sym_LParen    | (                                                  |
| Sym_RParen    | )                                                  |
| cte.string    | [\d\w\s_+-.,!@#$%^&\*();:\\\/\|<>=!¿¡?\\[\\]{}~]*" |
| St_Print      | print                                              |
| Cond_if       | if                                                 |
| Cond_else     | else                                               |
| Sym_SR        | [+\|-]                                             |
| Sym_MD        | [*\|/]                                             |
| cte_l         | cte l                                              |
| cte_f         | cte f                                              |
| ε             |                                                    |

[back to top](#Little Duck 2020)

## Grammar

​                   S -> PROGRAMA

PROGRAMA -> program id Sym_Semicolon P BLOQUE

​                   P -> VARS | ε

​            VARS -> var V

​                   V -> id V

​                 V1 -> Sym_Colon TIPO Sym_Semicolon V3

​                 V2 -> Sym_Dot V

​                 V3 -> V | ε

​              TIPO -> Type_int | Type_float

​       BLOQUE -> Sym_LCBracket B Sym_RCBracket

​                    B -> B1 | ε

​                  B1 -> ESTATUTO B

​    ESTATUTO -> ASIGNACION | CONDICION | ESCRITURA

ASIGNACION -> id Sym_Equal EXPRESION Sym_Semicolon

   EXPRESION -> EXP E

​                     E -> Sym_Rel EXP | ε

​     ESCRITURA -> St_Print Sym_LParen ES Sym_RParen Sym_Semicolon

​                     ES -> cte.string | ES1

​                    ES1 -> EXPRESION ES2

​                    ES2 -> Sym_Dot ES | ε

​     CONDICION -> Cond_If Sym_LParen EXPRESION Sym_RParen BLOQUE C

​                        C -> Cond_Else BLOQUE | ε

​                     EXP -> EX

​                       EX -> TERMINO EX1

​                     EX1 -> Sym_SR EX | ε

​           TERMINO -> T

​                          T -> FACTOR T1

​                        T1 -> Sym_MD T | ε

​              FACTOR -> F

​                          F -> Sym_LParen EXPRESION Sym_RParen | F1 VAR_CTE

​                        F1 -> Sym_SR | ε

​             VAR_CTE -> id | cte_l | cte_f

[back to top](#Little Duck 2020)

## Code
TBD

[back to top](#Little Duck 2020)

## Test Cases
TBD

[back to top](#Little Duck 2020)

## Compilation Results
TBD

[back to top](#Little Duck 2020)