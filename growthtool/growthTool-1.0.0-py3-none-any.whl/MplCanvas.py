import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
import matplotlib.ticker as mtick
from numpy import linspace, max as maxvalue, arange, isnan
from pandas import cut, interval_range


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=6, height=3, dpi=85):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor('#e3ddcf')
        self.fig = fig
        super(MplCanvas, self).__init__(fig)


class SingleModel(MplCanvas):
    def __init__(self, points, x, y, formula, labels, ylim,x_scan,y_scan, golden=False):
        super(SingleModel, self).__init__()
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_facecolor('#e3ddcf')
        self.ax1.grid(True, linestyle=':', which='both')

        # underline the model that has been chose in first scan
        faceC = 'none'
        if golden:
            faceC = '#db8d39'
        self.ax1.set_title(f"Adjusted scans into model", y=1.007, pad=14, fontsize=12, bbox=dict(facecolor=faceC, edgecolor='none'))
        self.ax1.set_xlabel(f"date", fontsize=9)
        self.ax1.set_ylabel(f"absolute fruit size", fontsize=9)
        self.ax1.axis(ymin=ylim[0], ymax=ylim[1])

        # set plots - depends on models values
        xs = linspace(0, maxvalue(formula.x.__array__()))
        ys = formula(xs)


        print("MplCanvas-x_scan:", x_scan)
        print("MplCanvas-y_scan:", y_scan)
        print("labels: ", labels)

        # plot model line and data points
        self.ax1.plot(xs, ys, '#cf4e32', lw=1)
        self.ax1.plot(x, y, 'ko', ms=2)

        # plot two scans values and mark
        self.ax1.plot(points[0][:2], points[1][:2], 'go:', ms=3)
        self.ax1.plot(x_scan, y_scan, '#857f7e',ms=3)


        # plot picking date values and mark
        self.ax1.plot(points[0][2], points[1][2], 'bo')

        # drawing model annotations
        self.ax1.annotate(labels['1st'], xy=(points[0][0], points[1][0]), xytext=(points[0][0], points[1][0] - 6),
                          fontweight='bold', fontsize=8)
        self.ax1.annotate(labels['2nd'], xy=(points[0][1], points[1][1]), xytext=(points[0][1], points[1][1] + 2),
                          fontweight='bold', fontsize=8)
        self.ax1.annotate(labels['pick'], xy=(points[0][2], points[1][2]), xytext=(points[0][2], points[1][2] - 4.2),
                          fontweight='bold', fontsize=8)
        self.ax1.annotate(round(labels['model_value'], 2), xy=(points[0][2], labels['model_value']),
                          xytext=(points[0][2], labels['model_value'] - 2), fontweight='bold', fontsize=8)


class sizeDistribution(MplCanvas):
    def __init__(self, result):

        super(sizeDistribution, self).__init__()
        # left graph
        # in case that avg pred size value fall out of customer caliber range

        x, y = result.get_left_graph()
        x_labels = x.apply(lambda w: w.left)
        if not all(isnan(value) for i, value in y.items()):
            self.ax1 = self.fig.add_subplot(121)
            self.ax1.bar(x.astype(str), y, color='#808000', width=0.7)
            self.ax1.set_facecolor('#e3ddcf')
            self.ax1.set_title('Size Distribution (2nd scan)')
            self.ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

            # ticks annoation and positioning
            ticks_loc = self.ax1.set_xticklabels(x_labels, fontsize=7)
            if len(ticks_loc) > 15:
                for i, tick in enumerate(ticks_loc):
                    tick.set_y(tick.get_position()[1] - (i % 2) * 0.05)

            # bar annotations
            for p in self.ax1.patches:
                if p.get_height() < 1:
                    pass
                else:
                    self.ax1.annotate(str(int(p.get_height())) + '%', (p.get_x() + p.get_width() * 0.2, p.get_height()), fontsize=8)

        # right graph
        # in case that avg pred size value fall out of customer caliber range
        y, y_potential, x = result.get_right_graph()
        if not all(isnan(value) for value in y):
            self.ax2 = self.fig.add_subplot(122)
            _X = arange(len(x))
            # Normalized bar
            # flip data according to packing method data
            y = y.sort_index(ascending=False).reset_index(drop=True)
            # Check if there is history actual packout, if not only one bar is plotted
            if y_potential is not None:
                w = 0.35
                l1 = self.ax2.bar(_X, y, width=w, color='#db8d39')
                l2 = self.ax2.bar(_X + w, y_potential, width=w, color='#808000')
                self.ax2.legend((l1, l2), ('model', 'history'), facecolor='#b0a7a2', fontsize=8.5, loc='upper left')
            else:
                w = 0.6
                self.ax2.bar(_X, y, width=w, color='#db8d39')

            # design
            self.ax2.set_facecolor('#e3ddcf')
            self.ax2.set_title('Projected Packing Distribution')
            self.ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
            self.ax2.set_xticks(_X)
            self.ax2.set_xticklabels(x, fontsize=9)

            # annotations
            for p in self.ax2.patches:
                if p.get_height() < 1:
                    pass
                else:
                    self.ax2.annotate(str(int(p.get_height())) + '%', (p.get_x(), p.get_height()), fontsize=7)


class OneBin(MplCanvas):
    def __init__(self, samples):
        super(OneBin, self).__init__()
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_facecolor((0.92, 0.92, 0.75))
        self.ax1.grid(True, linestyle=':', which='both')
        self.ax1.set_title('Samples distribution Bin-1', fontsize=16)
        self.ax1.set_xlabel(f"size", fontsize=11)
        self.ax1.set_ylabel(f"frequency", fontsize=11)

        # set dist
        binOne = interval_range(start=int(samples.min()), end=int(samples.max()), periods=int(samples.max()) - int(samples.min()), closed='left')
        dist = cut(samples, bins=binOne, include_lowest=True).value_counts(normalize=True).sort_index()
        _X = arange(int(samples.max()) - int(samples.min()))
        self.ax1.bar(_X, round(dist.mul(100), 1), width=0.92, color='#db8d39')
        self.ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        self.ax1.set_xticks(_X)
        self.ax1.set_xticklabels(binOne.left)
        self.ax1.tick_params(axis='x', which='major', labelsize=7.5)

        # in case of many bins to be deployed
        if len(binOne.left) > 35:
            self.ax1.xaxis.set_major_locator(pyplot.MaxNLocator(35))
