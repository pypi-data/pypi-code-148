# WTFPL

def main():
    import configparser

    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", help="",default="lambada.ini")

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    print(config.sections())

    from lambada.MonitoredApp import MonitoredApp
    from lambada.GUI import App

    a = App(100)
    for s in config.sections():
        ma = MonitoredApp(s,config[s])
        a.addApplication(ma)
    a.mainloop()

if __name__=="__main__":
    main()