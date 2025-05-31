from enum import Enum

class ClassificationEnum(Enum):
    viniferas = { 'code': 'subopt_01', 'name': 'Viníferas'}
    american = { 'code': 'subopt_02', 'name': 'Americanas e híbridas'}
    table_grape = { 'code': 'subopt_03', 'name': 'Uvas de mesa'}
    unrated = { 'code': 'subopt_04', 'name': 'Sem classificação'}