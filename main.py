"""The Flask App."""

# pylint: disable=broad-except

from flask import Flask, abort, jsonify, request,json
from rq.job import Job
from functions import web_long_function, offiaccount_function, wechat_long_function
from redis_es import elastic_write
from redis_resc import redis_conn, redis_queue_offiaccount, redis_queue_web, redis_queue_wechat
import datetime
import secrets

app = Flask(__name__)


def get_session():
    session = secrets.token_urlsafe(16)
    print(session)
    return session



@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"


@app.route("/offiaccount", methods=["POST", "GET"])
def offiaccount():
    """Enqueues a task into redis queue to be processes.
    Returns the job_id."""
    if request.method == "GET":
        query_param = request.args.get("external_id")
        if not query_param:
            abort(
                404,
                description=(
                    "No query parameter external_id passed. "
                    "Send a value to the external_id query parameter."
                ),
            )
        data = {"external_id": query_param}
    if request.method == "POST":
        data = request.json
        print(data)
    elastic_write('offiaccount',data)
    job = redis_queue_offiaccount.enqueue(offiaccount_function, data)
    print(job)
    return jsonify({"job_id": job.id})


@app.route("/web", methods=["POST", "GET"])
def web():
    """Enqueues a task into redis queue to be processes.
    Returns the job_id."""
    if request.method == "GET":
        query_param = request.args.get("external_id")
        if not query_param:
            abort(
                404,
                description=(
                    "No query parameter external_id passed. "
                    "Send a value to the external_id query parameter."
                ),
            )
        data = {"external_id": query_param}
    if request.method == "POST":
        data = request.json
    elastic_write('web', data)
    job = redis_queue_web.enqueue(web_long_function, data) 
    return jsonify({"job_id": job.id})


@app.route("/wechat", methods=["POST", "GET"])
def wechat():
    """Enqueues a task into redis queue to be processes.
    Returns the job_id."""
    if request.method == "GET":
        query_param = request.args.get("external_id")
        if not query_param:
            abort(
                404,
                description=(
                    "No query parameter external_id passed. "
                    "Send a value to the external_id query parameter."
                ),
            )
        data = {"external_id": query_param}
    if request.method == "POST":
        data = request.json
    elastic_write('wechat', data)
    job = redis_queue_wechat.enqueue(wechat_long_function, data)
    print(job)
    return jsonify({"job_id": job.id})


@app.route("/check_status")
def check_status():
    """Takes a job_id and checks its status in redis queue."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        abort(404, description=exception)

    return jsonify({"job_id": job.id, "job_status": job.get_status()})


@app.route("/get_result")
def get_result():
    """Takes a job_id and returns the job's result."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        abort(404, description=exception)

    if not job.result:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    print(job.result)
    return jsonify(job.result)
    #elastic_write('session',job.result)


if __name__ == "__main__":
    app.run(debug=True,port=7277)

