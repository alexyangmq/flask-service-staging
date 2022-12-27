import json
import logging
import boto3
import requests
def lambda_handler(event, context):   
    print(event)
    print(context)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.debug(json.dumps(event))
    codepipeline = boto3.client('codepipeline')
    s3 = boto3.client('s3')
    job_id = event['CodePipeline.job']['id']
    try:
        user_parameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        logger.info(f'User parameters: {user_parameters}')
        url = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        response = requests.get(url)
        logger.info(response)
        response = codepipeline.put_job_success_result(jobId=job_id)
        logger.debug(response)
    except Exception as error:
        logger.exception(error)
        response = codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': f'{error.__class__.__name__}: {str(error)}'
            }
        )
        logger.debug(response)

