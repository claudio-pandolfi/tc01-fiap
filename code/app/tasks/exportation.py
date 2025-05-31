
from bs4 import BeautifulSoup
import requests as httpRequest
from urllib.parse import urlencode as URLEncode
from app.models.exportation import Exportation

def scrapingExportationTask(product, year):
    filter = { 'opcao': 'opt_06', 'subopcao': product['code'], 'ano': year }
    exportations = []

    scrapingPage = BeautifulSoup(httpRequest.get(f"http://vitibrasil.cnpuv.embrapa.br/index.php?{URLEncode(filter)}").text, 'html.parser')

    scrapingData = scrapingPage.find('table', class_="tb_dados").tbody.find_all('tr')
    
    if not scrapingData:
        return { 'status': 404, 'message' : 'Não foi possível localizar os dados para a raspagem.'}, 404

    for singleData in scrapingData:
        exportation = Exportation.objects(
            country=singleData.find_all('td')[0].text.strip(),
            product=product['name'],
            year=filter['ano']

        ).first()

        if not exportation:
            exportation = Exportation(
                country=singleData.find_all('td')[0].text.strip(),
                product=product['name'],
                year=filter['ano'],
                quantity=singleData.find_all('td')[1].text.strip().replace('.','').replace('-','0'),
                amount=singleData.find_all('td')[2].text.strip().replace('.','').replace('-','0')
            ).save()
            exportations.append(exportation.to_dict())

    print(exportations)
    return exportations
