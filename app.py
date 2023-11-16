from app import create_app

app = create_app()

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.run(host='0.0.0.0', debug=True, port=8002, use_reloader=False)