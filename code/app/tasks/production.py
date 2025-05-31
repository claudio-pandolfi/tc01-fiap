
from bs4 import BeautifulSoup
import requests as httpRequest
from urllib.parse import urlencode as URLEncode
from app.models.production import Production

def scrapingProductionTask(year):
    filter = { 'opcao': 'opt_02', 'ano': year }
    productions = []

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
            production = Production.objects(
                product=productName,
                type=singleData.find_all('td')[0].text.strip(),
                year=filter['ano']
            ).first()

            if not production:
                production = Production(
                    product=productName,
                    type=singleRecord[0].text.strip(),
                    year=filter['ano'],
                    quantity=singleRecord[1].text.strip().replace('.','').replace('-','0')
                ).save()
                productions.append(production.to_dict())

    print(productions)
    return productions
