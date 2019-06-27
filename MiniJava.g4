grammar MiniJava ;
/* Regras Semanticas */

program : mainClass classDecl* EOF;

mainClass : CLASS ID LKEY PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN LKEY cmd RKEY RKEY ;

classDecl : CLASS ID (EXTENDS ID)? LKEY var* metodo* RKEY ;

var : tipo ID SEMI ; 

metodo : PUBLIC tipo ID LPAREN parametros? RPAREN LKEY var* cmd* RETURN exp SEMI RKEY ;

parametros: tipo ID (COMMA tipo ID)* ;

tipo : 	 INT LBRACKET RBRACKET # intVet
	| BOOLEAN # bool
	| INT # int
	| ID  # id
	; 

cmd : 
LKEY cmd* RKEY 
#nestedStatement
| IF LPAREN exp RPAREN cmd (ELSE cmd)? 
#ifElseStatement
| WHILE LPAREN exp RPAREN cmd 
#whileStatement
| SYSTEM_OUT LPAREN exp RPAREN SEMI 
#printStatement
| ID ATTR exp SEMI 
#variableAssignmentStatement
| ID LBRACKET exp RBRACKET ATTR exp SEMI
#arrayAssignmentStatement
;

exp : rexp (exp_aux)? ;
exp_aux : AND rexp (exp_aux)? ;

rexp : aexp (rexp_aux)? ;
rexp_aux : LT aexp (rexp_aux)? 
		 | EQ aexp (rexp_aux)? 
		 | NOTEQ aexp (rexp_aux)?  ;

aexp : mexp (aexp_aux)? ;
aexp_aux : PLUS mexp (aexp_aux)? 
	| MINUS mexp (aexp_aux)? ;

mexp : sexp (mexp_aux)? ;
mexp_aux : 	MULT sexp (mexp_aux)? 
			| DIV sexp (mexp_aux)? ;

sexp : NOT sexp 
	| MINUS sexp 
	| TRUE 
	| FALSE 
	| INTEIRO 
	| NULL 
	| NEW INT LBRACKET exp RBRACKET 
	| pexp (DOT LENGTH | LBRACKET exp RBRACKET)?  ;

pexp : ID (pexp_aux)? 
	| THIS (pexp_aux)? 
	| NEW ID LPAREN RPAREN (pexp_aux)? 
	| LPAREN exp RPAREN (pexp_aux)? ;

pexp_aux : DOT ID (LPAREN (exps)? RPAREN)? (pexp_aux)? ;

exps : exp (COMMA exp)*;

/* Regras Lexicas */

INTEIRO : [0-9]+;	//literal inteiro

TRUE  : 'true' ; //literal lógico true
FALSE : 'false' ; //literal lógico false

NULL : 'null' ; //literal nulo

//separadores
LPAREN : '(' ; 		// abre parenteses (left)
RPAREN : ')' ; 		// fecha parenteses (right)
LBRACKET : '[' ;	// abre colchete (left)
RBRACKET : ']' ;	// fecha colchete (right)
LKEY : '{' ; 		//abre chaves (left)
RKEY : '}' ;		//fecha chaves (rigth)
SEMI : ';' ; 
DOT : '.' ;
COMMA : ',' ;

ATTR : '=' ; 		//atribuicao
GT : '>' ;  
GE : '>=' ;
LT : '<' ;
LE : '<=' ;
NOTEQ : '!=' ; 		//diferente
EQ : '==' ;

PLUS  : '+' ;
MINUS : '-' ;
MULT  : '*' ;
DIV   : '/' ;

AND : '&&' ;
NOT  : '!' ;

ABSTRACT : 'abstract' ;
ASSERT : 'assert' ;
BOOLEAN : 'boolean' ;
BREAK : 'break' ;
BYTE : 'byte' ;
CASE : 'case' ;
CATCH : 'catch' ;
CHAR : 'char' ;
CLASS : 'class' ;
CONST : 'const' ;
CONTINUE : 'continue' ;
DEFAULT : 'default' ;
DO : 'do' ;
DOUBLE : 'double' ;
ELSE : 'else' ;
ENUM : 'enum' ;
EXTENDS : 'extends' ;
FINAL : 'final' ;
FINALLY : 'finally' ;
FLOAT : 'float' ;
FOR : 'for' ;
IF : 'if' ;
GOTO : 'goto' ;
IMPLEMENTS : 'implements' ;
IMPORT : 'import' ;
INSTANCEOF : 'instanceof' ;
INT : 'int' ;
INTERFACE : 'interface' ;
LENGTH : 'length' ;
LONG : 'long' ;
MAIN : 'main' ;
NATIVE : 'native' ;
NEW : 'new' ;
PACKAGE : 'package' ;
PRIVATE : 'private' ;
PROTECTED : 'protected' ;
PUBLIC : 'public' ;
RETURN : 'return' ;
SHORT : 'short' ;
STATIC : 'static' ;
STRICTFP : 'strictfp' ;
STRING : 'String' ;
SUPER : 'super' ;
SWITCH : 'switch' ;
SYNCHRONIZED : 'synchronized' ;
SYSTEM_OUT : 'System.out.println' ;
THIS : 'this' ;
THROW : 'throw' ;
THROWS : 'throws' ;
TRANSIENT : 'transient' ;
TRY : 'try' ;
VOID : 'void' ;
VOLATILE : 'volatile' ;
WHILE : 'while' ;



ID : [a-zA-Z_][a-zA-Z_0-9]* ; //identificador

// COMMENT and WS are stripped from the output token stream by sending
// to a different channel 'skip'

LINE_COMMENT : '//' .+? ('\n'|EOF) -> skip ;
COMMENT 	 : '/*' .*? '*/' -> skip ;			 // Match "/*" stuff "*/"
WS : [ \r\t\n\f]+ -> skip ;
