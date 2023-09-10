import time
import json
import logging
from botocore.exceptions import ClientError

import boto3
from joulescope import scan_require_one

# AWS Kinesis
kinesis_stream_name = 'kinesis-stream-name'
kinesis_client = boto3.client('kinesis')

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def put_data_to_kinesis(data, partition_key):
    try:
        response = kinesis_client.put_record(
        StreamName=kinesis_stream_name,
        Data=json.dumps(data),
        PartitionKey=partition_key
    )
        logger.info("Put record in stream %s.", kinesis_stream_name)
    except ClientError as e:
        logger.exception("Couldn't put record in stream %s.", kinesis_stream_name, e)
        raise

def main():
    try:
        with scan_require_one(config='auto') as jl_device:
            serial_number = jl_device.serial_number

            jl_device.start()

            try:
                while True:
                    data = jl_device.read()
                    if data is not None:
                        # Converting data to JSON format
                        json_data = {
                            "serial_number": serial_number,
                            "current": data['signals']['current'],
                            "voltage": data['accumulators']['voltage'],
                            "power": data['accumulators']['power']
                        }
                        # Sending data to AWS Kinesis
                        put_data_to_kinesis(json_data, '1')
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass
            finally:
                jl_device.stop()

    except Exception as e:
        logger.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()
