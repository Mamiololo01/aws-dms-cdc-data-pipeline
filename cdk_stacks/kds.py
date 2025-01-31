#!/usr/bin/env python3
import random
import string

import aws_cdk as cdk

from aws_cdk import (
  Duration,
  Stack,
  aws_kinesis,
)
from constructs import Construct

random.seed(37)

class KinesisDataStreamStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    KINESIS_DEFAULT_STREAM_NAME = 'PUT-{}'.format(''.join(random.sample((string.ascii_letters), k=5)))
    kinesis_stream_name = self.node.try_get_context('kinesis_stream_name') or KINESIS_DEFAULT_STREAM_NAME

    kinesis_stream = aws_kinesis.Stream(self, 'DMSTargetKinesisStream',
      retention_period=Duration.hours(24),
      stream_mode=aws_kinesis.StreamMode.ON_DEMAND,
      stream_name=kinesis_stream_name
    )

    self.kinesis_stream_name = kinesis_stream.stream_name
    self.kinesis_stream_arn = kinesis_stream.stream_arn

    cdk.CfnOutput(self, 'DMSTargetKinesisStreamName', value=self.kinesis_stream_name,
      export_name='DMSTargetKinesisStreamName')
    cdk.CfnOutput(self, 'DMSTargetKinesisStreamArn', value=self.kinesis_stream_arn,
      export_name='DMSTargetKinesisStreamArn')

