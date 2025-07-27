import boto3
import logging
from os import environ as environment

log = logging.getLogger("payment." + __name__)


class SNSService:

    def __init__(self):
        try:
            env = environment.get('ENVIRONMENT', 'development')
            region = environment.get('AWS_REGION', 'us-east-1')

            if env == 'production':
                self.client = boto3.client('sns', region_name=region)
            else:
                self.client = boto3.client(
                    'sns',
                    region_name=region,
                    aws_access_key_id=environment.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=environment.get('AWS_SECRET_ACCESS_KEY')
                )

            log.info("SNS client created successfully.")
        except Exception as e:
            log.exception(f"Error creating SNS Client: {e}")
            raise

    def get_or_create_topic(self, topic_name):
        try:
            # return "arn:aws:sns:us-east-1:829401394278:payment-approved"
            response = self.client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            log.info(f"SNS Topic '{topic_name}' created/retrieved with ARN: {topic_arn}")
            return topic_arn
        except Exception as e:
            log.exception(f"Error creating/retrieving SNS topic '{topic_name}': {e}")
            raise

    def publish_notification(self, topic_arn, message, subject):
        try:
            response = self.client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject
            )
            message_id = response['MessageId']
            log.info(f"Message published on SNS topic. Message ID: {message_id}")
            return message_id
        except Exception as e:
            log.exception(f"Error publishing message on topic {topic_arn}: {e}")
            raise

    def send_notification(self, topic_name, message, subject):
        try:
            log.info(f"Initiating notification sender to topic '{topic_name}'.")
            topic_arn = self.get_or_create_topic(topic_name)
            msg_id = self.publish_notification(topic_arn, message, subject)
            log.info(f"Notification send with success. Message ID: {msg_id}")
            return msg_id
        except Exception as e:
            log.exception(f"Error while sending notification to topic '{topic_name}': {e}")
            raise
