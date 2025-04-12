from ib_insync import IB, Future
import datetime
import logging

logger = logging.getLogger(__name__)

class IBService:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()
        
    def connect(self):
        """Connect to IB Gateway"""
        try:
            if not self.ib.isConnected():
                self.ib.connect(self.host, self.port, clientId=self.client_id)
                logger.info(f"Connected to IB Gateway on {self.host}:{self.port}")
                return True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IB Gateway"""
        if self.ib.isConnected():
            self.ib.disconnect()
            logger.info("Disconnected from IB Gateway")
    
    def get_vix_futures(self):
        """Get VIX futures data"""
        if not self.ib.isConnected():
            self.connect()
        
        futures_data = []
        
        # Get current month and year
        now = datetime.datetime.now()
        
        # Loop through the next 9 months to get all VIX futures
        for i in range(9):
            future_date = now + datetime.timedelta(days=30 * i)
            future_symbol = f"VX{future_date.strftime('%Y%m')}"
            
            contract = Future('VIX', future_date.strftime('%Y%m'), 'CFE')
            
            try:
                self.ib.qualifyContracts(contract)
                ticker = self.ib.reqMktData(contract)
                self.ib.sleep(1)  # Give time for data to arrive
                
                if ticker.lastGreeks:
                    futures_data.append({
                        'contract': future_symbol,
                        'price': ticker.last if ticker.last > 0 else ticker.close,
                        'bid': ticker.bid,
                        'ask': ticker.ask,
                        'volume': ticker.volume,
                        'open_interest': ticker.openInterest
                    })
            except Exception as e:
                logger.error(f"Error fetching data for {future_symbol}: {e}")
        
        return futures_data