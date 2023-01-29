from unittest import TestCase, main
import ganymede.notebook.query as query

class TestQueryFunctions(TestCase):      
    def test_query_dry_run_analysis(self):
        try:
            query.dry_run('SELECT * FROM (SELECT "sample", "query");')
        except Exception:
            self.fail("query.dry_run() raised Exception unexpectedly!")

    def test_query_results_analysis(self):
        try:
            query.results('SELECT * FROM (SELECT "sample", "query");')
        except Exception:
            self.fail("query.results() raised Exception unexpectedly!")
            

if __name__ == '__main__':
    main()