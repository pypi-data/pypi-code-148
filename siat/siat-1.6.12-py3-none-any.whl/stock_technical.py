# -*- coding: utf-8 -*-
"""
本模块功能：股票技术分析 technical analysis
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2023年1月27日
最新修订日期：2023年1月27日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')

from siat.common import *
from siat.translate import *
from siat.grafix import *
from siat.security_prices import *
from siat.stock import *
#==============================================================================
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(12.8,7.2)
plt.rcParams['figure.dpi']=300
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize']=11 #横轴字体大小
plt.rcParams['ytick.labelsize']=11 #纵轴字体大小

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14
legend_txt_size=14

import mplfinance as mpf

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    mpfrc={'font.family': 'SimHei'}

if czxt in ['darwin']: #MacOSX
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family': 'Heiti TC'}

if czxt in ['linux']: #website Jupyter
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family':'Heiti TC'}

# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
#==============================================================================
if __name__ =="__main__":
    ticker='AAPL'
    start='2022-12-1'
    end='2023-1-26'
    ahead_days=30*2
    start1=date_adjust(start,adjust=-ahead_days)
    
    df=get_price(ticker,start1,end)
    
    RSI_days=14
    
    MA_days=[5,20]
    
    MACD_fastperiod=12
    MACD_slowperiod=26
    MACD_signalperiod=9
    
    KDJ_fastk_period=5
    KDJ_slowk_period=3
    KDJ_slowk_matype=0
    KDJ_slowd_period=3
    KDJ_slowd_matype=0
    
    VOL_fastperiod=5
    VOL_slowperiod=10
    
    PSY_days=12
    
    ARBR_days=26
    
    CR_days=16
    CRMA_list=[5,10,20]
    
    EMV_days=14
    EMV_madays=9
    
    BULL_days=20
    BULL_nbdevup=2
    BULL_nbdevdn=2
    BULL_matype=0
    
    TRIX_days=12
    TRIX_madays=20
    
    DMA_fastperiod=10
    DMA_slowperiod=50
    DMA_madays=10
    
    BIAS_list=[6,12,24]
    
    CCI_days=14
    
    WR_list=[10,6]
    
    ROC_days=12
    ROC_madays=6
    
    DMI_DIdays=14
    DMI_ADXdays=6
    
def calc_technical(df,start,end, \
                   RSI_days=14, \
                   MA_days=[5,20], \
                   MACD_fastperiod=12,MACD_slowperiod=26,MACD_signalperiod=9, \
                   KDJ_fastk_period=9,KDJ_slowk_period=5,KDJ_slowk_matype=1, \
                   KDJ_slowd_period=5,KDJ_slowd_matype=1, \
                   VOL_fastperiod=5,VOL_slowperiod=10, \
                   PSY_days=12, \
                   ARBR_days=26, \
                   EMV_days=14,EMV_madays=9, \
                   BULL_days=20,BULL_nbdevup=2,BULL_nbdevdn=2,BULL_matype=0, \
                   TRIX_days=12,TRIX_madays=20, \
                   BIAS_list=[6,12,24], \
                   CCI_days=14, \
                   WR_list=[10,6], \
                   ROC_days=12,ROC_madays=6, \
                   DMI_DIdays=14,DMI_ADXdays=6):
    """
    功能：计算股票的技术分析指标
    输入：df，四种股价Open/Close/High/Low，成交量Volume
    输出：df
    支持的指标：
    RSI、OBV、MACD、 KDJ、 SAR、  VOL、 PSY、 ARBR、 CR、 EMV、 
    BOLL、 TRIX、 DMA、 BIAS、 CCI、 W%R、 ROC、 DMI
    """
    
    # 导入需要的包
    import talib    
    
    # RSI，相对强弱指标
    """
    计算公式：RSI有两种计算方法：
        第一种方法：
        假设A为N日内收盘价涨幅的正数之和，B为N日内收盘价涨幅的负数之和再乘以（-1），
        这样，A和B均为正，将A，B代入RSI计算公式，则：
        RSI(N) = A ÷ （A + B） × 100
        第二种方法：
        RS(相对强度) = N日内收盘价涨数和之均值 ÷ N日内收盘价跌数和之均值
        RSI = 100 - 100 ÷ （1+RS）
        
    指标解读：
    80-100 极强 卖出
    50-80 强 观望，谨慎卖出
    20-50 弱 观望，谨慎买入
    0-20 极弱 买入        
    """
    df['rsi'] = talib.RSI(df['Close'], timeperiod=RSI_days)
    
    #===== OBV：能量潮
    """
    OBV = 前一天的OBV ± 当日成交量
    说明：（当日收盘价高于前日收盘价，成交量定位为正值，取加号；当日收盘价低于前日收盘价，成交量定义为负值，取减号；二者相等计为0）
    """
    df['obv'] = talib.OBV(df['Close'],df['Volume'])
    
    #====== MA: 简单、加权移动平均
    """
    MA，又称移动平均线，是借助统计处理方式将若干天的股票价格加以平均，然后连接成一条线，用以观察股价趋势。
    移动平均线通常有3日、6日、10日、12日、24日、30日、72日、200日、288日、13周、26周、52周等等，不一而足，
    其目的在取得某一段期间的平均成本，而以此平均成本的移动曲线配合每日收盘价的线路变化分析某一期间多空的优劣形势，
    以研判股价的可能变化。
    一般来说，现行价格在平均价之上，意味着市场买力（需求）较大，行情看好；
    反之，行情价在平均价之下，则意味着供过于求，卖压显然较重，行情看淡。    
    """
    for mad in MA_days:
        df['ma'+str(mad)] = talib.MA(df['Close'],timeperiod=mad)
        df['ema'+str(mad)] = talib.EMA(df['Close'],timeperiod=mad)
    
    #===== MACD：指数平滑异同平均线
    """
    计算方法：快速时间窗口设为12日，慢速时间窗口设为26日，DIF参数设为9日
        3.1) 计算指数平滑移动平均值（EMA）
        12日EMA的计算公式为：
        EMA(12) = 昨日EMA(12)  ×  11 ÷ 13 + 今日收盘价 × 2 ÷ 13
        26日EMA的计算公式为：
        EMA(26) = 昨日EMA(26) × 25 ÷ 27 + 今日收盘价 × 2 ÷ 27
        
        3.2) 计算离差值（DIF）
        DIF = 今日EMA(12) – 今日EMA(26)
        
        3.3) 计算DIF的9日DEA
        根据差值计算其9日的DEA，即差值平均
        今日DEA = 昨日DEA × 8 ÷ 10 + 今日DIF × 2 ÷ 10    
    
    形态解读：
        1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。
        2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
        3.DEA线与K线发生背离，行情反转信号。
        4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号。
        
    MACD一则去掉移动平均线频繁的假讯号缺陷，二则能确保移动平均线最大的战果。
        1. MACD金叉：DIF由下向上突破DEM，为买入信号。
        2. MACD死叉：DIF由上向下突破DEM，为卖出信号。
        3. MACD绿转红：MACD值由负变正，市场由空头转为多头。
        4. MACD红转绿：MACD值由正变负，市场由多头转为空头。        
    """
    df['DIFF'],df['DEA'],df['MACD']=talib.MACD(df['Close'], \
                                fastperiod=MACD_fastperiod, \
                                slowperiod=MACD_slowperiod, \
                                signalperiod=MACD_signalperiod)

    # KDJ: 随机指标
    """
    计算公式：
        1) 以日KDJ数值的计算为例
        N日RSV = (CN – LN)÷(HN-LN) ×100
        说明：CN为第N日收盘价；LN为N日内的最低价；HN为N日内的最高价，RSV值始终在1~100间波动
        2) 计算K值与D值
        当日K值 = 2/3 × 前一日K值 + 1/3 × 当日RSV
        当日D值 = 2/3 × 前一日D值 + 1/3 × 当日K值
        如果没有前一日K值与D值，则可分别用50来代替
        3) 计算J值
        J = 3D – 2K    
    
    指标解读：
    
    """
    df['kdj_k'],df['kdj_d'] = talib.STOCH(df['High'],df['Low'],df['Close'], \
                        fastk_period=KDJ_fastk_period,
                        slowk_period=KDJ_slowk_period, 
                        slowk_matype=KDJ_slowk_matype, 
                        slowd_period=KDJ_slowd_period, 
                        slowd_matype=KDJ_slowd_matype)
    df['kdj_j'] = 3*df['kdj_k'] - 2*df['kdj_d']

    # SAR: 抛物转向
    """
    计算过程：
        1）先选定一段时间判断为上涨或下跌
        2）如果是看涨，则第一天的SAR值必须是近期内的最低价；
        如果是看跌，则第一天的SAR值必须是近期的最高价。
        3）第二天的SAR值，则为第一天的最高价（看涨时）或是最低价（看跌时）与第一天的SAR值的差距乘上加速因子，
        再加上第一天的SAR值就可以求得。
        4）每日的SAR值都可用上述方法类推，公式归纳如下：
        SAR(N) = SAR(N-1) + AF × [(EP(N-1) – SAR(N-1))]
        SAR(N) = 第N日的SAR值
        SAR(N-1) = 第(N-1)日的SAR值
        说明：AF表示加速因子；EP表示极点价，如果是看涨一段期间，则EP为这段时间的最高价，
        如果是看跌一段期间，则EP为这段时间的最低价；EP(N-1)等于第(N-1)日的极点价
        5）加速因子第一次取0.02，假若第一天的最高价比前一天的最高价还高，则加速因子增加0.02，
        如无新高则加速因子沿用前一天的数值，但加速因子最高不能超过0.2。反之，下跌也类推
        6）如果是看涨期间，计算出某日的SAR值比当日或前一日的最低价高，则应以当日或前一日的最低价为某日之SAR值；
        如果是看跌期间，计算某日的SAR值比当日或前一日的最高价低，则应以当日或前一日的最高价为某日的SAR值。
        7）SAR指标基准周期的参数为2，如2日、2周、2月等，其计算周期的参数变动范围为2~8
        8）SAR指标在股价分析系统的主图上显示为“O”形点状图。    
    """
    df['sar'] = talib.SAR(df['High'],df['Low'])

    # VOL: 成交量
    """
    柱状图是成交量，两条曲线是成交量的移动平均    
    """
    df['vol'+str(VOL_fastperiod)] = talib.MA(df['Volume'],timeperiod=VOL_fastperiod)
    df['vol'+str(VOL_slowperiod)] = talib.MA(df['Volume'],timeperiod=VOL_slowperiod)
    
    # PSY: 心理线
    """
    计算公式：
    PSY(N) = A/N × 100
    说明：N为天数，A为在这N天之中股价上涨的天数    
    """
    df['ext_0'] = df['Close']-df['Close'].shift(1)
    df['ext_1'] = 0
    df.loc[df['ext_0']>0,'ext_1'] = 1
    df['ext_2'] = df['ext_1'].rolling(window=PSY_days).sum()
    df['psy'] = (df['ext_2']/float(PSY_days))*100
    
    df.drop(columns = ['ext_0','ext_1','ext_2'],inplace=True) 
    
    # ARBR: 人气和意愿指标, AR为人气指标，BR为买卖意愿指标
    """
    计算公式：
    AR(N) = N日内（H-O）之和 ÷ N日内（O-L）之和 × 100
    说明：H表示当天最高价；L表示当天最低价；O表示当天开盘价；N表示设定的时间参数，一般原始参数日缺省值为26日
    BR(N) = N日内（H-CY）之和 ÷ N日内（CY-L）之和 × 100
    说明：H表示当天最高价；L表示当天最低价；CY表示前一交易日的收盘价，N表示设定的时间参数，一般原始参数缺省值为26日    
    """
    df['h_o'] = df['High'] - df['Open']
    df['o_l'] = df['Open'] - df['Low']
    df['h_o_sum'] = df['h_o'].rolling(window=ARBR_days).sum()
    df['o_l_sum'] = df['o_l'].rolling(window=ARBR_days).sum()
    df['ar'] = (df['h_o_sum']/df['o_l_sum'])*100
    df['h_c'] = df['High'] - df['Close']
    df['c_l'] = df['Close'] - df['Low']
    df['h_c_sum'] = df['h_c'].rolling(window=ARBR_days).sum()
    df['c_l_sum'] = df['c_l'].rolling(window=ARBR_days).sum()
    df['br'] = (df['h_c_sum']/df['c_l_sum'])*100

    df.drop(columns = ['h_o','o_l','h_o_sum','o_l_sum','h_c','c_l','h_c_sum','c_l_sum'],inplace=True) 

    # CR: 带状能力线或中间意愿指标
    """
    计算过程：
    1）计算中间价，取以下四种中一种，任选：
    中间价 = （最高价 + 最低价）÷2
    中间价 = （最高价 + 最低价 + 收盘价）÷3
    中间价 = （最高价 + 最低价 + 开盘价 + 收盘价）÷4
    中间价 = （2倍的开盘价 + 最高价 + 最低价）÷4
    2）计算CR:
    CR = N日内（当日最高价 – 上个交易日的中间价）之和 ÷ N日内（上个交易日的中间价 – 当日最低价）之和
    说明：N为设定的时间周期参数，一般原始参数日设定为26日
    3）计算CR值在不同时间周期内的移动平均值：这三条移动平均曲线分别为MA1 MA2 MA3,时间周期分别为5日 10日 20日    
    """
    df['m_price'] = (df['High'] + df['Low'])/2
    df['h_m'] = df['High']-df['m_price'].shift(1)
    df['m_l'] = df['m_price'].shift(1)-df['Low']
    df['h_m_sum'] = df['h_m'].rolling(window=CR_days).sum()
    df['m_l_sum'] = df['m_l'].rolling(window=CR_days).sum()
    df['cr'] = (df['h_m_sum']/df['m_l_sum'])*100
    
    for crmad in CRMA_list:
        df['crma'+str(crmad)] = talib.MA(df['cr'],timeperiod=crmad)
    
    df.drop(columns = ['m_price','h_m','m_l','h_m_sum','m_l_sum'],inplace=True) 
    
    # EMV: 简易波动指标
    """
    计算方法：
    1）先计算出三个因子A B C的数值。
    A = (当日最高价 + 当日最低价)÷2
    B = (上个交易日最高价 + 上个交易日最低价) ÷2
    C = 当日最高价 – 当日最低价
    2）求出EM数值
    EM = (A-B) ×C÷当日成交额
    3）求出EMV数值
    EMV = EM数值的N个交易日之和，N为时间周期，一般设为14日
    4）求出EMV的移动平均值EMVA
    EMVA = EMV的M日移动平均值，M一般设置9日    
    """
    df['a'] = (df['High']+df['Low'])/2
    df['b'] = (df['High'].shift(1)+df['Low'].shift(1))/2
    df['c'] = df['High'] - df['Low']
    
    df['Amount']=df['Close']*df['Volume']
    df['em'] = (df['a']-df['b'])*df['c']/df['Amount']
    df['emv'] = df['em'].rolling(window=EMV_days).sum()
    df['emva'] = talib.MA(df['emv'],timeperiod=EMV_madays)

    df.drop(columns = ['a','b','c'],inplace=True) 
    
    # BOLL: 布林线指标
    """
    计算公式：
        中轨线 = N日的移动平均线
        上轨线 = 中轨线 + 两倍的标准差
        下轨线 = 中轨线 – 两倍的标准差
    计算过程：
        1）先计算出移动平均值MA
        MA = N日内的收盘价之和÷N
        2）计算出标准差MD的平方
        MD的平方 = 每个交易日的（收盘价-MA）的N日累加之和的两次方 ÷ N
        3）求出MD
        MD = （MD的平方）的平方根
        4）计算MID、UPPER、LOWER的数值
        MID = (N-1)日的MA
        UPPER = MID + 2×MD
        LOWER = MID – 2×MD
        说明：N一般原始参数日缺省值为20日    
    
    指标解读：
        BOLL指标即布林线指标，其利用统计原理，求出股价的标准差及其信赖区间，
        从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。
        其上下限范围不固定，随股价的滚动而变化。布林指标股价波动在上限和下限的区间之内，
        这条带状区的宽窄，随着股价波动幅度的大小而变化，股价涨跌幅度加大时，带状区变宽，
        涨跌幅度狭小盘整时，带状区则变窄。    
    """
    df['upper'],df['mid'],df['lower'] = talib.BBANDS(df['Close'], \
                timeperiod=BULL_days, \
                nbdevup=BULL_nbdevup,nbdevdn=BULL_nbdevdn,matype=BULL_matype)                     
    
    # TRIX：三重指数平滑移动平均指标
    """
    
    """
    df['trix'] = talib.TRIX(df['Close'],timeperiod=TRIX_days)
    df['trma'] = talib.MA(df['trix'],timeperiod=TRIX_madays)    

    # DMA: 平均线差
    """
    计算公式：
    DDD(N) = N日短期平均值 – M日长期平均值
    AMA(N) = DDD的N日短期平均值
    计算过程：
    以求10日、50日为基准周期的DMA指标为例
    1）求出周期不等的两条移动平均线MA之间的差值
    DDD(10) = MA10 – MA50
    2）求DDD的10日移动平均数值
    DMA(10) = DDD(10)÷10
    """   
    df['ma_shortperiod'] = talib.MA(df['Close'],timeperiod=DMA_fastperiod)
    df['ma_longperiod'] = talib.MA(df['Close'],timeperiod=DMA_slowperiod)
    df['ddd'] = df['ma_shortperiod'] - df['ma_longperiod']
    df['dma'] = talib.MA(df['ddd'],timeperiod=DMA_madays)    
    
    df.drop(columns = ['ma_shortperiod','ma_longperiod','ddd'],inplace=True) 
    
    # BIAS: 乖离率
    """
    N日BIAS = （当日收盘价 – N日移动平均价）÷N日移动平均价×100
    
    指标解读：
    6日BIAS＞＋5％，是卖出时机；＜-5％，为买入时机。
    12日BIAS＞＋6％是卖出时机；＜-5.5％,为买入时机。
    24日BIAS＞＋9％是卖出时机；＜－8％，为买入时机。
    """
    df['ma6'] = talib.MA(df['Close'],timeperiod=BIAS_list[0])
    df['ma12'] = talib.MA(df['Close'],timeperiod=BIAS_list[1])
    df['ma24'] = talib.MA(df['Close'],timeperiod=BIAS_list[2])
    df['bias'] = ((df['Close']-df['ma6'])/df['ma6'])*100
    df['bias2'] = ((df['Close']-df['ma12'])/df['ma12'])*100
    df['bias3'] = ((df['Close']-df['ma24'])/df['ma24'])*100    
    
    df.drop(columns = ['ma6','ma12','ma24'],inplace=True) 

    # CCI: 顺势指标
    """
    计算过程：
    CCI(N日) = （TP-MA）÷MD÷0.015
    说明：TP = （最高价+最低价+收盘价）÷3；MA=最近N日收盘价的累计之和÷N；MD=最近N日（MA-收盘价）的累计之和÷N；0.015为计算系数；N为计算周期，默认为14天
    """    
    df['cci'] = talib.CCI(df['High'],df['Low'],df['Close'],timeperiod=CCI_days)

    # W%R: 威廉指标   
    """
    N日W%R = [(Hn-Ct)/(Hn-Ln)]*100
    Ct是计算日的收盘价；Hn/Ln为包括计算日当天的N周期内的最高（低）价  
    
    指标解读：
        威廉指标(William's %R) 原理：用当日收盘价在最近一段时间股价分布的相对位置来描述超买和超卖程度。
        算法：N日内最高价与当日收盘价的差，除以N日内最高价与最低价的差，结果放大100倍。
        参数：N 统计天数 一般取14天
        用法：
        1.低于20，超买，即将见顶，应及时卖出 
        2.高于80，超卖，即将见底，应伺机买进 
        3.与RSI、MTM指标配合使用，效果更好    
    """
    n = WR_list[0]
    df['h_10'] = df['High'].rolling(window=n).max()
    df['l_10'] = df['Low'].rolling(window=n).min()
    df['wr10'] = ((df['h_10']-df['Close'])/(df['h_10']-df['l_10']))*100
    
    n2 = WR_list[1]
    df['h_6'] = df['High'].rolling(window=n2).max()
    df['l_6'] = df['Low'].rolling(window=n2).min()
    df['wr6'] = ((df['h_6'] - df['Close']) / (df['h_6'] - df['l_6'])) * 100

    df.drop(columns = ['h_10','l_10','h_6','l_6'],inplace=True) 
    
    # ROC: 变动速率指标
    """
    计算过程：
    1）计算出ROC数值
    ROC = (当日收盘价 – N日前收盘价)÷N日前收盘价×100
    说明：N一般取值为12日
    2）计算ROC移动平均线（ROCMA）数值
    ROCMA = ROC的M日数值之和÷M
    说明：M一般取值为6日    
    """
    df['roc'] = talib.ROC(df['Close'],timeperiod=ROC_days)
    df['rocma'] = talib.MA(df['roc'],timeperiod=ROC_madays)    
    
    # DMI: 趋向指标
    """

    """     
    df['pdi'] = talib.PLUS_DI(df['High'],df['Low'],df['Close'],timeperiod=DMI_DIdays)
    df['mdi'] = talib.MINUS_DI(df['High'],df['Low'],df['Close'],timeperiod=DMI_DIdays)
    df['adx'] = talib.ADX(df['High'],df['Low'],df['Close'],timeperiod=DMI_ADXdays)
    df['adxr'] = talib.ADXR(df['High'],df['Low'],df['Close'],timeperiod=DMI_ADXdays)    
    
    
    return df
    