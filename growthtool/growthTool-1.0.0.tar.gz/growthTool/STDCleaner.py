import numpy as np
import pandas as pd
import enum

from scipy.stats import gaussian_kde, skew


class STDCleaner:

    class SkewnessSide(enum.Enum):
        Left = 1
        Right = -1

    @staticmethod
    def _get_min_max_caliper(manual_data, caliper_data):
        all_obs = pd.concat([manual_data, caliper_data])
        min_caliber = np.floor(np.min(all_obs))
        max_caliber = np.floor(np.max(all_obs))
        num_range = int(max_caliber - min_caliber + 1)
        return min_caliber, max_caliber, num_range

    @staticmethod
    def _get_mode(data_arr, obs_per_bin=50, kde_mode=True):
        if kde_mode:
            kde = gaussian_kde(data_arr)
            min_caliber, max_caliber, num_range = STDCleaner._get_min_max_caliper(pd.Series(data_arr),
                                                                                  pd.Series(data_arr))
            x_values = np.linspace(min_caliber, max_caliber, num=num_range * 4)
            pdf_estimated_values = kde(x_values)
            return x_values[np.argmax(pdf_estimated_values)]
        if len(data_arr) < 250:
            obs_per_bin = obs_per_bin / 4
        elif len(data_arr) < 500:
            obs_per_bin = obs_per_bin / 2
        n_bins = int(len(data_arr) / obs_per_bin)
        hist_data = np.histogram(data_arr, n_bins)
        hist_frame = pd.DataFrame({"count": hist_data[0], 'caliber_in_mm': hist_data[1][:-1]})
        hist_frame_sorted = hist_frame.sort_values("count", ascending=False)
        mode_value = hist_frame_sorted.iloc[:3]['caliber_in_mm'].mean()
        return mode_value

    @staticmethod
    def _one_side_std(data_arr, q=0.00125, side=SkewnessSide.Left):
        q_val1, q_val2, q_val3 = 0.33, 0.02, 0.00125
        if side == STDCleaner.SkewnessSide.Right:
            q_val1, q_val2, q_val3 = 1 - q_val1, 1 - q_val2, 1 - q_val3
        num_std = 1 if q == q_val1 else 2 if q == q_val2 else 3 if q == q_val3 else -1
        if num_std < 0:
            print("please give a proper quantile parameter")
        return np.abs(np.quantile(data_arr, q) - STDCleaner._get_mode(data_arr)) / num_std

    @staticmethod
    def _get_std_with_skewness(data_arr, skew_val, skewness_threshold=1.5):
        quantile = 0.02 if len(data_arr) < 500 else 0.00125
        if skew_val > skewness_threshold:
            side = STDCleaner.SkewnessSide.Left
        elif skew_val < -skewness_threshold:
            side = STDCleaner.SkewnessSide.Right
            quantile = 1 - quantile
        try:
            return STDCleaner._one_side_std(data_arr, q=quantile, side=side)
        except NameError:
            return np.std(data_arr)

    @staticmethod
    def clean_std(measurements_df, n_std=2, skew_threshold=1.5):
        data_arr = measurements_df['diameter'].to_numpy()
        skew_val = skew(data_arr)
        std_cal = STDCleaner._get_std_with_skewness(data_arr, skew_val, skewness_threshold=1.5)
        if np.abs(skew_val) > skew_threshold:
            center_caliber = STDCleaner._get_mode(data_arr)
        else:
            center_caliber = np.median(data_arr)
        l1 = data_arr >= center_caliber - n_std * std_cal
        l2 = data_arr <= center_caliber + n_std * std_cal
        return measurements_df[l1 & l2]