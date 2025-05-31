from app.enums.years import YearEnum
from app.exceptions.customException import YearException
from app.models.trading import Trading
from app.resources import queue
from app.tasks.trading import scrapingTradingTask
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from flask import request
from flask_restful import Resource
from rq import Retry

class TradingList(Resource):
    @jwt_required()
    @swag_from('../docs/trading/list.yml', methods=["GET"])
    def get(self):
        try:
            filter = {}
            if request.args.get('product'):
                filter['product__icontains'] = request.args.get('product')
            
            if request.args.get('year'):
                filter['year'] = request.args.get('year')

            tradings = Trading.objects(**filter)
            if not tradings:
                return { 'status': 404, 'message' : 'Lista de comercializações não encontrada'}, 404
            
            return [trading.to_dict() for trading in tradings]
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para buscar os documentos.'}, 400

class TradingShow(Resource):
    @jwt_required()
    @swag_from('../docs/trading/show.yml', methods=["GET"])
    def get(self, trading_id):
        try:
            trading = Trading.objects(_id=ObjectId(trading_id)).first()
            if not trading:
                return { 'status': 404, 'message' : 'Dados da comercialização não encontrado'}, 404
            
            return trading.to_dict() 
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de comercialização correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para obter o documento.'}, 400


class TradingCreate(Resource):
    @jwt_required()
    @swag_from('../docs/trading/create.yml', methods=["POST"])
    def post(self):
        try:
            trading = Trading(**request.get_json()).save()
            return trading.to_dict(), 201
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para cadastrar o documento. Verifique os dados enviado.'}, 400

                                   
class TradingUpdate(Resource):
    @jwt_required()
    @swag_from('../docs/trading/update.yml', methods=["PUT"])
    def put(self, trading_id):
        try:
            Trading.objects(_id=ObjectId(trading_id)).update(**request.get_json())

            trading = Trading.objects(_id=ObjectId(trading_id)).first()
            if not trading:
                return { 'status': 404, 'message' : 'Dados da comercialização não encontrado'}, 404
            
            return trading.to_dict()
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de comercialização correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para atualizar o documento. Verifique os dados enviado.'}, 400

class TradingDelete(Resource):
    @jwt_required()
    @swag_from('../docs/trading/delete.yml', methods=["DELETE"])
    def delete(self, trading_id):
        try:
            deleted_trading = Trading.objects(_id=ObjectId(trading_id)).delete()
            if not deleted_trading:
                return { 'status': 404, 'message' : 'Dados da comercialização não encontrado'}, 404

            return { 'status': 200, 'message' : 'Comercialização excluida com sucesso'}, 200
        except InvalidId:
            return { 'status': 400, 'message' : 'Informe o código de comercialização correto.'}, 400
        except:
            return { 'status': 400, 'message' : 'Ocorreu um problema para excluir o documento.'}, 400

class TradingScraping(Resource):
    @jwt_required()
    @swag_from('../docs/trading/scraping.yml', methods=["GET"])
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
                    scrapingTradingTask,
                    year,
                    retry=Retry(max=3)
                )
                jobs.append({ 'job_id': job.id, 'job_name': 'scrapingTradingTask', 'year': year})
            
            return { 'status': 200, 'message' : 'Raspagem dos registros sobre comercialização agendada com sucesso', 'jobs': jobs }, 200            
        except YearException as yearEx:
            return { 'status': 400, 'message' : str(yearEx)}, 400
        except ValueError:
            return { 'status': 400, 'message' : f'Ano inválido. Opções disponíveis: all, maior que {YearEnum['MIN'].value} ou menor que {YearEnum['MAX'].value}.'}, 400
        except:
           return { 'status': 400, 'message' : 'Erro ao buscar os registros sobre importação.'}, 400
