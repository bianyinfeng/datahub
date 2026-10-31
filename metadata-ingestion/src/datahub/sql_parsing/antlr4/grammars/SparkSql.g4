/**
 * SparkSql.g4 - Spark SQL dialect grammar extending SqlBase.
 *
 * Extensions:
 *  - LATERAL VIEW [OUTER] EXPLODE / POSEXPLODE / JSON_TUPLE
 *  - TRANSFORM ... USING
 *  - CLUSTER BY / DISTRIBUTE BY / SORT BY
 *  - CACHE TABLE / UNCACHE TABLE / REFRESH TABLE
 *  - MSCK REPAIR TABLE
 *  - INSERT OVERWRITE DIRECTORY
 *  - CREATE TABLE USING <format> (Delta Lake, Iceberg, Parquet, ORC, etc.)
 *  - GENERATE (Delta Lake)
 *  - OPTIMIZE TABLE (Delta Lake)
 *  - RESTORE TABLE (Delta Lake)
 *  - SHOW PARTITIONS / SHOW COLUMNS / SHOW TABLES
 *  - DESCRIBE TABLE / DESCRIBE QUERY
 *  - LOAD DATA [LOCAL] INPATH
 *  - Macro variable {macro_var} supported everywhere via SqlBase
 */
grammar SparkSql;

import SqlBase;

// ============================================================
// Override / extend statement rule
// ============================================================

statement
    : query                                                            # sparkQueryStatement
    | cteDefinition? insertStatement                                   # sparkInsertStmt
    | cteDefinition? mergeStatement                                    # sparkMergeStmt
    | createTableStatement                                             # sparkCreateTableStmt
    | createViewStatement                                              # sparkCreateViewStmt
    | dropStatement                                                    # sparkDropStmt
    | alterStatement                                                   # sparkAlterStmt
    | truncateStatement                                                # sparkTruncateStmt
    | analyzeStatement                                                 # sparkAnalyzeStmt
    | explainStatement                                                 # sparkExplainStmt
    | cacheTableStatement                                              # cacheTableStmt
    | uncacheTableStatement                                            # uncacheTableStmt
    | refreshTableStatement                                            # refreshTableStmt
    | msckRepairStatement                                              # msckRepairStmt
    | optimizeStatement                                                # optimizeStmt
    | restoreStatement                                                 # restoreStmt
    | generateStatement                                                # generateStmt
    | loadDataStatement                                                # loadDataStmt
    | showStatement                                                    # showStmt
    | describeStatement                                                # describeStmt
    | setStatement                                                     # sparkSetStmt
    | useStatement                                                     # sparkUseStmt
    ;

// ============================================================
// Spark-specific DDL / utility statements
// ============================================================

cacheTableStatement
    : CACHE (LAZY)? TABLE macroOrIdentifier (AS? query)?
    ;

uncacheTableStatement
    : UNCACHE TABLE (IF EXISTS)? macroOrIdentifier
    ;

refreshTableStatement
    : REFRESH (TABLE)? macroOrIdentifier
    ;

msckRepairStatement
    : MSCK REPAIR TABLE macroOrIdentifier
    ;

optimizeStatement
    : OPTIMIZE macroOrIdentifier
      (WHERE expression)?
      (ZORDER BY qualifiedIdentifier (COMMA qualifiedIdentifier)*)?
    ;

restoreStatement
    : RESTORE TABLE? macroOrIdentifier TO VERSION AS OF expression
    | RESTORE TABLE? macroOrIdentifier TO TIMESTAMP AS OF expression
    ;

generateStatement
    : GENERATE symlink_format_manifest FOR TABLE macroOrIdentifier
    ;

symlink_format_manifest
    : SYMLINK_FORMAT_MANIFEST
    ;

loadDataStatement
    : LOAD DATA LOCAL? INPATH stringLiteral OVERWRITE?
      INTO TABLE macroOrIdentifier partitionSpec?
    ;

showStatement
    : SHOW TABLES (IN identifier)? (LIKE stringLiteral)?              # showTables
    | SHOW PARTITIONS macroOrIdentifier (partitionSpec)?              # showPartitions
    | SHOW COLUMNS (FROM | IN) macroOrIdentifier                      # showColumns
    | SHOW CREATE TABLE macroOrIdentifier                             # showCreateTable
    | SHOW FUNCTIONS (LIKE stringLiteral)?                            # showFunctions
    ;

describeStatement
    : DESCRIBE (TABLE)? (EXTENDED | FORMATTED)?
      macroOrIdentifier partitionSpec?
      (identifier)?                                                    # describeTable
    | DESCRIBE (QUERY)? statement                                      # describeQuery
    ;

// ============================================================
// Override FROM clause to add Spark lateral views
// ============================================================

fromClause
    : FROM relation lateralView* pivotClause?
    ;

lateralView
    : LATERAL VIEW (OUTER)? tableGeneratingFunction AS alias=identifier
      (COMMA? columnAliasList)?
    | LATERAL VIEW (OUTER)? tableGeneratingFunction identifier
      AS columnAliasList
    ;

tableGeneratingFunction
    : funcName=identifier
      LPAREN (expression (COMMA expression)*)? RPAREN
    ;

columnAliasList
    : identifier (COMMA identifier)*
    ;

pivotClause
    : PIVOT LPAREN
        aggregates=namedExprList
        FOR pivotColumn=identifier
        IN LPAREN pivotValues+=pivotValue (COMMA pivotValues+=pivotValue)* RPAREN
      RPAREN
    ;

namedExprList : namedExpr (COMMA namedExpr)* ;
namedExpr     : expression (AS? identifier)? ;
pivotValue    : expression (AS? identifier)? ;

// ============================================================
// Override queryOrganization to add Spark ordering extensions
// ============================================================

queryOrganization
    : clusterByClause?
    | distributeByClause? sortByClause?
    | (ORDER BY sortItem (COMMA sortItem)*)?
      (LIMIT limit=(expression | ALL))?
      (OFFSET offset=expression)?
    ;

clusterByClause   : CLUSTER BY expression (COMMA expression)* ;
distributeByClause: DISTRIBUTE BY expression (COMMA expression)* ;
sortByClause      : SORT BY sortItem (COMMA sortItem)* ;

// ============================================================
// Override createTableStatement for Spark/Delta/Iceberg
// ============================================================

createTableStatement
    : CREATE (OR REPLACE)? (TEMPORARY | TEMP)?
      TABLE (IF NOT EXISTS)?
      tableName=macroOrIdentifier
      (LPAREN columnDef (COMMA columnDef)* (COMMA tableConstraint)* RPAREN)?
      (USING provider=identifier)?
      tableProperties?
      sparkTableOptions?
      partitionBy?
      sparkBucketSpec?
      (LOCATION location=stringLiteral)?
      (COMMENT comment=stringLiteral)?
      (AS query)?
    ;

sparkTableOptions
    : OPTIONS LPAREN tableProperty (COMMA tableProperty)* RPAREN
    ;

sparkBucketSpec
    : CLUSTERED BY
      LPAREN identifier (COMMA identifier)* RPAREN
      (SORTED BY LPAREN sortItem (COMMA sortItem)* RPAREN)?
      INTO INTEGER_VALUE BUCKETS
    ;

// ============================================================
// Spark TRANSFORM statement
// ============================================================

transformClause
    : TRANSFORM LPAREN expression (COMMA expression)* RPAREN
      (ROW FORMAT rowFormat)?
      USING stringLiteral
      (AS LPAREN columnAliasWithType (COMMA columnAliasWithType)* RPAREN)?
      (ROW FORMAT rowFormat)?
    ;

rowFormat
    : DELIMITED rowFormatField*
    | SERDE stringLiteral (WITH SERDEPROPERTIES LPAREN tableProperty (COMMA tableProperty)* RPAREN)?
    ;

rowFormatField
    : FIELDS TERMINATED BY stringLiteral (ESCAPED BY stringLiteral)?
    | COLLECTION ITEMS TERMINATED BY stringLiteral
    | MAP KEYS TERMINATED BY stringLiteral
    | LINES TERMINATED BY stringLiteral
    | NULL DEFINED AS stringLiteral
    ;

columnAliasWithType
    : identifier dataType?
    ;

// ============================================================
// Spark-specific keywords
// ============================================================

ANTI            : A N T I ;
BUCKETS         : B U C K E T S ;
CACHE           : C A C H E ;
CLUSTER         : C L U S T E R ;
CLUSTERED       : C L U S T E R E D ;
CODEGEN         : C O D E G E N ;
COLLECTION      : C O L L E C T I O N ;
COST            : C O S T ;
DELIMITED       : D E L I M I T E D ;
DESCRIBE        : D E S C R I B E ;
DISTRIBUTE      : D I S T R I B U T E ;
ESCAPED         : E S C A P E D ;
FIELDS          : F I E L D S ;
FORMATTED       : F O R M A T T E D ;
FUNCTIONS       : F U N C T I O N S ;
GENERATE        : G E N E R A T E ;
INPATH          : I N P A T H ;
ITEMS           : I T E M S ;
KEYS            : K E Y S ;
LAZY            : L A Z Y ;
LINES           : L I N E S ;
LOAD            : L O A D ;
LOCAL           : L O C A L ;
MSCK            : M S C K ;
OPTIONS         : O P T I O N S ;
OPTIMIZE        : O P T I M I Z E ;
OUTER           : O U T E R ;
PIVOT           : P I V O T ;
REPAIR          : R E P A I R ;
REFRESH         : R E F R E S H ;
RESTORE         : R E S T O R E ;
SERDEPROPERTIES : S E R D E P R O P E R T I E S ;
SHOW            : S H O W ;
SORT            : S O R T ;
SORTED          : S O R T E D ;
SYMLINK_FORMAT_MANIFEST : S Y M L I N K '_' F O R M A T '_' M A N I F E S T ;
TERMINATED      : T E R M I N A T E D ;
UNCACHE         : U N C A C H E ;
VERSION         : V E R S I O N ;
ZORDER          : Z O R D E R ;
