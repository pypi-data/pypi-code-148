import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.font_manager.fontManager.addfont('/home/fayalacruz/runs/reg_storm/info/plots/Helvetica.ttf')
mpl.font_manager.fontManager.addfont('/home/fayalacruz/runs/reg_storm/info/plots/Helvetica-Light.ttf')
mpl.font_manager.fontManager.addfont('/home/fayalacruz/runs/reg_storm/info/plots/Helvetica-Bold.ttf')

newparams = {'axes.grid': False,
             'lines.linewidth': 1.5,
             'ytick.labelsize':11,
             'xtick.labelsize':11,
             'axes.labelsize':12,
             'axes.titlesize':18,
             'legend.fontsize':13,
             'figure.titlesize':16,
             'font.family':'Helvetica Light'}
plt.rcParams.update(newparams)
