import os
from collections.abc import Iterable
from typing import Optional

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def query_builder(iterable_var: Iterable, cmd: Optional[str], value: Optional[str]) -> Iterable:
    mapped_data = map(lambda v: v.strip(), iterable_var)

    if cmd == 'unique':
        return set(mapped_data)

    if value:
        if cmd == 'filter':
            return filter(lambda v: value in v, mapped_data)
        elif cmd == 'map':
            arg = int(value)
            return map(lambda v: v.split(' ')[arg], mapped_data)
        elif cmd == 'limit':
            arg = int(value)
            return list(mapped_data)[:arg]
        elif cmd == 'sort':
            reverse = value == 'desc'
            return sorted(mapped_data, reverse=reverse)

    return mapped_data


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args['cmd1']
        cmd2 = request.args['cmd2']
        value1 = request.args['value1']
        value2 = request.args['value2']
        file_name = request.args['file_name']
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} was not found")

    with open(file_path) as fd:
        result = query_builder(fd, cmd1, value1)
        result = query_builder(result, cmd2, value2)
        content = '\n'.join(result)
        print(content)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
