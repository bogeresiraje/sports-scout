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
	def is_manager_code_valid(self, code):
		is_valid = 0
		account = None
		for cred in self._pending_accounts:
			if(cred[0] == code):
				account = cred
				self.create_manager_account(cred)
				is_valid = 1

				break

		return is_valid

	def is_scout_code_valid(self, code):
		is_valid = 0
		for acc in self._pending_accounts:
			if acc[0] == code:
				self.create_scout_account(acc)
				is_valid = 1

				break

		return is_valid

	def is_code_expired(self, created_time):
		max_waiting_time = datetime.timedelta(minutes=20)
		return ( datetime.datetime.now() - created_time ) > max_waiting_time

	def create_manager_account(self, acc):
		manager = ManagerHandler().set_manager(acc[1], acc[2], acc[3], acc[4], acc[5])
		for index in range(len(self._pending_accounts)):
			if self._pending_accounts[index][0] == acc[0]:
				self._pending_accounts.pop(index)
				break
		Logger().direct_login(manager.id)
		self.user_id = manager.id


	def create_scout_account(self, acc):
		scout = ScoutHandler().set_scout(first_name=acc[1], last_name=acc[2], email=acc[3],
				password=acc[4]
			)
		for index in range(len(self._pending_accounts)):
			if self._pending_accounts[index][0] == acc[0]:
				self._pending_accounts.pop(index)
				break

		Logger().direct_login(scout.id)
		self.user_id = scout.id

	def get_user_id(self):
		return self.user_id


class ScoutAccount:
	def __init__(self, first_name='', last_name='', email='', password=''):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password

	def is_manager_email_valid(self):
		return ManagerHandler().is_email_valid(self.email)

	def is_scout_email_valid(self):
		return ScoutHandler().is_email_valid(self.email)

	def add_to_pending(self):
		pending_account = (self._code, self.first_name, self.last_name, self.email, self.password,
		 		datetime.datetime.now()
		 	)
		account_set = AccountSet()
		account_set.add_user(pending_account)

	def send_verification(self):
		code = random.randint(1000,9999)
		self._code = str(code)
		send_mail(self._code, self.email)
		self.add_to_pending()


class ManagerAccount:
	def __init__(self, club_id, first_name, last_name, email, password):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.club_id = club_id
		self.password = password

	def is_manager_email_valid(self):
		return ManagerHandler().is_email_valid(self.email)

	def is_scout_email_valid(self):
		return ScoutHandler().is_email_valid(self.email)

	def add_to_pending(self):
		pending_account = (self.code, self.club_id, self.first_name, self.last_name, self.email, self.password,
		datetime.datetime.now())
		account_set = AccountSet()
		account_set.add_user(pending_account)

	def send_verification(self):
		code = random.randint(1000,9999)
		self.code = str(code)
		send_mail(self.code, self.email)
		self.add_to_pending()

