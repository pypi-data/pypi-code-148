import argparse, os, re

def main():
    parser = argparse.ArgumentParser(description='Plot the band structure from vaspkit result.',
                                     epilog='''
Example:
bandplot -o band.dat -p band.png
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",  action="version", version="bandplot 0.0.1")
    parser.add_argument('-k', "--kpoints",  default=[], type=str.upper, nargs='+')
    parser.add_argument('-s', "--size",     type=int,   nargs=2)
    parser.add_argument('-y', "--vertical", default=[-5.0, 5.0], type=float, nargs=2, help="vertical axis")
    parser.add_argument('-o', "--plot",     default="BAND.dat", type=str, help="plot figure from .dat file")
    parser.add_argument('-p', "--export",   default="BAND.png", type=str, help="plot figure filename")
    parser.add_argument('-l', "--klabels",  default="KLABELS",  type=str)
    args = parser.parse_args()

    KPOINTS = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('G', 'Γ', i))) for i in args.kpoints]

    if os.path.exists(args.plot):
        from bandplot import plots
        plots.main(args.plot, args.export, args.klabels, KPOINTS, args.size, args.vertical)

