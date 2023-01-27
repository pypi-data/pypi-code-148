import os, re
import numpy as np
import matplotlib.pyplot as plt

def main(PLOT, EXPORT, KLABELS, labels, figsize, vertical):
    with open(PLOT, "r") as main_file:
        lines = main_file.readlines()

    str0 = lines[0].split()
    if len(str0) == 2 and str0[1] == "Energy-Level(eV)":
        nkps = lines[1].split()
        m, n = int(nkps[-2]), int(nkps[-1])
        arr = np.zeros(m)
        bands = np.zeros((n,m))
        reverse = False
        for i in lines[2:]:
            str = i.split()
            if i[0] == '#':
                j = int(str[-1])
                k = 0
            elif len(str) > 0:
                if j == 1:
                    arr[k], bands[0,k] = float(str[0]), float(str[1])
                    k += 1
                else:
                    N = j - 1
                    if k == 0:
                        if float(str[0]) == 0:
                            reverse = False
                        else:
                            reverse = True
                    if reverse:
                        K = m-k-1
                    else:
                        K = k
                    bands[N,K] = float(str[1])
                    k += 1
            else:
                pass
        Noneispin(arr, bands, EXPORT, KLABELS, labels, figsize, vertical)
    elif len(str0) == 3 and str0[1] == "Spin-Up(eV)" and str0[2] == "Spin-down(eV)":
        nkps = lines[1].split()
        m, n = int(nkps[-2]), int(nkps[-1])
        arr = np.zeros(m)
        up = np.zeros((n,m))
        down = np.zeros((n,m))
        reverse = False
        for i in lines[2:]:
            str = i.split()
            if i[0] == '#':
                j = int(str[-1])
                k = 0
            elif len(str) > 0:
                if j == 1:
                    arr[k], up[0,k], down[0,k] = float(str[0]),float(str[1]),float(str[2])
                    k += 1
                else:
                    N = j - 1
                    if k == 0:
                        if float(str[0]) == 0:
                            reverse = False
                        else:
                            reverse = True
                    if reverse:
                        K = m-k-1
                    else:
                        K = k
                    up[N,K], down[N,K] = float(str[1]),float(str[2])
                    k += 1
            else:
                pass
        Ispin(arr, up, down, EXPORT, KLABELS, labels, figsize, vertical)
    else:
        pass

def Ispin(arr, up, down, EXPORT, KLABELS, labels, figsize, vertical):
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = 'Times New Roman'

    plt.figure(figsize=figsize)
    p_up = plt.plot(arr,up.T,color='red',linewidth=1,linestyle='-')
    p_do = plt.plot(arr,down.T,color='black',linewidth=1,linestyle=':')
    plt.legend([p_up[0],p_do[0]],['up','down'],frameon=False, prop={'style':'italic','size':'small'})
    plt.tick_params(axis='y', which='minor', color='gray')

    plt.axhline(linewidth=0.4,linestyle='-.',c='blue')
    if os.path.exists(KLABELS):
        with open(KLABELS, "r") as main_file:
            lines = main_file.read()

        lines=lines.split('\n')[1:]
        LABELS=[]
        for i in lines:
            if len(i.split()) == 0:
                break
            LABELS=LABELS+[i.split()]

        if len(LABELS) > 1:
            ticks=[float(i[1]) for i in LABELS]
            if len(ticks) > 2:
                ticks[0],ticks[-1] = arr[0],arr[-1]
                for i in ticks[1:-1]:
                    plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

            if len(labels) == 0:
                labels=[re.sub('Gamma|G','Γ',re.sub('Undefined|Un|[0-9]','',i[0])) for i in LABELS]

            diff = len(ticks)-len(labels)
            if diff > 0:
                for i in range(diff):
                    labels=labels+['']

            else:
                labels = labels[:len(ticks)]
            plt.xticks(ticks,labels)

    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Noneispin(arr, bands, EXPORT, KLABELS, labels, figsize, vertical):
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = 'Times New Roman'

    plt.figure(figsize=figsize)
    plt.plot(arr,bands.T,color='red',linewidth=1,linestyle='-')
    plt.tick_params(axis='y', which='minor', color='gray')

    plt.axhline(linewidth=0.4,linestyle='-.',c='blue')
    if os.path.exists(KLABELS):
        with open(KLABELS, "r") as main_file:
            lines = main_file.read()

        lines=lines.split('\n')[1:]
        LABELS=[]
        for i in lines:
            if len(i.split()) == 0:
                break
            LABELS=LABELS+[i.split()]

        if len(LABELS) > 1:
            ticks=[float(i[1]) for i in LABELS]
            if len(ticks) > 2:
                ticks[0],ticks[-1] = arr[0],arr[-1]
                for i in ticks[1:-1]:
                    plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')

            if len(labels) == 0:
                labels=[re.sub('Gamma|G','Γ',re.sub('Undefined|Un|[0-9]','',i[0])) for i in LABELS]

            diff = len(ticks)-len(labels)
            if diff > 0:
                for i in range(diff):
                    labels=labels+['']

            else:
                labels = labels[:len(ticks)]
            plt.xticks(ticks,labels)

    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Energy (eV)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

