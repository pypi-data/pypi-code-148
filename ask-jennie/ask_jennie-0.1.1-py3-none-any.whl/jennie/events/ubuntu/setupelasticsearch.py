import os

def setup_elasticsearch():
    os.system('wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -')
    os.system('echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list')
    os.system('sudo apt update')
    os.system('apt-get install elasticsearch')
    open('/etc/elasticsearch/elasticsearch.yml', "a").write("network.host: localhost")
    os.system("systemctl start elasticsearch")
    os.system("systemctl enable elasticsearch")
    print ("\n\nElastic Search Is live on port 9200\n\n")