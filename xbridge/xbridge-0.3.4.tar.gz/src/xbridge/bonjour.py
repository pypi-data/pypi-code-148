

from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo, ZeroconfServiceTypes
import socket

deviceType = '_xbridge._tcp.local.'
zeroconf = Zeroconf()
# print('Zeronconf init!!!')

class MyListener:

    def remove_service(self, zeroconf, type, name):
        simple_name = name.split('.')[0]
        print("[-] Service \"%s\" removed" % (simple_name))

    def add_service(self, zeroconf, type, name):
        try:
            simple_name = name.split('.')[0]
            info = zeroconf.get_service_info(type, name)
            ip = socket.inet_ntoa(info.addresses[0])
            port = info.port
            print("[+] Service \"%s\" added. ip=%s, port=%d" % (simple_name,ip,port))
        except:
            print("[+] Service \"%s\" added." % (name))
            print(info)

    def update_service(self, zeroconf, type, name):
        try:
            simple_name = name.split('.')[0]
            info = zeroconf.get_service_info(type, name)
            ip = socket.inet_ntoa(info.addresses[0])
            port = info.port
            print("[u] Service \"%s\" updated. ip=%s, port=%d" % (simple_name,ip,port))
        except:
            print("[u] Service \"%s\" updated." % (name))
            print(info)

def get_ip_port(info):
    ip = socket.inet_ntoa(info.addresses[0])
    port = info.port
    return (ip, port)

def get_service_info(name):
    info = zeroconf.get_service_info(deviceType, name + "." + deviceType, timeout=10000)
    return info

def register_service(name, ip, port) -> ServiceInfo:
    print("try register service %s on %s" % (name, port))

    # ip = '172.0.0.1'

    # # try:
    # #     for temp in socket.gethostbyname_ex(socket.gethostname())[2]:
    # #         if temp.startswith('192.'):
    # #             ip = temp
    # #             break
    # # except Exception:
    # #     print("can't get IP")

    # try:
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     s.connect(('8.8.8.8', 80))
    #     ip = s.getsockname()[0]
    # finally:
    #     s.close()
        
    print('my ip: %s' % ip)
    info = ServiceInfo(deviceType,
                       name + "." + deviceType, port,
                       properties={
                           'protocol':'rsocket/ws',
                           'path': "/",
                       },
                       addresses = [ip])

    zeroconf.register_service(info, allow_name_change=True)
    print(info)
    return info

def unregister_service(info):
    print("try unregister service %s" % (info.name))
    zeroconf.unregister_service(info)

def discover_service():
    print("browse service")

    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_xbridge._tcp.local.", listener)
    # browser = ServiceBrowser(zeroconf, "._tcp.local.", listener)

    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()

def update_service(info):
    zeroconf.update_service(info)
    print(info)


# print("all serivce types:")
# print('\n'.join(ZeroconfServiceTypes.find()))
# print()


