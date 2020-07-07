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
PROBLEM_URL_TEMPLATE = 'https://atcoder.jp/contests/{contest_id}/tasks'

TOPIC_ARN = os.environ['TOPIC_ARN']
SUBJECT = os.environ['SUBJECT']

## lambdaの場合、外部パッケージのインストールが面倒だったため、一旦dictデータを作成。
PROBLEM_CATEGORIES = {
        "dp (dynamic programming / 動的計画法)":["abc040_c" ,"abc044_c" ,"abc054_d" ,"abc087_c" ,"abc099_c" ,"abc103_d" ,"abc129_c" ,"abc135_d" ,"abc141_e" ,"abc142_e" ,"abc145_e" ,"abc153_e" ,"abc154_e"],
        "累積和 (prefix sum)":["abc037_c" ,"abc038_c" ,"abc077_c" ,"abc084_d" ,"abc087_c" ,"abc089_d" ,"abc095_d" ,"abc098_c" ,"abc106_d" ,"abc122_c" ,"abc124_d" ,"abc125_c" ,"abc129_d" ,"abc134_c" ,"abc149_e" ,"abc154_d" ,"abc162_d" ,"abc172_c" ],
        "imos 法 (imos method)":["abc014_c" ,"abc017_c" ,"abc035_c" ,"abc072_c" ,"abc080_d" ,"abc127_c" ,"abc141_c"],
        "しゃくとり法 (two pointer)":["abc032_c" ,"abc098_d" ,"abc130_d" ,"abc172_c"],
        "sliding window":["abc037_c" ,"abc124_d" ,"abc154_d"],
        "union-find forest / disjoint-set data structure":["abc040_d" ,"abc049_d" ,"abc075_c" ,"abc087_d" ,"abc097_d" ,"abc120_d" ,"abc126_e" ,"abc157_d"],
        "dfs (深さ優先探索)":["abc049_d" ,"abc070_d" ,"abc087_d" ,"abc126_d" ,"abc138_d" ,"abc146_d" ,"abc148_f"],
        "bfs (幅優先探索)":["abc007_c" ,"abc049_d" ,"abc070_d" ,"abc088_d" ,"abc126_d" ,"abc138_d" ,"abc151_d" ,"abc168_d"],
        "ダイクストラ法 (dijkstra's algorithm)":["abc070_d"],
        "二分探索 (binary search)":["abc030_c" ,"abc077_c" ,"abc113_c" ,"abc119_d" ,"abc134_e" ,"abc143_d" ,"abc144_e" ,"abc146_c" ,"abc149_e" ,"abc153_f" ,"abc172_c"],
        "ビット全探索":["abc080_c" ,"abc147_c" ,"abc167_c"],
        "ワーシャルフロイド":["abc012_d" ,"abc016_c" ,"abc021_c" ,"abc051_d" ,"abc073_d" ,"abc079_d" ,"abc143_e" ,"abc151_d"],
        "優先度付きキュー (priority queue)":["abc123_d" ,"abc137_d" ,"abc141_d"],
        "素因数分解":["abc052_c" ,"abc114_d" ,"abc142_d" ,"abc152_e" ,"abc169_d" ,"abc172_d"],
        "エラトステネスの篩":["abc084_d" ,"abc114_d" ,"abc149_c" ,"abc152_e" ,"abc172_d"],
        "フェルマーの小定理":["abc034_c" ,"abc132_d" ,"abc145_d" ,"abc151_e" ,"abc152_e" ,"abc156_d" ,"abc167_e" ,"abc171_f"],
        "パスカルの三角形":["abc132_d"],
        "区分木 (segment tree)":["abc103_d" ,"abc125_c" ,"abc153_f" ,"abc157_e"],
        "sparse table":["abc125_c"],
        "disjoint sparse table":["abc125_c"],
        "bit (binary indexed tree) / fenwick tree":["abc103_d" ,"abc153_f"],
        "平衡二分探索木":["abc134_e" ,"abc170_e"]
    }


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_content():
    text = create_contest_url("今週の学習コンテストはこちら！！！\n"+PROBLEM_URL_TEMPLATE)
    COLOR = "good"
    atachements = {"text":text,"color":COLOR}
    return atachements

def create_contest_url(text):
    contest_type = random.choice(CONTESTS)
    number = str(random.randint(contest_type["range_oldest"],contest_type["range_latest"])).zfill(3)
    return text.format(contest_id=contest_type["name"]+number)

def get_probrem():
    text = create_problem_url("今週のピックアップアルゴリズムは{argorithm}です。本アルゴリズムを使用した問題はこちら！！！\n"+PROBLEM_URL_TEMPLATE+"/{probrem_id}")
    COLOR = "good"
    atachements = {"text":text,"color":COLOR}
    return atachements

def create_problem_url(text):
    argorithm,probrem_ids = random.choice(list(PROBLEM_CATEGORIES.items()))
    probrem_id = random.choice(probrem_ids)
    return text.format(contest_id=probrem_id[:-2],argorithm=argorithm,probrem_id=probrem_id)

def lambda_handler(event, context):
    # SlackにPOSTする内容をセット
    slack_message = {
        'url' : SLACK_POST_URL,
        'message': {
        'channel': SLACK_CHANNEL,
        "attachments": [get_content(),get_probrem()]
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