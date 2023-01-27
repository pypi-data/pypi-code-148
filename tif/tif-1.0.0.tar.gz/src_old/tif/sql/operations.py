import string
from fabric.connection import Connection
from tif.fabric import cli
from datetime import datetime

def import_db(c : Connection, dump_location : string):
    with c.cd(dump_location):
        c.run("ls")
        user = cli.prompt(">>> Enter DB user: ")
        db = cli.prompt(">>> Enter DB name: ")
        dump = cli.prompt(">>> Enter dump filename: ")
        if (user and db and dump):
            c.run("mysql -u{} -p {} < {}".format(user, db, dump), pty=True)
            cli.puts(".:~ Import finished: {0}".format(dump))
        else:
            cli.puts("!!! Aborted")

def dump(c : Connection, host : string, user : string, database : string, dump_location : string, defaults_extra_file = None):
    with c.cd(dump_location):
        now = datetime.now()
        date_and_time = now.strftime("%m-%d-%Y_%H:%M:%S")
        dump = "{}_{}.sql.gz".format(database, date_and_time)
        if defaults_extra_file:
            result = c.run("mysqldump --defaults-extra-file={} -h{} -u{} {} | gzip > {}".format(defaults_extra_file, host, user, database, dump), warn=True)
        else:
            result = c.run("mysqldump -h{} -u{} -p {} | gzip > {}".format(host, user, database, dump), warn=True)
        if(result.return_code == 0):
            cli.puts(".:~ Database dump successfully completed and stored in {} directory: {}".format(dump_location, dump))
        else:
            cli.puts("!!! Aborted with errors")