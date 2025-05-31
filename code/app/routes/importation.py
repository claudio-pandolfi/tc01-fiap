from app.resources.importation import ImportationList, ImportationCreate, ImportationShow, ImportationUpdate, ImportationDelete, ImportationScraping

def importation_routes(api):
    api.add_resource(ImportationList, '/importation')
    api.add_resource(ImportationCreate, '/importation')
    api.add_resource(ImportationShow, '/importation/<string:importation_id>')
    api.add_resource(ImportationUpdate, '/importation/<string:importation_id>')
    api.add_resource(ImportationDelete, '/importation/<string:importation_id>')
    api.add_resource(ImportationScraping, '/importation/scraping')