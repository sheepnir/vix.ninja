import yfinance as yf
import logging

logger = logging.getLogger(__name__)

class YahooService:
    @staticmethod
    def get_vix_index():
        """Get current VIX index value from Yahoo Finance"""
        try:
            vix_ticker = yf.Ticker("^VIX")
            vix_data = vix_ticker.history(period="1d")
            
            if not vix_data.empty:
                current_value = vix_data['Close'].iloc[-1]
                return {
                    'value': current_value,
                    'timestamp': vix_data.index[-1].to_pydatetime()
                }
            else:
                logger.error("No VIX data returned from Yahoo Finance")
                return None
        except Exception as e:
            logger.error(f"Error fetching VIX data from Yahoo Finance: {e}")
            return None