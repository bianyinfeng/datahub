/**
 * SqlBase.g4 - Shared base grammar for SQL dialects.
 *
 * Supports macro variable syntax: {macro_var_name}
 * Macro variables may appear wherever an identifier, literal, or expression
 * is expected (table names, column names, WHERE conditions, string values, etc.)
 *
 * Derived grammars: SparkSql.g4, OpenGaussSql.g4
 */
grammar SqlBase;

// ============================================================
// Parser Rules
// ============================================================

singleStatement
    : statement SEMI? EOF
    ;

statement
    : query                                                            # queryStatement
    | cteDefinition? insertStatement                                   # insertStmt
    | cteDefinition? mergeStatement                                    # mergeStmt
    | createTableStatement                                             # createTableStmt
    | createViewStatement                                              # createViewStmt
    | createMaterializedViewStatement                                  # createMatViewStmt
    | dropStatement                                                    # dropStmt
    | alterStatement                                                   # alterStmt
    | truncateStatement                                                # truncateStmt
    | analyzeStatement                                                 # analyzeStmt
    | explainStatement                                                 # explainStmt
    | setStatement                                                     # setStmt
    | useStatement                                                     # useStmt
    ;

// ---- Query ---------------------------------------------------

query
    : cteDefinition? queryTerm queryOrganization
    ;

cteDefinition
    : WITH RECURSIVE? namedQuery (COMMA namedQuery)*
    ;

namedQuery
    : name=identifier (LPAREN columnAliases RPAREN)? AS LPAREN query RPAREN
    ;

queryTerm
    : queryPrimary                                                      # queryTermDefault
    | left=queryTerm operator=(UNION | INTERSECT | EXCEPT | MINUS)
      setQuantifier? right=queryTerm                                   # setOperation
    ;

setQuantifier
    : ALL
    | DISTINCT
    ;

queryPrimary
    : querySpecification                                               # queryPrimaryDefault
    | TABLE macroOrIdentifier                                          # table
    | LPAREN query RPAREN                                              # subquery
    ;

querySpecification
    : selectClause
      fromClause?
      whereClause?
      groupByClause?
      havingClause?
      windowClause?
      qualifyClause?
    ;

selectClause
    : SELECT setQuantifier? selectItem (COMMA selectItem)*
    ;

selectItem
    : expression (AS? alias=identifier)?                               # selectExpression
    | star=STAR                                                        # selectStar
    | qualifier=identifier DOT star=STAR                              # selectQualifiedStar
    ;

fromClause
    : FROM relation (COMMA relation)*
    ;

relation
    : relationPrimary joinRelation*
    ;

joinRelation
    : joinType JOIN relationPrimary joinCriteria?
    | NATURAL joinType? JOIN relationPrimary
    | CROSS JOIN relationPrimary
    ;

joinType
    : INNER?
    | LEFT OUTER?
    | LEFT SEMI
    | RIGHT OUTER?
    | FULL OUTER?
    | LEFT ANTI
    ;

joinCriteria
    : ON expression
    | USING LPAREN identifier (COMMA identifier)* RPAREN
    ;

relationPrimary
    : macroOrIdentifier (AS? alias=identifier)?                        # tableName
    | LPAREN query RPAREN (AS? alias=identifier)?                     # subqueryRelation
    | LATERAL LPAREN query RPAREN (AS? alias=identifier)?             # lateral
    | UNNEST LPAREN expression (COMMA expression)* RPAREN
      (WITH ORDINALITY)? (AS? alias=identifier
      (LPAREN columnAliases RPAREN)?)?                                 # unnestRelation
    ;

whereClause    : WHERE expression ;
groupByClause  : GROUP BY groupByItem (COMMA groupByItem)* ;
havingClause   : HAVING expression ;
qualifyClause  : QUALIFY expression ;
windowClause   : WINDOW namedWindow (COMMA namedWindow)* ;

namedWindow
    : name=identifier AS windowSpec
    ;

groupByItem
    : expression
    | ROLLUP  LPAREN groupByItemList RPAREN
    | CUBE    LPAREN groupByItemList RPAREN
    | GROUPING SETS LPAREN groupByItemSet (COMMA groupByItemSet)* RPAREN
    ;

groupByItemList : expression (COMMA expression)* ;
groupByItemSet  : LPAREN groupByItemList RPAREN | LPAREN RPAREN ;

queryOrganization
    : (ORDER BY sortItem (COMMA sortItem)*)?
      (LIMIT limitClause)?
      (OFFSET offset=expression)?
      (FETCH FIRST fetchCount=expression ROWS ONLY)?
    ;

limitClause : ALL | expression ;

sortItem
    : expression ordering=(ASC | DESC)? (NULLS nullOrder=(FIRST | LAST))?
    ;

// ---- Insert --------------------------------------------------

insertStatement
    : INSERT insertMode INTO? target=macroOrIdentifier
      partitionSpec?
      (columnList)?
      (query | VALUES valueList (COMMA valueList)*)
    ;

insertMode
    : OVERWRITE
    | INTO
    ;

partitionSpec
    : PARTITION LPAREN partitionVal (COMMA partitionVal)* RPAREN
    ;

partitionVal
    : identifier (EQ literal)?
    ;

columnList
    : LPAREN identifier (COMMA identifier)* RPAREN
    ;

columnAliases
    : identifier (COMMA identifier)*
    ;

valueList
    : LPAREN expression (COMMA expression)* RPAREN
    ;

// ---- Merge ---------------------------------------------------

mergeStatement
    : MERGE INTO? target=macroOrIdentifier (AS? targetAlias=identifier)?
      USING source=mergeSource (AS? sourceAlias=identifier)?
      ON condition=expression
      whenClause+
    ;

mergeSource
    : macroOrIdentifier
    | LPAREN query RPAREN
    ;

whenClause
    : WHEN MATCHED (AND expression)? THEN mergeAction
    | WHEN NOT MATCHED (AND expression)? THEN INSERT VALUES valueList
    | WHEN NOT MATCHED (AND expression)? THEN INSERT columnList? VALUES valueList
    ;

mergeAction
    : UPDATE SET assignmentList
    | DELETE
    ;

assignmentList
    : assignment (COMMA assignment)*
    ;

assignment
    : identifier EQ expression
    ;

// ---- DDL -----------------------------------------------------

createTableStatement
    : CREATE (OR REPLACE)? (TEMPORARY | TEMP)? (EXTERNAL)?
      TABLE (IF NOT EXISTS)?
      tableName=macroOrIdentifier
      (LPAREN columnDef (COMMA columnDef)* (COMMA tableConstraint)* RPAREN)?
      tableProperties?
      partitionBy?
      (AS query)?
    ;

createViewStatement
    : CREATE (OR REPLACE)? (TEMPORARY | TEMP)?
      VIEW (IF NOT EXISTS)?
      viewName=macroOrIdentifier
      (LPAREN columnAliases RPAREN)?
      AS query
    ;

createMaterializedViewStatement
    : CREATE MATERIALIZED VIEW (IF NOT EXISTS)?
      viewName=macroOrIdentifier
      (LPAREN columnAliases RPAREN)?
      AS query
    ;

dropStatement
    : DROP (TABLE | VIEW | MATERIALIZED VIEW | SEQUENCE | INDEX | FUNCTION | PROCEDURE)
      (IF EXISTS)? macroOrIdentifier
    ;

alterStatement
    : ALTER TABLE macroOrIdentifier alterTableAction
    ;

alterTableAction
    : ADD COLUMN columnDef
    | DROP COLUMN identifier
    | RENAME TO identifier
    | RENAME COLUMN identifier TO identifier
    | ALTER COLUMN identifier (SET | DROP) NOT NULL
    ;

truncateStatement
    : TRUNCATE TABLE? macroOrIdentifier
    ;

analyzeStatement
    : ANALYZE TABLE macroOrIdentifier COMPUTE STATISTICS (FOR COLUMNS columnAliases)?
    ;

explainStatement
    : EXPLAIN (EXTENDED | CODEGEN | COST | FORMATTED)? statement
    ;

setStatement
    : SET identifier EQ expression
    ;

useStatement
    : USE identifier
    ;

// ---- Column & Table Definitions ------------------------------

columnDef
    : name=identifier dataType
      (NOT NULL)?
      (DEFAULT expression)?
      columnConstraint*
      columnComment?
    ;

columnConstraint
    : PRIMARY KEY
    | UNIQUE
    | REFERENCES macroOrIdentifier (LPAREN identifier RPAREN)?
    | CHECK LPAREN expression RPAREN
    ;

tableConstraint
    : (CONSTRAINT name=identifier)?
      ( PRIMARY KEY LPAREN identifier (COMMA identifier)* RPAREN
      | UNIQUE LPAREN identifier (COMMA identifier)* RPAREN
      | FOREIGN KEY LPAREN identifier (COMMA identifier)* RPAREN
        REFERENCES macroOrIdentifier
      | CHECK LPAREN expression RPAREN
      | EXCLUDE USING identifier
        LPAREN excludeElement (COMMA excludeElement)* RPAREN
        (WHERE LPAREN expression RPAREN)?
      )
    ;

excludeElement
    : identifier WITH identifier
    ;

partitionBy
    : PARTITION BY? partitionType? LPAREN expression (COMMA expression)* RPAREN
    ;

partitionType
    : RANGE | LIST | HASH
    ;

tableProperties
    : WITH? LPAREN tableProperty (COMMA tableProperty)* RPAREN
    | TBLPROPERTIES LPAREN tableProperty (COMMA tableProperty)* RPAREN
    | STORED AS identifier
    | LOCATION stringLiteral
    | USING identifier
    ;

tableProperty
    : key=propertyKey (EQ? value=propertyValue)?
    ;

propertyKey   : identifier (DOT identifier)* | stringLiteral ;
propertyValue : literal | identifier ;

columnComment : COMMENT stringLiteral ;

// ---- Data Types ----------------------------------------------

dataType
    : baseType (LPAREN INTEGER_VALUE (COMMA INTEGER_VALUE)? RPAREN)?   # primitiveType
    | dataType ARRAY                                                    # arrayType
    | ARRAY LT dataType GT                                             # arrayTypeAngle
    | MAP LT dataType COMMA dataType GT                                # mapType
    | STRUCT LT structField (COMMA structField)* GT                    # structType
    | macroVar                                                          # macroDataType
    ;

baseType
    : STRING | INT | INTEGER | BIGINT | SMALLINT | TINYINT | BOOLEAN
    | FLOAT | DOUBLE | DECIMAL | NUMERIC | DATE | TIMESTAMP
    | TIMESTAMP_TZ | INTERVAL | BINARY | BYTES | CHAR | CHARACTER
    | VARCHAR | TEXT | BYTEA | JSONB | JSON | UUID | SERIAL | BIGSERIAL
    | SMALLSERIAL | REAL | MONEY | BIT | VARBIT | INET | CIDR | MACADDR
    | TSVECTOR | TSQUERY | OID | VOID | RECORD | GEOMETRY | GEOGRAPHY
    ;

structField
    : identifier COLON dataType (COMMENT stringLiteral)?
    ;

// ---- Expressions ---------------------------------------------

expression
    : booleanExpression
    ;

booleanExpression
    : valueExpression                                                   # passThrough
    | NOT booleanExpression                                            # logicalNot
    | left=booleanExpression op=AND right=booleanExpression           # logicalBinary
    | left=booleanExpression op=OR  right=booleanExpression           # logicalBinary
    | EXISTS LPAREN query RPAREN                                       # exists
    ;

valueExpression
    : primaryExpression                                                # valueExprDefault
    | operator=(MINUS | PLUS | TILDE) valueExpression                 # unaryArithmetic
    | left=valueExpression op=HAT right=valueExpression               # bitwiseXor
    | left=valueExpression
      op=(STAR | SLASH | PERCENT | DIV | MOD)
      right=valueExpression                                            # arithmeticBinary
    | left=valueExpression
      op=(PLUS | MINUS | CONCAT_PIPE)
      right=valueExpression                                            # arithmeticBinary
    | left=valueExpression
      op=(AMPERSAND | PIPE)
      right=valueExpression                                            # bitwiseBinary
    | left=valueExpression comparisonOperator right=valueExpression   # comparison
    | valueExpression NOT? BETWEEN lo=valueExpression
      AND hi=valueExpression                                           # between
    | valueExpression NOT? IN LPAREN expression (COMMA expression)* RPAREN # inList
    | valueExpression NOT? IN LPAREN query RPAREN                     # inSubquery
    | valueExpression NOT? LIKE pattern=valueExpression
      (ESCAPE escape=valueExpression)?                                 # like
    | valueExpression NOT? ILIKE pattern=valueExpression              # ilike
    | valueExpression NOT? RLIKE pattern=valueExpression              # rlike
    | valueExpression IS NOT? NULL                                     # isNull
    | valueExpression IS NOT? DISTINCT FROM valueExpression           # isDistinctFrom
    | valueExpression JSONB_ARROW valueExpression                      # jsonArrow
    | valueExpression JSONB_DARROW valueExpression                     # jsonDoubleArrow
    | valueExpression JSONB_HASH_ARROW valueExpression                 # jsonHashArrow
    | valueExpression JSONB_CONTAINS valueExpression                   # jsonContains
    | valueExpression JSONB_CONTAINED_BY valueExpression               # jsonContainedBy
    | valueExpression FULLTEXT_MATCH valueExpression                   # fulltextMatch
    ;

primaryExpression
    : literal                                                          # literalExpr
    | macroVar                                                         # macroVarExpr
    | STAR                                                             # star
    | functionCall                                                     # funcCall
    | LPAREN expression RPAREN                                        # parenthesized
    | LPAREN query RPAREN                                              # scalarSubquery
    | CASE whenClauseExpr+ (ELSE elseExpr=expression)? END            # searched_case
    | CASE operand=expression
      whenClauseExpr+ (ELSE elseExpr=expression)? END                 # simple_case
    | CAST LPAREN expression AS dataType RPAREN                       # cast
    | TRY_CAST LPAREN expression AS dataType RPAREN                   # tryCast
    | primaryExpression DOT identifier                                 # dereference
    | primaryExpression LBRACKET expression RBRACKET                  # subscript
    | identifier                                                       # columnRef
    | INTERVAL expression intervalField (TO intervalField)?           # interval
    | TIMESTAMP stringLiteral                                         # timestampLiteral
    | arrayExpression                                                  # array
    | mapExpression                                                    # map
    | STRUCT LPAREN (namedArgument (COMMA namedArgument)*)? RPAREN    # struct
    | EXTRACT LPAREN identifier FROM expression RPAREN                # extract
    | primaryExpression OVER windowSpec                               # windowExpr
    | FILTER LPAREN WHERE expression RPAREN                           # filterExpr
    ;

whenClauseExpr : WHEN condition=expression THEN result=expression ;

functionCall
    : funcName=qualifiedIdentifier
      LPAREN (setQuantifier? expression (COMMA expression)* | STAR)? RPAREN
      (FILTER LPAREN WHERE expression RPAREN)?
      (OVER windowSpec)?
    | functionCall WITHIN GROUP LPAREN ORDER BY sortItem (COMMA sortItem)* RPAREN
    ;

namedArgument : identifier ARROW expression | expression ;

arrayExpression : ARRAY LPAREN (expression (COMMA expression)*)? RPAREN ;
mapExpression   : MAP LPAREN (expression (COMMA expression)*)? RPAREN ;

windowSpec
    : identifier                                                       # windowRef
    | LPAREN
        (existingWindowName=identifier)?
        (PARTITION BY expression (COMMA expression)*)?
        (ORDER BY sortItem (COMMA sortItem)*)?
        windowFrame?
      RPAREN                                                           # windowSpecExpr
    ;

windowFrame
    : frameType=(RANGE | ROWS | GROUPS)
      (frameBound | BETWEEN frameBound AND frameBound)
    ;

frameBound
    : UNBOUNDED PRECEDING
    | CURRENT ROW
    | expression (PRECEDING | FOLLOWING)
    | UNBOUNDED FOLLOWING
    ;

intervalField
    : YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND
    | YEARS | MONTHS | WEEKS | DAYS | HOURS | MINUTES | SECONDS
    ;

comparisonOperator
    : EQ | NEQ | LT | GT | LTE | GTE | NSEQ
    ;

// ---- Identifiers & Literals ----------------------------------

qualifiedIdentifier
    : identifier (DOT identifier)*
    ;

macroOrIdentifier
    : macroVar
    | qualifiedIdentifier
    ;

macroVar
    : MACRO_VAR
    ;

identifier
    : strictIdentifier
    | nonReserved
    ;

strictIdentifier
    : IDENTIFIER
    | BACKQUOTED_IDENTIFIER
    | DOUBLE_QUOTED_IDENTIFIER
    ;

literal
    : NULL                                                             # nullLiteral
    | booleanLiteral                                                   # boolLiteral
    | INTEGER_VALUE                                                    # intLiteral
    | DECIMAL_VALUE                                                    # decLiteral
    | FLOAT_VALUE                                                      # floatLiteral
    | stringLiteral                                                    # strLiteral
    | DOLLAR_QUOTED_STRING                                             # dollarLiteral
    ;

booleanLiteral : TRUE | FALSE ;

stringLiteral
    : (STRING_LITERAL | UNICODE_STRING)+
    ;

// ============================================================
// Lexer Rules
// ============================================================

// Macro variable token — highest priority
MACRO_VAR
    : '{' [a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]* '}'
    ;

// Keywords (alphabetical)
ADD            : A D D ;
ALL            : A L L ;
ALTER          : A L T E R ;
ANALYZE        : A N A L Y Z E ;
AND            : A N D ;
ANTI           : A N T I ;
ARRAY          : A R R A Y ;
AS             : A S ;
ASC            : A S C ;
AT             : A T ;
BETWEEN        : B E T W E E N ;
BIGINT         : B I G I N T ;
BIGSERIAL      : B I G S E R I A L ;
BIT            : B I T ;
BOOLEAN        : B O O L E A N ;
BOTH           : B O T H ;
BINARY         : B I N A R Y ;
BYTES          : B Y T E S ;
BYTEA          : B Y T E A ;
BY             : B Y ;
CACHE          : C A C H E ;
CALL           : C A L L ;
CASCADE        : C A S C A D E ;
CASE           : C A S E ;
CAST           : C A S T ;
CHAR           : C H A R ;
CHARACTER      : C H A R A C T E R ;
CHECK          : C H E C K ;
CIDR           : C I D R ;
CLUSTER        : C L U S T E R ;
CODEGEN        : C O D E G E N ;
COLLECT        : C O L L E C T ;
COLUMN         : C O L U M N ;
COMMENT        : C O M M E N T ;
COMPUTE        : C O M P U T E ;
CONCAT         : C O N C A T ;
CONSTRAINT     : C O N S T R A I N T ;
COPY           : C O P Y ;
COST           : C O S T ;
CREATE         : C R E A T E ;
CROSS          : C R O S S ;
CUBE           : C U B E ;
CURRENT        : C U R R E N T ;
DATA           : D A T A ;
DATABASE       : D A T A B A S E ;
DATE           : D A T E ;
DAY            : D A Y ;
DAYS           : D A Y S ;
DECIMAL        : D E C I M A L ;
DEFAULT        : D E F A U L T ;
DEFINED        : D E F I N E D ;
DELETE         : D E L E T E ;
DESC           : D E S C ;
DISTINCT       : D I S T I N C T ;
DISTRIBUTE     : D I S T R I B U T E ;
DIV            : D I V ;
DOUBLE         : D O U B L E ;
DROP           : D R O P ;
ELSE           : E L S E ;
END            : E N D ;
ESCAPE         : E S C A P E ;
EXCEPT         : E X C E P T ;
EXCHANGE       : E X C H A N G E ;
EXCLUDE        : E X C L U D E ;
EXISTS         : E X I S T S ;
EXPLAIN        : E X P L A I N ;
EXTENDED       : E X T E N D E D ;
EXTERNAL       : E X T E R N A L ;
EXTRACT        : E X T R A C T ;
FALSE          : F A L S E ;
FETCH          : F E T C H ;
FILTER         : F I L T E R ;
FIRST          : F I R S T ;
FLOAT          : F L O A T ;
FOLLOWING      : F O L L O W I N G ;
FOR            : F O R ;
FOREIGN        : F O R E I G N ;
FORMATTED      : F O R M A T T E D ;
FROM           : F R O M ;
FULL           : F U L L ;
FUNCTION       : F U N C T I O N ;
GEOGRAPHY      : G E O G R A P H Y ;
GEOMETRY       : G E O M E T R Y ;
GROUP          : G R O U P ;
GROUPS         : G R O U P S ;
GROUPING       : G R O U P I N G ;
HAVING         : H A V I N G ;
HASH           : H A S H ;
HOUR           : H O U R ;
HOURS          : H O U R S ;
IF             : I F ;
ILIKE          : I L I K E ;
IN             : I N ;
INDEX          : I N D E X ;
INET           : I N E T ;
INLINE         : I N L I N E ;
INNER          : I N N E R ;
INSERT         : I N S E R T ;
INT            : I N T ;
INTEGER        : I N T E G E R ;
INTERSECT      : I N T E R S E C T ;
INTERVAL       : I N T E R V A L ;
INTO           : I N T O ;
IS             : I S ;
JOIN           : J O I N ;
JSON           : J S O N ;
JSONB          : J S O N B ;
KEY            : K E Y ;
LANGUAGE       : L A N G U A G E ;
LAST           : L A S T ;
LATERAL        : L A T E R A L ;
LEADING        : L E A D I N G ;
LIKE           : L I K E ;
LIMIT          : L I M I T ;
LIST           : L I S T ;
LOCATION       : L O C A T I O N ;
MACADDR        : M A C A D D R ;
MAP            : M A P ;
MATCH          : M A T C H ;
MATCHED        : M A T C H E D ;
MATERIALIZED   : M A T E R I A L I Z E D ;
MERGE          : M E R G E ;
MINUTE         : M I N U T E ;
MINUTES        : M I N U T E S ;
MINUS          : M I N U S ;
MOD            : M O D ;
MONEY          : M O N E Y ;
MONTH          : M O N T H ;
MONTHS         : M O N T H S ;
MSCK           : M S C K ;
NATURAL        : N A T U R A L ;
NOT            : N O T ;
NULL           : N U L L ;
NULLS          : N U L L S ;
NUMERIC        : N U M E R I C ;
OF             : O F ;
OFFSET         : O F F S E T ;
OID            : O I D ;
ON             : O N ;
ONLY           : O N L Y ;
OR             : O R ;
ORDER          : O R D E R ;
ORDINALITY     : O R D I N A L I T Y ;
OUTER          : O U T E R ;
OVER           : O V E R ;
OVERWRITE      : O V E R W R I T E ;
PARTITION      : P A R T I T I O N ;
PRECEDING      : P R E C E D I N G ;
PRIMARY        : P R I M A R Y ;
PROCEDURE      : P R O C E D U R E ;
QUALIFY        : Q U A L I F Y ;
RANGE          : R A N G E ;
REAL           : R E A L ;
RECORD         : R E C O R D ;
RECURSIVE      : R E C U R S I V E ;
REFERENCES     : R E F E R E N C E S ;
REFRESH        : R E F R E S H ;
REPAIR         : R E P A I R ;
REPLACE        : R E P L A C E ;
RESTRICT       : R E S T R I C T ;
RETURNING      : R E T U R N I N G ;
LEFT           : L E F T ;
RIGHT          : R I G H T ;
RLIKE          : R L I K E ;
ROLLUP         : R O L L U P ;
ROW            : R O W ;
ROWS           : R O W S ;
SAMPLE         : S A M P L E ;
SECOND         : S E C O N D ;
SECONDS        : S E C O N D S ;
SELECT         : S E L E C T ;
SEMI           : S E M I ;
SEQUENCE       : S E Q U E N C E ;
SERIAL         : S E R I A L ;
BIGSERIAL_KW   : B I G S E R I A L ;
SMALLSERIAL    : S M A L L S E R I A L ;
SERDE          : S E R D E ;
SET            : S E T ;
SETS           : S E T S ;
SHOW           : S H O W ;
SMALLINT       : S M A L L I N T ;
SORT           : S O R T ;
STATISTICS     : S T A T I S T I C S ;
STORED         : S T O R E D ;
STRING         : S T R I N G ;
STRUCT         : S T R U C T ;
TABLE          : T A B L E ;
TABLES         : T A B L E S ;
TBLPROPERTIES  : T B L P R O P E R T I E S ;
TEMP           : T E M P ;
TEMPORARY      : T E M P O R A R Y ;
TEXT           : T E X T ;
THEN           : T H E N ;
TIME           : T I M E ;
TIMESTAMP      : T I M E S T A M P ;
TIMESTAMP_TZ   : T I M E S T A M P T Z ;
TINYINT        : T I N Y I N T ;
TO             : T O ;
TRAILING       : T R A I L I N G ;
TRANSFORM      : T R A N S F O R M ;
TRIM           : T R I M ;
TRUE           : T R U E ;
TRY_CAST       : T R Y '_' C A S T ;
TSQUERY        : T S Q U E R Y ;
TSVECTOR       : T S V E C T O R ;
TRUNCATE       : T R U N C A T E ;
TYPE           : T Y P E ;
UNBOUNDED      : U N B O U N D E D ;
UNCACHE        : U N C A C H E ;
UNION          : U N I O N ;
UNIQUE         : U N I Q U E ;
UNNEST         : U N N E S T ;
UPDATE         : U P D A T E ;
USE            : U S E ;
USING          : U S I N G ;
UUID           : U U I D ;
VALUES         : V A L U E S ;
VARBIT         : V A R B I T ;
VARCHAR        : V A R C H A R ;
VIEW           : V I E W ;
VOID           : V O I D ;
WEEK           : W E E K ;
WEEKS          : W E E K S ;
WHEN           : W H E N ;
WHERE          : W H E R E ;
WINDOW         : W I N D O W ;
WITH           : W I T H ;
WITHIN         : W I T H I N ;
YEAR           : Y E A R ;
YEARS          : Y E A R S ;

nonReserved
    : ADD | ALL | ALTER | ANALYZE | ANTI | ARRAY | ASC | AT | BIGINT | BIT | BOOLEAN
    | BOTH | BYTES | BYTEA | BY | CACHE | CALL | CASCADE | CHAR | CHARACTER | CIDR
    | CLUSTER | CODEGEN | COLLECT | COLUMN | COMMENT | COMPUTE | CONCAT | CONSTRAINT
    | COPY | COST | DATA | DATABASE | DATE | DAY | DAYS | DECIMAL | DEFAULT | DEFINED
    | DELETE | DESC | DISTRIBUTE | DIV | DOUBLE | DROP | ESCAPE | EXCHANGE | EXCLUDE
    | EXPLAIN | EXTENDED | EXTERNAL | FETCH | FILTER | FIRST | FLOAT | FOLLOWING
    | FOR | FOREIGN | FORMATTED | FULL | FUNCTION | GROUP | GROUPS | GROUPING | HASH
    | HOUR | HOURS | IF | INDEX | INET | INLINE | INT | INTEGER | INTERSECT
    | INTERVAL | IS | JSON | JSONB | KEY | LANGUAGE | LAST | LATERAL | LEADING
    | LIKE | LIMIT | LIST | LOCATION | MACADDR | MAP | MATCH | MATCHED | MATERIALIZED
    | MINUTE | MINUTES | MINUS | MOD | MONEY | MONTH | MONTHS | MSCK | NATURAL
    | NULLS | NUMERIC | OFFSET | OID | ONLY | ORDINALITY | OUTER | PARTITION
    | PRECEDING | PRIMARY | PROCEDURE | QUALIFY | RANGE | REAL | RECORD | RECURSIVE
    | REFERENCES | REFRESH | REPAIR | REPLACE | RESTRICT | RETURNING | RLIKE | ROLLUP
    | ROWS | SAMPLE | SECOND | SECONDS | SEMI | SEQUENCE | SERIAL | SERDE | SETS
    | SHOW | SMALLINT | SORT | STATISTICS | STORED | STRING | STRUCT | TABLES
    | TBLPROPERTIES | TEMP | TEMPORARY | TEXT | TIME | TIMESTAMP | TIMESTAMP_TZ
    | TINYINT | TO | TRAILING | TRANSFORM | TRIM | TSQUERY | TSVECTOR | TRUNCATE
    | TYPE | UNBOUNDED | UNCACHE | UNIQUE | USE | UUID | VARBIT | VARCHAR | VOID
    | WEEK | WEEKS | WITHIN | YEAR | YEARS
    ;

// Operators
EQ     : '=' ;
NEQ    : '<>' | '!=' ;
LT     : '<' ;
GT     : '>' ;
LTE    : '<=' ;
GTE    : '>=' ;
NSEQ   : '<=>' ;

PLUS         : '+' ;
MINUS_OP     : '-' ;
STAR         : '*' ;
SLASH        : '/' ;
PERCENT      : '%' ;
TILDE        : '~' ;
AMPERSAND    : '&' ;
PIPE         : '|' ;
HAT          : '^' ;
CONCAT_PIPE  : '||' ;
ARROW        : '=>' ;
COLON        : ':' ;
SEMI         : ';' ;
COMMA        : ',' ;
DOT          : '.' ;
LPAREN       : '(' ;
RPAREN       : ')' ;
LBRACKET     : '[' ;
RBRACKET     : ']' ;

// JSONB operators
JSONB_ARROW       : '->' ;
JSONB_DARROW      : '->>' ;
JSONB_HASH_ARROW  : '#>' ;
JSONB_CONTAINS    : '@>' ;
JSONB_CONTAINED_BY: '<@' ;
FULLTEXT_MATCH    : '@@' ;

// Literals
INTEGER_VALUE
    : DIGIT+
    ;

DECIMAL_VALUE
    : DIGIT+ DOT DIGIT*
    | DOT DIGIT+
    ;

FLOAT_VALUE
    : DIGIT+ (DOT DIGIT*)? EXPONENT
    | DOT DIGIT+ EXPONENT
    ;

STRING_LITERAL
    : '\'' ( ~'\'' | '\'\'')* '\''
    | '"' ( ~'"' | '""')* '"'  // double-quote string (non-standard, Hive/Spark compat)
    ;

UNICODE_STRING
    : 'U&' '\'' ( ~'\'' | '\'\'')* '\''
    ;

DOLLAR_QUOTED_STRING
    : '$' TAG? '$' .*? '$' TAG? '$'
    ;

// Identifiers
IDENTIFIER
    : (LETTER | '_') (LETTER | DIGIT | '_')*
    ;

BACKQUOTED_IDENTIFIER
    : '`' (~'`' | '``')* '`'
    ;

DOUBLE_QUOTED_IDENTIFIER
    : '"' (~'"' | '""')* '"'
    ;

// Whitespace and comments
SIMPLE_COMMENT  : '--' ~[\r\n]* '\r'? '\n'? -> channel(HIDDEN) ;
BRACKETED_COMMENT : '/*' .*? '*/' -> channel(HIDDEN) ;
WS : [ \t\r\n]+ -> channel(HIDDEN) ;

// Fragments
fragment DIGIT  : [0-9] ;
fragment LETTER : [a-zA-Z\u4e00-\u9fa5] ;
fragment EXPONENT : [eE] [+-]? DIGIT+ ;
fragment TAG    : [a-zA-Z_]+ ;

// Case-insensitive keyword fragments
fragment A : [aA]; fragment B : [bB]; fragment C : [cC]; fragment D : [dD];
fragment E : [eE]; fragment F : [fF]; fragment G : [gG]; fragment H : [hH];
fragment I : [iI]; fragment J : [jJ]; fragment K : [kK]; fragment L : [lL];
fragment M : [mM]; fragment N : [nN]; fragment O : [oO]; fragment P : [pP];
fragment Q : [qQ]; fragment R : [rR]; fragment S : [sS]; fragment T : [tT];
fragment U : [uU]; fragment V : [vV]; fragment W : [wW]; fragment X : [xX];
fragment Y : [yY]; fragment Z : [zZ];
