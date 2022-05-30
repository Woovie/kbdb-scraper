"""
Scrapes website data and writes it to an SQS queue to be processed later into different structured
data.
"""
# pylint: disable=logging-fstring-interpolation
# see: https://github.com/PyCQA/pylint/issues/3512

import logging

import boto3
from botocore.exceptions import ClientError

sqs = boto3.resource('sqs')


class MessageWrapper:
    """
    Wrapper class for sending SQS messages
    """
    def __init__(self, logger: str = __name__, queue: dict = None):
        self.logger = logging.getLogger(logger)
        self.queue = queue

    def send_message(self, message_body, message_attributes=None):
        """
        Send a message to an Amazon SQS queue.

        :param queue: The queue that receives the message.
        :param message_body: The body text of the message.
        :param message_attributes: Custom attributes of the message. These are key-value
                                pairs that can be whatever you want.
        :return: The response from SQS that contains the assigned message ID.
        """
        if not message_attributes:
            message_attributes = {}

        try:
            response = self.queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
        except ClientError as error:
            self.logger.exception("Send message failed: %s", message_body)
            raise error
        else:
            return response

    def send_messages(self, messages):
        """
        Send a batch of messages in a single request to an SQS queue.
        This request may return overall success even when some messages were not sent.
        The caller must inspect the Successful and Failed lists in the response and
        resend any failed messages.

        :param queue: The queue to receive the messages.
        :param messages: The messages to send to the queue. These are simplified to
                        contain only the message body and attributes.
        :return: The response from SQS that contains the list of successful and failed
                messages.
        """
        try:
            entries = [{
                'Id': str(ind),
                'MessageBody': msg['body'],
                'MessageAttributes': msg['attributes']
            } for ind, msg in enumerate(messages)]
            response = self.queue.send_messages(Entries=entries)
            if 'Successful' in response:
                for msg_meta in response['Successful']:
                    self.logger.info(
                        "Message sent: %s: %s",
                        msg_meta['MessageId'],
                        messages[int(msg_meta['Id'])]['body']
                    )
            if 'Failed' in response:
                for msg_meta in response['Failed']:
                    self.logger.warning(
                        "Failed to send: %s: %s",
                        msg_meta['MessageId'],
                        messages[int(msg_meta['Id'])]['body']
                    )
        except ClientError as error:
            self.logger.exception("Send messages failed to queue: %s", self.queue)
            raise error
        else:
            return response

    def receive_messages(self, max_number, wait_time):
        """
        Receive a batch of messages in a single request from an SQS queue.

        :param queue: The queue from which to receive messages.
        :param max_number: The maximum number of messages to receive. The actual number
                        of messages received might be less.
        :param wait_time: The maximum time to wait (in seconds) before returning. When
                        this number is greater than zero, long polling is used. This
                        can result in reduced costs and fewer false empty responses.
        :return: The list of Message objects received. These each contain the body
                of the message and metadata and custom attributes.
        """
        try:
            messages = self.queue.receive_messages(
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            for msg in messages:
                self.logger.info("Received message: %s: %s", msg.message_id, msg.body)
        except ClientError as error:
            self.logger.exception("Couldn't receive messages from queue: %s", self.queue)
            raise error
        else:
            return messages


class QueueWrapper:
    """
    Wrapper class for the SQS queue
    """
    def __init__(self, logger: str = __name__):
        self.logger = logging.getLogger(logger)

    def create_queue(self, name, attributes=None):
        """
        Creates an Amazon SQS queue.

        :param name: The name of the queue. This is part of the URL assigned to the queue.
        :param attributes: The attributes of the queue, such as maximum message size or
                        whether it's a FIFO queue.
        :return: A Queue object that contains metadata about the queue and that can be used
                to perform queue operations like sending and receiving messages.
        """
        if not attributes:
            attributes = {}

        try:
            queue = sqs.create_queue(
                QueueName=name,
                Attributes=attributes
            )
            self.logger.info("Created queue '%s' with URL=%s", name, queue.url)
        except ClientError as error:
            self.logger.exception("Couldn't create queue named '%s'.", name)
            raise error
        else:
            return queue

    def get_queue(self, name):
        """
        Gets an SQS queue by name.

        :param name: The name that was used to create the queue.
        :return: A Queue object.
        """
        try:
            queue = sqs.get_queue_by_name(QueueName=name)
            self.logger.info("Got queue '%s' with URL=%s", name, queue.url)
        except ClientError as error:
            self.logger.exception("Couldn't get queue named %s.", name)
            raise error
        else:
            return queue
