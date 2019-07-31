from flask import session
from main.models import *
from main.api.data.data import ManagerHandler, ScoutHandler


class Logger:
	@staticmethod
	def is_loggedin(username):
		try:
			session[username]
			return True
		except:
			return False

	@staticmethod
	def delete_account(user_id, user_status):
		if user_status == 'scout':
			ScoutHandler().delete_scout(user_id)
			Logger().logout(user_id)
		else:
			ManagerHandler().delete_manager(user_id)
			Logger().delete_manager(user_id)

	@staticmethod
	def is_manager(email):
		try:
			ManagerHandler().get_manager_by_email(email)
			return True
		except:
			return False

	@staticmethod
	def direct_login(id):
		session[str(id)] = True

	@staticmethod
	def is_scout(email):
		try:
			ScoutHandler().get_scout_by_email(email)
			return True
		except:
			return False

	@staticmethod
	def login_manager(email, password):
		manager = ManagerHandler().get_manager_by_email(email)
		if manager['password'] == password and manager['email'] == email:
			session[str(manager['id'])] = True
			return manager

	@staticmethod
	def login_scout(email, password):
		scout = ScoutHandler().get_scout_by_email(email)
		if scout['password'] == password and scout['email'] == email:
			session[str(scout['id'])] = True
			return scout

	@staticmethod
	def logout(user_id):
		try:
			session.pop(str(user_id), -1)
		except:
			pass
