import logging
import requests
import json
from datetime import datetime
import re
from string import Template
import os
import pandas
import csv

#logging.basicConfig(level=logging.INFO)

base_url = 'http://divulgacandcontas.tse.jus.br/divulga'

def create_functions_from_endpoints(endpoints_file=None):
    """
    From endpoints.md file, create Python functions
    with same name
    """
    if endpoints_file is None:
        here = os.path.dirname(os.path.abspath(__file__))
        endpoints_file = os.path.join(here, '..', '..', 'references', 'endpoints.md')
        endpoints_file = os.path.abspath(endpoints_file)
    with open(endpoints_file) as fl:
        file_content = fl.read()
    functions = file_content.split('*')[1:]
    expression = re.compile("`([A-Za-z0-9/:=\-\?]*)`")
    tuples = [expression.findall(x) for x in functions]
    output = {}
    expression_args = re.compile(':[A-Za-z0-9]*')
    for tup in tuples:
        function_name = tup[0]
        arguments = expression_args.findall(tup[1])
        def function(tup=tup, **kwargs):
            url = Template(tup[1].replace(':','$')).substitute(kwargs)
            req = requests.get(base_url + url)
            try:
                return req.json()
            except json.decoder.JSONDecodeError:
                logging.error('=== ERRO === Endpoint inválido: {}'.format(url))
                return None
        output[function_name] = (arguments, function)
    return output

functions = create_functions_from_endpoints()

def get_estados_municipios(folder_save=None):
    """
    Obtém lista de estados e municípios
    """
    if folder_save is None:
        here = os.path.dirname(os.path.abspath(__file__))
        folder_save = os.path.join(here, '..', '..', 'references')
        folder_save = os.path.abspath(folder_save)
    arquivo_estados = os.path.join(folder_save, 'Estados.csv')
    arquivo_municipios = os.path.join(folder_save, 'Municipios.csv')
    if os.path.exists(arquivo_estados):
        estados = pandas.read_csv(arquivo_estados)
        estados['sigla'] = estados['sigla'].apply(lambda x:str(x))
        estados = estados.to_dict('records')
    else:
        estados = functions['getResourceUfs'][1]()
        pandas.DataFrame(estados).to_csv(arquivo_estados, index=False, quoting=csv.QUOTE_NONNUMERIC)
    if os.path.exists(arquivo_municipios):
        municipios = pandas.read_csv(arquivo_municipios)
        municipios['sigla'] = municipios['sigla'].apply(lambda x:str(x).zfill(5))
        municipios = municipios.to_dict('records')
    else:
        municipios = []
        for estado in estados:
            this = functions['getResourceMunicipiosPorUf'][1](uf=estado['sigla'])
            municipios += this
        df = pandas.DataFrame(municipios)
        df['sigla'] = df['sigla'].apply(lambda x:str(x).zfill(5))
        df.to_csv(arquivo_municipios, index=False, quoting=csv.QUOTE_NONNUMERIC)
    return estados, municipios


def get_eleicoes(folder_save=None):
    """
    Obtém as eleições que ocorreram, incluindo as suplementares
    """
    if folder_save is None:
        here = os.path.dirname(os.path.abspath(__file__))
        folder_save = os.path.join(here, '..', '..', 'references')
        folder_save = os.path.abspath(folder_save)
    arquivo = os.path.join(folder_save, 'Eleicoes.csv')
    if os.path.exists(arquivo):
        return pandas.read_csv(arquivo).to_dict('records')
    else:
        anos = functions['getResourceAnosEleitorais'][1]()
        estados, _ = get_estados_municipios()
        eleicoes = []
        eleicoes += functions['getResourceEleicoesOrdinarias'][1]()
        for ano in anos:
            for ue in estados:
                this = functions['getResourceEleicoesSuplementares'][1](ano=ano,sgUe=ue['sigla'])
                eleicoes += this
        pandas.DataFrame(eleicoes).to_csv(arquivo, index=False)
        return eleicoes


def get_candidatos(folder_save=None, ano=2018):
    """
    Obtém os candidatos a eleições em um dado ano
    """
    if folder_save is None:
        here = os.path.dirname(os.path.abspath(__file__))
        folder_save = os.path.join(here, '..', '..', 'data', 'raw')
        folder_save = os.path.abspath(folder_save)
    eleicoes = get_eleicoes()
    eleicoes = [x for x in eleicoes if x['ano']==ano]
    estados, municipios = get_estados_municipios()
    estados = [x['sigla'] for x in estados]
    municipios = [x['sigla'] for x in municipios]
    logging.info('Encontrado lista de estados')
    function = functions['getResourceCandidatos'][1]
    if ano % 4 == 2:
        ue = estados + ['BR']
    elif ano % 4 == 0:
        ue = municipios
    candidatos_O = []
    candidatos_S = []

    for eleicao in eleicoes:
        regiao = eleicao['siglaUF']
        if isinstance(regiao, str):
            regiao = [regiao]
        else:
            regiao = ue
        print(regiao)
        if eleicao['tipoAbrangencia'] == 'M':
            cargos = range(11,14)
        else:
            cargos = range(1,11)
        for estado in regiao:
            for cargo in cargos:
                params = {
                    'ano':ano,
                    'sgUe':estado,
                    'eleicao':eleicao['id'],
                    'cargo':cargo,
                }
                logging.info('Executando função com parâmetros {}...'.format(params.values()))
                this = function(**params)
                logging.info('API retornou com {} resultados.'.format(len(this['candidatos'])))
                if eleicao['tipoEleicao'] == 'O':
                    candidatos_O += this['candidatos']
                elif eleicao['tipoEleicao'] == 'S':
                    candidatos_S += this['candidatos']
                else:
                    logging.warning('Tipo de eleição desconhecido: {}'.format(eleicao['id']))
                
    file_base = 'Candidatos_{:d}'.format(ano)
    file_candidatos_O = os.path.join(folder_save, file_base+'_ord.json')
    file_candidatos_S = os.path.join(folder_save, file_base+'_sup.json')
    if len(candidatos_O)>0:
        with open(file_candidatos_O, 'w') as f:
            json.dump(candidatos_O, f)
            logging.info('Arquivo salvo: {}'.format(file_candidatos_O.split('/')[-1]))
    if len(candidatos_S)>0:
        with open(file_candidatos_S, 'w') as f:
            json.dump(candidatos_S, f)
            logging.info('Arquivo salvo: {}'.format(file_candidatos_S.split('/')[-1]))

def read_candidatos(input_filepath):
    """
    Lê a lista de candidatos
    """
    with open(input_filepath) as f:
        candidatos = json.load(f)
    return candidatos

def get_bens(ano=2018):
    """
    Consulta a base de bens
    """
    here = os.path.dirname(os.path.abspath(__file__))
    file_read = os.path.join(here, '..', '..', 'data', 'raw', 'Candidatos_{}_*.json'.format(ano))
    file_read = os.path.abspath(file_read)
    input_filepath = glob.glob(file_read)
    for fl in input_filepath:
        candidatos = read_candidatos(fl)
        bens = []
        for candidato in candidatos:
            params = {
                'sqEleicao': candidato['eleicao']['id'],
                'ano': candidato['eleicao']['ano'], 
                'sgUe':
                'idCargo',
                'nrPartido',
                'nrCandidato': candidato['numero'],
                'sqCandidato':
            }


/rest/v1/prestador/consulta/:sqEleicao/:ano/:sgUe/:idCargo/:nrPartido/:nrCandidato/:sqCandidato

if __name__=='__main__':
    anos = functions['getResourceAnosEleitorais'][1]()
    for ano in anos[0:]:
        get_candidatos(ano=ano)