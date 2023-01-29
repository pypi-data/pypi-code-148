from collections import namedtuple
from pathlib import Path
import sqlite3 as sql

import pandas as pd

import datatypes.sqlite
from metaerg.datatypes import sqlite

Feature = namedtuple('Feature', datatypes.sqlite.FEATURE_FIELDS)

SQLITE_CREATE_TABLE_SYNTAX = '''CREATE TABLE features(
    id TEXT PRIMARY_KEY,
    genome TEXT,
    contig TEXT,
    start INT,
    end INT,
    strand INT,
    type TEXT,
    inference TEXT,
    subsystems TEXT,
    descr TEXT,
    taxon TEXT,
    notes TEXT,
    aa_seq TEXT,
    nt_seq TEXT,
    antismash TEXT,
    signal_peptide TEXT,
    tmh INT,
    tmh_topology TEXT,
    blast TEXT,
    cdd TEXT,
    hmm TEXT
)'''

SQLITE_UPDATE_SYNTAX = '''UPDATE features SET
    genome = ?,
    contig = ?,
    start = ?,
    end = ?,
    strand = ?,
    type = ?,
    inference = ?,
    subsystems = ?,
    descr = ?,
    taxon = ?,
    notes = ?,
    aa_seq = ?,
    nt_seq = ?,
    antismash = ?,
    signal_peptide = ?,
    tmh = ?,
    tmh_topology = ?,
    blast = ?,
    cdd = ?,
    hmm = ? 
WHERE id = ?'''

def create_db(sql_db, feather_file):
    sql_db.unlink(missing_ok=True)

    connection = sql.connect(sql_db)
    cursor = connection.cursor()

    cursor.execute(SQLITE_CREATE_TABLE_SYNTAX)

    feature_data = pd.read_feather(feather_file)
    print(len(feature_data), 'features')

    for f in feature_data.itertuples(index=False):
        cursor.execute('INSERT INTO features VALUES(?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?)', tuple(f))
    connection.commit()
    connection.close()


def read_feature_from_db(sql_connection, id) -> dict:
    cursor = sql_connection.cursor()
    result = cursor.execute('SELECT * FROM features WHERE id = ?', (id,))
    return Feature(*result.fetchone())._asdict()


def save_feature_to_db(sql_connection, feature:dict):
    cursor = sql_connection.cursor()
    id = feature.pop('id')
    feature['id'] = id
    cursor.execute(SQLITE_UPDATE_SYNTAX, tuple(feature.values()))
    sql_connection.commit()


def main():
    dir = Path('/home/kinestetika/Seq/test')
    sql_db = dir / 'g0000.db'

    # feather_file = dir / 'g0000.all_genes.feather'
    #create_db(sql_db, feather_file)

    connection = sqlite.connect_to_db(sql_db)
    print(sqlite.count_features(connection))

    for feature in sqlite.read_all_features(connection, type='CDS', additional_sql='end - start >= 240 AND subsystems LIKE "%ribosomal protein%"'):
        print(feature.id, feature.end - feature.start, feature.descr)


    a_feature = sqlite.read_feature_by_id(connection, 'g0000.c0064.03915')

    print(f'"{a_feature.antismash}"')
    #for k, v in a_feature.__dict__.items():
    #    print(k, v)


    #a_feature.start = 2
    #a_feature.type = 'CDS'
    #a_feature.aa_seq = a_feature.aa_seq[:-4]

    #a_feature.start = 3
    #a_feature.type = 'mRNA'
    #a_feature.aa_seq = a_feature.aa_seq + 'marc' # '[:-4]

    #sqlite.update_feature_in_db(connection, a_feature)

    #b_feature = sqlite.read_feature_by_id(connection, 'g0000.c0064.03915')
    #print(b_feature)
    #print(b_feature['id'], b_feature['start'], b_feature['end'], b_feature['type'], a_feature['aa_seq'])

    #for row in cursor.execute('SELECT * FROM features'):
    #    feature = Feature(*row)
    #    print(feature.id)


if __name__ == "__main__":
    main()

