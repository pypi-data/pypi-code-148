import os
from jennie.events.ubuntu.nginxfiles import *

def install_phpmyadmin():
    os.system("wget https://files.phpmyadmin.net/phpMyAdmin/5.1.0/phpMyAdmin-5.1.0-all-languages.tar.gz")
    os.system("tar -xvf phpMyAdmin-5.1.0-all-languages.tar.gz")
    os.system("mv phpMyAdmin-5.1.0-all-languages /var/www/html/phpmyadmin")
    os.system("rm -rf phpMyAdmin-5.1.0-all-languages.tar.gz")
    nginx_config = DEFAULT_PHPMYADMIN_CONF
    open("/etc/nginx/conf.d/default.conf", "w").write(nginx_config)
    os.system("systemctl reload nginx")
    print ('''\n\nphpmyadmin is up and running at http://YOURIP/phpmyadmin/.\n\n''')