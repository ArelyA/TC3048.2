# TC3048.2

## Status: In Progress

El proyecto fue redefinido. Se a establecido un scope más alcanzable y se está trabajando en el diseño de un MVP de funcionalidad. A grandes rasgos se planea definir un lenguaje que permita realizar un análisis básico de **lenguaje natural** del contenido de archivos de texto. 

La declaración de variables se hará de forma automática; en cuanto estas reciban su valor (asignación) se definirá su tipo y se separará su identificador. Los tipos de datos que se manejarán serán: bool, int, float, string y file (extensión .txt). También se manejarán listas de cada uno de estos tipos. Las listas estarán limitadas a UNA dimensión.

| Tipo                      | Contenido                                                    |
| ------------------------- | ------------------------------------------------------------ |
| CTE_BOOL                  | True \| False                                                |
| CTE_INT                   | \d+                                                          |
| CTE_FLOAT                 | \d+\\.d+                                                     |
| CTE_STRING                | "[\d\w]*"                                                    |
| CTE_FILE                  | (\.{0,2}\/){0,1}[\d\w\_\-]+[\d\w\_\-\/]*[\d\w\_\-]+\.txt     |
| Arreglos unidimensionales | Acepta todos los tipos de dato anteriores.  [elem (, elem)*] |

Las palabras reservadas consisten de los tipos de datos junto con los nombre de las funciones base. Los nombres de las funciones especiales también serán palabras reservadas, pero estarán descritos en otra tabla.

| Palabra reservada |
| ----------------- |
| bool              |
| int               |
| float             |
| string            |
| file              |
| if                |
| else              |
| while             |
| for               |
| in                |
| print             |
| read              |
| def               |
| range             |
| len               |
| write             |
| range             |
| getLine           |
| getWord           |
| append            |
| clean             |
| norm              |
| join              |
| create            |
| delete            |
| count             |
| return            |

Los tokens a considerar son los siguientes:

| Token         | Contenido                                            |
| ------------- | ---------------------------------------------------- |
| ID            | /[a-zA-Z_]\w*/                                       |
| TERM_OPT      | * \| /                                               |
| EXP_OPT       | + \| -                                               |
| COMP_OPT      | >= \| <= \| == \| != \|< \| >                        |
| NOT           | not                                                  |
| EXPRESION_AND | and                                                  |
| EXPRESION_OR  | or                                                   |
| TYPE_OPT      | int \| float \| string \| file                       |
| _NEWLINE      | /(\r?\n[\t ]*)+/                                     |
| WHITESPACE    | /[\t \f]+/                                           |
| INLINE        | /\\[\t \f]*\r?\n/                                    |
| SH_COMMENT    | /#\[^\n\]*/                                          |
| CPP_COMMENT   | /\/\/\[^\n\]*/                                       |
| C_COMMENT     | "/*" /(.\|\n)*?/ "*/"                                |
| _INDENT       | *vacío, utilizado para poder manejar la indentación* |
| _DEDENT       | *vacío, utilizado para poder manejar la indentación* |

Funciones especiales:

| Variable     | Funcion   | Descripción                                                  |
| ------------ | --------- | ------------------------------------------------------------ |
| func_count   | count     | recibe un string a buscar y regresa las veces que este se repite |
| func_size    | size      | regresa el tamaño del archivo (nivel palabra)                |
| func_pos     | POS       | regresa el part-of-speech de cada token (nivel palabra)      |
| func_tok     | tokenize  | regresa el archivo separado en tokens, ya sea por oración o por palabra. TBD |
| func_norm    | normalize | pasa todas las letras a minúsculas y remueve todos los símbolos, la lista de símbolos a remover se puede ser definida por el usuario. Símbolos base = Todo excepto puntos, números y espacios |
| func_clean   | clean     | remueve HTML y regresa el texto limpio                       |
| func_unigram | unigram   | regresa las veces que se repite cada palabra                 |
| func_bigram  | bigram    | regresa las veces que aparece un par de palabras consecutivas |
| func_ngram   | ngram     | regresa las veces que aparece un conjunto de n palabras consecutivas |

### Notas (01.05.2021)

* Se generaron algunos de los diagramas necesarios y se continua definiendo el lenguaje.
* A la hora de compilar no se requerirá especificar el nombre del programa ni se va a pedir una función main; la función principal tomará el nombre del archivo sin incluir la extensión.
* Pendiente agregar y desarrollar funciones de manipulación de strings
	
	* Y definir dónde incluirlas
* Desarrollar PROGRAM
* Pendiente desarrollar funciones especiales. Serán agregadas a STMT

#### Dudas
* Debería aceptar regex? (para manipulación de strings y probablemente algo se pueda hace con files)
* Es correcto incluir string y file en VAR_CTE? 
	* Ambas podrían usar + para concatenaciones 
	* O \* para repeticiones... que es concatenarse consigo mismas x veces
		 Ejemplo : ->  cte_string ->\* -> cte_int ->
### Notas (15.05.2021)
* Se generaron los diagramas necesarios y se refactorizaron las Funciones (Pendiente hacer los cambios en este documento). https://lucid.app/lucidchart/invitations/accept/inv_92f1d942-4b56-487e-a7c5-0b062013fd72
* Se comenzó a planear el lexer y parser con sus respectivos puntos neurálgicos.
### Notas (25.05.2021)
* Se terminaron parser y lexer
* Se empezaron a agregar y desarrollar puntos neurálgicos
* Se tiene una primera versión para estructuras de tablas de funciones y de variables
* Se creó el cubo semántico para operaciones básicas
* Se crearon funciones para operaciones básicas
* Se comenzó a generar cuádruplos
* Se comenzó a generar las estructuras para memoria

### Notas (ENTREGA)
* Falta actualizar la documentación
* Compila y ejecuta:
  * Evaluación de expresiones
  * Manejo de arreglos
  * Manejo de archivos
  * Impresión