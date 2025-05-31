from app.enums.products import ImportationProductsEnum
from app.enums.years import YearEnum
from app.exceptions.customException import ProductTypeException, YearException
from app.models.importation import Importation
from app.resources import queue
from app.tasks.importation import scrapingImportationTask
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from rq import Retry

class ImportationList(Resource):
    @jwt_required()
    @swag_from('../docs/importation/list.yml', methods=["GET"])
    def get(self):
        try:
            filter = {}
            if request.args.get('country'):
                filter['country__icontains'] = request.args.get('country')

            if request.args.get('product'):
                filter['product__icontains'] = request.args.get('product')
            
            if request.args.get('year'):
                filter['year'] = request.args.get('year')

            importations = Importation.objects(**filter)
            if not importations:
                return { 'status': 404, 'message' : 'Lista de comercializações não encontrada'}, 404
            
            return [importation.to_dict() for importation in importations]
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para buscar os documentos.'}, 400

class ImportationShow(Resource):
    @jwt_required()
    @swag_from('../docs/importation/show.yml', methods=["GET"])
    def get(self, importation_id):
        try:
            importation = Importation.objects(_id=ObjectId(importation_id)).first()
            if not importation:
                return { 'status': 404, 'message' : 'Dados da importação não encontrado'}, 404
            
            return importation.to_dict() 
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de importação correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para obter o documento.'}, 400


class ImportationCreate(Resource):
    @jwt_required()
    @swag_from('../docs/importation/create.yml', methods=["POST"])
    def post(self):
        try:
            importation = Importation(**request.get_json()).save()
            return importation.to_dict(), 201
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para cadastrar o documento. Verifique os dados enviado.'}, 400

                                   
class ImportationUpdate(Resource):
    @jwt_required()
    @swag_from('../docs/importation/update.yml', methods=["PUT"])
    def put(self, importation_id):
        try:
            Importation.objects(_id=ObjectId(importation_id)).update(**request.get_json())

            importation = Importation.objects(_id=ObjectId(importation_id)).first()
            if not importation:
                return { 'status': 404, 'message' : 'Dados da importação não encontrado'}, 404
            
            return importation.to_dict()
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de importação correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para atualizar o documento. Verifique os dados enviado.'}, 400

class ImportationDelete(Resource):
    @jwt_required()
    @swag_from('../docs/importation/delete.yml', methods=["DELETE"])
    def delete(self, importation_id):
        try:
            deleted_importation = Importation.objects(_id=ObjectId(importation_id)).delete()
            if not deleted_importation:
                return { 'status': 404, 'message' : 'Dados da importação não encontrado'}, 404

            return { 'status': 200, 'message' : 'Importação excluida com sucesso'}, 200
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de importação correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para excluir o documento.'}, 400

class ImportationScraping(Resource):
    @jwt_required()
    @swag_from('../docs/importation/scraping.yml', methods=["GET"])
    def get(self):
        try:
            products = ['wine']
            years = [2023]

            if request.args.get('product') and request.args.get('product') != 'all':
                products = [
                    product.strip() for product in request.args.get('product').split(',') 
                    if product.strip() in [productEnum.name for productEnum in ImportationProductsEnum]
                ]
            
            if request.args.get('year') and request.args.get('year') != 'all':
                years = [
                    int(year.strip()) for year in request.args.get('year').split(',')
                    if int(year.strip()) > YearEnum['MIN'].value and int(year.strip()) <= YearEnum['IMPORTATION_MAX'].value
                ]

            if request.args.get('product') == 'all':
                products = [productEnum.name for productEnum in ImportationProductsEnum]

            if request.args.get('year') == 'all':
                years = [year for year in range(YearEnum['MIN'].value, YearEnum['IMPORTATION_MAX'].value + 1)]

            if not products:
                raise ProductTypeException([productEnum.name for productEnum in ImportationProductsEnum])
            if not years:
                raise YearException(YearEnum['MIN'].value, YearEnum['IMPORTATION_MAX'].value)
            
            jobs = []
            for product in products:
                for year in years:
                    productEnum = ImportationProductsEnum[product].value
                    job = queue.enqueue(
                        scrapingImportationTask,
                        args=(productEnum, year),
                        retry=Retry(max=3)
                    )
                    jobs.append({ 'job_id': job.id, 'job_name': 'scrapingImportationTask', 'product': product, 'year': year})
            
            return { 'status': 200, 'message' : 'Agendamento sobre importação realizado com sucesso', 'jobs': jobs }, 200            
        except ProductTypeException as productTypeEx:
            return { 'status': 400, 'message' : str(productTypeEx)}, 400
        except YearException as yearEx:
            return { 'status': 400, 'message' : str(yearEx)}, 400
        except ValueError:
            return { 'status': 400, 'message' : f'Ano inválido. Opções disponíveis: all, maior que {YearEnum['MIN'].value} ou menor que {YearEnum['IMPORTATION_MAX'].value}.'}, 400
        except:
           return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre importação.'}, 400