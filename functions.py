"""Define functions to use in redis queue."""

from flask import abort,json
import requests
from rq import get_current_job

from redis_es import elastic_write
from redis_resc import redis_queue_web_result, redis_queue_offiaccount_result, redis_queue_wechat_result
from sys_config import FAQ_URL
import secrets
import time
import secrets


def get_session():
    session = secrets.token_urlsafe(16)
    print(session)
    return session




def some_message_function(some_input):
    """A genera function for redis queue."""
    job = get_current_job()

    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }


def wechat_long_function(some_input):
    """An example function for redis queue."""
    job = get_current_job()

    dict={
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }
    job_id = dict["job_id"]
    print("job_id")
    print(job_id)
    try:
        responce = {}
        responce['sender'] = dict['input']['sender']
        responce['message'] = dict['input']['message']
        #responce = dict['input']
        json_dict = json.dumps(responce)
        req = requests.post(FAQ_URL, json_dict)
    except Exception as exception:
        abort(404, description=exception)

    if not responce:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    dict["result"] = req.json()
    #dict["time"] = time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
    redis_queue_wechat_result.enqueue(some_message_function, dict)

    result = {
        "job_id": job.id,
        "sessionid":get_session(),
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": req.json(),
    }
    elastic_write('response_result', result)
    return result


def web_long_function(some_input):
    """An example function for redis queue."""
    job = get_current_job()
    dict = {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }
    job_id = dict["job_id"]
    print("job_id")
    print(job_id)
    try:
        responce = {}
        responce['sender'] = dict['input']['sender']
        responce['message'] = dict['input']['message']    
        #responce = dict['input']
        json_dict = json.dumps(responce)
        req = requests.post(FAQ_URL, json_dict)
    except Exception as exception:
        abort(404, description=exception)

    if not responce:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    dict["result"]=req.json()
    #dict["time"] = time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
    redis_queue_web_result.enqueue(some_message_function, dict)
    result = {
        "job_id": job.id,
        "sessionid":get_session(),
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": req.json(),
    }
    elastic_write('response_result', result)
    return req.json()


def offiaccount_function(some_input):
    """An example function for redis queue."""
    print("aaaaaa")
    job = get_current_job()

    dict={

        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }
    job_id = dict["job_id"]
    print("job_id")
    print(job_id)
    try:
        responce = dict['input']
        json_dict = json.dumps(responce)
        req = requests.post(FAQ_URL, json_dict)
    except Exception as exception:
        abort(404, description=exception)

    if not responce:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    dict["result"] = req.json()
    redis_queue_offiaccount_result.enqueue(some_message_function, dict)
    result = {
        "job_id": job.id,
        "sessionid":get_session(),
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": req.json(),
    }
    elastic_write('response_result', result)
    return result

