# TC3048.2

## Status: In Progress

El proyecto fue redefinido. Se a establecido un scope más alcanzable y se está trabajando en el diseño de un MVP de funcionalidad. A grandes rasgos se planea definir un lenguaje que permita realizar un análisis básico de **lenguaje natural** del contenido de archivos de texto. 

La declaración de variables se hará de forma automática; en cuanto estas reciban su valor (asignación) se definirá su tipo y se separará su identificador. Los tipos de datos que se manejarán serán: bool, int, float, string y file (extensión .txt). También se manejarán listas de cada uno de estos tipos. Las listas estarán limitadas a UNA dimensión.

| Tipo       | Contenido                                                    |
| ---------- | ------------------------------------------------------------ |
| cte_bool   | True \| False                                                |
| cte_int    | \d+                                                          |
| cte_float  | \d+\\.d+                                                     |
| cte_string | "[\d\w]*"                                                    |
| cte_file   | (\.{0,2}\/){0,1}[\d\w\_\-]+[\d\w\_\-\/]*[\d\w\_\-]+\.txt     |
| list       | Acepta todos los tipos de dato anteriores. TBD en diagrama -> de 0 a n elementos entre brackets [] y separados por comas , |

Las palabras reservadas consisten de los tipos de datos junto con los nombre de las funciones base. Los nombres de las funciones especiales también serán palabras reservadas, pero estarán descritos en otra tabla.

| Variable    | Palabra reservada |
| ----------- | ----------------- |
| type_bool   | bool              |
| type_int    | int               |
| type_float  | float             |
| type_string | string            |
| type_file   | file              |
| cond_if     | if                |
| cond_else   | else              |
| stmt_while  | while             |
| stmt_for    | for               |
| stmt_in     | in                |
| func_print  | print             |
| func_read   | read              |
| stmt_def    | def               |
| stmt_range  | range             |
| func_len    | len               |

Los tokens a considerar son los siguientes:

| Token      | Contenido    |
| ---------- | ------------ |
| id         | [\w]+[\d\w]* |
| sym_sum    | +            |
| sym_sub    | -            |
| sym_mult   | *            |
| sym_div    | /            |
| sym_and    | AND          |
| sym_or     | OR           |
| sym_less   | <            |
| sym_great  | >            |
| sym_not    | NOT          |
| sym_eq     | ==           |
| sym_asig   | =            |
| sym_Lparen | (            |
| sym_Rparen | )            |
| sym_Lbrack | [            |
| sym_Rbrack | ]            |
| sym_dot    | .            |
| sym_mod    | %            |
| sym_comm   | #            |
| sym_tab    | /t           |

Funciones especiales:

| Variable     | Funcion   | Descripción                                                  |
| ------------ | --------- | ------------------------------------------------------------ |
| func_count   | count     | recibe un string a buscar y regresa las veces que este se repite |
| func_size    | size      | regresa el tamaño del archivo (nivel palabra)                |
| func_pos     | POS       | regresa el part-of-speech de cada token (nivel palabra)      |
| func_lemm    | lemmatize | regresa los tokens (nivel palabra) lematizados               |
| func_stem    | stem      | regresa la raíz de cada token (nivel palabra)                |
| func_tok     | tokenize  | regresa el archivo separado en tokens, ya sea por oración o por palabra. TBD |
| func_norm    | normalize | pasa todas las letras a minúsculas y remueve todos los símbolos, la lista de símbolos a remover se puede ser definida por el usuario. Símbolos base = Todo excepto puntos, números y espacios |
| func_clean   | clean     | remueve HTML y regresa el texto limpio                       |
| func_NER     | NER       | regresa el name entity relation de cada token (nivel palabra) |
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