from enum import Enum

class ImportationProductsEnum(Enum):
    wine = { 'code': 'subopt_01', 'name': 'Vinho de mesa'}
    sparkling = { 'code': 'subopt_02', 'name': 'Espumante'}
    grape = { 'code': 'subopt_03', 'name': 'Uvas frescas'}
    raisin = { 'code': 'subopt_04', 'name': 'Uvas passas'}
    juice = { 'code': 'subopt_05', 'name': 'Suco de uva'}

class ExportationProductsEnum(Enum):
    wine = { 'code': 'subopt_01', 'name': 'Vinho de mesa'}
    sparkling = { 'code': 'subopt_02', 'name': 'Espumante'}
    grape = { 'code': 'subopt_03', 'name': 'Uvas frescas'}
    juice = { 'code': 'subopt_04', 'name': 'Suco de uva'}