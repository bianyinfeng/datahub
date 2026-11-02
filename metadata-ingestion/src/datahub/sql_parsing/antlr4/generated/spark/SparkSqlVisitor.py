# Generated from /home/runner/work/datahub/datahub/metadata-ingestion/src/datahub/sql_parsing/antlr4/grammars/SparkSql.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SparkSqlParser import SparkSqlParser
else:
    from SparkSqlParser import SparkSqlParser

# This class defines a complete generic visitor for a parse tree produced by SparkSqlParser.

class SparkSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SparkSqlParser#sparkQueryStatement.
    def visitSparkQueryStatement(self, ctx:SparkSqlParser.SparkQueryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkInsertStmt.
    def visitSparkInsertStmt(self, ctx:SparkSqlParser.SparkInsertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkMergeStmt.
    def visitSparkMergeStmt(self, ctx:SparkSqlParser.SparkMergeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkCreateTableStmt.
    def visitSparkCreateTableStmt(self, ctx:SparkSqlParser.SparkCreateTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkCreateViewStmt.
    def visitSparkCreateViewStmt(self, ctx:SparkSqlParser.SparkCreateViewStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkDropStmt.
    def visitSparkDropStmt(self, ctx:SparkSqlParser.SparkDropStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkAlterStmt.
    def visitSparkAlterStmt(self, ctx:SparkSqlParser.SparkAlterStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkTruncateStmt.
    def visitSparkTruncateStmt(self, ctx:SparkSqlParser.SparkTruncateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkAnalyzeStmt.
    def visitSparkAnalyzeStmt(self, ctx:SparkSqlParser.SparkAnalyzeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkExplainStmt.
    def visitSparkExplainStmt(self, ctx:SparkSqlParser.SparkExplainStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#cacheTableStmt.
    def visitCacheTableStmt(self, ctx:SparkSqlParser.CacheTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#uncacheTableStmt.
    def visitUncacheTableStmt(self, ctx:SparkSqlParser.UncacheTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#refreshTableStmt.
    def visitRefreshTableStmt(self, ctx:SparkSqlParser.RefreshTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#msckRepairStmt.
    def visitMsckRepairStmt(self, ctx:SparkSqlParser.MsckRepairStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#optimizeStmt.
    def visitOptimizeStmt(self, ctx:SparkSqlParser.OptimizeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#restoreStmt.
    def visitRestoreStmt(self, ctx:SparkSqlParser.RestoreStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#generateStmt.
    def visitGenerateStmt(self, ctx:SparkSqlParser.GenerateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#loadDataStmt.
    def visitLoadDataStmt(self, ctx:SparkSqlParser.LoadDataStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showStmt.
    def visitShowStmt(self, ctx:SparkSqlParser.ShowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#describeStmt.
    def visitDescribeStmt(self, ctx:SparkSqlParser.DescribeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkSetStmt.
    def visitSparkSetStmt(self, ctx:SparkSqlParser.SparkSetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkUseStmt.
    def visitSparkUseStmt(self, ctx:SparkSqlParser.SparkUseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#cacheTableStatement.
    def visitCacheTableStatement(self, ctx:SparkSqlParser.CacheTableStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#uncacheTableStatement.
    def visitUncacheTableStatement(self, ctx:SparkSqlParser.UncacheTableStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#refreshTableStatement.
    def visitRefreshTableStatement(self, ctx:SparkSqlParser.RefreshTableStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#msckRepairStatement.
    def visitMsckRepairStatement(self, ctx:SparkSqlParser.MsckRepairStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#optimizeStatement.
    def visitOptimizeStatement(self, ctx:SparkSqlParser.OptimizeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#restoreStatement.
    def visitRestoreStatement(self, ctx:SparkSqlParser.RestoreStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#generateStatement.
    def visitGenerateStatement(self, ctx:SparkSqlParser.GenerateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#symlink_format_manifest.
    def visitSymlink_format_manifest(self, ctx:SparkSqlParser.Symlink_format_manifestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#loadDataStatement.
    def visitLoadDataStatement(self, ctx:SparkSqlParser.LoadDataStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showTables.
    def visitShowTables(self, ctx:SparkSqlParser.ShowTablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showPartitions.
    def visitShowPartitions(self, ctx:SparkSqlParser.ShowPartitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showColumns.
    def visitShowColumns(self, ctx:SparkSqlParser.ShowColumnsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showCreateTable.
    def visitShowCreateTable(self, ctx:SparkSqlParser.ShowCreateTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#showFunctions.
    def visitShowFunctions(self, ctx:SparkSqlParser.ShowFunctionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#describeTable.
    def visitDescribeTable(self, ctx:SparkSqlParser.DescribeTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#describeQuery.
    def visitDescribeQuery(self, ctx:SparkSqlParser.DescribeQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#fromClause.
    def visitFromClause(self, ctx:SparkSqlParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#lateralView.
    def visitLateralView(self, ctx:SparkSqlParser.LateralViewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tableGeneratingFunction.
    def visitTableGeneratingFunction(self, ctx:SparkSqlParser.TableGeneratingFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnAliasList.
    def visitColumnAliasList(self, ctx:SparkSqlParser.ColumnAliasListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#pivotClause.
    def visitPivotClause(self, ctx:SparkSqlParser.PivotClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#namedExprList.
    def visitNamedExprList(self, ctx:SparkSqlParser.NamedExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#namedExpr.
    def visitNamedExpr(self, ctx:SparkSqlParser.NamedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#pivotValue.
    def visitPivotValue(self, ctx:SparkSqlParser.PivotValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#queryOrganization.
    def visitQueryOrganization(self, ctx:SparkSqlParser.QueryOrganizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#clusterByClause.
    def visitClusterByClause(self, ctx:SparkSqlParser.ClusterByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#distributeByClause.
    def visitDistributeByClause(self, ctx:SparkSqlParser.DistributeByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sortByClause.
    def visitSortByClause(self, ctx:SparkSqlParser.SortByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#createTableStatement.
    def visitCreateTableStatement(self, ctx:SparkSqlParser.CreateTableStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkTableOptions.
    def visitSparkTableOptions(self, ctx:SparkSqlParser.SparkTableOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sparkBucketSpec.
    def visitSparkBucketSpec(self, ctx:SparkSqlParser.SparkBucketSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#transformClause.
    def visitTransformClause(self, ctx:SparkSqlParser.TransformClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#rowFormat.
    def visitRowFormat(self, ctx:SparkSqlParser.RowFormatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#rowFormatField.
    def visitRowFormatField(self, ctx:SparkSqlParser.RowFormatFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnAliasWithType.
    def visitColumnAliasWithType(self, ctx:SparkSqlParser.ColumnAliasWithTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:SparkSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#query.
    def visitQuery(self, ctx:SparkSqlParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#cteDefinition.
    def visitCteDefinition(self, ctx:SparkSqlParser.CteDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#namedQuery.
    def visitNamedQuery(self, ctx:SparkSqlParser.NamedQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#queryTermDefault.
    def visitQueryTermDefault(self, ctx:SparkSqlParser.QueryTermDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#setOperation.
    def visitSetOperation(self, ctx:SparkSqlParser.SetOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#setQuantifier.
    def visitSetQuantifier(self, ctx:SparkSqlParser.SetQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#queryPrimaryDefault.
    def visitQueryPrimaryDefault(self, ctx:SparkSqlParser.QueryPrimaryDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#table.
    def visitTable(self, ctx:SparkSqlParser.TableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#subquery.
    def visitSubquery(self, ctx:SparkSqlParser.SubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#querySpecification.
    def visitQuerySpecification(self, ctx:SparkSqlParser.QuerySpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#selectClause.
    def visitSelectClause(self, ctx:SparkSqlParser.SelectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#selectExpression.
    def visitSelectExpression(self, ctx:SparkSqlParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#selectStar.
    def visitSelectStar(self, ctx:SparkSqlParser.SelectStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#selectQualifiedStar.
    def visitSelectQualifiedStar(self, ctx:SparkSqlParser.SelectQualifiedStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#relation.
    def visitRelation(self, ctx:SparkSqlParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:SparkSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#joinType.
    def visitJoinType(self, ctx:SparkSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#joinCriteria.
    def visitJoinCriteria(self, ctx:SparkSqlParser.JoinCriteriaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tableName.
    def visitTableName(self, ctx:SparkSqlParser.TableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#subqueryRelation.
    def visitSubqueryRelation(self, ctx:SparkSqlParser.SubqueryRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#lateral.
    def visitLateral(self, ctx:SparkSqlParser.LateralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#unnestRelation.
    def visitUnnestRelation(self, ctx:SparkSqlParser.UnnestRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#whereClause.
    def visitWhereClause(self, ctx:SparkSqlParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#groupByClause.
    def visitGroupByClause(self, ctx:SparkSqlParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#havingClause.
    def visitHavingClause(self, ctx:SparkSqlParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#qualifyClause.
    def visitQualifyClause(self, ctx:SparkSqlParser.QualifyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#windowClause.
    def visitWindowClause(self, ctx:SparkSqlParser.WindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#namedWindow.
    def visitNamedWindow(self, ctx:SparkSqlParser.NamedWindowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#groupByItem.
    def visitGroupByItem(self, ctx:SparkSqlParser.GroupByItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#groupByItemList.
    def visitGroupByItemList(self, ctx:SparkSqlParser.GroupByItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#groupByItemSet.
    def visitGroupByItemSet(self, ctx:SparkSqlParser.GroupByItemSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#limitClause.
    def visitLimitClause(self, ctx:SparkSqlParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#sortItem.
    def visitSortItem(self, ctx:SparkSqlParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#insertStatement.
    def visitInsertStatement(self, ctx:SparkSqlParser.InsertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#insertMode.
    def visitInsertMode(self, ctx:SparkSqlParser.InsertModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#partitionSpec.
    def visitPartitionSpec(self, ctx:SparkSqlParser.PartitionSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#partitionVal.
    def visitPartitionVal(self, ctx:SparkSqlParser.PartitionValContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnList.
    def visitColumnList(self, ctx:SparkSqlParser.ColumnListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnAliases.
    def visitColumnAliases(self, ctx:SparkSqlParser.ColumnAliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#valueList.
    def visitValueList(self, ctx:SparkSqlParser.ValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#mergeStatement.
    def visitMergeStatement(self, ctx:SparkSqlParser.MergeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#mergeSource.
    def visitMergeSource(self, ctx:SparkSqlParser.MergeSourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#whenClause.
    def visitWhenClause(self, ctx:SparkSqlParser.WhenClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#mergeAction.
    def visitMergeAction(self, ctx:SparkSqlParser.MergeActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#assignmentList.
    def visitAssignmentList(self, ctx:SparkSqlParser.AssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#assignment.
    def visitAssignment(self, ctx:SparkSqlParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#createViewStatement.
    def visitCreateViewStatement(self, ctx:SparkSqlParser.CreateViewStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#createMaterializedViewStatement.
    def visitCreateMaterializedViewStatement(self, ctx:SparkSqlParser.CreateMaterializedViewStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#dropStatement.
    def visitDropStatement(self, ctx:SparkSqlParser.DropStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#alterStatement.
    def visitAlterStatement(self, ctx:SparkSqlParser.AlterStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#alterTableAction.
    def visitAlterTableAction(self, ctx:SparkSqlParser.AlterTableActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#truncateStatement.
    def visitTruncateStatement(self, ctx:SparkSqlParser.TruncateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#analyzeStatement.
    def visitAnalyzeStatement(self, ctx:SparkSqlParser.AnalyzeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#explainStatement.
    def visitExplainStatement(self, ctx:SparkSqlParser.ExplainStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#setStatement.
    def visitSetStatement(self, ctx:SparkSqlParser.SetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#useStatement.
    def visitUseStatement(self, ctx:SparkSqlParser.UseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnDef.
    def visitColumnDef(self, ctx:SparkSqlParser.ColumnDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnConstraint.
    def visitColumnConstraint(self, ctx:SparkSqlParser.ColumnConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tableConstraint.
    def visitTableConstraint(self, ctx:SparkSqlParser.TableConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#excludeElement.
    def visitExcludeElement(self, ctx:SparkSqlParser.ExcludeElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#partitionBy.
    def visitPartitionBy(self, ctx:SparkSqlParser.PartitionByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#partitionType.
    def visitPartitionType(self, ctx:SparkSqlParser.PartitionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tableProperties.
    def visitTableProperties(self, ctx:SparkSqlParser.TablePropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tableProperty.
    def visitTableProperty(self, ctx:SparkSqlParser.TablePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#propertyKey.
    def visitPropertyKey(self, ctx:SparkSqlParser.PropertyKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#propertyValue.
    def visitPropertyValue(self, ctx:SparkSqlParser.PropertyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnComment.
    def visitColumnComment(self, ctx:SparkSqlParser.ColumnCommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#arrayType.
    def visitArrayType(self, ctx:SparkSqlParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#structType.
    def visitStructType(self, ctx:SparkSqlParser.StructTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#macroDataType.
    def visitMacroDataType(self, ctx:SparkSqlParser.MacroDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#arrayTypeAngle.
    def visitArrayTypeAngle(self, ctx:SparkSqlParser.ArrayTypeAngleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#mapType.
    def visitMapType(self, ctx:SparkSqlParser.MapTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#primitiveType.
    def visitPrimitiveType(self, ctx:SparkSqlParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#baseType.
    def visitBaseType(self, ctx:SparkSqlParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#structField.
    def visitStructField(self, ctx:SparkSqlParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#expression.
    def visitExpression(self, ctx:SparkSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#passThrough.
    def visitPassThrough(self, ctx:SparkSqlParser.PassThroughContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#logicalNot.
    def visitLogicalNot(self, ctx:SparkSqlParser.LogicalNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#exists.
    def visitExists(self, ctx:SparkSqlParser.ExistsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#logicalBinary.
    def visitLogicalBinary(self, ctx:SparkSqlParser.LogicalBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#bitwiseBinary.
    def visitBitwiseBinary(self, ctx:SparkSqlParser.BitwiseBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#comparison.
    def visitComparison(self, ctx:SparkSqlParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#jsonDoubleArrow.
    def visitJsonDoubleArrow(self, ctx:SparkSqlParser.JsonDoubleArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#like.
    def visitLike(self, ctx:SparkSqlParser.LikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#inSubquery.
    def visitInSubquery(self, ctx:SparkSqlParser.InSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#valueExprDefault.
    def visitValueExprDefault(self, ctx:SparkSqlParser.ValueExprDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#bitwiseXor.
    def visitBitwiseXor(self, ctx:SparkSqlParser.BitwiseXorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#jsonContainedBy.
    def visitJsonContainedBy(self, ctx:SparkSqlParser.JsonContainedByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#jsonArrow.
    def visitJsonArrow(self, ctx:SparkSqlParser.JsonArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#rlike.
    def visitRlike(self, ctx:SparkSqlParser.RlikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#jsonContains.
    def visitJsonContains(self, ctx:SparkSqlParser.JsonContainsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#jsonHashArrow.
    def visitJsonHashArrow(self, ctx:SparkSqlParser.JsonHashArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#fulltextMatch.
    def visitFulltextMatch(self, ctx:SparkSqlParser.FulltextMatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#isNull.
    def visitIsNull(self, ctx:SparkSqlParser.IsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#ilike.
    def visitIlike(self, ctx:SparkSqlParser.IlikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#unaryArithmetic.
    def visitUnaryArithmetic(self, ctx:SparkSqlParser.UnaryArithmeticContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#arithmeticBinary.
    def visitArithmeticBinary(self, ctx:SparkSqlParser.ArithmeticBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#inList.
    def visitInList(self, ctx:SparkSqlParser.InListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#isDistinctFrom.
    def visitIsDistinctFrom(self, ctx:SparkSqlParser.IsDistinctFromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#between.
    def visitBetween(self, ctx:SparkSqlParser.BetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#timestampLiteral.
    def visitTimestampLiteral(self, ctx:SparkSqlParser.TimestampLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#struct.
    def visitStruct(self, ctx:SparkSqlParser.StructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#dereference.
    def visitDereference(self, ctx:SparkSqlParser.DereferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#macroVarExpr.
    def visitMacroVarExpr(self, ctx:SparkSqlParser.MacroVarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#star.
    def visitStar(self, ctx:SparkSqlParser.StarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#subscript.
    def visitSubscript(self, ctx:SparkSqlParser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#columnRef.
    def visitColumnRef(self, ctx:SparkSqlParser.ColumnRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#searched_case.
    def visitSearched_case(self, ctx:SparkSqlParser.Searched_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#filterExpr.
    def visitFilterExpr(self, ctx:SparkSqlParser.FilterExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#cast.
    def visitCast(self, ctx:SparkSqlParser.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#extract.
    def visitExtract(self, ctx:SparkSqlParser.ExtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#array.
    def visitArray(self, ctx:SparkSqlParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#literalExpr.
    def visitLiteralExpr(self, ctx:SparkSqlParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#parenthesized.
    def visitParenthesized(self, ctx:SparkSqlParser.ParenthesizedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#windowExpr.
    def visitWindowExpr(self, ctx:SparkSqlParser.WindowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#interval.
    def visitInterval(self, ctx:SparkSqlParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#funcCall.
    def visitFuncCall(self, ctx:SparkSqlParser.FuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#simple_case.
    def visitSimple_case(self, ctx:SparkSqlParser.Simple_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#map.
    def visitMap(self, ctx:SparkSqlParser.MapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#scalarSubquery.
    def visitScalarSubquery(self, ctx:SparkSqlParser.ScalarSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#tryCast.
    def visitTryCast(self, ctx:SparkSqlParser.TryCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#whenClauseExpr.
    def visitWhenClauseExpr(self, ctx:SparkSqlParser.WhenClauseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#functionCall.
    def visitFunctionCall(self, ctx:SparkSqlParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#namedArgument.
    def visitNamedArgument(self, ctx:SparkSqlParser.NamedArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#arrayExpression.
    def visitArrayExpression(self, ctx:SparkSqlParser.ArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#mapExpression.
    def visitMapExpression(self, ctx:SparkSqlParser.MapExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#windowRef.
    def visitWindowRef(self, ctx:SparkSqlParser.WindowRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#windowSpecExpr.
    def visitWindowSpecExpr(self, ctx:SparkSqlParser.WindowSpecExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#windowFrame.
    def visitWindowFrame(self, ctx:SparkSqlParser.WindowFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#frameBound.
    def visitFrameBound(self, ctx:SparkSqlParser.FrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#intervalField.
    def visitIntervalField(self, ctx:SparkSqlParser.IntervalFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:SparkSqlParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#qualifiedIdentifier.
    def visitQualifiedIdentifier(self, ctx:SparkSqlParser.QualifiedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#macroOrIdentifier.
    def visitMacroOrIdentifier(self, ctx:SparkSqlParser.MacroOrIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#macroVar.
    def visitMacroVar(self, ctx:SparkSqlParser.MacroVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#identifier.
    def visitIdentifier(self, ctx:SparkSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#strictIdentifier.
    def visitStrictIdentifier(self, ctx:SparkSqlParser.StrictIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#nullLiteral.
    def visitNullLiteral(self, ctx:SparkSqlParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#boolLiteral.
    def visitBoolLiteral(self, ctx:SparkSqlParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#intLiteral.
    def visitIntLiteral(self, ctx:SparkSqlParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#decLiteral.
    def visitDecLiteral(self, ctx:SparkSqlParser.DecLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#floatLiteral.
    def visitFloatLiteral(self, ctx:SparkSqlParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#strLiteral.
    def visitStrLiteral(self, ctx:SparkSqlParser.StrLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#dollarLiteral.
    def visitDollarLiteral(self, ctx:SparkSqlParser.DollarLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:SparkSqlParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#stringLiteral.
    def visitStringLiteral(self, ctx:SparkSqlParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparkSqlParser#nonReserved.
    def visitNonReserved(self, ctx:SparkSqlParser.NonReservedContext):
        return self.visitChildren(ctx)



del SparkSqlParser