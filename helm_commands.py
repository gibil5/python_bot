import functools
import asyncio
import subprocess
import pykube
import logging
import uuid
logging.basicConfig(level=logging.DEBUG)

NAMESPACE = "robotdemosuccess"
def retry(retry_count=50, delay=5, allowed_exceptions=(KeyError)):
    def decorator(f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            result = None
            last_exception = None
            for _ in range(retry_count):
                try:
                    result = f(*args, **kwargs)
                    if result: 
                        return result
                except allowed_exceptions as e:
                    last_exception = e
                logging.debug(f"Waiting for {delay} seconds before retrying again")
                await asyncio.sleep(delay)

            if last_exception is not None:
                raise type(last_exception) from last_exception
            return result

        return wrapper
    return decorator


@retry()
def GetJob(RUN_ID):
    config = pykube.KubeConfig.from_env()
    api = pykube.HTTPClient(config)
    
    
    job = pykube.Job.objects(api).filter(
                namespace=NAMESPACE,
                selector={"app.kubernetes.io/id": RUN_ID}
            ).get()
    
    status = job.labels["app.kubernetes.io/status"]
    if status is None:
        raise ValueError()
    logging.debug(status)
    return True

    

# RUN_ID = str(uuid.uuid4())

# logging.debug(f"TEST ID: {RUN_ID}")

# REPO_ADD = "helm repo add --insecure-skip-tls-verify --username=admin --password=Harbor12345 testscripts https://harbor.intergies.com/chartrepo/testscripts"
# REPO_LIST = "helm repo list"
# RUN_TEST = f'helm install --insecure-skip-tls-verify --generate-name --namespace=robotdemosuccess --set-string EXTERNAL_RUN_ID={RUN_ID} --set-string SLACK_CHANNEL="taf-bot" --set-string ROBOT_OPTIONS="--expandkeywords TAG:run-all -i run-all" testscripts/demosuccess'

def RunCommand(command):
    logging.debug(f"Starting RunCommand")
    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    if result.stderr.decode('utf-8') != '':
        output = result.stdout.decode('utf-8')
        #error = result.stderr.decode('utf-8')
    logging.debug(output)
    #logging.debug(error)


# if __name__ == '__main__':
#     RunCommand(REPO_ADD)
#     RunCommand(REPO_LIST)
#     RunCommand('helm repo update')
#     RunCommand('helm search repo')
#     RunCommand(RUN_TEST)

    
#     asyncio.run(GetJob(RUN_ID))

#Preparing for execution (pod/contaire are being created)
#Test in Progress (pod has been created, but no FAIL/PASS label yet)
