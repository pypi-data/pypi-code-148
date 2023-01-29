

from openautomatumdronedata.automatumBokehSever import *


def main():
    print('Opening Bokeh application on http://localhost:5000/')

    # Setting num_procs here means we can't touch the IOLoop before now, we must
    # let Server handle that. If you need to explicitly handle IOLoops then you
    # will need to use the lower level BaseServer class.

    server = Server({'/': automatumDataBokeh}, num_procs=1)
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

if __name__ == "__main__":
    main()