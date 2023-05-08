from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer
from models.db import db
from models.task import Task
from log.formatter import set_formatter
import config
import requests
import os

app = Flask("app",
            static_url_path='',
            static_folder='public')
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
set_formatter(app.logger)

kafka_producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVER'])

@app.route("/")
def index():
    try:
        tasks = Task.query.order_by(Task.id).all()
        return render_template("index.html", tasks=tasks)
    except Exception as e:
        return str(e)


@app.route("/tasks/create", methods=['POST'])
def create():
    global kafka_producer
    try:
        app.logger.info("creating new task: %s", request.form.to_dict())
        task = Task()
        task.title = request.form["title"]
        task.note = request.form["note"]
        db.session.add(task)
        db.session.commit()
        return jsonify({'id': task.id})
    except Exception as e:
        app.logger.exception(str(e))
        return str(e)


@app.route("/tasks/emoji", methods=['POST'])
def emoji():
    try:
        task = Task.query.get(request.form["id"])
        task.emoji = request.form["emoji"]
        db.session.commit()
        return ""
    except Exception as e:
        app.logger.exception(str(e))
        return str(e)


@app.route("/tasks/done", methods=['POST'])
def done():
    try:
        app.logger.info("updating task state: %s", request.form.to_dict())
        task = Task.query.get(request.form["id"])
        task.done = request.form["done"] == "true"
        db.session.commit()
        return ""
    except Exception as e:
        app.logger.exception(str(e))
        return str(e)


@app.route("/tasks/delete", methods=['POST'])
def delete():
    try:
        app.logger.warning("deleting task %s", request.form.to_dict())
        kafka_producer.send('deleted-tasks', request.form["id"].encode()).get(timeout=60)
        return jsonify({'id': request.form["id"]})
    except Exception as e:
        app.logger.exception(str(e))
        return str(e)


@app.route("/live")
def live():
    try:
        return requests.get("http://live-backend:3001/live", params={'id': request.args["id"]}).text
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, use_reloader=True)
