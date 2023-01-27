import argparse, os, re

def main():
    parser = argparse.ArgumentParser(description='Plot the phonon band structure from phonopy result.',
                                     epilog='''
Example:
pbandplot -o band.dat -p pband.png
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",  action="version", version="pbandplot 0.0.1.1")
    parser.add_argument('-k', "--kpoints",  default=[], type=str.upper, nargs='+')
    parser.add_argument('-s', "--size",     type=int,   nargs=2)
    parser.add_argument('-b', "--broken",   type=float, nargs=3)
    parser.add_argument('-y', "--vertical", type=float, nargs=2, help="vertical axis")
    parser.add_argument('-o', "--plot",    default="BAND.dat", type=str, help="plot figure from .dat file")
    parser.add_argument('-p', "--export",  default="BAND.png", type=str, help="plot figure filename")
    
    args = parser.parse_args()

    KPOINTS = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('G', 'Γ', i))) for i in args.kpoints]

    if os.path.exists(args.plot):
        from pbandplot import plots
        plots.main(args.plot, args.export, KPOINTS, args.size, args.vertical, args.broken)

