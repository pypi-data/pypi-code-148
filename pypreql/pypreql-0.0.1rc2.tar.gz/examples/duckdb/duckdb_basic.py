
eng = create_engine("duckdb:///:memory:")
eng.execute("register", ("dataframe_name", pd.DataFrame(...)))

eng.execute("select * from dataframe_name")