# WTFPL

def main():
    import toml

    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", help="Config file",default="lambada.toml")
    parser.add_argument("--noauto", help="does not launch tasks", action="store_false", dest="auto")

    args = parser.parse_args()

    config = toml.load(args.config)
    print(config)

    from lambada.MonitoredApp import MonitoredApp
    from lambada.GUI import App

    a = App(100)
    for s in config:
        ma = MonitoredApp.get(s,config[s])
        a.addApplication(ma)
        if args.auto:
            ma.launch()

    a.mainloop()
    a.stopAll()

if __name__=="__main__":
    main()
