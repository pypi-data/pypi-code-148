import os
import shutil
from contextlib import contextmanager
import pandas as pd
import bodo


@bodo.jit
def get_rank():
    return bodo.libs.distributed_api.get_rank()


@bodo.jit
def barrier():
    return bodo.libs.distributed_api.barrier()


@contextmanager
def ensure_clean(filename):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(filename) and os.path.isfile(
                filename):
                os.remove(filename)
        except Exception as ehp__nlzi:
            print('Exception on removing file: {error}'.format(error=ehp__nlzi)
                )


@contextmanager
def ensure_clean_dir(dirname):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(dirname) and os.path.isdir(
                dirname):
                shutil.rmtree(dirname)
        except Exception as ehp__nlzi:
            print('Exception on removing directory: {error}'.format(error=
                ehp__nlzi))


@contextmanager
def ensure_clean2(pathname):
    try:
        yield
    finally:
        barrier()
        if get_rank() == 0:
            try:
                if os.path.exists(pathname) and os.path.isfile(pathname):
                    os.remove(pathname)
            except Exception as ehp__nlzi:
                print('Exception on removing file: {error}'.format(error=
                    ehp__nlzi))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as ehp__nlzi:
                print('Exception on removing directory: {error}'.format(
                    error=ehp__nlzi))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    wrul__olab = MPI.COMM_WORLD
    try:
        tyl__uqzsm = None
        if bodo.get_rank() == 0:
            tyl__uqzsm = f'{table_name_prefix}_{uuid.uuid4().hex}'
        tyl__uqzsm = wrul__olab.bcast(tyl__uqzsm)
        yield tyl__uqzsm
    finally:
        bodo.barrier()
        afr__mjzg = None
        if bodo.get_rank() == 0:
            try:
                mdpkb__apqn = create_engine(conn)
                kskpn__csl = mdpkb__apqn.connect()
                kskpn__csl.execute(f'drop table if exists {tyl__uqzsm}')
            except Exception as ehp__nlzi:
                afr__mjzg = ehp__nlzi
        afr__mjzg = wrul__olab.bcast(afr__mjzg)
        if isinstance(afr__mjzg, Exception):
            raise afr__mjzg


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    wrul__olab = MPI.COMM_WORLD
    try:
        tyl__uqzsm = None
        if bodo.get_rank() == 0 or not parallel:
            tyl__uqzsm = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            tyl__uqzsm = wrul__olab.bcast(tyl__uqzsm)
        yield tyl__uqzsm
    finally:
        if parallel:
            bodo.barrier()
        afr__mjzg = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {tyl__uqzsm}', conn)
            except Exception as ehp__nlzi:
                afr__mjzg = ehp__nlzi
        if parallel:
            afr__mjzg = wrul__olab.bcast(afr__mjzg)
        if isinstance(afr__mjzg, Exception):
            raise afr__mjzg
