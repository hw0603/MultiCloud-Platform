from src.shared.security import deps
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from src.users.infrastructure import repositories
from config.api_config import settings


app = FastAPI()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


@app.get("/")
def get_userinfo_from_db(db: Session = Depends(deps.get_db)):
    user = repositories.get_user_by_username(db, "admin")
    return object_as_dict(user)


@app.get("/info")
def get_instance_state():
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION = 'ap-northeast-2'

    import boto3
    import datetime
    from operator import itemgetter

    now = datetime.datetime.utcnow()  # Now time in UTC format
    past = now - datetime.timedelta(minutes=60)  # Minus 60 minutes

    # Amazon Cloud Watch connection
    client_cw = boto3.client(
        'cloudwatch',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    # Amazon EC2 connection
    client_ec2 = boto3.client(
        'ec2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    response = client_ec2.describe_instances()  # Get all instances from Amazon EC2

    for reservation in response["Reservations"]:
        print(reservation)
        for instance in reservation["Instances"]:

            # This will print output the value of the Dictionary key 'InstanceId'
            print(instance["InstanceId"])

            if (instance["State"]["Name"] == "running"):
                print("Instance is running")
            else:
                print("Instance is not running")
                continue

            # Get CPU Utilization for each InstanceID
            CPUUtilization = client_cw.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId',
                             'Value': instance["InstanceId"]}],
                StartTime=past,
                EndTime=now,
                Period=60,
                Statistics=['Average']
            )

            # CPU Utilization results
            datapoints = CPUUtilization['Datapoints']
            print(*datapoints, sep='\n')
            last_datapoint = sorted(datapoints, key=itemgetter(
                'Timestamp'))[-1]    # Last result
            # Last utilization
            utilization = last_datapoint['Average']
            # Last utilization in %
            load = round(utilization, 3)
            # Last utilization timestamp
            timestamp = str(last_datapoint['Timestamp'])
            print(f"CPU사용량: {load}% - {timestamp}")

    # client = boto3.client('ec2', region_name='ap-northeast-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # client = boto3.client('cloudwatch', region_name='ap-northeast-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # response = client.get_metric_statistics(
    #     Namespace='AWS/EC2',
    #     MetricName='CPUUtilization',
    #     Dimensions=[
    #         {
    #             'Name': 'InstanceId',
    #             'Value': 'i-038e85971e2fceb8b'
    #         },
    #     ],
    #     StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
    #     EndTime=datetime.datetime.utcnow(),
    #     Period=60,
    #     Statistics=[
    #         'Average',
    #     ],
    #     Unit='Percent'
    # )
    """    
    StatusCheckFailed_System
    CPUUtilization
    StatusCheckFailed_Instance
    EBSWriteBytes
    EBSReadOps
    EBSReadBytes
    NetworkPacketsIn
    NetworkIn
    EBSByteBalance%
    NetworkOut
    MetadataNoToken
    EBSIOBalance%
    NetworkPacketsOut
    StatusCheckFailed
    EBSWriteOps
    """

    # try:
    #     response = client.describe_instances()
    #     return response
    # except botocore.exceptions.ClientError as e:
    #     print(e.response['Error']['Message'])
    return f"CPU사용량: {load}% - {timestamp}"
