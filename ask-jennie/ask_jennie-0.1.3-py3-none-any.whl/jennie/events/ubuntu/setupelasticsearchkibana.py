import os
from jennie.events.ubuntu.nginxfiles import KIBANA_CONF
from jennie.events.ubuntu.setupelasticsearch import setup_elasticsearch

def setup_elasticsearchkibana():
    setup_elasticsearch()
    os.system("apt-get install kibana")
    os.system('systemctl enable kibana')
    os.system('systemctl start kibana')
    os.system("apt-get install nginx -y")
    os.system("sudo service nginx start")
    open("/etc/nginx/conf.d/kibana.conf", "w").write(KIBANA_CONF)
    os.system("sudo ufw allow 8100")
    os.system("sudo service nginx reload")
    print ("\n\nKibana is up and running at on port 8100\n\n")