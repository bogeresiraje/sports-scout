import datetime
import random

from main.api.data.data import *
from main.api.access_control.logger import Logger
from main.api.access_control.mail import send_mail


class AccountSet:
	_pending_accounts = []

	def __init__(self):
		pass

	def add_user(self, mock_account):
		self._pending_accounts.append(mock_account)

	# cred -> credentials
	def is_code_valid(self, code):
		is_valid = 0
		account = None
		for cred in self._pending_accounts:
			if(cred[0] == code):
				account = cred
				if self.is_code_expired(cred[4]):
					is_valid = -1
				else:
					self.create_new_account(cred)
					is_valid = 1

				break

		return is_valid

	def is_code_expired(self, created_time):
		max_waiting_time = datetime.timedelta(minutes=10)
		return ( datetime.datetime.now() - created_time ) > max_waiting_time

	def create_new_account(self, cred):
		user = UserHandler().set_user(cred[1], cred[2], cred[3])
		for index in range(len(self._pending_accounts)):
			if account[index][0] == cred[0]:
				self._pending_accounts.pop(index)
				break
		Logger().login(user.username, user.password)
		self._cred = {'id': user.id, 'username': user.username }

	def get_credentials(self):
		return self._cred


class MockAccount:
	def __init__(self, email, username, password):
		self._email = email
		self._username = username
		self._password = password

	def is_email_valid(self):
		return UserHandler().is_email_valid(self._email)

	def is_username_valid(self):
		return UserHandler().is_username_valid(self._username)

	def add_to_pending(self):
		pending_account = (self._code, self._username, self._email, self._password, datetime.datetime.now())
		account_set = AccountSet()
		account_set.add_user(pending_account)

	def send_verification(self):
		code = random.randint(1000,9999)
		self._code = str(code)
		send_mail(self._code, self._email)
		self.add_to_pending()
