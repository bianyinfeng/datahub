/**
 * OpenGaussSql.g4 - OpenGauss/PostgreSQL dialect grammar extending SqlBase.
 *
 * Extensions beyond SqlBase:
 *  - COPY FROM / COPY TO (stdin/stdout/file)
 *  - CREATE/ALTER SEQUENCE
 *  - Full-text search: tsvector, tsquery, @@ operator, to_tsvector(), plainto_tsquery()
 *  - JSONB operators: ->, ->>, #>, @>, <@
 *  - CREATE TABLE ... PARTITION BY RANGE/LIST/HASH with partition clauses
 *  - CREATE/ALTER/REFRESH MATERIALIZED VIEW
 *  - CREATE/DROP INDEX CONCURRENTLY ... USING GIN/GiST/BRIN/BTREE
 *  - RETURNING clause in INSERT/UPDATE/DELETE
 *  - CREATE OR REPLACE FUNCTION / PROCEDURE ... LANGUAGE plpgsql
 *  - DO $$ ... $$ anonymous block
 *  - VACUUM / REINDEX / CLUSTER TABLE
 *  - LOCK TABLE
 *  - LISTEN / NOTIFY
 *  - SAVEPOINT / RELEASE / ROLLBACK TO
 *  - SELECT ... FOR UPDATE / SHARE
 *  - FETCH from cursor
 *  - Macro variable {macro_var} supported everywhere via SqlBase
 */
grammar OpenGaussSql;

import SqlBase;

// ============================================================
// Override statement rule
// ============================================================

statement
    : query (forClause)?                                               # ogQueryStatement
    | cteDefinition? insertStatement returningClause?                 # ogInsertStmt
    | updateStatement returningClause?                                # ogUpdateStmt
    | deleteStatement returningClause?                                # ogDeleteStmt
    | cteDefinition? mergeStatement                                    # ogMergeStmt
    | createTableStatement                                             # ogCreateTableStmt
    | createViewStatement                                              # ogCreateViewStmt
    | createMaterializedViewStatement                                  # ogCreateMatViewStmt
    | refreshMaterializedViewStatement                                 # ogRefreshMatViewStmt
    | createIndexStatement                                             # ogCreateIndexStmt
    | dropStatement                                                    # ogDropStmt
    | alterStatement                                                   # ogAlterStmt
    | truncateStatement                                                # ogTruncateStmt
    | analyzeStatement                                                 # ogAnalyzeStmt
    | explainStatement                                                 # ogExplainStmt
    | copyStatement                                                    # ogCopyStmt
    | createSequenceStatement                                          # ogCreateSeqStmt
    | alterSequenceStatement                                           # ogAlterSeqStmt
    | createFunctionStatement                                          # ogCreateFuncStmt
    | createProcedureStatement                                         # ogCreateProcStmt
    | doStatement                                                      # ogDoStmt
    | vacuumStatement                                                  # ogVacuumStmt
    | reindexStatement                                                 # ogReindexStmt
    | lockStatement                                                    # ogLockStmt
    | listenStatement                                                  # ogListenStmt
    | notifyStatement                                                  # ogNotifyStmt
    | savepointStatement                                               # ogSavepointStmt
    | transactionStatement                                             # ogTransactionStmt
    | setStatement                                                     # ogSetStmt
    | useStatement                                                     # ogUseStmt
    | showStatement                                                    # ogShowStmt
    ;

// ============================================================
// OpenGauss-specific DML
// ============================================================

updateStatement
    : (WITH RECURSIVE? namedQuery (COMMA namedQuery)*)?
      UPDATE ONLY? target=macroOrIdentifier (AS? alias=identifier)?
      SET assignmentList
      (FROM relation (COMMA relation)*)?
      (WHERE expression | WHERE CURRENT OF identifier)?
    ;

deleteStatement
    : (WITH RECURSIVE? namedQuery (COMMA namedQuery)*)?
      DELETE FROM ONLY? target=macroOrIdentifier (AS? alias=identifier)?
      (USING relation (COMMA relation)*)?
      (WHERE expression | WHERE CURRENT OF identifier)?
    ;

returningClause
    : RETURNING selectItem (COMMA selectItem)*
    ;

forClause
    : FOR (UPDATE | SHARE | NO KEY UPDATE | KEY SHARE)
      (OF macroOrIdentifier (COMMA macroOrIdentifier)*)?
      (NOWAIT | SKIP LOCKED)?
    ;

// ============================================================
// COPY
// ============================================================

copyStatement
    : COPY macroOrIdentifier (LPAREN identifier (COMMA identifier)* RPAREN)?
      (FROM | TO) copySource copyOptions?
    | COPY LPAREN statement RPAREN TO copySource copyOptions?
    ;

copySource
    : stringLiteral
    | STDIN
    | STDOUT
    | PROGRAM stringLiteral
    ;

copyOptions
    : WITH? LPAREN copyOption (COMMA copyOption)* RPAREN
    | (BINARY | DELIMITER stringLiteral | NULL stringLiteral
       | CSV (HEADER)? (QUOTE stringLiteral)?
         (ESCAPE stringLiteral)? (FORCE (NOT)? NULL identifier (COMMA identifier)*)?
       | ENCODING stringLiteral)*
    ;

copyOption
    : FORMAT identifier
    | DELIMITER stringLiteral
    | NULL stringLiteral
    | HEADER booleanLiteral?
    | QUOTE stringLiteral
    | ESCAPE stringLiteral
    | ENCODING stringLiteral
    | FREEZE booleanLiteral?
    | FORCE_NULL columnList
    | FORCE_NOT_NULL columnList
    | BINARY
    | OID
    ;

// ============================================================
// SEQUENCE
// ============================================================

createSequenceStatement
    : CREATE (TEMP | TEMPORARY)? SEQUENCE (IF NOT EXISTS)? macroOrIdentifier
      sequenceOption*
    ;

alterSequenceStatement
    : ALTER SEQUENCE (IF EXISTS)? macroOrIdentifier sequenceOption+
    | ALTER SEQUENCE (IF EXISTS)? macroOrIdentifier OWNED BY (macroOrIdentifier | NONE)
    ;

sequenceOption
    : START (WITH)? INTEGER_VALUE
    | INCREMENT (BY)? INTEGER_VALUE
    | MAXVALUE INTEGER_VALUE
    | NO MAXVALUE
    | MINVALUE INTEGER_VALUE
    | NO MINVALUE
    | CACHE INTEGER_VALUE
    | CYCLE
    | NO CYCLE
    | OWNED BY macroOrIdentifier
    ;

// ============================================================
// CREATE INDEX
// ============================================================

createIndexStatement
    : CREATE UNIQUE? INDEX CONCURRENTLY? (IF NOT EXISTS)?
      name=identifier?
      ON ONLY? table=macroOrIdentifier
      (USING method=identifier)?
      LPAREN indexElement (COMMA indexElement)* RPAREN
      (INCLUDE LPAREN identifier (COMMA identifier)* RPAREN)?
      (WITH LPAREN tableProperty (COMMA tableProperty)* RPAREN)?
      (TABLESPACE identifier)?
      (WHERE expression)?
    ;

indexElement
    : expression (opclass=identifier)? (ASC | DESC)?
      (NULLS (FIRST | LAST))?
    ;

// ============================================================
// REFRESH MATERIALIZED VIEW
// ============================================================

refreshMaterializedViewStatement
    : REFRESH MATERIALIZED VIEW CONCURRENTLY? macroOrIdentifier
      (WITH (NO)? DATA)?
    ;

// ============================================================
// CREATE FUNCTION / PROCEDURE
// ============================================================

createFunctionStatement
    : CREATE (OR REPLACE)? FUNCTION (IF NOT EXISTS)?
      funcName=macroOrIdentifier
      LPAREN (funcParam (COMMA funcParam)*)? RPAREN
      (RETURNS returnType=dataType | RETURNS TABLE LPAREN funcParam (COMMA funcParam)* RPAREN)?
      funcBody+
    ;

createProcedureStatement
    : CREATE (OR REPLACE)? PROCEDURE (IF NOT EXISTS)?
      procName=macroOrIdentifier
      LPAREN (funcParam (COMMA funcParam)*)? RPAREN
      funcBody+
    ;

funcParam
    : (paramMode)? (paramName=identifier)? dataType (DEFAULT expression)?
    ;

paramMode : IN | OUT | INOUT | VARIADIC ;

funcBody
    : LANGUAGE identifier
    | AS funcBodyDef (COMMA funcBodyDef)?
    | TRANSFORM FOR TYPE dataType (COMMA FOR TYPE dataType)*
    | WINDOW
    | (IMMUTABLE | STABLE | VOLATILE)
    | (CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT)
    | (EXTERNAL)? SECURITY (INVOKER | DEFINER)
    | PARALLEL (UNSAFE | RESTRICTED | SAFE)
    | COST INTEGER_VALUE
    | ROWS INTEGER_VALUE
    | SET identifier (TO | EQ) expression
    | SET identifier FROM CURRENT
    | RESET identifier
    | RESET ALL
    ;

funcBodyDef
    : stringLiteral
    | DOLLAR_QUOTED_STRING
    ;

// ============================================================
// DO block (anonymous function)
// ============================================================

doStatement
    : DO (LANGUAGE identifier)? (stringLiteral | DOLLAR_QUOTED_STRING)
    ;

// ============================================================
// Maintenance statements
// ============================================================

vacuumStatement
    : VACUUM (FULL)? (FREEZE)? (VERBOSE)? (ANALYZE)?
      (macroOrIdentifier (LPAREN identifier (COMMA identifier)* RPAREN)?)?
    ;

reindexStatement
    : REINDEX (INDEX | TABLE | SCHEMA | DATABASE | SYSTEM) CONCURRENTLY?
      macroOrIdentifier
    ;

lockStatement
    : LOCK TABLE? macroOrIdentifier (COMMA macroOrIdentifier)*
      (IN lockMode MODE)? (NOWAIT)?
    ;

lockMode
    : ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE
    | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE
    ;

listenStatement  : LISTEN identifier ;
notifyStatement  : NOTIFY identifier (COMMA stringLiteral)? ;

savepointStatement
    : SAVEPOINT identifier
    | RELEASE (SAVEPOINT)? identifier
    | ROLLBACK (WORK | TRANSACTION)? TO (SAVEPOINT)? identifier
    ;

transactionStatement
    : BEGIN (WORK | TRANSACTION)? transactionMode*
    | COMMIT (WORK | TRANSACTION)? (AND (NO)? CHAIN)?
    | ROLLBACK (WORK | TRANSACTION)? (AND (NO)? CHAIN)?
    | START TRANSACTION transactionMode*
    ;

transactionMode
    : ISOLATION LEVEL isolationLevel
    | (READ WRITE | READ ONLY)
    | (NOT)? DEFERRABLE
    ;

isolationLevel
    : SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED
    ;

showStatement
    : SHOW identifier
    | SHOW ALL
    | SHOW TRANSACTION ISOLATION LEVEL
    ;

// ============================================================
// Override createTableStatement for OpenGauss partitioning
// ============================================================

createTableStatement
    : CREATE (UNLOGGED)? TABLE (IF NOT EXISTS)?
      tableName=macroOrIdentifier
      (LPAREN columnDef (COMMA columnDef)* (COMMA tableConstraint)* RPAREN)?
      tableProperties?
      ogPartitionBy?
      ogInheritClause?
      (WITH LPAREN tableProperty (COMMA tableProperty)* RPAREN)?
      (WITHOUT OIDS)?
      (TABLESPACE identifier)?
    | CREATE (UNLOGGED)? TABLE (IF NOT EXISTS)?
      tableName=macroOrIdentifier
      (LPAREN columnDef (COMMA columnDef)* (COMMA tableConstraint)* RPAREN)?
      AS query
      (WITH (NO)? DATA)?
    ;

ogPartitionBy
    : PARTITION BY (RANGE | LIST | HASH)
      LPAREN expression (COMMA expression)* RPAREN
      (ogPartitionDef (COMMA ogPartitionDef)*)?
    ;

ogPartitionDef
    : PARTITION identifier
      ( VALUES LESS THAN LPAREN expression (COMMA expression)* RPAREN
      | VALUES IN LPAREN expression (COMMA expression)* RPAREN
      | VALUES WITH LPAREN INTEGER_VALUE RPAREN
      )
      (TABLESPACE identifier)?
      (ogPartitionDef (COMMA ogPartitionDef)*)?
    ;

ogInheritClause
    : INHERITS LPAREN macroOrIdentifier (COMMA macroOrIdentifier)* RPAREN
    ;

// ============================================================
// Override expressions to support OpenGauss-specific ops
// ============================================================

valueExpression
    : primaryExpression                                                # ogValueExprDefault
    | operator=(MINUS | PLUS | TILDE) valueExpression                 # ogUnaryArithmetic
    | left=valueExpression op=HAT right=valueExpression               # ogBitwiseXor
    | left=valueExpression
      op=(STAR | SLASH | PERCENT | DIV | MOD)
      right=valueExpression                                            # ogArithmeticBinary
    | left=valueExpression
      op=(PLUS | MINUS | CONCAT_PIPE | TYPECAST)
      right=valueExpression                                            # ogArithmeticBinary2
    | left=valueExpression
      op=(AMPERSAND | PIPE)
      right=valueExpression                                            # ogBitwiseBinary
    | left=valueExpression comparisonOperator right=valueExpression   # ogComparison
    | valueExpression NOT? BETWEEN lo=valueExpression
      AND hi=valueExpression                                           # ogBetween
    | valueExpression NOT? IN LPAREN expression (COMMA expression)* RPAREN # ogInList
    | valueExpression NOT? IN LPAREN query RPAREN                     # ogInSubquery
    | valueExpression NOT? LIKE pattern=valueExpression
      (ESCAPE escape=valueExpression)?                                 # ogLike
    | valueExpression NOT? ILIKE pattern=valueExpression              # ogIlike
    | valueExpression NOT? SIMILAR TO pattern=valueExpression         # ogSimilar
    | valueExpression IS NOT? NULL                                     # ogIsNull
    | valueExpression IS NOT? DISTINCT FROM valueExpression           # ogIsDistinct
    | valueExpression TYPECAST dataType                               # castOp
    | valueExpression JSONB_ARROW valueExpression                      # ogJsonArrow
    | valueExpression JSONB_DARROW valueExpression                     # ogJsonDoubleArrow
    | valueExpression JSONB_HASH_ARROW valueExpression                 # ogJsonHashArrow
    | valueExpression JSONB_HASH_DARROW valueExpression                # ogJsonHashDarrow
    | valueExpression JSONB_CONTAINS valueExpression                   # ogJsonContains
    | valueExpression JSONB_CONTAINED_BY valueExpression               # ogJsonContainedBy
    | valueExpression JSONB_DELETE_KEY valueExpression                 # ogJsonDeleteKey
    | valueExpression FULLTEXT_MATCH valueExpression                   # ogFulltextMatch
    | valueExpression FULLTEXT_MATCH_PARTIAL valueExpression           # ogFulltextMatchPartial
    | ARRAY arrayLiteralExpr                                          # ogArrayLiteral
    | ROW LPAREN expression (COMMA expression)* RPAREN                # ogRowLiteral
    ;

arrayLiteralExpr
    : LBRACKET (expression (COMMA expression)*)? RBRACKET
    | LBRACKET arrayLiteralExpr (COMMA arrayLiteralExpr)* RBRACKET
    ;

// ============================================================
// OpenGauss-specific operators
// ============================================================

TYPECAST             : '::' ;
JSONB_HASH_DARROW    : '#>>' ;
JSONB_DELETE_KEY     : '#-' ;
FULLTEXT_MATCH_PARTIAL: '@@@' ;

// ============================================================
// OpenGauss-specific keywords
// ============================================================

ACCESS           : A C C E S S ;
BEGIN_KW         : B E G I N ;
BINARY           : B I N A R Y ;
CACHE            : C A C H E ;
CALLED           : C A L L E D ;
CHAIN            : C H A I N ;
COMMITTED        : C O M M I T T E D ;
CONCURRENTLY     : C O N C U R R E N T L Y ;
COST             : C O S T ;
CURRENT_OF       : C U R R E N T ' ' O F ;
CYCLE            : C Y C L E ;
DEFINER          : D E F I N E R ;
DEFERRABLE       : D E F E R R A B L E ;
DO               : D O ;
EXCLUSIVE        : E X C L U S I V E ;
FORCE_NOT_NULL   : F O R C E '_' N O T '_' N U L L ;
FORCE_NULL       : F O R C E '_' N U L L ;
FREEZE           : F R E E Z E ;
FULL             : F U L L ;
IMMUTABLE        : I M M U T A B L E ;
INCLUDE          : I N C L U D E ;
INHERITS         : I N H E R I T S ;
INPUT_KW         : I N P U T ;
INOUT            : I N O U T ;
INVOKER          : I N V O K E R ;
ISOLATION        : I S O L A T I O N ;
KEY_SHARE        : K E Y ' ' S H A R E ;
LANGUAGE         : L A N G U A G E ;
LEVEL            : L E V E L ;
LISTEN           : L I S T E N ;
LOCKED           : L O C K E D ;
LOCK_KW          : L O C K ;
MAXVALUE         : M A X V A L U E ;
MINVALUE         : M I N V A L U E ;
MODE             : M O D E ;
NO               : N O ;
NONE             : N O N E ;
NOTIFY           : N O T I F Y ;
NOWAIT           : N O W A I T ;
OIDS             : O I D S ;
OUT              : O U T ;
OWNED            : O W N E D ;
PARALLEL         : P A R A L L E L ;
PROGRAM          : P R O G R A M ;
READ             : R E A D ;
REINDEX          : R E I N D E X ;
RELEASE          : R E L E A S E ;
REPEATABLE       : R E P E A T A B L E ;
RESET            : R E S E T ;
ROLLBACK         : R O L L B A C K ;
ROWS             : R O W S ;
SAFE             : S A F E ;
SAVEPOINT        : S A V E P O I N T ;
SCHEMA           : S C H E M A ;
SECURITY         : S E C U R I T Y ;
SERIALIZABLE     : S E R I A L I Z A B L E ;
SHARE            : S H A R E ;
SIMILAR          : S I M I L A R ;
SKIP_KW          : S K I P ;
STABLE           : S T A B L E ;
START            : S T A R T ;
STDIN            : S T D I N ;
STDOUT           : S T D O U T ;
STRICT_KW        : S T R I C T ;
SYSTEM           : S Y S T E M ;
TABLESPACE       : T A B L E S P A C E ;
TRANSACTION      : T R A N S A C T I O N ;
TYPE             : T Y P E ;
UNCOMMITTED      : U N C O M M I T T E D ;
UNLOGGED         : U N L O G G E D ;
UNSAFE           : U N S A F E ;
UPDATE           : U P D A T E ;
VACUUM           : V A C U U M ;
VARIADIC         : V A R I A D I C ;
VERBOSE          : V E R B O S E ;
VOLATILE         : V O L A T I L E ;
WINDOW           : W I N D O W ;
WITHOUT          : W I T H O U T ;
WORK             : W O R K ;
WRITE            : W R I T E ;
