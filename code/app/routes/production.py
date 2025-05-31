from app.resources.production import ProductionList, ProductionShow, ProductionCreate, ProductionUpdate, ProductionDelete, ProductionScraping

def production_routes(api):
    api.add_resource(ProductionList, '/production')
    api.add_resource(ProductionCreate, '/production')
    api.add_resource(ProductionScraping, '/production/scraping')
    api.add_resource(ProductionShow, '/production/<string:production_id>')
    api.add_resource(ProductionUpdate, '/production/<string:production_id>')
    api.add_resource(ProductionDelete, '/production/<string:production_id>')