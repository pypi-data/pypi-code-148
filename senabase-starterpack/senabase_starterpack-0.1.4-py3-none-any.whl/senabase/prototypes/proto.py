import yaml

from senabase.starterpack import sb_pg, sb_log

try:
    sb_log.configure('proto')

    with open('./bin/cfg/cfg.yaml') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        cfg_pg = cfg['pg']
        host = cfg_pg['host']
        port = cfg_pg['port']
        dbname = cfg_pg['dbname']
        usrid = cfg_pg['usrid']
        usrpw = cfg_pg['usrpw']
        sb_pg.configure(host, port, dbname, usrid, usrpw)

        q1 = 'select now()'
        rs = sb_pg.get(q1)
        sb_log.d(rs)
except Exception as ex:
    sb_log.e(ex)
