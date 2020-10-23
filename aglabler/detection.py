import boto3
import json
from typing import Dict, Any


MIN_CONFIDENCE: float = 0.9
MAX_LABELS: int = 1000
OUTPUT_STREAM = 'detection'
ERROR_STREAM = 'errors'


def partition(record: Dict[str, Any]) -> str:
    return record['kinesisRecordMetadata']['partitionKey']


def sequence_number(record) -> str:
    return record['kinesisRecordMetadata']['sequenceNumber']


def s3_file(record: Dict[str, Any]) -> str:
    device_id = partition(record)
    image_id = record['recordId']
    timestamp = record['approximateArrivalTimestamp']
    return f'{device_id}/{image_id}-{timestamp}'


def handler(event, context):
    rekog = boto3.client('rekognition')
    kinesis = boto3.client('kinessis')
    for record in event['records']:
        stream = OUTPUT_STREAM
        partition_key = partition(record)
        sequence = sequence_number(record)
        file = s3_file(record)
        payload = {
            's3': file
        }
        try:
            detection = rekog.detect_labels(
                {'Bytes': record['data']},
                MaxLabels=MAX_LABELS,
                MinConfidence=MIN_CONFIDENCE)
            payload['detection'] = detection
        except Exception as e:
            stream = ERROR_STREAM
            payload['error'] = 'recognition failed'

        kinesis.put_record(
            StreamName=stream,
            Data=json.dumps(payload),
            PartitionKey=partition_key,
            SequenceNumberForOrdering=sequence
        )

