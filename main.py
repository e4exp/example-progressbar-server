from typing import Dict
import json
import time

from flask import Flask, request
import flask
from icecream import ic
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import redis

app: Flask = Flask(__name__)
# アップロードできるファイルサイズを1MBに制限
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# redisに接続する準備
redis_client: redis.client.Redis = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True,
)


# 進捗を返すためのエンドポイント
@app.route("/progress", methods=['POST'])
def get_progress():
    ic(request.values)

    try:
        id_request: int = request.values["id"]
        if redis_client.exists(id_request):
            # redisから進捗を取り出す
            progress: int = redis_client.get(id_request)
        else:
            progress: int = 100
    except:
        progress: int = 100

    data: Dict[str, int] = {
        "progress": progress,
    }
    response: flask.wrappers.Response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )
    # CORS
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ファイルアップロード用のエンドポイント
@app.route("/upload", methods=['POST'])
def upload_file():

    ic(request.files)
    ic(request.values)
    id_request: int = request.values["id"]

    # ファイルを読み込む
    file_in: FileStorage = request.files['file']
    name_file: str = file_in.filename
    if name_file == "":
        data: Dict[str, str] = {"result": "filename must not empty"}
        response: flask.wrappers.Response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json',
        )
        return response
    name_file: str = secure_filename(name_file)

    # ============
    # ファイル処理。今回は何もしない
    # ============
    # 進捗の初期化
    progress: int = 0
    redis_client.set(id_request, progress)

    n: int = 10
    for i in range(n):
        time.sleep(1)

        # 進捗の登録
        progress: int = int((i + 1) / n * 100)
        redis_client.set(id_request, progress)

    # ============
    # 送信
    # ============
    result: str = "success"
    data: Dict[str, str] = {
        "result": result,
    }
    response: flask.wrappers.Response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )

    # CORS
    response.headers.add('Access-Control-Allow-Origin', '*')

    # 進捗の消去
    redis_client.delete(id_request)
    return response
