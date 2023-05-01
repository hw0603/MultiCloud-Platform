import boto3
import datetime


def get_instance_state(id: str, secret: str, region: str, instanceId: str, metrics: list):
    now = datetime.datetime.utcnow()  # 현재 시각 (UTC 포맷)
    past = now - datetime.timedelta(minutes=60)  # 60분의 timedelta

    # AWS Cloudwatch 연결 설정
    client_cw = boto3.client(
        'cloudwatch',
        aws_access_key_id=id,
        aws_secret_access_key=secret,
        region_name=region
    )

    result = {}
    for metric in metrics:
        # instanceId에 대해 metrics를 설정하여 60분간의 평균값을 가져옴
        stats = client_cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric,
            Dimensions=[{'Name': 'InstanceId', 'Value': instanceId}],
            StartTime=past,
            EndTime=now,
            Period=60,
            Statistics=['Average']
        )

        # 통계치 조회 결과
        datapoints = stats['Datapoints']

        # last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]    # Last result

        # # Last utilization
        # utilization = last_datapoint['Average']

        # # Last utilization timestamp
        # timestamp = str(last_datapoint['Timestamp'])

        result.update({metric: datapoints})

    return result


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
            if (instance["State"]["Name"] == "running"):
                instance_list.append(instance["InstanceId"])

    return instance_list

