import os
import pandas as pd
from utils import recommender as rec_engine
import logging

# Changed the max read of the dataframe rows
pd.options.display.max_rows = 9999

# Initializing logger
logger = logging.getLogger(__name__)

jobs = {}
job_list = {}

def render_job_file_data(df):
    for index, row in df.iterrows():
        job_list[row.loc['title']] = {
            'skills': row.loc['required_skills'].split(", "),
            'id':  row.loc['id']
        }
        skills = row.loc['required_skills'].split(", ")
        for skill in skills:
            if not jobs.get(skill):
                jobs[skill] = [row.loc['title']]
            if row.loc['title'] not in jobs.get(skill):
                jobs.get(skill).extend([row.loc['title']])

def read_file_path(foldername):
    logger.info(f"Preparing {foldername} folder path")
    dir = os.path.join(os.path.abspath('.'), f'{foldername}/')
    return (dir, os.listdir(dir))

def read_csv_files(file_path, file):
    logger.info(f"Reading {file} file")
    file_content = pd.read_csv(os.path.join(file_path, file))
    df = pd.DataFrame(file_content)
    return df

def process_csv_files():
    # Read the jobs csv file inside jobs folder
    dir, job_csv_files = read_file_path('jobs')
    if not job_csv_files:
        logger.info("No CSV Files in Jobs folder found")
        return
    
    # Read the Jobs file contents and render it
    for file in job_csv_files:
        df_csv_content = read_csv_files(dir, file)
        render_job_file_data(df_csv_content)

    # Read the job seekers csv file inside job_seekers folder
    dir, job_seeker_csv_files = read_file_path('job_seekers')
    if not job_seeker_csv_files:
        logger.info("No CSV Files in job_seekers folder found")
        return
    
    response = rec_engine.recommendation_engine(dir, job_seeker_csv_files, jobs, job_list)
    return response
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info('Started')
    response = process_csv_files()
    if response is not None:
        logger.info('Finished')

    