from app.enums.classification import ClassificationEnum
from app.enums.years import YearEnum
from app.exceptions.customException import ClassificationException, YearException
from app.models.processing import Processing
from app.resources import queue
from app.tasks.processing import scrapingProcessingTask
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from rq import Retry

class ProcessingList(Resource):
    @jwt_required()
    @swag_from('../docs/processing/list.yml', methods=["GET"])
    def get(self):
        try:
            filter = {}
            if request.args.get('cultivation'):
                filter['cultivation__icontains'] = request.args.get('cultivation')
            
            if request.args.get('year'):
                filter['year'] = request.args.get('year')

            processings = Processing.objects(**filter)
            if not processings:
                return { 'status': 404, 'message' : 'Lista de processamentos não encontrado.'}, 404
            
            return [processing.to_dict() for processing in processings]
        except:
            return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre processamento.'}, 400

class ProcessingShow(Resource):
    @jwt_required()
    @swag_from('../docs/processing/show.yml', methods=["GET"])
    def get(self, processing_id):
        try:
            processing = Processing.objects(_id=ObjectId(processing_id)).first()
            if not processing:
                return { 'status': 404, 'message' : 'Registro sobre processamento não encontrado.'}, 404
            
            return processing.to_dict() 
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de processamento correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao localizar o registro sobre processamento.'}, 400


class ProcessingCreate(Resource):
    @jwt_required()
    @swag_from('../docs/processing/create.yml', methods=["POST"])
    def post(self):
        try:
            processing = Processing(**request.get_json()).save()
            return processing.to_dict(), 201
        except:
            return { 'status': 400, 'message' : 'Erro ao cadastrar o registro sobre processamento. Verifique os dados enviado.'}, 400

                                   
class ProcessingUpdate(Resource):
    @jwt_required()
    @swag_from('../docs/processing/update.yml', methods=["PUT"])
    def put(self, processing_id):
        try:
            Processing.objects(_id=ObjectId(processing_id)).update(**request.get_json())

            processing = Processing.objects(_id=ObjectId(processing_id)).first()
            if not processing:
                return { 'status': 404, 'message' : 'Registro sobre processamento não encontrado.'}, 404
            
            return processing.to_dict()
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de processamento correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao atualizar o registro sobre processamento. Verifique os dados enviado.'}, 400

class ProcessingDelete(Resource):
    @jwt_required()
    @swag_from('../docs/processing/delete.yml', methods=["DELETE"])
    def delete(self, processing_id):
        try:
            deleted_processing = Processing.objects(_id=ObjectId(processing_id)).delete()
            if not deleted_processing:
                return { 'status': 404, 'message' : 'Registro sobre processamento não encontrado.'}, 404

            return { 'status': 200, 'message' : 'Processamento excluido com sucesso'}, 200
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de processamento correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao excluir o registro sobre processamento.'}, 400


class ProcessingScraping(Resource):
    @jwt_required()
    @swag_from('../docs/processing/scraping.yml', methods=["GET"])
    def get(self):
        try:
            classifications = ['viniferas']
            years = [2023]

            if request.args.get('classification') and request.args.get('classification') != 'all':
                classifications = [
                    classification.strip() for classification in request.args.get('classification').split(',') 
                    if classification.strip() in [classificationEnum.name for classificationEnum in ClassificationEnum]
                ]
            
            if request.args.get('year') and request.args.get('year') != 'all':
                years = [
                    int(year.strip()) for year in request.args.get('year').split(',')
                    if int(year.strip()) > YearEnum['MIN'].value and int(year.strip()) <= YearEnum['MAX'].value
                ]

            if request.args.get('classification') == 'all':
                classifications = [classificationEnum.name for classificationEnum in ClassificationEnum]

            if request.args.get('year') == 'all':
                years = [year for year in range(YearEnum['MIN'].value, YearEnum['MAX'].value + 1)]

            if not classifications:
                raise ClassificationException([productEnum.name for productEnum in ClassificationEnum])
            if not years:
                raise YearException(YearEnum['MIN'].value, YearEnum['MAX'].value)
            
            jobs = []
            for classification in classifications:
                for year in years:
                    classificationEnum = ClassificationEnum[classification].value
                    job = queue.enqueue(
                        scrapingProcessingTask,
                        args=(classificationEnum, year),
                        retry=Retry(max=3)
                    )
                    jobs.append({ 'job_id': job.id, 'job_name': 'scrapingProcessingTask', 'classification': classification, 'year': year})

            return { 'status': 200, 'message' : 'Raspagem dos registros sobre processamento agendada com sucesso.', 'jobs': jobs }, 200            
        except ClassificationException as classificationEx:
            return { 'status': 400, 'message' : str(classificationEx)}, 400
        except YearException as yearEx:
            return { 'status': 400, 'message' : str(yearEx)}, 400
        except ValueError:
            return { 'status': 400, 'message' : f'Ano inválido. Opções disponíveis: all, maior que {YearEnum['MIN'].value} ou menor que {YearEnum['MAX'].value}.'}, 400
        except:
           return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre importação.'}, 400