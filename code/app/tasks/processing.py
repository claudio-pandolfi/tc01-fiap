
from bs4 import BeautifulSoup
import requests as httpRequest
from urllib.parse import urlencode as URLEncode
from app.models.processing import Processing

def scrapingProcessingTask(classification, year):
    filter = { 'opcao': 'opt_03', 'subopcao': classification['code'], 'ano': year }
    processings = []

    scrapingPage = BeautifulSoup(httpRequest.get(f"http://vitibrasil.cnpuv.embrapa.br/index.php?{URLEncode(filter)}").text, 'html.parser')

    scrapingData = scrapingPage.find('table', class_="tb_dados").tbody.find_all('tr')
    
    if not scrapingData:
        return { 'status': 404, 'message' : 'Não foi possível localizar os dados para a raspagem.'}, 404

    productName = ''
    for singleData in scrapingData:
        singleRecord = singleData.find_all('td')
        if 'tb_item' in singleRecord[0]['class']:
            productName = singleRecord[0].text.strip()

        if 'tb_subitem' in singleRecord[0]['class']:
            processing = Processing.objects(
                product=productName,
                cultivation=singleRecord[0].text.strip(),
                classification=classification['name'],
                year=filter['ano']
            ).first()

            if not processing:
                processing = Processing(
                    product=productName,
                    cultivation=singleRecord[0].text.strip(),
                    classification=classification['name'],
                    year=filter['ano'],
                    quantity=singleRecord[1].text.strip().replace('.','').replace('-','0').replace('nd','0').replace('*','0')
                ).save()
                processings.append(processing.to_dict())

    print(processings)
    return processings
