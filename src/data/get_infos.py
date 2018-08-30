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

def get_lista_candidatos(folder_save=None, ano=2018):
    """
    Obtém os candidatos a eleições em um dado ano
    """
    if folder_save is None:
        here = os.path.dirname(os.path.abspath(__file__))
        folder_save = os.path.join(here, '..', '..', 'data', 'raw')
        folder_save = os.path.abspath(folder_save)
    file_base = 'Lista_{:d}'.format(ano)
    file_candidatos_O = os.path.join(folder_save, file_base+'_ord.json')
    file_candidatos_S = os.path.join(folder_save, file_base+'_sup.json')
    if not os.path.exists(file_candidatos_O):
        make_lista_candidatos(folder_save, ano)
    try:
        with open(file_candidatos_O) as f:
            candidatos_O = json.load(f)
    except IOError:
        candidatos_O = []
    try:
        with open(file_candidatos_S) as f:
            candidatos_S = json.load(f)
    except IOError:
        candidatos_S = []
    return candidatos_O, candidatos_S


def make_lista_candidatos(folder_save, ano=2018):
    """
    Cria os candidatos a eleições em um dado ano
    """
    file_base = 'Lista_{:d}'.format(ano)
    file_candidatos_O = os.path.join(folder_save, file_base+'_ord.json')
    file_candidatos_S = os.path.join(folder_save, file_base+'_sup.json')

    eleicoes = get_eleicoes()
    eleicoes = [x for x in eleicoes if x['ano']==ano]
    estados, municipios = get_estados_municipios()
    estados = [x['sigla'] for x in estados]
    municipios = [x['sigla'] for x in municipios]
    logging.info('Encontrado lista de estados e municípios.')
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
                for cand in this['candidatos']:
                    cand_dict = {
                        'ano': ano,
                        'sgUe': estado,
                        'eleicao': cand['eleicao']['id'],
                        'cargo': cand['cargo']['codigo'],
                        'id': cand['id'],
                        'partido': cand['partido']['numero'],
                        'numero': cand['numero'],
                    }
                    if eleicao['tipoEleicao'] == 'O':
                        candidatos_O.append(cand_dict)
                    elif eleicao['tipoEleicao'] == 'S':
                        candidatos_S.append(cand_dict)
                    else:
                        logging.warning('Tipo de eleição desconhecido: {}'.format(eleicao['id']))
                
    with open(file_candidatos_O, 'w') as f:
        json.dump(candidatos_O, f)
        logging.info('Arquivo salvo: {}'.format(file_candidatos_O.split('/')[-1]))
    with open(file_candidatos_S, 'w') as f:
        json.dump(candidatos_S, f)
        logging.info('Arquivo salvo: {}'.format(file_candidatos_S.split('/')[-1]))


def get_candidato_info(candidato):
    """
    Retorna informação sobre um candidato
    """
    params = {
        'ano': candidato['ano'],
        'sgUe': candidato['sgUe'],
        'eleicao': candidato['eleicao'],
        'idCandidato': candidato['id'],
    }
    function = functions['getResourceCandidato'][1]
    this = function(**params)
    if len(this):
        logging.info('Informação pessoal obtida sobre candidato {}'.format(candidato['id']))
        return this

def get_candidato_financeiro(candidato):
    """
    Retorna informação financeira sobre um candidato
    """
    params = {
        'sqEleicao': candidato['eleicao'],
        'ano': candidato['ano'],
        'sgUe': candidato['sgUe'],
        'idCargo': candidato['cargo'],
        'nrPartido': str(candidato['numero'])[:2],
        'nrCandidato': candidato['numero'],
        'sqCandidato': candidato['id'],
    }
    function = functions['getResourcePrestador'][1]
    this = function(**params)
    if len(this):
        logging.info('Informação financeira obtida sobre candidato {}'.format(candidato['id']))
        return this

def main(folder_save=None, ano=2018):
    if folder_save is None:
        here = os.path.dirname(os.path.abspath(__file__))
        folder_save = os.path.join(here, '..', '..', 'data', 'raw')
        folder_save = os.path.abspath(folder_save)
    file_base_cand = os.path.join(folder_save, 'Candidatos_{:d}'.format(ano))
    file_base_fin = os.path.join(folder_save, 'Financeiro_{:d}'.format(ano))
    candidatos = get_lista_candidatos(ano=ano)
    for ls, label in zip(candidatos, ['_ord','_sup']):
        ls_cand, ls_fin = [],[]
        try:
            for cand in ls:
                ls_cand.append(get_candidato_info(cand))
                ls_fin.append(get_candidato_financeiro(cand))
        except KeyboardInterrupt:
            pass
        with open(file_base_cand + label + '.json', 'w') as f:
            json.dump(ls_cand, f)
        with open(file_base_fin + label + '.json', 'w') as f:
            json.dump(ls_fin, f)
        




if __name__=='__main__':
    anos = functions['getResourceAnosEleitorais'][1]()
    for ano in anos[0:]:
        # get_lista_candidatos(ano=ano)
        main(ano=ano)