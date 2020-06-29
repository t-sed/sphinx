#!/usr/bin/env python
# encoding: utf-8

import os
import json
import boto3
import random
import logging
import datetime

SLACK_POST_URL = os.environ['SLACK_POST_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
CONTESTS=[{"name":"agc","range_oldest":1,"range_latest":46},{"name":"abc","range_oldest":1,"range_latest":171}]
PROBLEM_URL_TEMPLATE = 'https://atcoder.jp/contests/{}/tasks'

TOPIC_ARN = os.environ['TOPIC_ARN']
SUBJECT = os.environ['SUBJECT']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_content():
    text = "今週の問題はこちら！！！\n"+create_contest_url()
    COLOR = "good"
    atachements = {"text":text,"color":COLOR}
    return atachements

def create_contest_url():
    contest_type = random.choice(CONTESTS)
    number = str(random.randint(contest_type["range_oldest"],contest_type["range_latest"])).zfill(3)
    return PROBLEM_URL_TEMPLATE.format(contest_type["name"]+number)

def lambda_handler(event, context):

    # SlackにPOSTする内容をセット
    slack_message = {
        'url' : SLACK_POST_URL,
        'message': {
        'channel': SLACK_CHANNEL,
        "attachments": [get_content()]
        }
    }
    logger.info(slack_message)
        # SNSに投げる処理を実装する
    client = boto3.client('sns')
    request = {
            'TopicArn': TOPIC_ARN,
            'Message': json.dumps(slack_message),
            'Subject': SUBJECT
        }
    response = client.publish(**request)
    logger.info(response)