from eolymp.atlas import statement_pb2, atlas_pb2
from eolymp.atlas.atlas_http import AtlasClient

from peolymp.abstract import AbstractAPI
from peolymp.utils import get_many


class AtlasAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(AtlasAPI, self).__init__(**kwargs)
        self.client = AtlasClient(self.http_client, url=self.get_url())

    def create_statement(self, prob_id, locale, title, link, source=""):
        s = statement_pb2.Statement(problem_id=prob_id, locale=locale, title=title, content="", download_link=link,
                                    format=statement_pb2.Statement.Format.TEX, source=source)
        return self.client.CreateStatement(atlas_pb2.CreateStatementInput(problem_id=prob_id, statement=s)).statement_id

    def update_statement(self, problem_id, statement):
        return self.client.UpdateStatement(
            atlas_pb2.UpdateStatementInput(problem_id=problem_id, statement_id=statement.id, statement=statement))

    def delete_statement(self, prob_id, statement_id):
        self.client.DeleteStatement(atlas_pb2.DeleteStatementInput(statement_id=statement_id, problem_id=prob_id))

    def get_statements(self, prob_id):
        return self.client.ListStatements(atlas_pb2.ListStatementsInput(problem_id=prob_id)).items

    def get_problems(self):
        def __get_problems(offset, size):
            return self.client.ListProblems(request=atlas_pb2.ListProblemsInput(offset=offset, size=size))

        return get_many(__get_problems)
