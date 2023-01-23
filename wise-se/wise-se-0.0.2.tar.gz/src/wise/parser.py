from typing import Dict, Optional

import antlr4
from antlr4 import InputStream, ParserRuleContext, RuleContext
from antlr4.Token import CommonToken

from wise.imp import (
    Imp,
    Aexpr,
    Skip,
    Var,
    Aff,
    Cst,
    Add,
    Sub,
    Ite,
    Ble,
    Err,
    Bcst,
    Beq,
    Bnot,
    Band,
    Bor,
    Seq,
    Loop,
)
from wise.imp_language.ImpLanguageLexer import ImpLanguageLexer
from wise.imp_language.ImpLanguageListener import ImpLanguageListener
from wise.imp_language.ImpLanguageParser import ImpLanguageParser


class BailPrintErrorStrategy(antlr4.BailErrorStrategy):
    def recover(self, recognizer: antlr4.Parser, e: antlr4.RecognitionException):
        recognizer._errHandler.reportError(recognizer, e)
        super().recover(recognizer, e)


def parse_tree_text(elem: RuleContext | CommonToken) -> str:
    if isinstance(elem, CommonToken):
        return elem.text
    else:
        return elem.getText()


class ImpEmitter(ImpLanguageListener):
    def __init__(self):
        self.__result: Optional[Imp] = None

        self.__aexprs: Dict[ParserRuleContext, Aexpr] = {}
        self.__bexprs: Dict[ParserRuleContext, Bexpr] = {}
        self.__progs: Dict[ParserRuleContext, Imp] = {}

    def result(self):
        assert self.__result is not None
        return self.__result

    def exitStart(self, ctx: ImpLanguageParser.StartContext):
        self.__result = self.__progs[ctx.imp()]

    def exitVar(self, ctx: ImpLanguageParser.VarContext):
        self.__aexprs[ctx] = Var(parse_tree_text(ctx.ID()))

    def exitCst(self, ctx: ImpLanguageParser.CstContext):
        self.__aexprs[ctx] = Cst(int(parse_tree_text(ctx.NUM())))

    def exitAdd(self, ctx: ImpLanguageParser.AddContext):
        self.__aexprs[ctx] = Add(
            self.__aexprs[ctx.aexpr(0)], self.__aexprs[ctx.aexpr(1)]
        )

    def exitSub(self, ctx: ImpLanguageParser.SubContext):
        self.__aexprs[ctx] = Sub(
            self.__aexprs[ctx.aexpr(0)], self.__aexprs[ctx.aexpr(1)]
        )

    def exitApar(self, ctx: ImpLanguageParser.AparContext):
        self.__aexprs[ctx] = self.__aexprs[ctx.aexpr()]

    def exitBcst(self, ctx: ImpLanguageParser.BcstContext):
        self.__bexprs[ctx] = Bcst(ctx.FALSE() is None)

    def exitBle(self, ctx: ImpLanguageParser.BleContext):
        self.__bexprs[ctx] = Ble(
            self.__aexprs[ctx.aexpr(0)], self.__aexprs[ctx.aexpr(1)]
        )

    def exitBeq(self, ctx: ImpLanguageParser.BeqContext):
        self.__bexprs[ctx] = Beq(
            self.__aexprs[ctx.aexpr(0)], self.__aexprs[ctx.aexpr(1)]
        )

    def exitBnot(self, ctx: ImpLanguageParser.BnotContext):
        self.__bexprs[ctx] = Bnot(self.__bexprs[ctx.bexpr()])

    def exitBand(self, ctx: ImpLanguageParser.BandContext):
        self.__bexprs[ctx] = Band(
            self.__bexprs[ctx.bexpr(0)], self.__bexprs[ctx.bexpr(1)]
        )

    def exitBor(self, ctx: ImpLanguageParser.BorContext):
        self.__bexprs[ctx] = Bor(
            self.__bexprs[ctx.bexpr(0)], self.__bexprs[ctx.bexpr(1)]
        )

    def exitBpar(self, ctx: ImpLanguageParser.BparContext):
        self.__bexprs[ctx] = self.__bexprs[ctx.bexpr()]

    def exitSkip(self, ctx: ImpLanguageParser.SkipContext):
        self.__progs[ctx] = Skip()

    def exitIte(self, ctx: ImpLanguageParser.IteContext):
        self.__progs[ctx] = Ite(
            self.__bexprs[ctx.bexpr()],
            self.__progs[ctx.imp(0)],
            self.__progs[ctx.imp(1)],
        )

    def exitSeq(self, ctx: ImpLanguageParser.SeqContext):
        self.__progs[ctx] = Seq(self.__progs[ctx.imp(0)], self.__progs[ctx.imp(1)])

    def exitAff(self, ctx: ImpLanguageParser.AffContext):
        self.__progs[ctx] = Aff(parse_tree_text(ctx.ID()), self.__aexprs[ctx.aexpr()])

    def exitErr(self, ctx: ImpLanguageParser.ErrContext):
        self.__progs[ctx] = Err()

    def exitLoop(self, ctx: ImpLanguageParser.LoopContext):
        self.__progs[ctx] = Loop(self.__bexprs[ctx.bexpr()], self.__progs[ctx.imp()])


def parse_imp(inp: str) -> Imp:
    lexer = ImpLanguageLexer(InputStream(inp))
    parser = ImpLanguageParser(antlr4.CommonTokenStream(lexer))
    parser._errHandler = BailPrintErrorStrategy()
    imp_emitter = ImpEmitter()
    antlr4.ParseTreeWalker().walk(imp_emitter, parser.start())
    return imp_emitter.result()
