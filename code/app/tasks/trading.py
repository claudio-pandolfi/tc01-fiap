
from bs4 import BeautifulSoup
import requests as httpRequest
from urllib.parse import urlencode as URLEncode
from app.models.trading import Trading

def scrapingTradingTask(year):
    filter = { 'opcao': 'opt_04', 'ano': year }
    tradings = []

    scrapingPage = BeautifulSoup(httpRequest.get(f"http://vitibrasil.cnpuv.embrapa.br/index.php?{URLEncode(filter)}").text, 'html.parser')

    scrapingData = scrapingPage.find('table', class_="tb_dados").tbody.find_all('tr')
    
    if not scrapingData:
        return { 'status': 404, 'message' : 'Não foi possível localizar os dados para a raspagem.'}, 404

    productName = ''
    lastRecord = None
    for singleData in scrapingData:
        singleRecord = singleData.find_all('td')
        if 'tb_item' in singleRecord[0]['class']:
            productName = singleRecord[0].text.strip()
            if lastRecord != None and 'tb_item' in lastRecord[0]['class']:
                trading = Trading.objects(
                    product=lastRecord[0].text.strip(),
                    type='Sem classificação',
                    year=filter['ano']
                ).first()

                if not trading:
                    trading = Trading(
                        product=lastRecord[0].text.strip(),
                        type='Sem classificação',
                        year=filter['ano'],
                        amount=lastRecord[1].text.strip().replace('.','').replace('-','0')
                    ).save()
                    tradings.append(trading.to_dict())

        if 'tb_subitem' in singleRecord[0]['class']:
            trading = Trading.objects(
                product=productName,
                type=singleData.find_all('td')[0].text.strip(),
                year=filter['ano']
            ).first()

            if not trading:
                trading = Trading(
                    product=productName,
                    type=singleRecord[0].text.strip(),
                    year=filter['ano'],
                    amount=singleRecord[1].text.strip().replace('.','').replace('-','0')
                ).save()
                tradings.append(trading.to_dict())
        
        lastRecord = singleRecord

    print(tradings)
    return tradings
