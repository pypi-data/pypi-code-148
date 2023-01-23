import pandas as pd
import numpy as np 


def supertrend(df,atr_longitud,factor):
    price_diffs = [df['high'].astype(float) - df['low'].astype(float),df['high'].astype(float) - df['close'].astype(float).shift(),df['close'].astype(float).shift() - df['low'].astype(float)]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    atr = true_range.ewm(alpha=1/atr_longitud,min_periods=atr_longitud).mean() 
    hl2 = (df['high'].astype(float) + df['low'].astype(float)) / 2
    final_upperband = upperband = hl2 + (factor * atr)
    final_lowerband = lowerband = hl2 - (factor * atr)
    supertrend = [True] * len(df)
    for i in range(1, len(df.index)):
        curr, prev = i, i-1
        if df['close'].astype(float)[curr] > final_upperband[prev]:
            supertrend[curr] = True
        elif df['close'].astype(float)[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        else:
            supertrend[curr] = supertrend[prev]
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan
    lista=pd.DataFrame({'Supertrend': supertrend}, index=df.index)
    super10=lista.iloc[-10].bool()
    super9=lista.iloc[-9].bool()
    super8=lista.iloc[-8].bool()
    super7=lista.iloc[-7].bool()
    super6=lista.iloc[-6].bool()
    super5=lista.iloc[-5].bool()
    super4=lista.iloc[-4].bool()
    super3=lista.iloc[-3].bool()
    super2=lista.iloc[-2].bool()
    super1=lista.iloc[-1].bool()
    seniales=""
    if super1==True and super2==True and super3==False and super4==False and super5==False and super6==False:
        seniales="Compra"

    elif super1==True or super2==True or super3==True or super4==True:
        seniales="Compra"

    elif super1==False or super2==False  or super3==False or super4==False:
        seniales="Venta"

    elif super1==False and super2==False and super3==True and super4==True and super5==True and super6==True:
        seniales="Venta"

    return seniales
def bandas_bollinger(df, longitud, desviacion):
    df['media'] = df['close'].rolling(window=longitud).mean()
    media_movil = df['close'].rolling(window=longitud).mean()
    desviacion_estandar = df['close'].rolling(window=longitud).std(ddof=0)
    banda_superior = media_movil.astype(float) + desviacion * desviacion_estandar.astype(float)
    banda_inferior = media_movil.astype(float) - desviacion * desviacion_estandar.astype(float)
    ultima_media = df['media'].iloc[-1]
    ultima_banda_superior = banda_superior.iloc[-1]
    ultima_banda_inferior = banda_inferior.iloc[-1]
    return ultima_media, ultima_banda_superior, ultima_banda_inferior
def estocastico(df,k_periodo,d_periodo):
    high_roll = df["high"].rolling(k_periodo).max()
    low_roll = df["low"].rolling(k_periodo).min()
    num = df["close"].astype(float) - low_roll.astype(float)
    denom = high_roll.astype(float) - low_roll.astype(float)
    df["%K"] = (num / denom) * 100
    df["%D"] = df["%K"].rolling(d_periodo).mean()
    estocasticok=df["%K"].iloc[-1]
    estocasticod=df["%D"].iloc[-1]
    return estocasticok,estocasticod
def macd(df,rapidaema,lentoema,senialperiodo):
    k = df['close'].ewm(span=rapidaema, adjust=False, min_periods=rapidaema).mean()
    d = df['close'].ewm(span=lentoema, adjust=False, min_periods=lentoema).mean()
    macd = k - d
    macd_s = macd.ewm(span=senialperiodo, adjust=False, min_periods=senialperiodo).mean()
    macd_h = macd - macd_s
    macdb=macd.iloc[-1]
    macdsenial=macd_s.iloc[-1]
    divergencia=macd_h.iloc[-1]
    return macdb,macdsenial,divergencia
def rsi(df,rsi_period,ema,longirsi,emamovil):
    close_delta = df['close'].astype(float).diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    if ema == "ema":
        ma_up = up.ewm(com = rsi_period - 1, adjust=True, min_periods = rsi_period).mean()
        ma_down = down.ewm(com = rsi_period - 1, adjust=True, min_periods = rsi_period).mean()
        cierreema=df['close'].ewm(com = rsi_period - 1, adjust=True, min_periods = rsi_period).mean()
    elif ema=="sma":
        ma_up = up.rolling(rsi_period).mean()
        ma_down = down.rolling(rsi_period).mean()
    rsimedia = ma_up / ma_down
    rrmme=100 - (100/(1 + rsimedia))

    if emamovil=="sma":
        medidia=rrmme.rolling(longirsi).mean().iloc[-1]
        valormedia=medidia
    elif emamovil=="ema":
        medidia=rrmme.ewm(span=longirsi, min_periods=longirsi).mean()
        valormedia=medidia.iloc[-1]
    rsivalor = rrmme.iloc[-1]
    return rsivalor,valormedia
def tendenciaactual(df,cualma,ma1,ma2,ma3):
    if cualma=="sma":
        mavalor1 = df['close'].rolling(ma1).mean().iloc[-1]
        mavalor2 = df['close'].rolling(ma2).mean().iloc[-1]
        mavalor3 = df['close'].rolling(ma3).mean().iloc[-1]
    elif cualma=="ema":
        mavalor1 = df['close'].ewm(span=ma1, min_periods=ma1).mean().iloc[-1]
        mavalor2 = df['close'].ewm(span=ma2, min_periods=ma2).mean().iloc[-1]
        mavalor3 = df['close'].ewm(span=ma3, min_periods=ma3).mean().iloc[-1]

    if float(mavalor1) > float(mavalor2) and float(mavalor1) > float(mavalor3):
        tendencia="ALCISTA"

    if float(mavalor1) > float(mavalor2) and float(mavalor1) < float(mavalor3):
        tendencia="TENDICIA ALCISTA INICIA"

    if float(mavalor1) < float(mavalor2) and float(mavalor1) < float(mavalor3):
        tendencia="BAJISTA"

    if float(mavalor1) < float(mavalor2) and float(mavalor1) > float(mavalor3):
        tendencia="TENDENCIA BAJISTA INICIA"

    return tendencia
def soportesyresistencias(df,tipo):
    alto=df['high'].iloc[-2]
    bajo=df['low'].iloc[-2]
    cierre=df['close'].iloc[-2]
    open=df['open'].iloc[-1]

    if tipo=="tradicional":
        pp = ((alto + bajo + cierre))/3
        re1 = (pp *2) - bajo
        so1 = (pp *2) - alto
        re2 = pp  + (alto - bajo)
        so2 = pp - (alto - bajo)

    if tipo=="classic":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = (pp *2) - bajo
        so1 = (pp *2) - alto
        re2 = pp  + 1 * pivot_range
        so2 = pp  - 1 * pivot_range
    elif tipo=="fibonacci":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = pp + 0.382 * pivot_range
        so1 = pp - 0.382 * pivot_range
        re2 = pp + 0.618 * pivot_range
        so2 = pp - 0.618 * pivot_range
    elif tipo=="woodie":
        pp = ((alto + bajo + open *2))/4
        pivot_range = alto - bajo
        re1 = pp * 2 - bajo
        so1 = pp *2 - alto
        re2 = pp + 1 * pivot_range
        so2 = pp - 1 * pivot_range
    elif tipo=="camarilla":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = cierre + pivot_range * 1.1 / 12.0
        so1 = cierre - pivot_range * 1.1 / 12.0
        re2 = cierre + pivot_range * 1.1 / 6.0
        so2 = cierre - pivot_range * 1.1 / 6.0


    return pp,so1,re1,so2,re2
def squeeze_momentum(df,length, mult, length_KC, mult_KC):

# calculate BB
    m_avg = df['close'].rolling(window=length).mean()
    m_std = df['close'].rolling(window=length).std(ddof=0)
    df['upper_BB'] = m_avg + mult * m_std
    df['lower_BB'] = m_avg - mult * m_std

    # calculate true range
    df['tr0'] = abs(df["high"] - df["low"])
    df['tr1'] = abs(df["high"] - df["close"].shift())
    df['tr2'] = abs(df["low"] - df["close"].shift())
    df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)

    # calculate KC
    range_ma = df['tr'].rolling(window=length_KC).mean()
    df['upper_KC'] = m_avg + range_ma * mult_KC
    df['lower_KC'] = m_avg - range_ma * mult_KC

    # calculate bar value
    highest = df['high'].rolling(window = length_KC).max()
    lowest = df['low'].rolling(window = length_KC).min()
    m1 = (highest + lowest)/2
    df['value'] = (df['close'] - (m1 + m_avg)/2)
    fit_y = np.array(range(0,length_KC))
    df['value'] = df['value'].rolling(window = length_KC).apply(lambda x: 
                            np.polyfit(fit_y, x, 1)[0] * (length_KC-1) + 
                            np.polyfit(fit_y, x, 1)[1], raw=True)

    # check for 'squeeze'
    df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])
    df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

    # buying window for long position:
    # 1. black cross becomes gray (the squeeze is released)
    long_cond1 = (df['squeeze_off'].iloc[-2] == False) & (df['squeeze_off'].iloc[-1] == True) 
    # 2. bar value is positive => the bar is light green k
    long_cond2 = df['value'].iloc[-1] > 0
    enter_long = long_cond1 and long_cond2

    # buying window for short position:
    # 1. black cross becomes gray (the squeeze is released)
    short_cond1 = (df['squeeze_off'].iloc[-2] == False) & (df['squeeze_off'].iloc[-1] == True) 
    # 2. bar value is negative => the bar is light red 
    short_cond2 = df['value'].iloc[-1] < 0
    enter_short = short_cond1 and short_cond2

    if enter_long:
        signal = "comprar"
    elif enter_short:
        signal = "vender"
    else:
        signal = "ninguna"

    return signal
def dmi(df,period,perioddi):
    df = df.copy()
    alphate = 1 / period
    adxperiodo = 1 / perioddi
    df['H-L'] = df['high'] - df['low']
    df['H-C'] = np.abs(df['high'] - df['close'].shift(1))
    df['L-C'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis = 1)
    del df['H-L'], df['H-C'], df['L-C']
    df['ATR'] = df['TR'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['H-pH'] = df['high'] - df['high'].shift(1)
    df['pL-L'] = df['low'].shift(1) - df['low']
    df['+DX'] = np.where((df['H-pH'] > df['pL-L']) & (df['H-pH'] > 0),df['H-pH'],0.0)
    df['-DX'] = np.where((df['H-pH'] < df['pL-L']) & (df['pL-L'] > 0),df['pL-L'],0.0)
    del df['H-pH'], df['pL-L']
    df['S+DM'] = df['+DX'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['S-DM'] = df['-DX'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['+DMI'] = (df['S+DM'] / df['ATR']) * 100
    df['-DMI'] = (df['S-DM'] / df['ATR']) * 100
    masx=df['+DMI'].iloc[-1]
    menosx=df['-DMI'].iloc[-1]
    df['DX'] = (np.abs(df['+DMI'] - df['-DMI']) / (df['+DMI'] + df['-DMI'])) * 100
    df['ADX'] = df['DX'].ewm(alpha = alphate, adjust = False).mean()
    del df['DX'], df['ATR'], df['TR'], df['-DX'], df['+DX'], df['+DMI'], df['-DMI']
    adxx=df['ADX'].iloc[-1]
    return adxx,masx,menosx
def aroon(df,periodoaron):
    df['up'] = 100 * df['high'].rolling(periodoaron + 1).apply(lambda x: x.argmax()) / periodoaron
    df['dn'] = 100 * df['low'].rolling(periodoaron + 1).apply(lambda x: x.argmin()) / periodoaron
    return df['up'].iloc[-1], df['dn'].iloc[-1]
def chandelierexit(df, atr_period, atrmulti):
    # Convertir los precios a float y comprobar si son válidos
    try:
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
    except ValueError:
        return ''
    
    # Calcular el Average True Range (ATR)
    df['range'] = df['high'] - df['low']
    df['Avg TR'] = df['range'].rolling(atr_period).mean()
    
    # Calcular el Chandelier Exit
    rolling_high = df["high"].rolling(atr_period).max()
    rolling_low = df["low"].rolling(atr_period).min()
    comprach = rolling_high - df['Avg TR'] * atrmulti
    ventach = rolling_low + df['Avg TR'] * atrmulti
    
    # Devolver la señal de compra o venta
    if df['close'].iloc[-1] > comprach.iloc[-1]:
        return 'comprar'
    else:
        return 'vender'
def rvi(df, longitud):
    open=df['open']
    close=df['close']
    high=df['high']
    low=df['low']
    a = close - open
    b = 2 * (close.shift(1) - open.shift(1))
    c = 2 * (close.shift(2) - open.shift(2))
    d = close.shift(3) - open.shift(3)
    numerator = a + b + c + d
    e = high - low
    f = 2 * (high.shift(1) - low.shift(1))
    g = 2 * (high.shift(2) - low.shift(2))
    h = high.shift(3) - low.shift(3)
    denominator = e + f + g + h
    rvi = numerator.rolling(longitud).mean() / denominator.rolling(longitud).mean()
    rvi1 = 2 * rvi.shift(1)
    rvi2 = 2 * rvi.shift(2)
    rvi3 = rvi.shift(3)
    rvi_signal = (rvi + rvi1 + rvi2 + rvi3) / 6
    return rvi.iloc[-1],rvi_signal.iloc[-1]
def williamd(df,periodo):
    highh = df['high'].rolling(periodo).max() 
    lowl = df['low'].rolling(periodo).min()
    wr = -100 * ((highh - df['close']) / (highh - lowl))
    return wr.iloc[-1]
def keltnerchannel(df,cual, longitud, multipl, atrlongi):
    tr1 = pd.DataFrame(df['high'] - df['low'])
    tr2 = pd.DataFrame(abs(df['high'] - df['close'].shift()))
    tr3 = pd.DataFrame(abs(df['low'] - df['close'].shift()))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(alpha = 1/atrlongi).mean()
    if cual=="sma":
        kc_middle = df['close'].rolling(longitud).mean()
        kc_upper = df['close'].rolling(longitud).mean() + multipl * atr
        kc_lower = df['close'].rolling(longitud).mean() - multipl * atr
    elif cual=="ema":
        kc_middle = df['close'].ewm(span=longitud, min_periods=longitud).mean()
        kc_upper = df['close'].ewm(span=longitud, min_periods=longitud).mean() + multipl * atr
        kc_lower = df['close'].ewm(span=longitud, min_periods=longitud).mean() - multipl * atr
    return kc_middle.iloc[-1], kc_upper.iloc[-1], kc_lower.iloc[-1]
def coppockcurve(df, roclargo, roccorto,wma):
    close=df['close']


    differencea = close.diff(roclargo)
    nprev_valueses = close.shift(roclargo)
    longROC = (differencea / nprev_valueses) * 100

    difference = close.diff(roccorto)
    nprev_values = close.shift(roccorto)
    shortROC = (difference / nprev_values) * 100

    ROC = longROC + shortROC

    weights = np.arange(1, wma + 1)

    wma = ROC.rolling(wma).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw = True)
   
   
    cc = wma.iloc[-1]
    return cc
def ao(df, corto,largo):
    
    # calculamos el medio
    medio = (df['high'] + df['low']) / 2
    # calculamos las medias
    cor=medio.rolling(corto).mean()
    lar=medio.rolling(largo).mean()
    #restamos los promedios
    ocilador=cor - lar
    return ocilador.iloc[-1]
