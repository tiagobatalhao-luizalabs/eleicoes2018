import logging
import requests
import json

log = logging.getLogger(__name__)

def make_url_2018_busca(estado, id_):
    """
    Cria o endpoint da URL para buscar 
    informações de um candidato
    """
    url_base = 'http://divulgacandcontas.tse.jus.br/divulga/rest/v1/'
    url_base+= 'candidatura/buscar/{year}/{state}/{election}/candidato/{id_}'
    params = {
        'year': '2018',
        'state': str(estado),
        'election': '2022802018',
        'id_': str(id_)
    }
    return url_base.format(**params)


def get_info_candidato(estado, id_ ):
    """
    Retorna um JSON com informação sobre
    um candidato
    """
    url = make_url_2018_busca(estado, id_)
    req = requests.get(url)
    try:
        info = req.json()
        log.info('Encontrado: estado {}, id {}'.format(estado, id_))
        return info
    except json.decoder.JSONDecodeError:
        log.error('Não encontrado: estado {}, id {}'.format(estado, id_))
        return None


def get_lista_candidatos(filename=None):
    """
    Retorna uma lista de candidatos e ids
    """
    candidates = []
    if filename is None:
        filename = '../../data/external/ListaCandidatos.csv'
    with open(filename) as fl:
        for line in fl.readlines():
            candidates.append(line.split(','))
    return candidates


def main(input_filepath, output_filepath):
    """
    Gera todos os json de candidatos e salva 
    na pasta raw
    """
    candidates = get_lista_candidatos(input_filepath)
    info = []
    try:
        for candidate in candidates:
            this = get_info_candidato(*candidate)
            if this and len(this)>0:
                info.append(this)
    except KeyboardInterrupt:
        pass
    with open(output_filepath, 'w') as fl:
        json.dump(info, fl)
