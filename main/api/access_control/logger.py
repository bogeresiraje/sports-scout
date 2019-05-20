from flask import session
from main.models import *
from main.api.data.data import ManagerHandler


class Logger:
	@staticmethod
	def is_loggedin(username):
		try:
			session[username]
			return True
		except:
			return False

	@staticmethod
	def login_manager(username, password):
		manager = ManagerHandler().get_manager_by_username(username)
		if manager.password == password and manager.username == username:
			session[username] = True
			return manager

		elif manager.password == password and manager.email == username:
			session[username] = True
			return manager

	@staticmethod
	def logout(username):
		session.pop(username)
