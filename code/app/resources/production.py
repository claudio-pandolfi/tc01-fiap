from app.enums.years import YearEnum
from app.exceptions.customException import YearException
from app.models.production import Production
from app.resources import queue
from app.tasks.production import scrapingProductionTask
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request, jsonify
from flasgger import swag_from
from rq import Retry

class ProductionList(Resource):
    @jwt_required()
    @swag_from('../docs/production/list.yml', methods=["GET"])
    def get(self):
        try:
            filter = {}
            if request.args.get('product'):
                filter['product__icontains'] = request.args.get('product')
            
            if request.args.get('year'):
                filter['year'] = request.args.get('year')

            productions = Production.objects(**filter)
            if not productions:
                return jsonify({ 'status': 404, 'message' : 'Lista de produções não encontrada'}), 404
            
            return [production.to_dict() for production in productions]
        except:
            return jsonify({ 'status': 400, 'message' : 'Ocorreu um problema para buscar os documentos.'}), 400

class ProductionShow(Resource):
    @jwt_required()
    @swag_from('../docs/production/show.yml', methods=["GET"])
    def get(self, production_id):
        try:
            production = Production.objects(_id=ObjectId(production_id)).first()
            if not production:
                return { 'status': 404, 'message' : 'Dados da produção não encontrado'}, 404
            
            return production.to_dict() 
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de produção correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para obter o documento.'}, 400


class ProductionCreate(Resource):
    @jwt_required()
    @swag_from('../docs/production/create.yml', methods=["POST"])
    def post(self):
        try:
            production = Production(**request.get_json()).save()
            return production.to_dict(), 201
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para cadastrar o documento. Verifique os dados enviado.'}, 400

                                   
class ProductionUpdate(Resource):
    @jwt_required()
    @swag_from('../docs/production/update.yml', methods=["PUT"])
    def put(self, production_id):
        try:
            Production.objects(_id=ObjectId(production_id)).update(**request.get_json())

            production = Production.objects(_id=ObjectId(production_id)).first()
            if not production:
                return { 'status': 404, 'message' : 'Dados da produção não encontrado'}, 404
            
            return production.to_dict()
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de produção correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para atualizar o documento. Verifique os dados enviado.'}, 400

class ProductionDelete(Resource):
    @jwt_required()
    @swag_from('../docs/production/delete.yml', methods=["DELETE"])
    def delete(self, production_id):
        try:
            deleted_production = Production.objects(_id=ObjectId(production_id)).delete()
            if not deleted_production:
                return { 'status': 404, 'message' : 'Dados da produção não encontrado'}, 404

            return { 'status': 200, 'message' : 'Produção excluida com sucesso'}, 200
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de produção correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para excluir o documento.'}, 400

class ProductionScraping(Resource):
    @jwt_required()
    @swag_from('../docs/production/scraping.yml', methods=["GET"])
    def get(self):
        try:
            years = [2023]

            if request.args.get('year') and request.args.get('year') != 'all':
                years = [
                    int(year.strip()) for year in request.args.get('year').split(',')
                    if int(year.strip()) > YearEnum['MIN'].value and int(year.strip()) <= YearEnum['MAX'].value
                ]

            if request.args.get('year') == 'all':
                years = [year for year in range(YearEnum['MIN'].value, YearEnum['MAX'].value + 1)]

            if not years:
                raise YearException(YearEnum['MIN'].value, YearEnum['MAX'].value)
            
            jobs = []
            for year in years:
                job = queue.enqueue(
                    scrapingProductionTask,
                    year,
                    retry=Retry(max=3)
                )
                jobs.append({ 'job_id': job.id, 'job_name': 'scrapingProductionTask', 'year': year})
            
            return { 'status': 200, 'message' : 'Raspagem dos registros sobre produção agendada com sucesso.', 'jobs': jobs }, 200            
        except YearException as yearEx:
            return { 'status': 400, 'message' : str(yearEx)}, 400
        except ValueError:
            return { 'status': 400, 'message' : f'Ano inválido. Opções disponíveis: all, maior que {YearEnum['MIN'].value} ou menor que {YearEnum['MAX'].value}.'}, 400
        except:
           return { 'status': 400, 'message' : 'Erro ao agendar a raspagem sobre produção.'}, 400