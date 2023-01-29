import os, random, time
from jennie.events.ubuntu.uwsgifiles import *
from jennie.events.ubuntu.nginxfiles import *


def deploy_django(port, domain):
    dir_arr = os.getcwd().split("/")
    main_dir = ""
    for i in range(0, len(dir_arr)-1):
        main_dir += dir_arr[i] + "/"
    main_dir = main_dir[:-1]
    project_dir = dir_arr[-1]
    port_exchange = 95 + random.randint(10, 99)

    if port == "http":
        django_nginx_file = DJANGO_HTTP_CONF
        os.system("ufw allow 'Nginx Full'")
    elif port == "https":
        django_nginx_file = DJANGO_HTTPS_CONF
        os.system("sudo add-apt-repository ppa:certbot/certbot")
        os.system("sudo apt install python-certbot-nginx -y")
        os.system("certbot --nginx -d {}".format(domain))
        os.system("ufw allow 'Nginx Full'")
    else:
        django_nginx_file = DJANGO_PORT_CONF.replace("PORT", port)
        os.system("ufw allow {}".format(port))

    domain_name = domain.replace(".", "").replace("-", "")
    django_nginx_file = django_nginx_file.replace("DOMAIN_NAME", domain).replace("PORT_EXCHANGE", str(port_exchange))
    uwsgi_ini_file = DJANGO_CONF.replace("PROJECT_DIR", project_dir).replace("PORT_EXCHANGE", str(port_exchange)).replace("MAIN_DIR", main_dir)

    os.system("apt-get install nginx -y")
    os.system("service nginx start")
    os.system("pip3 install uwsgi")
    os.system("mkdir /etc/uwsgi")
    open("/etc/systemd/system/uwsgi.service", "w").write(UWSGI_EMPEROR_SERVICE)
    open("/etc/nginx/conf.d/{}.conf".format(domain_name).format(), "w").write(django_nginx_file)
    open("/etc/uwsgi/server.ini", "w").write(uwsgi_ini_file)


    os.system("systemctl restart uwsgi.service")
    os.system("sudo systemctl reload nginx")
    time.sleep(2)
    print ("\n\nDjango Deployed on port {} on  domain {}\n\n".format(port, domain))



