'''Formula:
+DM = current high – previous high;
–DM = previous low – current low;

+DI = shows increasing values in case of bull markets, i.e. it rises when prices rise
-DI = shows increasing values in case of bear markets, i.e. it rises when prices fall

ADX = {[(+DI)-(-DI)]/[(+DI)+(-DI)]}*100
'''
@Strategy(timeperiod=5)
def adx_strategy(ohlcv_pred):
  tp = adx_strategy.timeperiod

  DIminus = talib.MINUS_DI(ohlcv_pred['high'], ohlcv_pred['low'], ohlcv_pred['close'],timeperiod=tp)
  DIplus = talib.PLUS_DI(ohlcv_pred['high'], ohlcv_pred['low'], ohlcv_pred['close'],timeperiod=tp)
  
  adx = talib.ADX(ohlcv_pred['high'], ohlcv_pred['low'], ohlcv_pred['close'],timeperiod=tp)
  
  exits = (DIminus > DIplus) & (adx > 25)   #SHORT pos.  -DI > +DI & adx > 25  
  entries = (DIplus > DIminus) & (adx > 25) #LONG pos.  +DI > -DI & adx > 25
  
  figure = {
      'overlaps': {
          str(tp) + 'adx': adx,
          str(tp) + 'minus': DIminus,
          str(tp) + 'plus': DIplus,
        }
    }
  return entries, exits, #figure
