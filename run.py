from main.app import app, db
from main.api.blueprint import api


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
