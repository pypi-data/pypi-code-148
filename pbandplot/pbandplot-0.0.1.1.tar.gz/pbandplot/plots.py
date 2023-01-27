import numpy as np
import matplotlib.pyplot as plt

def main(PLOT, EXPORT, labels, figsize, vertical, broken):
    with open(PLOT, "r") as main_file:
        lines = main_file.readlines()
    
    ticks = [float(i) for i in lines[1].split()[1:]]
    arr = []
    fre = []
    k = 0
    for i in lines[2:]:
        str = i.split()
        if len(str) > 0:
            j = float(str[0])
            if j == 0.0:
                k += 1
            if k == 1:
                arr.append(j)
                fre.append(float(str[1]))
            else:
                fre.append(float(str[1]))
    
    arr = np.array(arr)
    fre = np.array(fre).reshape(-1,len(arr))
    if broken is None:
        Nobroken(arr, fre, ticks, EXPORT, labels, figsize, vertical)
    else:
        Broken(arr, fre, ticks, EXPORT, labels, figsize, vertical, broken)

def Broken(arr, fre, ticks, EXPORT, labels, figsize, vertical, broken):
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = 'Times New Roman'
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[broken[2], 1-broken[2]], figsize=figsize)
    fig.subplots_adjust(hspace=0.0)
    ax1.plot(arr,fre.T,color='red',linewidth=1,linestyle='-')
    ax2.plot(arr,fre.T,color='red',linewidth=1,linestyle='-')
    plt.xlim(arr[0], arr[-1])
    if vertical is None:
        vertical = plt.ylim()

    ax1.set_ylim(broken[1], vertical[1])
    ax2.set_ylim(vertical[0], broken[0])
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.set_ticks_position(position='none')

    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax2.axhline(linewidth=0.4,linestyle='-.',c='blue')
    
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            ax1.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
            ax2.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
    
    diff = len(ticks)-len(labels)
    if diff > 0:
        for i in range(diff):
            labels=labels+['']
    else:
        labels = labels[:len(ticks)]
    
    plt.xticks(ticks,labels)
    plt.suptitle('Frequency (THz)', rotation=90, x=0.06, y=0.6)
    kwargs = dict(marker=[(-1, -1), (1, 1)], markersize=6,
                  linestyle='', color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0.02, 0.02], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [0.98, 0.98], transform=ax2.transAxes, **kwargs)
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

def Nobroken(arr, fre, ticks, EXPORT, labels, figsize, vertical):
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.figure(figsize=figsize)
    plt.plot(arr,fre.T,color='red',linewidth=1,linestyle='-')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.axhline(linewidth=0.4,linestyle='-.',c='blue')
    
    if len(ticks) > 2:
        ticks[0],ticks[-1] = arr[0],arr[-1]
        for i in ticks[1:-1]:
            plt.axvline(i,linewidth=0.4,linestyle='-.',c='gray')
    
    diff = len(ticks)-len(labels)
    if diff > 0:
        for i in range(diff):
            labels=labels+['']
    else:
        labels = labels[:len(ticks)]
    
    plt.xticks(ticks,labels)
    plt.xlim(arr[0], arr[-1])
    plt.ylim(vertical)
    plt.ylabel('Frequency (THz)')
    plt.savefig(EXPORT, dpi=750, transparent=True, bbox_inches='tight')

