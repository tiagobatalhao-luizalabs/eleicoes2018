# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
import json
import glob

# import get_infos

@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # get_infos.get_estados_municipios()
    # get_infos.get_eleicoes()
    # get_infos.main(ano=2018)

    profiles = []
    expenses = []
    folder = os.path.dirname(os.path.abspath(__file__))
    folder_data = os.path.abspath(os.path.join(folder, '..', '..', 'data'))
    for fl in glob.glob(os.path.join(folder_data, 'external/s3bucket/prof*')):
        with open(fl, 'r') as f:
            profiles.append(json.load(f))
    with open(os.path.join(folder_data, 'raw/S3_2018_profiles.json'), 'w') as f:
        json.dump(profiles, f)
    for fl in glob.glob(os.path.join(folder_data, 'external/s3bucket/expens*')):
        with open(fl, 'r') as f:
            expenses.append(json.load(f))
    with open(os.path.join(folder_data, 'raw/S3_2018_expenses.json'), 'w') as f:
        json.dump(expenses, f)
        


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
