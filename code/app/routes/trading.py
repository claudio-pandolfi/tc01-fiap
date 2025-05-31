from app.resources.trading import TradingList, TradingCreate, TradingShow, TradingUpdate, TradingDelete, TradingScraping

def trading_routes(api):
    api.add_resource(TradingList, '/trading')
    api.add_resource(TradingCreate, '/trading')
    api.add_resource(TradingShow, '/trading/<string:trading_id>')
    api.add_resource(TradingUpdate, '/trading/<string:trading_id>')
    api.add_resource(TradingDelete, '/trading/<string:trading_id>')
    api.add_resource(TradingScraping, '/trading/scraping')

