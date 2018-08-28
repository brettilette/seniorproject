from flask import Flask
from flask import Response
from flask import json
from flask import jsonify
from flask import request
from flask import Blueprint
from flask import render_template

app = Flask(__name__)

@app.route('/_api/hydraGraph')
def api_response():
    db = GraphDatabase("http://localhost:7475/db/data")

    nodes = getNodes(db)
    rels = getRels(db)

    q = "START n = node(*) RETURN n"
    params = {}
    querySquenceObject = db.query(q, params = params, returns = RAW)

    for node in querySquenceObject[1:]:
        n = node.pop()
        data = n.get('data')
        name = data.get('name')
        description = data.get('description')

        self = n.get('self')
        self = urlparse(self)
        uid = doRegEX(self)
