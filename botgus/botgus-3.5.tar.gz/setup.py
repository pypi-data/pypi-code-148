from distutils.core import setup

long_description = '''
INDICADORES DE BOT GUS
\n
INDICADORES LISTOS PARA BINANCE:
\n
FUNCION PARA OBTENER DATOS HISTORICOS DE BINANCE:
\n

def datos():
\n
    if temporalidad=="1M":
\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1MINUTE, "4 hours ago UTC")
\n
    if temporalidad=="5M":\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_5MINUTE, "17 hours ago UTC")\n
    if temporalidad=="15M":\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_15MINUTE, "3 days ago UTC")\n
    if temporalidad=="30M":\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_30MINUTE, "5 days ago UTC")\n
    if temporalidad=="1H":\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1HOUR, "9 days ago UTC")\n
    if temporalidad=="4H":\n
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_4HOUR, "34 days ago UTC")\n
    data = pd.DataFrame(klines)\n
    data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']\n
    datos = data[['open', 'high', 'low', 'close','volume']].astype(float)\n
    df=datos.copy()\n
    return df\n
\n
Formato de funcion:
supertrend(df,atr_longitud,factor)
\n
Devuelve 1: señal de Compra o Venta
\n
Valores devueltos:
\n
Compra
\n
Venta
\n
Forma de llamarlo:\n
botgus.supertrend(datos(),10,3)
\n
bandas_bollinger(df, longitud, desviacion)
\n
Devuelve 3 valores: valor banda superior, valor banda inferior, valor media movil.
\n
Valores devueltos:
\n
Banda superior
\n
Media movil
\n
Banda inferior
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
estocastico(df,k_periodo,d_periodo)
Devuelve 2 valores: Valor estocastico K y estocastico D
\n
Forma de llamarlo:\n
botgus.estocastico(datos(),14,3)
\n
macd(df,rapidaema,lentoema,senialperiodo)
Devuelve 3 valores: Valor Macd, Valor señal de macd, valor divergencia
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
rsi(df,rsi_period,ema,longirsi,emamovil)
Devuelve 2 valores: Valor de rsi y valor de media movil de rsi
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
tendenciaactual(df,cualma,ma1,ma2,ma3)
Devuelve 1: Valor de tendencia actual
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
soportesyresistencias(df,tipo)
Devuelve 5 valores: Pivote central, soporte 1, resistencia 1, soporte 2, resistencia 2
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
squeeze_momentum(df,length, mult, length_KC, mult_KC):
Devuelve 1: Valor de compra o venta
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
dmi(df,period,perioddi)
Devuelve 3: Valores adx, adx + , adx -
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
aroon(df,periodoaron)
Devuelve 2: Valores Arron arriba, Arron Abajo
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
chandelierexit(df, atr_period, atrmulti)
Devuelve 1: Valor de compra o venta
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
rvi(df, longitud)
Devuelve 2: Valores rvi y rvi señal
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
williamd(df,periodo)
Devuelve 1: Valor william %D
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n

keltnerchannel(df,cual, longitud, multipl, atrlongi)
Devuelve 3: Valores banda superior, banda inferior, media movil
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n

coppockcurve(df, roclargo, roccorto,wma):
Devuelve 1: Valor curva coppock
\n
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
\n
ao(df, corto,largo)
Devuelve 1: Valor oscilador asombroso
Forma de llamarlo:\n
botgus.bandas_bollinger(datos(),20,2)
'''

setup(name='botgus',
      version='3.5',
      py_modules=['botgus'],
      description='BOTGUS forma de uso',
      long_description=long_description,
      )
