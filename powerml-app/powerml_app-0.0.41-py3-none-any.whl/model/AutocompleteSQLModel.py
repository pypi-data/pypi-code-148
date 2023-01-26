
from powerml import PowerML
import logging
import re
logger = logging.getLogger(__name__)


class AutocompleteSQLModel:
    def __init__(self,
                 config={},
                 max_output_tokens=256,
                 temperature=0.0,
                 ):
        self.model = PowerML(config, "sql/v1")
        self.max_output_tokens = max_output_tokens
        self.table_schemas = []
        self.example_queries = []
        self.temperature = temperature

    def fit(self, table_schemas=[], example_queries=[]):
        """
        Parameters
        ----------
        table_schemas : list
            Takes in a list of schema definitions where each element of the
            list corresponds to the schema for one table.
        example_queries: list
            Takes a list of sql queries that have been used with {table_schemas}
            to get sql results.
        """
        self.table_schemas = table_schemas
        self.example_queries = example_queries

    def predict(self, sql_prompt):
        """
        Parameters
        ----------
        sql_prompt: string
            The beginning of a SQL prompt to be autocompleted.

        Returns
        str : The sql autocompletion
        -------
        """
        table_schemas = ''
        if hasattr(self, 'table_schemas'):
            table_schemas = "\n".join(self.table_schemas)
            if table_schemas:
                table_schemas += '\n\n'
        example_queries = ''
        if hasattr(self, 'example_queries'):
            example_queries = "\n".join([query + 'END' for query in self.example_queries])
            if example_queries:
                example_queries += '\n\n'
        prompt = {
            "{{input}}": sql_prompt,
            "{{examples}}": example_queries,
            "{{table_schemas}}": table_schemas
        }

        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            stop=['\\\\nEND', '\\nEND', '\nEND', 'END', ';', '--'],
            temperature=self.temperature,)

        return self.post_process(output)

    def post_process(self, output):
        # TODO: replace with stop tokens
        results = re.split('\\\\nEND|\\nEND|\nEND|END|;|--', output)
        return results[0].strip()
