# from numpy import array, max as max_np, linspace
from scipy import interpolate
# from scipy.interpolate import splev
# import matplotlib.pyplot as plt
import pickle
# import blockInfo
from os.path import join, isdir
# from os import mkdir
# from json import load

import settings

def update():
    degree = settings.config['interpolate_params']['degree']
    smooth_f = settings.config['interpolate_params']['smooth_f']

    models_info = settings.open_models_info()
    samples_info = settings.open_models_samples()
    lines = []
    for i, model in models_info.iterrows():
        func = None
        x = samples_info[samples_info['model_id'] == model['model_id']]['accumulated_days']
        y = samples_info[samples_info['model_id'] == model['model_id']]['size']
        try:
            spl = interpolate.splrep(x, y, s=smooth_f, k=degree)
            func = interpolate.PPoly.from_spline(spl)
            # prints
            # xs = linspace(0, max_np(func.x.__array__()), 100)
            # ys = splev(xs, spl)
            # plt.plot(xs, ys, 'g', lw=3)
            # plt.plot(x, y, 'ro', ms=5)
            # plt.title(model.model_id)
            # plt.xlabel('Days')
            # plt.ylabel('Fruit size')
            # if isdir(join('output', 'models')) is False:
            #     mkdir(join('output', 'models'))
            # plt.savefig(join('output', 'models', model.model_id))
            # plt.close()
        except TypeError as e:
            print(repr(e), model.model_id)
        except ValueError as e:
            print(repr(e), model.model_id)
        finally:
            lines.append(func)
            # update place in .pkl
            models_info.at[i, 'model_formula'] = i

    with open(join(settings.dep_path, 'interpolator.pkl'), 'wb') as f:
        pickle.dump(lines, f)
    models_info.to_csv(join(settings.dep_path, 'models_info.csv'),index=False)

if __name__ == '__main__':
    update()