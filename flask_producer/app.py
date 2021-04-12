from producer import app

if __name__ == '__main__':
    app.run(
        host=app.config.get('SERVICE_HOST'),
        port=app.config.get('SERVICE_PORT'),
        threaded=app.config.get('THREADED'),
        debug=app.config.get('DEBUG')
    )
