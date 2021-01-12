# /usr/bin/python
# -*- coding:utf-8 -*-
# @Time         : 2020-08-29 14:02
# @Author       : mmy
# @Site         : 
# @File         : redis_es.py
# @Software     : PyCharm
from elasticsearch import Elasticsearch

from sys_config import ELASTIC_SEARCH_HOST


def elastic_write(index,data):

    es = Elasticsearch([ELASTIC_SEARCH_HOST], request_timeout=60)
    es.index(index= index, doc_type="data", body=data,request_timeout=60)
    return "success"
