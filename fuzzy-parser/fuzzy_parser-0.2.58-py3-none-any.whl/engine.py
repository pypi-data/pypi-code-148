from pyswip import Prolog
from datetime import date


class Engine:

    """
    Parser for abbreviated, ambiguous, incomplete dates in multiple languages
    """

    def __init__(self, context=date.today()):
        self.context = context.strftime('date(%Y,%m,%d)')
        self.prolog = Prolog()
        next(self.prolog.query("use_module(library(abbreviated_dates))"))

    def when(self, time_expression: str):
        """
        Explore all possible solutions
        :param time_expression: a time expression in a natural language
        :return: a solution or an empty list
        """
        escaped_quotes = time_expression.replace("'", "''")
        query = self.prolog.query(f"parse({self.context}, '{escaped_quotes}', Date, Trace)")
        return next(iter([self.transform(solution) for solution in query]), ([], []))

    @staticmethod
    def transform(solution):
        semantic = [eval(period if type(period) is str else period.value, {'date': date}) for period in solution["Date"]]
        syntax = [trace if type(trace) is str else trace.value for trace in solution["Trace"]]
        return semantic, syntax
