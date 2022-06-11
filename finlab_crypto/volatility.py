import math
import numpy as np

#---------------------------------------------------------------------------------------------------------------------------#
#format dataframe labels ['open,'high','low','close']
# Markdown formulas of Parkinson
'''
The **Parkinson** volatility:
$$PHV = \sqrt{\frac{1}{4Nln_{ret}2}\sum_{i=1}^N(ln_{ret}\frac{x_t^{(h)}}{x_t^{(l)}})^2}$$
where $h_i$ denotes the daily high price, 
$l_i$ is the daily low price, 
'''
#where is x_t^{(h)} is high price time series and x_t^{(l)} is the low price time series
#format dataframe labels ['open,'high','low','close']
#e.g., to use:
# from finlab_cryptoAITA.finlab_crypto import volatility
# TICKER = 'WAVESBUSD'
#TIMEFRAME = '1m'
#ohlcv = finlab_crypto.crawler.get_ncandles_binance(TICKER, TIMEFRAME, 60*6)
#p_vol = volatility.get_histovol_parkinson(ohlcv, N=60, trading_period=ohlcv.shape[0])
#line_vol = volatility.plot_phv(gk_vol)
#line_vol.show()

def get_histovol_parkinson(df, N=30, trading_period=252, clean=True):

    rs = (1.0 / (4.0 * math.log(2.0))) * ((df['high'] / df['low']).apply(np.log))**2.0

    def f(v):
        return (trading_periods * v.mean())**0.5
    
    result = rs.rolling(
        window=window,
        center=False
    ).apply(func=f)
    
    if clean:
        return result.dropna()
    else:
        return result
#---------------------------------------------------------------------------------------------------------------------------#
      
#format dataframe labels ['open,'high','low','close']
# Markdown formulas of GKHV
'''
The **Garman & Klass** volatility:
$$GK=\sqrt{\frac{1}{N}\sum_{i=1}^N \frac{1}{2}(ln\frac{h_i}{l_i})^2-\frac{1}{N}\sum_{i=1}^N(2ln2-1)(ln\frac{c_i}{o_i})^2}$$
where $h_i$ denotes the daily high price, 
$l_i$ is the daily low price, 
$c_i$ is the daily closing price and $o_i$ is the daily opening price.
'''

#format dataframe labels ['open,'high','low','close']
#e.g., to use:
# from finlabCryptoAITA.finlab_crypto import volatility
# TICKER = 'WAVESBUSD'
#TIMEFRAME = '1m'
#ohlcv = finlab_crypto.crawler.get_ncandles_binance(TICKER, TIMEFRAME, 60*6)
#gk_vol = volatility.get_histovol_gk(ohlcv, N=60, trading_period=ohlcv.shape[0])
#line_vol = volatility.plot_gkhv(gk_vol)
#line_vol.show()

def get_histovol_gk(df, N=30, trading_period=252, dropnan=True):

    log_hl = (df['high'] / df['low']).apply(np.log)
    log_co = (df['close'] / df['open']).apply(np.log)

    rs = 0.5 * log_hl**2 - (2*math.log(2)-1) * log_co**2
    
    def vol_mean(vol):
        return (trading_period * vol.mean())**0.5
    
    sigmaGK = rs.rolling(window=N, center=False).apply(func=vol_mean)
    
    if dropnan:
        return sigmaGK.dropna()
    else:
        return sigmaGK
#---------------------------------------------------------------------------------------------------------------------------#

# Markdown formulas of YZHV
'''
The **Yang & Zhang** volatility:
$$\sigma_{OpentoCloseVol}^2 = \frac{1}{N-1}\sum_{i=1}^N(ln\frac{c_i}{o_i} - ln\frac{c_i}{o_i})^2$$

$$\sigma_{OvernightVol}^2 = \frac{1}{N-1}\sum_{i=1}^N(ln\frac{o_i}{c_{i-1}} - ln\frac{o_i}{c_{i-1}})^2$$

$$\sigma_{YZ} = \sqrt{\sigma_{OvernightVol}^2 +k\sigma_{OpentoCloseVol}^2+(1-k)\sigma^2_{RS}}$$

where $k = \frac{0.34}{1.34+\frac{N+1}{N-1}}$
'''

#format dataframe labels ['open,'high','low','close']
#e.g., to use:
# from finlab_cryptoAITA.finlab_crypto import volatility
# TICKER = 'WAVESBUSD'
#TIMEFRAME = '1m'
#ohlcv = finlab_crypto.crawler.get_ncandles_binance(TICKER, TIMEFRAME, 60*6)
#yz_vol = volatility.get_histovol_yz(ohlcv, N=60, trading_period=ohlcv.shape[0])
#line_vol = volatility.plot_yzhv(yz_vol)
#line_vol.show()

def get_histovol_yz(df, N=30, trading_period=252, dropnan=True):
    """Calcualte Yang and Zhang history volatility.
    Args:
        df: the pandas dataframe with columns ['open','high','low'.'close'] labels.
    Return: pandas series with YZ volatility values.
    """

    k = 0.34 / (1.34 + (N + 1) / (N - 1))
    
    log_oc = (df['open'] / df['close'].shift(1)).apply(np.log)
    log_oc_sq = log_oc**2

    log_cc = (df['close'] / df['close'].shift(1)).apply(np.log)
    log_cc_sq = log_cc**2
    
    log_ho = (df['high'] / df['open']).apply(np.log)
    log_lo = (df['low'] / df['open']).apply(np.log)
    log_co = (df['close'] / df['open']).apply(np.log)
    
    close_vol = log_cc_sq.rolling(window=N, center=False).sum() * (1.0 / (N - 1.0))
    open_vol = log_oc_sq.rolling(window=N, center=False).sum() * (1.0 / (N - 1.0))

    rs = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)
    win_rs = rs.rolling(window=N, center=False).sum() * (1.0 / (N - 1.0))

    sigmaYZ = (open_vol + k * close_vol + (1 - k) * win_rs).apply(np.sqrt) * math.sqrt(trading_period)

    if dropnan:
        return sigmaYZ.dropna()
    else:
        return sigmaYZ
        
#-----------------------------------------------------------------------------------#
#-----------------------      PLOT functions        --------------------------------#

import plotly.express as px
import plotly.graph_objects as go

#-----------------------------------------------------#
#          GUI History Volatility Estimators          #
#-----------------------------------------------------#
# plotly.graph_objects
def plot_hv(series):
  """plot scatter line of GK history volatility.

    Args:
        series: a pandas series from get_histovol_yz.
    
    Return: a Figure plotly class to render with fig.show()
    """
  colors = px.colors.qualitative.Plotly
  fig = go.Figure()
  fig.add_traces(go.Scatter(x=series.index, y = series, mode = 'lines', line=dict(color=colors[0])))
  
  return fig
  
#-------------------------------------------------------------------------------#
