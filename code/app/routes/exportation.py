from app.resources.exportation import ExportationList, ExportationCreate, ExportationShow, ExportationUpdate, ExportationDelete, ExportationScraping

def exportation_routes(api):
    api.add_resource(ExportationList, '/exportation')
    api.add_resource(ExportationCreate, '/exportation')
    api.add_resource(ExportationShow, '/exportation/<string:exportation_id>')
    api.add_resource(ExportationUpdate, '/exportation/<string:exportation_id>')
    api.add_resource(ExportationDelete, '/exportation/<string:exportation_id>')
    api.add_resource(ExportationScraping, '/exportation/scraping')