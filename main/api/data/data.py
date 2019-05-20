import os
import datetime
from flask import jsonify
from werkzeug import secure_filename
from main.app import app, db
from main.models import *
from main.api.data.sort import Sort
from main.api.data.structured_date import structure_date, enumerate_month


class ManagerHandler:
	@staticmethod
	def set_manager(name='hannz', photo='default.jpg', email='hannzjavas@gmail.com', password='12345', year=1996,
					month=9, date=25):
		date_obj = datetime.datetime(year, month, date)
		manager = Manager(username=name, email=email, password=password, date_of_birth=date_obj)
		db.session.add(manager)
		db.session.commit()
		return manager

	@staticmethod
	def get_manager(manager_id):
		return Manager.query.get(manager_id)

	@staticmethod
	def get_manager_by_username(username):
		return Manager.query.filter(Manager.username == username)[0]

	@staticmethod
	def get_username(manager_id):
		return Manager.query.get(manager_id).username


# handler class for the user plus all the different actions that can be performed by the scout
class ScoutHandler:
	@staticmethod
	def set_scout(name='hannz', photo='default.jpg', email='hannzjavas@gmail.com', password='12345', year=1996,
					month=9, date=25, club='Ondupdaraka FC', league='Uganda Premier League'):
		date_obj = datetime.datetime(year, month, date)
		scout = Scout(username=name, email=email, password=password, date_of_birth=date_obj)
		db.session.add(scout)
		db.session.commit()
		return scout

	@staticmethod
	def get_scout(scout_id):
		return Scout.query.get(scout_id)

	@staticmethod
	def delete_scout(scout_id):
		scout = Scout.query.get(scout_id)
		db.session.delete(scout)
		db.session.commit()
		return scout

	@staticmethod
	def is_email_valid(email):
		users = list(User.query.filter(User.email == email).all())
		return len(users) == 0

	@staticmethod
	def is_username_valid(username):
		users = list(User.query.filter(User.username == username).all())
		return len(users) == 0


	@staticmethod
	def is_user(user_id):
		return bool(User.query.get(user_id))

	@staticmethod
	def set_view(user_id, body):
		user = User.query.get(user_id)
		view = View(body=body)
		user.views.append(view)
		db.session.add_all([user, view])
		db.session.commit()
		return view

	@staticmethod
	def get_view(view_id):
		return View.query.get(view_id)

	@staticmethod
	def delete_view(view_id):
		view = View.query.get(view_id)
		db.session.delete(view)
		db.session.commit()
		return view

	@staticmethod
	def get_views_list():
		return View.query.order_by(View.created_time.desc()).all()

	@staticmethod
	def set_reply(view_id, creator_id, body):
		creator = User.query.get(creator_id).username
		view = View.query.get(view_id)
		reply = Reply(creator=creator, body=body)
		view.replies.append(reply)
		db.session.add_all([view, reply])
		db.session.commit()
		return reply

	@staticmethod
	def get_replies(view_id):
		return View.query.get(view_id).replies


class ClubHandler:
	@staticmethod
	def set_club(name, league, logo):
		logo_name = secure_filename(logo.filename)
		logo_file = os.path.join(app.config['CLUB_LOGOS'], logo_name)
		logo.save(logo_file)

		club = Club(name=name, league=league, logo_name=logo_name)
		
		db.session.add(club)
		db.session.commit()
		return club

	@staticmethod
	def delete_club(club_id):
		club = Club.query.get(club_id)
		db.session.delete(club)
		db.session.commit()
		return club

	@staticmethod
	def get_all_clubs():
		return Club.query.all()

	@staticmethod
	def get_club(club_id):
		return Club.query.get(club_id)

	@staticmethod
	def get_club_by_manager(manager):
		manager_obj = Manager.query.filter(Manager.username == manager)[0]
		return manager_obj.clubs.all()[0]

class FeedbackHandler:
	@staticmethod
	def get_feedback_comment():
		return FeedbackComment.query.all()[0]

	@staticmethod
	def set_feedback(feedback_body):
		feedback = FeedbackComment(body=feedback_body)
		db.session.add(feedback)
		db.session.commit()
		return feedback

	@staticmethod
	def update_feedback(feedback_id, feedback_body):
		feedback = FeedbackComment.query.get(feedback_id)
		feedback.body = feedback_body
		db.session.add(feedback)
		db.session.commit()
		return feedback



# class for managing players
class PlayerHandler:
	@staticmethod
	def set_player(name, role, image_file):
		season = SeasonHandler().get_curr_season()

		image_name = secure_filename(image_file.filename)
		image = os.path.join(app.config['PLAYER_IMG_DIR'], image_name)
		image_file.save(image)
		player = Player(name=name, role=role, image_name=image_name)

		season.players.append(player)

		db.session.add(player)
		db.session.commit()

		return player

	@staticmethod
	def get_player(player_id):
		return Player.query.get(player_id)

	@staticmethod
	def delete_player(player_id):
		player = Player.query.get(player_id)
		db.session.delete(player)
		db.session.commit()
		return player


	@staticmethod
	def get_all_players():
		season  = SeasonHandler().get_curr_season()
		return season, season.players

	@staticmethod
	def edit_player(player_id, name, role):
		player = Player.query.get(player_id)
		player.name = name
		player.role = role

		db.session.add(player)
		db.session.commit()
		return player

	@staticmethod
	def edit_player_with_photo(player_id, name, role, photo):
		player = Player.query.get(player_id)

		image_name = secure_filename(photo.filename)
		image = os.path.join(app.config['PLAYER_IMG_DIR'], image_name)
		photo.save(image)

		player.name = name
		player.role = role
		player.image_name = image_name

		db.session.add(player)
		db.session.commit()
		return player

	@staticmethod
	def get_players_list_by_goals():
		return list(Player.query.order_by(Player.goals.desc()).all())

	@staticmethod
	def get_players_list_by_assists():
		return list(Player.query.order_by(Player.assists.desc()).all())

	@staticmethod
	def get_players_list_by_yellow():
		return list(Player.query.order_by(Player.yellow_cards.desc()).all())

	@staticmethod
	def get_players_list_by_red():
		return list(Player.query.order_by(Player.red_cards.desc()).all())

	@staticmethod
	def persist_player_goals(player_id, goals):
		player = Player.query.get(player_id)
		player.goals = goals
		db.session.add(player)
		db.session.commit()

	@staticmethod
	def persist_player_assists(player_id, assists):
		player = Player.query.get(player_id)
		player.assists = assists
		db.session.add(player)
		db.session.commit()

	@staticmethod
	def persist_player_yellow_cards(player_id, yellow_cards):
		player = Player.query.get(player_id)
		player.yellow_cards = yellow_cards
		db.session.add(player)
		db.session.commit()

	@staticmethod
	def persist_player_red_cards(player_id, red_cards):
		player = Player.query.get(player_id)
		player.red_cards = red_cards
		db.session.add(player)
		db.session.commit()
