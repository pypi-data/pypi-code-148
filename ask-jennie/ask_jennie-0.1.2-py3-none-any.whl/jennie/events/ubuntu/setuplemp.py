import os, random, string
from jennie.events.ubuntu.nginxfiles import *

def setup_lemp():
    os.system("add-apt-repository universe")
    os.system("apt-get update")
    os.system("apt-get install nginx mysql-server php-fpm php-mysql php-mbstring php-gettext apache2-utils libmysqlclient-dev -y")
    os.system("ufw allow 'Nginx Full'")

    os.system("unlink /etc/nginx/sites-enabled/default")
    nginx_config = DEFAULT_CONF
    default_php = DEFAULT_PHP_PAGE

    open("/etc/nginx/conf.d/default.conf", "w").write(nginx_config)
    open("/var/www/html/index.php", "w").write(default_php)
    os.system("service php-fpm7.2 start")

    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    command = '''mysql -u root --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MYSQL_PASSWORD';"'''.replace("MYSQL_PASSWORD", password)
    os.system(command)

    os.system("systemctl reload nginx")
    print("\n\nInstalled Nginx, MySQL, php \nMySQL Credentials"
          "\n\tuser: root"
          "\n\tpassword: " + password)