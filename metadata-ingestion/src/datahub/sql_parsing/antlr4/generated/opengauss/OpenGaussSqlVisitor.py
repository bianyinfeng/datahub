# Generated from /home/runner/work/datahub/datahub/metadata-ingestion/src/datahub/sql_parsing/antlr4/grammars/OpenGaussSql.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OpenGaussSqlParser import OpenGaussSqlParser
else:
    from OpenGaussSqlParser import OpenGaussSqlParser

# This class defines a complete generic visitor for a parse tree produced by OpenGaussSqlParser.

class OpenGaussSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OpenGaussSqlParser#ogQueryStatement.
    def visitOgQueryStatement(self, ctx:OpenGaussSqlParser.OgQueryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogInsertStmt.
    def visitOgInsertStmt(self, ctx:OpenGaussSqlParser.OgInsertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogUpdateStmt.
    def visitOgUpdateStmt(self, ctx:OpenGaussSqlParser.OgUpdateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogDeleteStmt.
    def visitOgDeleteStmt(self, ctx:OpenGaussSqlParser.OgDeleteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogMergeStmt.
    def visitOgMergeStmt(self, ctx:OpenGaussSqlParser.OgMergeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateTableStmt.
    def visitOgCreateTableStmt(self, ctx:OpenGaussSqlParser.OgCreateTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateViewStmt.
    def visitOgCreateViewStmt(self, ctx:OpenGaussSqlParser.OgCreateViewStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateMatViewStmt.
    def visitOgCreateMatViewStmt(self, ctx:OpenGaussSqlParser.OgCreateMatViewStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogRefreshMatViewStmt.
    def visitOgRefreshMatViewStmt(self, ctx:OpenGaussSqlParser.OgRefreshMatViewStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateIndexStmt.
    def visitOgCreateIndexStmt(self, ctx:OpenGaussSqlParser.OgCreateIndexStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogDropStmt.
    def visitOgDropStmt(self, ctx:OpenGaussSqlParser.OgDropStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogAlterStmt.
    def visitOgAlterStmt(self, ctx:OpenGaussSqlParser.OgAlterStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogTruncateStmt.
    def visitOgTruncateStmt(self, ctx:OpenGaussSqlParser.OgTruncateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogAnalyzeStmt.
    def visitOgAnalyzeStmt(self, ctx:OpenGaussSqlParser.OgAnalyzeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogExplainStmt.
    def visitOgExplainStmt(self, ctx:OpenGaussSqlParser.OgExplainStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCopyStmt.
    def visitOgCopyStmt(self, ctx:OpenGaussSqlParser.OgCopyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateSeqStmt.
    def visitOgCreateSeqStmt(self, ctx:OpenGaussSqlParser.OgCreateSeqStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogAlterSeqStmt.
    def visitOgAlterSeqStmt(self, ctx:OpenGaussSqlParser.OgAlterSeqStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateFuncStmt.
    def visitOgCreateFuncStmt(self, ctx:OpenGaussSqlParser.OgCreateFuncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogCreateProcStmt.
    def visitOgCreateProcStmt(self, ctx:OpenGaussSqlParser.OgCreateProcStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogDoStmt.
    def visitOgDoStmt(self, ctx:OpenGaussSqlParser.OgDoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogVacuumStmt.
    def visitOgVacuumStmt(self, ctx:OpenGaussSqlParser.OgVacuumStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogReindexStmt.
    def visitOgReindexStmt(self, ctx:OpenGaussSqlParser.OgReindexStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogLockStmt.
    def visitOgLockStmt(self, ctx:OpenGaussSqlParser.OgLockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogListenStmt.
    def visitOgListenStmt(self, ctx:OpenGaussSqlParser.OgListenStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogNotifyStmt.
    def visitOgNotifyStmt(self, ctx:OpenGaussSqlParser.OgNotifyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogSavepointStmt.
    def visitOgSavepointStmt(self, ctx:OpenGaussSqlParser.OgSavepointStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogTransactionStmt.
    def visitOgTransactionStmt(self, ctx:OpenGaussSqlParser.OgTransactionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogSetStmt.
    def visitOgSetStmt(self, ctx:OpenGaussSqlParser.OgSetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogUseStmt.
    def visitOgUseStmt(self, ctx:OpenGaussSqlParser.OgUseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogShowStmt.
    def visitOgShowStmt(self, ctx:OpenGaussSqlParser.OgShowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#updateStatement.
    def visitUpdateStatement(self, ctx:OpenGaussSqlParser.UpdateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#deleteStatement.
    def visitDeleteStatement(self, ctx:OpenGaussSqlParser.DeleteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#returningClause.
    def visitReturningClause(self, ctx:OpenGaussSqlParser.ReturningClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#forClause.
    def visitForClause(self, ctx:OpenGaussSqlParser.ForClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#copyStatement.
    def visitCopyStatement(self, ctx:OpenGaussSqlParser.CopyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#copySource.
    def visitCopySource(self, ctx:OpenGaussSqlParser.CopySourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#copyOptions.
    def visitCopyOptions(self, ctx:OpenGaussSqlParser.CopyOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#copyOption.
    def visitCopyOption(self, ctx:OpenGaussSqlParser.CopyOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createSequenceStatement.
    def visitCreateSequenceStatement(self, ctx:OpenGaussSqlParser.CreateSequenceStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#alterSequenceStatement.
    def visitAlterSequenceStatement(self, ctx:OpenGaussSqlParser.AlterSequenceStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#sequenceOption.
    def visitSequenceOption(self, ctx:OpenGaussSqlParser.SequenceOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createIndexStatement.
    def visitCreateIndexStatement(self, ctx:OpenGaussSqlParser.CreateIndexStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#indexElement.
    def visitIndexElement(self, ctx:OpenGaussSqlParser.IndexElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#refreshMaterializedViewStatement.
    def visitRefreshMaterializedViewStatement(self, ctx:OpenGaussSqlParser.RefreshMaterializedViewStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createFunctionStatement.
    def visitCreateFunctionStatement(self, ctx:OpenGaussSqlParser.CreateFunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createProcedureStatement.
    def visitCreateProcedureStatement(self, ctx:OpenGaussSqlParser.CreateProcedureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#funcParam.
    def visitFuncParam(self, ctx:OpenGaussSqlParser.FuncParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#paramMode.
    def visitParamMode(self, ctx:OpenGaussSqlParser.ParamModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#funcBody.
    def visitFuncBody(self, ctx:OpenGaussSqlParser.FuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#funcBodyDef.
    def visitFuncBodyDef(self, ctx:OpenGaussSqlParser.FuncBodyDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#doStatement.
    def visitDoStatement(self, ctx:OpenGaussSqlParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#vacuumStatement.
    def visitVacuumStatement(self, ctx:OpenGaussSqlParser.VacuumStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#reindexStatement.
    def visitReindexStatement(self, ctx:OpenGaussSqlParser.ReindexStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#lockStatement.
    def visitLockStatement(self, ctx:OpenGaussSqlParser.LockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#lockMode.
    def visitLockMode(self, ctx:OpenGaussSqlParser.LockModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#listenStatement.
    def visitListenStatement(self, ctx:OpenGaussSqlParser.ListenStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#notifyStatement.
    def visitNotifyStatement(self, ctx:OpenGaussSqlParser.NotifyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#savepointStatement.
    def visitSavepointStatement(self, ctx:OpenGaussSqlParser.SavepointStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#transactionStatement.
    def visitTransactionStatement(self, ctx:OpenGaussSqlParser.TransactionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#transactionMode.
    def visitTransactionMode(self, ctx:OpenGaussSqlParser.TransactionModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#isolationLevel.
    def visitIsolationLevel(self, ctx:OpenGaussSqlParser.IsolationLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#showStatement.
    def visitShowStatement(self, ctx:OpenGaussSqlParser.ShowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createTableStatement.
    def visitCreateTableStatement(self, ctx:OpenGaussSqlParser.CreateTableStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogPartitionBy.
    def visitOgPartitionBy(self, ctx:OpenGaussSqlParser.OgPartitionByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogPartitionDef.
    def visitOgPartitionDef(self, ctx:OpenGaussSqlParser.OgPartitionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogInheritClause.
    def visitOgInheritClause(self, ctx:OpenGaussSqlParser.OgInheritClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogBetween.
    def visitOgBetween(self, ctx:OpenGaussSqlParser.OgBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogComparison.
    def visitOgComparison(self, ctx:OpenGaussSqlParser.OgComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogIlike.
    def visitOgIlike(self, ctx:OpenGaussSqlParser.OgIlikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogIsNull.
    def visitOgIsNull(self, ctx:OpenGaussSqlParser.OgIsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogValueExprDefault.
    def visitOgValueExprDefault(self, ctx:OpenGaussSqlParser.OgValueExprDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogUnaryArithmetic.
    def visitOgUnaryArithmetic(self, ctx:OpenGaussSqlParser.OgUnaryArithmeticContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogFulltextMatch.
    def visitOgFulltextMatch(self, ctx:OpenGaussSqlParser.OgFulltextMatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogInSubquery.
    def visitOgInSubquery(self, ctx:OpenGaussSqlParser.OgInSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogFulltextMatchPartial.
    def visitOgFulltextMatchPartial(self, ctx:OpenGaussSqlParser.OgFulltextMatchPartialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogInList.
    def visitOgInList(self, ctx:OpenGaussSqlParser.OgInListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonDoubleArrow.
    def visitOgJsonDoubleArrow(self, ctx:OpenGaussSqlParser.OgJsonDoubleArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonHashArrow.
    def visitOgJsonHashArrow(self, ctx:OpenGaussSqlParser.OgJsonHashArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonContains.
    def visitOgJsonContains(self, ctx:OpenGaussSqlParser.OgJsonContainsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonDeleteKey.
    def visitOgJsonDeleteKey(self, ctx:OpenGaussSqlParser.OgJsonDeleteKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogBitwiseXor.
    def visitOgBitwiseXor(self, ctx:OpenGaussSqlParser.OgBitwiseXorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogBitwiseBinary.
    def visitOgBitwiseBinary(self, ctx:OpenGaussSqlParser.OgBitwiseBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogRowLiteral.
    def visitOgRowLiteral(self, ctx:OpenGaussSqlParser.OgRowLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogArrayLiteral.
    def visitOgArrayLiteral(self, ctx:OpenGaussSqlParser.OgArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogArithmeticBinary.
    def visitOgArithmeticBinary(self, ctx:OpenGaussSqlParser.OgArithmeticBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonHashDarrow.
    def visitOgJsonHashDarrow(self, ctx:OpenGaussSqlParser.OgJsonHashDarrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogLike.
    def visitOgLike(self, ctx:OpenGaussSqlParser.OgLikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogIsDistinct.
    def visitOgIsDistinct(self, ctx:OpenGaussSqlParser.OgIsDistinctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogSimilar.
    def visitOgSimilar(self, ctx:OpenGaussSqlParser.OgSimilarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#castOp.
    def visitCastOp(self, ctx:OpenGaussSqlParser.CastOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonArrow.
    def visitOgJsonArrow(self, ctx:OpenGaussSqlParser.OgJsonArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogJsonContainedBy.
    def visitOgJsonContainedBy(self, ctx:OpenGaussSqlParser.OgJsonContainedByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#ogArithmeticBinary2.
    def visitOgArithmeticBinary2(self, ctx:OpenGaussSqlParser.OgArithmeticBinary2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#arrayLiteralExpr.
    def visitArrayLiteralExpr(self, ctx:OpenGaussSqlParser.ArrayLiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:OpenGaussSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#query.
    def visitQuery(self, ctx:OpenGaussSqlParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#cteDefinition.
    def visitCteDefinition(self, ctx:OpenGaussSqlParser.CteDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#namedQuery.
    def visitNamedQuery(self, ctx:OpenGaussSqlParser.NamedQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#queryTermDefault.
    def visitQueryTermDefault(self, ctx:OpenGaussSqlParser.QueryTermDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#setOperation.
    def visitSetOperation(self, ctx:OpenGaussSqlParser.SetOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#setQuantifier.
    def visitSetQuantifier(self, ctx:OpenGaussSqlParser.SetQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#queryPrimaryDefault.
    def visitQueryPrimaryDefault(self, ctx:OpenGaussSqlParser.QueryPrimaryDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#table.
    def visitTable(self, ctx:OpenGaussSqlParser.TableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#subquery.
    def visitSubquery(self, ctx:OpenGaussSqlParser.SubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#querySpecification.
    def visitQuerySpecification(self, ctx:OpenGaussSqlParser.QuerySpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#selectClause.
    def visitSelectClause(self, ctx:OpenGaussSqlParser.SelectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#selectExpression.
    def visitSelectExpression(self, ctx:OpenGaussSqlParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#selectStar.
    def visitSelectStar(self, ctx:OpenGaussSqlParser.SelectStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#selectQualifiedStar.
    def visitSelectQualifiedStar(self, ctx:OpenGaussSqlParser.SelectQualifiedStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#fromClause.
    def visitFromClause(self, ctx:OpenGaussSqlParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#relation.
    def visitRelation(self, ctx:OpenGaussSqlParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:OpenGaussSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#joinType.
    def visitJoinType(self, ctx:OpenGaussSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#joinCriteria.
    def visitJoinCriteria(self, ctx:OpenGaussSqlParser.JoinCriteriaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#tableName.
    def visitTableName(self, ctx:OpenGaussSqlParser.TableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#subqueryRelation.
    def visitSubqueryRelation(self, ctx:OpenGaussSqlParser.SubqueryRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#lateral.
    def visitLateral(self, ctx:OpenGaussSqlParser.LateralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#unnestRelation.
    def visitUnnestRelation(self, ctx:OpenGaussSqlParser.UnnestRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#whereClause.
    def visitWhereClause(self, ctx:OpenGaussSqlParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#groupByClause.
    def visitGroupByClause(self, ctx:OpenGaussSqlParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#havingClause.
    def visitHavingClause(self, ctx:OpenGaussSqlParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#qualifyClause.
    def visitQualifyClause(self, ctx:OpenGaussSqlParser.QualifyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#windowClause.
    def visitWindowClause(self, ctx:OpenGaussSqlParser.WindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#namedWindow.
    def visitNamedWindow(self, ctx:OpenGaussSqlParser.NamedWindowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#groupByItem.
    def visitGroupByItem(self, ctx:OpenGaussSqlParser.GroupByItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#groupByItemList.
    def visitGroupByItemList(self, ctx:OpenGaussSqlParser.GroupByItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#groupByItemSet.
    def visitGroupByItemSet(self, ctx:OpenGaussSqlParser.GroupByItemSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#queryOrganization.
    def visitQueryOrganization(self, ctx:OpenGaussSqlParser.QueryOrganizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#limitClause.
    def visitLimitClause(self, ctx:OpenGaussSqlParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#sortItem.
    def visitSortItem(self, ctx:OpenGaussSqlParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#insertStatement.
    def visitInsertStatement(self, ctx:OpenGaussSqlParser.InsertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#insertMode.
    def visitInsertMode(self, ctx:OpenGaussSqlParser.InsertModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#partitionSpec.
    def visitPartitionSpec(self, ctx:OpenGaussSqlParser.PartitionSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#partitionVal.
    def visitPartitionVal(self, ctx:OpenGaussSqlParser.PartitionValContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnList.
    def visitColumnList(self, ctx:OpenGaussSqlParser.ColumnListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnAliases.
    def visitColumnAliases(self, ctx:OpenGaussSqlParser.ColumnAliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#valueList.
    def visitValueList(self, ctx:OpenGaussSqlParser.ValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#mergeStatement.
    def visitMergeStatement(self, ctx:OpenGaussSqlParser.MergeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#mergeSource.
    def visitMergeSource(self, ctx:OpenGaussSqlParser.MergeSourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#whenClause.
    def visitWhenClause(self, ctx:OpenGaussSqlParser.WhenClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#mergeAction.
    def visitMergeAction(self, ctx:OpenGaussSqlParser.MergeActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#assignmentList.
    def visitAssignmentList(self, ctx:OpenGaussSqlParser.AssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#assignment.
    def visitAssignment(self, ctx:OpenGaussSqlParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createViewStatement.
    def visitCreateViewStatement(self, ctx:OpenGaussSqlParser.CreateViewStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#createMaterializedViewStatement.
    def visitCreateMaterializedViewStatement(self, ctx:OpenGaussSqlParser.CreateMaterializedViewStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#dropStatement.
    def visitDropStatement(self, ctx:OpenGaussSqlParser.DropStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#alterStatement.
    def visitAlterStatement(self, ctx:OpenGaussSqlParser.AlterStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#alterTableAction.
    def visitAlterTableAction(self, ctx:OpenGaussSqlParser.AlterTableActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#truncateStatement.
    def visitTruncateStatement(self, ctx:OpenGaussSqlParser.TruncateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#analyzeStatement.
    def visitAnalyzeStatement(self, ctx:OpenGaussSqlParser.AnalyzeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#explainStatement.
    def visitExplainStatement(self, ctx:OpenGaussSqlParser.ExplainStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#setStatement.
    def visitSetStatement(self, ctx:OpenGaussSqlParser.SetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#useStatement.
    def visitUseStatement(self, ctx:OpenGaussSqlParser.UseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnDef.
    def visitColumnDef(self, ctx:OpenGaussSqlParser.ColumnDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnConstraint.
    def visitColumnConstraint(self, ctx:OpenGaussSqlParser.ColumnConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#tableConstraint.
    def visitTableConstraint(self, ctx:OpenGaussSqlParser.TableConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#excludeElement.
    def visitExcludeElement(self, ctx:OpenGaussSqlParser.ExcludeElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#partitionBy.
    def visitPartitionBy(self, ctx:OpenGaussSqlParser.PartitionByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#partitionType.
    def visitPartitionType(self, ctx:OpenGaussSqlParser.PartitionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#tableProperties.
    def visitTableProperties(self, ctx:OpenGaussSqlParser.TablePropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#tableProperty.
    def visitTableProperty(self, ctx:OpenGaussSqlParser.TablePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#propertyKey.
    def visitPropertyKey(self, ctx:OpenGaussSqlParser.PropertyKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#propertyValue.
    def visitPropertyValue(self, ctx:OpenGaussSqlParser.PropertyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnComment.
    def visitColumnComment(self, ctx:OpenGaussSqlParser.ColumnCommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#arrayType.
    def visitArrayType(self, ctx:OpenGaussSqlParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#structType.
    def visitStructType(self, ctx:OpenGaussSqlParser.StructTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#macroDataType.
    def visitMacroDataType(self, ctx:OpenGaussSqlParser.MacroDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#arrayTypeAngle.
    def visitArrayTypeAngle(self, ctx:OpenGaussSqlParser.ArrayTypeAngleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#mapType.
    def visitMapType(self, ctx:OpenGaussSqlParser.MapTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#primitiveType.
    def visitPrimitiveType(self, ctx:OpenGaussSqlParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#baseType.
    def visitBaseType(self, ctx:OpenGaussSqlParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#structField.
    def visitStructField(self, ctx:OpenGaussSqlParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#expression.
    def visitExpression(self, ctx:OpenGaussSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#passThrough.
    def visitPassThrough(self, ctx:OpenGaussSqlParser.PassThroughContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#logicalNot.
    def visitLogicalNot(self, ctx:OpenGaussSqlParser.LogicalNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#exists.
    def visitExists(self, ctx:OpenGaussSqlParser.ExistsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#logicalBinary.
    def visitLogicalBinary(self, ctx:OpenGaussSqlParser.LogicalBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#timestampLiteral.
    def visitTimestampLiteral(self, ctx:OpenGaussSqlParser.TimestampLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#struct.
    def visitStruct(self, ctx:OpenGaussSqlParser.StructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#dereference.
    def visitDereference(self, ctx:OpenGaussSqlParser.DereferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#macroVarExpr.
    def visitMacroVarExpr(self, ctx:OpenGaussSqlParser.MacroVarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#star.
    def visitStar(self, ctx:OpenGaussSqlParser.StarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#subscript.
    def visitSubscript(self, ctx:OpenGaussSqlParser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#columnRef.
    def visitColumnRef(self, ctx:OpenGaussSqlParser.ColumnRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#searched_case.
    def visitSearched_case(self, ctx:OpenGaussSqlParser.Searched_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#filterExpr.
    def visitFilterExpr(self, ctx:OpenGaussSqlParser.FilterExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#cast.
    def visitCast(self, ctx:OpenGaussSqlParser.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#extract.
    def visitExtract(self, ctx:OpenGaussSqlParser.ExtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#array.
    def visitArray(self, ctx:OpenGaussSqlParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#literalExpr.
    def visitLiteralExpr(self, ctx:OpenGaussSqlParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#parenthesized.
    def visitParenthesized(self, ctx:OpenGaussSqlParser.ParenthesizedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#windowExpr.
    def visitWindowExpr(self, ctx:OpenGaussSqlParser.WindowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#interval.
    def visitInterval(self, ctx:OpenGaussSqlParser.IntervalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#funcCall.
    def visitFuncCall(self, ctx:OpenGaussSqlParser.FuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#simple_case.
    def visitSimple_case(self, ctx:OpenGaussSqlParser.Simple_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#map.
    def visitMap(self, ctx:OpenGaussSqlParser.MapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#scalarSubquery.
    def visitScalarSubquery(self, ctx:OpenGaussSqlParser.ScalarSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#tryCast.
    def visitTryCast(self, ctx:OpenGaussSqlParser.TryCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#whenClauseExpr.
    def visitWhenClauseExpr(self, ctx:OpenGaussSqlParser.WhenClauseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#functionCall.
    def visitFunctionCall(self, ctx:OpenGaussSqlParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#namedArgument.
    def visitNamedArgument(self, ctx:OpenGaussSqlParser.NamedArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#arrayExpression.
    def visitArrayExpression(self, ctx:OpenGaussSqlParser.ArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#mapExpression.
    def visitMapExpression(self, ctx:OpenGaussSqlParser.MapExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#windowRef.
    def visitWindowRef(self, ctx:OpenGaussSqlParser.WindowRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#windowSpecExpr.
    def visitWindowSpecExpr(self, ctx:OpenGaussSqlParser.WindowSpecExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#windowFrame.
    def visitWindowFrame(self, ctx:OpenGaussSqlParser.WindowFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#frameBound.
    def visitFrameBound(self, ctx:OpenGaussSqlParser.FrameBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#intervalField.
    def visitIntervalField(self, ctx:OpenGaussSqlParser.IntervalFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:OpenGaussSqlParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#qualifiedIdentifier.
    def visitQualifiedIdentifier(self, ctx:OpenGaussSqlParser.QualifiedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#macroOrIdentifier.
    def visitMacroOrIdentifier(self, ctx:OpenGaussSqlParser.MacroOrIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#macroVar.
    def visitMacroVar(self, ctx:OpenGaussSqlParser.MacroVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#identifier.
    def visitIdentifier(self, ctx:OpenGaussSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#strictIdentifier.
    def visitStrictIdentifier(self, ctx:OpenGaussSqlParser.StrictIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#nullLiteral.
    def visitNullLiteral(self, ctx:OpenGaussSqlParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#boolLiteral.
    def visitBoolLiteral(self, ctx:OpenGaussSqlParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#intLiteral.
    def visitIntLiteral(self, ctx:OpenGaussSqlParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#decLiteral.
    def visitDecLiteral(self, ctx:OpenGaussSqlParser.DecLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#floatLiteral.
    def visitFloatLiteral(self, ctx:OpenGaussSqlParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#strLiteral.
    def visitStrLiteral(self, ctx:OpenGaussSqlParser.StrLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#dollarLiteral.
    def visitDollarLiteral(self, ctx:OpenGaussSqlParser.DollarLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:OpenGaussSqlParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#stringLiteral.
    def visitStringLiteral(self, ctx:OpenGaussSqlParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenGaussSqlParser#nonReserved.
    def visitNonReserved(self, ctx:OpenGaussSqlParser.NonReservedContext):
        return self.visitChildren(ctx)



del OpenGaussSqlParser