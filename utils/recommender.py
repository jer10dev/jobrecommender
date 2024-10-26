import pandas as pd
import os
import math
import logging

logger = logging.getLogger(__name__)

def recommendation_engine(file_path, file_list, jobs, job_list):
    logger.info("Recommendation Engine is starting")
    
    if not file_list:
        logger.info("No data found for recommendation")
        return
    
    for file in file_list:
        file_content = pd.read_csv(os.path.join(file_path, file))
        df = pd.DataFrame(file_content)
        
    data = []
    
    for index, row in df.iterrows():
        skills = row.loc['skills'].split(", ")
        recommended_job_list = []
        [recommended_job_list.extend(jobs.get(skill)) for skill in skills]
        for l in list(set(recommended_job_list)):
            data.append({
                'jobseeker_id': row.loc['id'], 
                'jobseeker_name':  row.loc['name'], 
                'job_id':  job_list[l]['id'],
                'job_title': l,
                'matching_skill_count':  len(list(set(job_list[l]['skills']) & set(row.loc['skills'].split(", ")))),
                'matching_skill_percent': math.floor((len(list(set(job_list[l]['skills']) & set(row.loc['skills'].split(", ")))) * 100) / len(job_list[l]['skills']))
            })

    df = pd.DataFrame(data)   
    df = df.sort_values(by=['jobseeker_id', 'matching_skill_percent', 'job_id'], ascending=[True, False, True]) 
    df = df.set_index('jobseeker_id')
    logging.info("The Final output is..")
    # Newline character for better reading
    print("\n", df, "\n")
    logging.info("Execution of Engine done..")
    return df
