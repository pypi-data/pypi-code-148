import os,sys,sqlite3 as sqlite

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("sqlitescripting - Execute a raw SQL creation file to a SQLITE DB, for paired used with sqlacodegen")
	parser.add_argument("-d","--db", help="The name of the datebase file", nargs=1, default="newoutput.db")
	parser.add_argument("-s","--sql", help="The sql scripting file to be executed", nargs=1)
	return parser.parse_args()

def execute_scripts(db_file, sqlite_script):
    conn = sqlite.connect(db_file)
    try:
        cursor = conn.cursor()
        with open(sqlite_script, "r") as reader:
            contents = reader.readlines()

        single_line = ' '.join(contents)
        for exe in single_line.split(';'):
            exe = exe.strip()
            if exe != '':
                exe += ";"
                print(exe)
                cursor.execute(exe)
                conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
	args = getArgs()

    execute_scripts(args.db, args.sql)
