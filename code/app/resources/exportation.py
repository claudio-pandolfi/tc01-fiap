from app.enums.products import ExportationProductsEnum
from app.enums.years import YearEnum
from app.exceptions.customException import ProductTypeException, YearException
from app.models.exportation import Exportation
from app.resources import queue
from app.tasks.exportation import scrapingExportationTask
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from rq import Retry

class ExportationList(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/list.yml', methods=["GET"])
    def get(self):
        try:
            filter = {}
            if request.args.get('country'):
                filter['country__icontains'] = request.args.get('country')

            if request.args.get('product'):
                filter['product__icontains'] = request.args.get('product')
            
            if request.args.get('year'):
                filter['year'] = request.args.get('year')

            exportations = Exportation.objects(**filter)
            if not exportations:
                return { 'status': 404, 'message' : 'Lista de exportações não encontrado.'}, 404
            
            return [exportation.to_dict() for exportation in exportations]
        except:
            return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre exportação.'}, 400

class ExportationShow(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/show.yml', methods=["GET"])
    def get(self, exportation_id):
        try:
            exportation = Exportation.objects(_id=ObjectId(exportation_id)).first()
            if not exportation:
                return { 'status': 404, 'message' : 'Registro sobre exportação não encontrado.'}, 404
            
            return exportation.to_dict() 
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de exportação correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao localizar o registro sobre exportação.'}, 400


class ExportationCreate(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/create.yml', methods=["POST"])
    def post(self):
        try:
            exportation = Exportation(**request.get_json()).save()
            return exportation.to_dict(), 201
        except:
            return { 'status': 400, 'message' : 'Erro ao cadastrar o registro sobre exportação. Verifique os dados enviado.'}, 400

                                   
class ExportationUpdate(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/update.yml', methods=["PUT"])
    def put(self, exportation_id):
        try:
            Exportation.objects(_id=ObjectId(exportation_id)).update(**request.get_json())

            exportation = Exportation.objects(_id=ObjectId(exportation_id)).first()
            if not exportation:
                return { 'status': 404, 'message' : 'Registro sobre exportação não encontrado.'}, 404
            
            return exportation.to_dict()
        except InvalidId:
            return { 'status': 400, 'message' : 'Registro sobre exportação não encontrado.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao atualizar o registro sobre exportação. Verifique os dados enviado.'}, 400

class ExportationDelete(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/delete.yml', methods=["DELETE"])
    def delete(self, exportation_id):
        try:
            deleted_exportation = Exportation.objects(_id=ObjectId(exportation_id)).delete()
            if not deleted_exportation:
                return { 'status': 404, 'message' : 'Registro sobre exportação não encontrado'}, 404

            return { 'status': 200, 'message' : 'Registro de exportação excluido com sucesso'}, 200
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de exportação correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Erro ao excluir o registro sobre exportação.'}, 400

class ExportationScraping(Resource):
    @jwt_required()
    @swag_from('../docs/exportation/scraping.yml', methods=["GET"])
    def get(self):
        try:
            products = ['wine']
            years = [2023]

            if request.args.get('product') and request.args.get('product') != 'all':
                products = [
                    product.strip() for product in request.args.get('product').split(',') 
                    if product.strip() in [productEnum.name for productEnum in ExportationProductsEnum]
                ]
            
            if request.args.get('year') and request.args.get('year') != 'all':
                years = [
                    int(year.strip()) for year in request.args.get('year').split(',')
                    if int(year.strip()) > YearEnum['MIN'].value and int(year.strip()) <= YearEnum['EXPORTATION_MAX'].value
                ]

            if request.args.get('product') == 'all':
                products = [productEnum.name for productEnum in ExportationProductsEnum]

            if request.args.get('year') == 'all':
                years = [year for year in range(YearEnum['MIN'].value, YearEnum['EXPORTATION_MAX'].value + 1)]

            if not products:
                raise ProductTypeException([productEnum.name for productEnum in ExportationProductsEnum])
            if not years:
                raise YearException(YearEnum['MIN'].value, YearEnum['EXPORTATION_MAX'].value)
            
            jobs = []
            for product in products:
                for year in years:
                    productEnum = ExportationProductsEnum[product].value
                    job = queue.enqueue(
                        scrapingExportationTask,
                        args=(productEnum, year),
                        retry=Retry(max=3)
                    )
                    jobs.append({ 'job_id': job.id, 'job_name': 'scrapingExportationTask', 'product': product, 'year': year})
            
            return { 'status': 200, 'message' : 'Agendamento sobre exportação realizado com sucesso', 'jobs': jobs }, 200            
        except ProductTypeException as productTypeEx:
            return { 'status': 400, 'message' : str(productTypeEx)}, 400
        except YearException as yearEx:
            return { 'status': 400, 'message' : str(yearEx)}, 400
        except ValueError:
            return { 'status': 400, 'message' : f'Ano inválido. Opções disponíveis: all, maior que {YearEnum['MIN'].value} ou menor que {YearEnum['EXPORTATION_MAX'].value}.'}, 400
        except:
           return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre exportação.'}, 400