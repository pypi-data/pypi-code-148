import re

__builders = dict()
__default_ohlc = ["open", "high", "low", "close"]


def __get_file_name(class_name):
    res = re.findall("[A-Z][^A-Z]*", class_name)
    return "_".join([cur.lower() for cur in res])


def __load_module(module_path):
    p = module_path.rfind(".") + 1
    super_module = module_path[p:]
    try:
        module = __import__(module_path, fromlist=[super_module], level=0)
        return module
    except ImportError as e:
        raise e


def __get_class_by_name(class_name):
    file_name = __get_file_name(class_name)
    mod_name = "candlestick_patterns.patterns." + file_name
    if mod_name not in __builders:
        module = __load_module(mod_name)
        __builders[mod_name] = module
    else:
        module = __builders[mod_name]
    return getattr(module, class_name)


def __create_object(class_name, target):
    return __get_class_by_name(class_name)(target=target)


def hanging_man(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    hanging_man = __create_object("Hanging Man", target)
    return hanging_man.has_pattern(candles_df, ohlc, is_reversed)


def bearish_harami(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    bearish_harami = __create_object("Bearish Harami", target)
    return bearish_harami.has_pattern(candles_df, ohlc, is_reversed)


def bullish_harami(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    bullish_harami = __create_object("Bullish Harami", target)
    return bullish_harami.has_pattern(candles_df, ohlc, is_reversed)


def gravestone_doji(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    gravestone_doji = __create_object("Gravestone Doji", target)
    return gravestone_doji.has_pattern(candles_df, ohlc, is_reversed)


def dark_cloud_cover(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    dark_cloud_cover = __create_object("Dark Cloud Cover", target)
    return dark_cloud_cover.has_pattern(candles_df, ohlc, is_reversed)


def doji(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    doji = __create_object("Doji", target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)


def doji_star(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    doji_star = __create_object("Doji Star", target)
    return doji_star.has_pattern(candles_df, ohlc, is_reversed)


def dragonfly_doji(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    dragonfly_doji = __create_object("Dragonfly Doji", target)
    return dragonfly_doji.has_pattern(candles_df, ohlc, is_reversed)


def bearish_engulfing(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    bearish_engulfing = __create_object("Bearish Engulfing", target)
    return bearish_engulfing.has_pattern(candles_df, ohlc, is_reversed)


def bullish_engulfing(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    bullish_engulfing = __create_object("Bullish Engulfing", target)
    return bullish_engulfing.has_pattern(candles_df, ohlc, is_reversed)


def hammer(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    hammer = __create_object("Hammer", target)
    return hammer.has_pattern(candles_df, ohlc, is_reversed)


def inverted_hammer(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    inverted_hammer = __create_object("Inverted Hammer", target)
    return inverted_hammer.has_pattern(candles_df, ohlc, is_reversed)


def morning_star(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    morning_star = __create_object("Morning Star", target)
    return morning_star.has_pattern(candles_df, ohlc, is_reversed)


def morning_star_doji(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    morning_star_doji = __create_object("Morning Star Doji", target)
    return morning_star_doji.has_pattern(candles_df, ohlc, is_reversed)


def piercing_pattern(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    piercing_pattern = __create_object("Piercing Pattern", target)
    return piercing_pattern.has_pattern(candles_df, ohlc, is_reversed)


def raindrop(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    raindrop = __create_object("Raindrop", target)
    return raindrop.has_pattern(candles_df, ohlc, is_reversed)


def raindrop_doji(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    raindrop_doji = __create_object("Raindrop Doji", target)
    return raindrop_doji.has_pattern(candles_df, ohlc, is_reversed)


def star(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    star = __create_object("Star", target)
    return star.has_pattern(candles_df, ohlc, is_reversed)


def shooting_star(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    shooting_star = __create_object("Shooting Star", target)
    return shooting_star.has_pattern(candles_df, ohlc, is_reversed)


def check_all_patterns(candles_df, ohlc=__default_ohlc, is_reversed=False, target=None):
    all_results = {}
    all_results["Hanging Man"] = hanging_man(
        candles_df, ohlc, is_reversed, target)
    all_results["Bearish Harami"] = bearish_harami(
        candles_df, ohlc, is_reversed, target)
    all_results["Bullish Harami"] = bullish_harami(
        candles_df, ohlc, is_reversed, target)
    all_results["Gravestone Doji"] = gravestone_doji(
        candles_df, ohlc, is_reversed, target)
    all_results["Dark Cloud Cover"] = dark_cloud_cover(
        candles_df, ohlc, is_reversed, target)
    all_results["Doji"] = doji(candles_df, ohlc, is_reversed, target)
    all_results["Doji Star"] = doji_star(candles_df, ohlc, is_reversed, target)
    all_results["Dragonfly Doji"] = dragonfly_doji(
        candles_df, ohlc, is_reversed, target)
    all_results["Bearish Engulfing"] = bearish_engulfing(
        candles_df, ohlc, is_reversed, target)
    all_results["Bullish Engulfing"] = bullish_engulfing(
        candles_df, ohlc, is_reversed, target)
    all_results["Hammer"] = hammer(candles_df, ohlc, is_reversed, target)
    all_results["Inverted Hammer"] = inverted_hammer(
        candles_df, ohlc, is_reversed, target)
    all_results["Morning Star"] = morning_star(
        candles_df, ohlc, is_reversed, target)
    all_results["Morning Star Doji"] = morning_star_doji(
        candles_df, ohlc, is_reversed, target)
    all_results["Piercing Pattern"] = piercing_pattern(
        candles_df, ohlc, is_reversed, target)
    all_results["Raindrop"] = raindrop(candles_df, ohlc, is_reversed, target)
    all_results["Raindrop Doji"] = raindrop_doji(
        candles_df, ohlc, is_reversed, target)
    all_results["Star"] = star(candles_df, ohlc, is_reversed, target)
    all_results["Shooting Star"] = shooting_star(
        candles_df, ohlc, is_reversed, target)
    return all_results
