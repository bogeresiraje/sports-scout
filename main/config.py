import os


class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/sports'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = '@&*((()HDKD?<>IEUIUYGBJKHSHUI((W*((w9ehfhcnxowweijcnii'
	STATIC_DIR = os.path.join(APPLICATION_DIR, 'api/uploads')
	CLUB_LOGOS = os.path.join(STATIC_DIR, 'club_logos')
	USER_IMG_DIR = os.path.join(STATIC_DIR, 'user_images')
	PLAYER_IMG_DIR = os.path.join(STATIC_DIR, 'player_images')
	TECHNICAL_IMG_DIR = os.path.join(STATIC_DIR, 'technical_images')
	DEBUG = True

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = 'ronniwallace2017@gmail.com'
	MAIL_PASSWORD = 'wilishere06'
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
