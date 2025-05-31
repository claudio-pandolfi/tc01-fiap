from app.resources.processing import ProcessingList, ProcessingShow, ProcessingCreate, ProcessingUpdate, ProcessingDelete, ProcessingScraping

def processing_routes(api):
    api.add_resource(ProcessingList, '/processing')
    api.add_resource(ProcessingCreate, '/processing')
    api.add_resource(ProcessingShow, '/processing/<string:processing_id>')
    api.add_resource(ProcessingUpdate, '/processing/<string:processing_id>')
    api.add_resource(ProcessingDelete, '/processing/<string:processing_id>')
    api.add_resource(ProcessingScraping, '/processing/scraping')