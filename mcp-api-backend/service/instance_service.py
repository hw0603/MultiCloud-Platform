import boto3
import datetime
from operator import itemgetter
from config.api_config import settings


def get_instance_state():
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION = 'ap-northeast-2'

    now = datetime.datetime.utcnow()  # 현재 시각 (UTC 포맷)
    past = now - datetime.timedelta(minutes=60)  # 60분의 timedelta

    # AWS Cloudwatch 연결 설정
    client_cw = boto3.client(
        'cloudwatch',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    # AWS EC2 연결 설정
    client_ec2 = boto3.client(
        'ec2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    response = client_ec2.describe_instances()  # Amazon EC2의 모든 인스턴스 정보를 가져옴

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

            # 각 InstanceID에 대해 CPU 사용률을 가져옴
            CPUUtilization = client_cw.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance["InstanceId"]}],
                StartTime=past,
                EndTime=now,
                Period=60,
                Statistics=['Average']
            )

            # CPU Utilization 결과
            datapoints = CPUUtilization['Datapoints']
            print(*datapoints, sep='\n')
            last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]    # Last result
            # Last utilization
            utilization = last_datapoint['Average']
            # Last utilization in %
            load = round(utilization, 3)
            # Last utilization timestamp
            timestamp = str(last_datapoint['Timestamp'])
            print(f"CPU사용량: {load}% - {timestamp}")

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

    return f"CPU사용량: {load}% - {timestamp}"


def get_instance_list(id, secret, region):
    # AWS EC2 연결 설정
    client_ec2 = boto3.client(
        'ec2',
        aws_access_key_id=id,
        aws_secret_access_key=secret,
        region_name=region
    )

    response = client_ec2.describe_instances()  # Amazon EC2의 모든 인스턴스 정보를 가져옴

    instance_list = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_list.append(instance["InstanceId"])

    return instance_list

