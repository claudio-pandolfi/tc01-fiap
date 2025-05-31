
from app.enums.years import YearEnum

class YearException(Exception):
    def __init__(self, yearMin, yearMax):
        super().__init__(f'Ano inválido. Opções disponíveis: all, maior que {yearMin} ou menor que {yearMax}.')

class ProductTypeException(Exception):
    def __init__(self, productType):
        super().__init__(f'Produto inválido. Opções disponíveis: all, {", ".join(map(str, productType))}.' )

class ClassificationException(Exception):
    def __init__(self, classification):
        super().__init__(f'Classificação inválida. Opções disponíveis: all, {", ".join(map(str, classification))}.' )