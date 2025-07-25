from unittest.mock import patch, MagicMock
from engine.tests.unit import PaymentUnitTest
from engine.app.services.amazon_sns.snsService import SNSService


class TestSNSService(PaymentUnitTest):

    @patch("engine.app.services.amazon_sns.snsService.boto3.client")
    @patch("engine.app.services.amazon_sns.snsService.environment", {
        'ENVIRONMENT': 'development',
        'AWS_ACCESS_KEY_ID': 'fake_key',
        'AWS_SECRET_ACCESS_KEY': 'fake_secret',
        'AWS_REGION': 'us-east-1'
    })
    def test_init_success_development(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client

        service = SNSService()
        self.assertEqual(service.client, mock_client)
        mock_boto_client.assert_called_once_with(
            'sns',
            region_name='us-east-1',
            aws_access_key_id='fake_key',
            aws_secret_access_key='fake_secret'
        )

    @patch("engine.app.services.amazon_sns.snsService.boto3.client")
    @patch("engine.app.services.amazon_sns.snsService.environment", {
        'ENVIRONMENT': 'production',
        'AWS_REGION': 'us-east-1'
    })
    def test_init_success_production(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client

        service = SNSService()
        self.assertEqual(service.client, mock_client)
        mock_boto_client.assert_called_once_with('sns', region_name='us-east-1')

    @patch("engine.app.services.amazon_sns.snsService.boto3.client", side_effect=Exception("Connection failed"))
    @patch("engine.app.services.amazon_sns.snsService.environment", {})
    def test_init_failure_raises_exception(self, mock_boto_client):
        with self.assertRaises(Exception) as context:
            SNSService()

        self.assertIn("Connection failed", str(context.exception))

    @patch.object(SNSService, '__init__', lambda x: None)
    def test_get_or_create_topic_success(self):
        service = SNSService()
        service.client = MagicMock()
        service.client.create_topic.return_value = {'TopicArn': 'arn:aws:sns:123:test-topic'}

        topic_arn = service.get_or_create_topic('test-topic')

        self.assertEqual(topic_arn, 'arn:aws:sns:123:test-topic')
        service.client.create_topic.assert_called_once_with(Name='test-topic')

    @patch.object(SNSService, '__init__', lambda x: None)
    def test_get_or_create_topic_failure(self):
        service = SNSService()
        service.client = MagicMock()
        service.client.create_topic.side_effect = Exception("Create topic error")

        with self.assertRaises(Exception) as context:
            service.get_or_create_topic('test-topic')

        self.assertIn("Create topic error", str(context.exception))

    @patch.object(SNSService, '__init__', lambda x: None)
    def test_publish_notification_success(self):
        service = SNSService()
        service.client = MagicMock()
        service.client.publish.return_value = {'MessageId': '123456'}

        msg_id = service.publish_notification('arn:aws:sns:123:test-topic', 'hello', 'greeting')

        self.assertEqual(msg_id, '123456')
        service.client.publish.assert_called_once_with(
            TopicArn='arn:aws:sns:123:test-topic',
            Message='hello',
            Subject='greeting'
        )

    @patch.object(SNSService, '__init__', lambda x: None)
    def test_publish_notification_failure(self):
        service = SNSService()
        service.client = MagicMock()
        service.client.publish.side_effect = Exception("Publish failed")

        with self.assertRaises(Exception) as context:
            service.publish_notification('arn:aws:sns:123:test-topic', 'hello', 'greeting')

        self.assertIn("Publish failed", str(context.exception))

    @patch.object(SNSService, "get_or_create_topic", return_value="arn:aws:sns:123:test-topic")
    @patch.object(SNSService, "publish_notification", return_value="msg-123")
    @patch.object(SNSService, '__init__', lambda x: None)
    def test_send_notification_success(self, mock_publish, mock_get_topic):
        service = SNSService()

        result = service.send_notification("topic-name", "message body", "subject")

        self.assertEqual(result, "msg-123")
        mock_get_topic.assert_called_once_with("topic-name")
        mock_publish.assert_called_once_with("arn:aws:sns:123:test-topic", "message body", "subject")

    @patch.object(SNSService, "get_or_create_topic", side_effect=Exception("Fail in get_or_create_topic"))
    @patch.object(SNSService, '__init__', lambda x: None)
    def test_send_notification_failure_on_get_topic(self, mock_get_topic):
        service = SNSService()

        with self.assertRaises(Exception) as context:
            service.send_notification("topic-name", "message body", "subject")

        self.assertIn("Fail in get_or_create_topic", str(context.exception))

    @patch.object(SNSService, "get_or_create_topic", return_value="arn:aws:sns:123:test-topic")
    @patch.object(SNSService, "publish_notification", side_effect=Exception("Fail in publish"))
    @patch.object(SNSService, '__init__', lambda x: None)
    def test_send_notification_failure_on_publish(self, mock_publish, mock_get_topic):
        service = SNSService()

        with self.assertRaises(Exception) as context:
            service.send_notification("topic-name", "message body", "subject")

        self.assertIn("Fail in publish", str(context.exception))
