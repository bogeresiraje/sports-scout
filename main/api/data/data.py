import os
import datetime
from flask import jsonify
from werkzeug import secure_filename
from main.app import app, db
from main.models import *
from main.api.data.sort import Sort, CustomSort
from main.api.data.structured_date import structure_date, enumerate_month
from main.api.data.helper import *


class ManagerHandler:
	@staticmethod
	def set_manager(club_id, first_name, last_name, email, password):
		club = Club.query.get(club_id)
		manager = Manager(first_name=first_name, last_name=last_name, email=email, password=password)
		club.manager.append(manager)
		db.session.add(manager)
		db.session.commit()
		return manager

	@staticmethod
	def update_photo(manager_id=None, image=None):
		manager = Manager.query.get(manager_id)

		image_file = os.path.join(app.config['USER_IMG_DIR'], secure_filename(image.filename))
		image_name = os.path.basename(image_file)
		manager.image_name = image_name
		db.session.commit()

		image.save(image_file)

	@staticmethod
	def delete_manager(manager_id):
		manager = Manager.query.get(manager_id)
		db.session.delete(manager)
		db.session.commit()

	@staticmethod
	def get_manager(manager_id):
		manager_obj = Manager.query.get(manager_id)
		manager = {}
		manager.update(manager_obj.__dict__)
		manager.pop('_sa_instance_state', -1)

		club_obj = manager_obj.clubs.all()[0]
		club = {}
		club.update(club_obj.__dict__)
		club.pop('_sa_instance_state', -1)

		manager.update({ 'club': club })

		return manager

	@staticmethod
	def get_all_managers():
		managers = []

		managers_obj = Manager.query.all()
		for manager_obj in managers_obj:
			manager = {}
			manager.update(manager_obj.__dict__)
			manager.pop('_sa_instance_state')
			managers.append(manager)

		return managers


	@staticmethod
	def get_all_managers_with_clubs():
		managers = []

		managers_obj = Manager.query.all()
		for manager_obj in managers_obj:
			manager = {}
			manager.update(manager_obj.__dict__)
			manager.pop('_sa_instance_state')

			club = {}
			club_obj = manager_obj.clubs.all()[0]
			club.update(club_obj.__dict__)
			club.pop('_sa_instance_state')

			manager.update({'club': club})

			managers.append(manager)

		return managers


	@staticmethod
	def get_manager_by_email(email):
		manager = {}
		manager_obj = Manager.query.filter(Manager.email == email)[0]
		manager.update(manager_obj.__dict__)
		manager.pop('_sa_instance_state')
		return manager

	@staticmethod
	def get_username(manager_id):
		return Manager.query.get(manager_id).username

	@staticmethod
	def is_email_valid(email):
		managers = list(Manager.query.filter(Manager.email == email))
		return not bool(len(managers))

	@staticmethod
	def is_username_valid(username):
		managers = list(Manager.query.filter(Manager.username == username))
		scouts = list(Scout.query.filter(Scout.username == username))
		return not (bool(len(managers)) and bool(len(scouts)))


# handler class for the user plus all the different actions that can be performed by the scout
class ScoutHandler:
	@staticmethod
	def set_scout(first_name='', last_name='', email='', password=''):
		scout = Scout(first_name=first_name, last_name=last_name, email=email, password=password)
		db.session.add(scout)
		db.session.commit()
		return scout

	@staticmethod
	def update_photo(scout_id=None, image=None):
		scout = Scout.query.get(scout_id)

		image_file = os.path.join(app.config['USER_IMG_DIR'], secure_filename(image.filename))
		image_name = os.path.basename(image_file)
		scout.image_name = image_name
		db.session.commit()

		image.save(image_file)

	@staticmethod
	def delete_scout(scout_id):
		scout = Scout.query.get(scout_id)
		db.session.selete(scout)
		db.session.commit()

	@staticmethod
	def get_scout(scout_id):
		scout = {}
		scout_obj = Scout.query.get(scout_id)
		scout.update(scout_obj.__dict__)
		scout.pop('_sa_instance_state')
		return scout

	@staticmethod
	def get_all_scouts():
		scouts = []
		scouts_list = Scout.query.all()
		for scout_obj in scouts_list:
			scout = {}
			scout.update(scout_obj.__dict__)
			scout.pop('_sa_instance_state')
			scouts.append(scout)

		return scouts

	@staticmethod
	def filter_scouts(user_id, user_status):
		scouts = []

		scouts_list = Scout.query.filter(Scout.id != user_id) if user_status == 'status' else Scout.query.all()

		for scout_obj in scouts_list:
			scout = {}
			scout.update(scout_obj.__dict__)
			scout.pop('_sa_instance_state')
			scouts.append(scout)

		return scouts

	@staticmethod
	def get_scout_by_email(email):
		scout = {}
		scout_obj = Scout.query.filter(Scout.email == email)[0]
		scout.update(scout_obj.__dict__)
		scout.pop('_sa_instance_state')
		return scout

	@staticmethod
	def delete_scout(scout_id):
		scout = Scout.query.get(scout_id)
		db.session.delete(scout)
		db.session.commit()
		return scout

	@staticmethod
	def is_email_valid(email):
		scouts = list(Scout.query.filter(Scout.email == email).all())
		return len(scouts) == 0


	@staticmethod
	def is_user(user_id):
		return bool(User.query.get(user_id))

	@staticmethod
	def migrate_names():
		scouts = Scout.query.all()
		for scout in scouts:
			scout.first_name = scout.username
			scout.last_name = ''
		db.session.commit()


class MessageHandler:
	@staticmethod
	def set_message(sender_id, sender_status, receiver_id, receiver_status, body):
		if sender_status == 'scout':
			sender = Scout.query.get(sender_id)
		else:
			sender = Manager.query.get(sender_id)

		if receiver_status == 'scout':
			receiver = Scout.query.get(receiver_id)
		else:
			receiver = Manager.query.get(receiver_id)

		sent = Message(tag='sent', sender_id=sender_id, sender_status=sender_status,
			receiver_id=receiver_id, receiver_status=receiver_status, body=body)

		received = Message(tag='received', sender_id=sender_id, sender_status=sender_status,
			receiver_id=receiver_id, receiver_status=receiver_status, body=body)

		sender.messages.append(sent)
		receiver.messages.append(received)

		db.session.add_all([sender, receiver])
		db.session.commit()

		messages = []
		messages_obj = Message.query.filter((Message.receiver_id == receiver_id and
			Message.receiver_status == receiver_status) or (Message.sender_id == receiver_id and
			Message.sender_status == receiver_status ))

		for message in messages_obj:
			msg = {}
			msg.update(message.__dict__)
			msg.pop('_sa_instance_state')
			messages.append(msg)

		return messages

	@staticmethod
	def get_messages(user_id, user_status, other_id, other_status):
		if user_status == 'scout':
			user = Scout.query.get(user_id) 
		else:
			user = Manager.query.get(user_id)

		messages_obj = user.messages
		messages = []

		for message in messages_obj:
			if (message.sender_id == other_id and message.sender_status == other_status) \
				or (message.receiver_id == other_id and message.receiver_status == other_status):
				msg = {}
				msg.update(message.__dict__)
				msg.pop('_sa_instance_state')
				messages.append(msg)

		return messages



class ClubHandler:
	@staticmethod
	def set_club(name, league, logo):
		logo_file = os.path.join(app.config['CLUB_LOGOS'], secure_filename(logo.filename))
		logo_name = os.path.basename(logo_file)
		logo.save(logo_file)

		club = Club(name=name, league=league, logo_name=logo_name)
		
		db.session.add(club)
		db.session.commit()
		return club

	@staticmethod
	def get_club(club_id):
		club = {}
		club_obj = Club.query.get(club_id)
		club.update(club_obj.__dict__)
		club.pop('_sa_instance_state')
		return club

	@staticmethod
	def delete_club(club_id):
		club = Club.query.get(club_id)
		db.session.delete(club)
		db.session.commit()
		return club

	@staticmethod
	def get_all_clubs():
		return Club.query.order_by(Club.ave_rating.desc()).all()

	@staticmethod
	def get_clubs_without_managers():
		clubs = []
		clubs_obj = Club.query.order_by(Club.ave_rating.desc()).all()
		for club_obj in clubs_obj:
			if len(club_obj.manager) == 0:
				club = {}
				club.update(club_obj.__dict__)
				club.pop('_sa_instance_state')
				club.pop('manager')
				clubs.append(club)
		return clubs


	@staticmethod
	def get_detailed_club(club_id):
		club = {}
		club_obj = Club.query.get(club_id)
		club.update(club_obj.__dict__)
		club.pop('_sa_instance_state', -1)
		club.pop('manager', -1)
		club.pop('players', -1)
		club['ave_rating'] = round(club['ave_rating'] * 100)

		manager_obj = club_obj.manager[0] if len(club_obj.manager) else {}
		manager = {}
		try:
			manager.update(manager_obj.__dict__)
		except:
			pass

		manager.pop('_sa_instance_state', -1)
		club.update({ 'manager': manager })

		players = []
		players_obj = club_obj.players
		for player_obj in players_obj:
			player = {}
			player.update(player_obj.__dict__)
			player.pop('_sa_instance_state')
			player['curr_perf'] = round(player['curr_perf'] * 100)
			players.append(player)

		club.update({ 'players': players })
		return club

	@staticmethod
	def get_clubs_with_players():
		temp_clubs = Club.query.order_by(Club.ave_rating.desc()).all()
		clubs = []
		for temp_club in temp_clubs:

			temp_players_list = temp_club.players
			players_obj = []
			for temp_player in temp_players_list:
				player_obj = {}
				player_obj.update(temp_player.__dict__)
				player_obj.pop('_sa_instance_state', -1)
				players_obj.append(player_obj)

			club_obj = {}
			club_obj.update(temp_club.__dict__)
			club_obj.pop('_sa_instance_state', -1)

			_temp = temp_club.__dict__
			_temp.pop('_sa_instance_state', -1)

			players = { 'players': players_obj }
			club_obj.update(players)
			clubs.append(club_obj)

		return clubs

	@staticmethod
	def get_club(club_id):
		return Club.query.get(club_id)

	@staticmethod
	def get_club_by_manager(manager_id):
		manager = Manager.query.get(manager_id)
		club_obj = manager.clubs.all()[0]
		club = {}
		club.update(club_obj.__dict__)
		club.pop('_sa_instance_state')
		club.pop('manager', -1)
		club.pop('players', -1)
		return club


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
	def set_player(club_name, first_name, last_name, role, photo, year, month, date):
		photo_name = secure_filename(photo.filename)
		date_of_birth = datetime.datetime(int(year), int(month), int(date))

		player = Player(first_name=first_name, last_name=last_name, role=role, photo_name=photo_name,
							date_of_birth=date_of_birth, week=0
						)

		photo_file = os.path.join(app.config['PLAYER_IMG_DIR'], photo_name)
		photo.save(photo_file)

		club = Club.query.filter(Club.name == club_name).first()
		club.players.append(player)

		perf = Performance(week=0, performance=0)
		player.performance.append(perf)

		db.session.add_all([player, perf])
		db.session.commit()

		return player

	@staticmethod
	def get_my_players(manager_id):
		manager = Manager.query.get(manager_id)

		club = manager.clubs.all()[0]

		players = []
		players_obj = club.players
		for player_obj in players_obj:
			player = {}
			player.update(player_obj.__dict__)
			player.pop('_sa_instance_state')
			player.pop('stats', -1)
			player.pop('performance', -1)
			player['curr_perf'] = round(player['curr_perf'] * 100)
			players.append(player)

		return club.name, players

	@staticmethod
	def update_player_perf(player_id, perf):
		player = Player.query.get(player_id)
		player.curr_perf = perf
		db.session.commit()

	@staticmethod
	def delete_player(player_id):
		player = Player.query.get(player_id)
		db.session.delete(player)
		db.session.commit()
		return player

	@staticmethod
	def get_player(player_id):
		player = {}
		player_obj = Player.query.get(player_id)
		player.update(player_obj.__dict__)
		player.pop('_sa_instance_state')
		#player['curr_perf'] = round(player['curr_perf'] * 100)
		return player

	@staticmethod
	def get_player_with_stats(player_id):
		player = {}
		player_obj = Player.query.get(player_id)
		player_stats = player_obj.stats

		goals_against = 0
		saves = 0
		goals_for = 0
		crosses = 0
		crosses_successful = 0
		assists = 0
		shots_for = 0
		shots_for_ontarget = 0
		tackles = 0
		fouls = 0
		interceptions = 0
		clearances = 0
		shots_blocked = 0

		for stat in player_stats:
			goals_against = goals_against + stat.goals_against
			saves = saves + stat.saves
			shots_for_ontarget = shots_for_ontarget + stat.shots_for_ontarget
			crosses = crosses + stat.crosses
			crosses_successful = crosses_successful + stat.crosses_successful
			goals_for = goals_for + stat.goals_for
			assists = assists + stat.assists
			shots_for = shots_for + stat.shots_for
			tackles = tackles + stat.tackles
			fouls = fouls + stat.fouls
			interceptions = interceptions + stat.interceptions
			clearances = clearances + stat.clearances
			shots_blocked = shots_blocked + stat.shots_blocked

		player.update(player_obj.__dict__)
		player['curr_perf'] = round(player['curr_perf'] * 100)
		player.pop('_sa_instance_state')
		player.pop('stats')

		stats_dict = {
						'goals_against': goals_against,
						'saves': saves,
						'shots_for_ontarget': shots_for_ontarget,
						'crosses': crosses,
						'crosses_successful': crosses_successful,
						'goals_for': goals_for,
						'assists': assists,
						'shots_for': shots_for,
						'tackles': tackles,
						'fouls': fouls,
						'interceptions': interceptions,
						'clearances': clearances,
						'shots_blocked': shots_blocked
					}
		player.update(stats_dict)
		return player

	@staticmethod
	def get_player_perf(player_id):
		player = Player.query.get(player_id)
		player_perf = []
		perf_list = player.performance
		for perf_obj in perf_list:
			perf = {}
			perf.update(perf_obj.__dict__)
			perf.pop('_sa_instance_state', -1)
			perf.pop('id', -1)
			perf['performance'] = round(perf['performance'] * 100)
			player_perf.append(perf)
		return player_perf


	@staticmethod
	def update_player(player_id=None, first_name=None, last_name=None, role=None):
		player = Player.query.get(player_id)
		player.first_name = first_name
		player.last_name = last_name
		player.role = role

		db.session.commit()
		return player


	@staticmethod
	def update_player_with_photo(player_id=None, first_name=None, last_name=None, role=None,
			photo=None
		):
		player = Player.query.get(player_id)
		player.first_name = first_name
		player.last_name = last_name
		player.role = role

		photo_file = os.path.join(app.config['PLAYER_IMG_DIR'], secure_filename(photo.filename))
		photo_name = os.path.basename(photo_file)
		photo.save(photo_file)

		player.photo_name = photo_name

		db.session.commit()

		return player


	@staticmethod
	def delete_player(player_id):
		player = Player.query.get(player_id)
		db.session.delete(player)
		db.session.commit()
		return player

	@staticmethod
	def get_all_players():
		players_obj = Player.query.order_by(Player.curr_perf.desc()).all()
		players = []
		for player_sa in players_obj:
			player = {}
			player.update(player_sa.__dict__)
			player.pop('_sa_instance_state')
			#player['curr_perf'] = round(player['curr_perf'] * 100)
			players.append(player)

		return players

	@staticmethod
	def get_all_players_with_clubs():
		players_obj = Player.query.order_by(Player.curr_perf.desc()).all()
		players = []
		for player_sa in players_obj:
			club_sa = player_sa.clubs.all()[0]

			club = club_sa.__dict__
			player = player_sa.__dict__

			temp_club = {}
			temp_club.update(club)
			temp_club.pop('_sa_instance_state', -1)
			_club = { 'club': temp_club }

			temp_player = {}
			temp_player.update(player)
			temp_player.pop('_sa_instance_state', -1)
			temp_player['curr_perf'] = round(temp_player['curr_perf'] * 100)
			temp_player.update(_club)

			players.append(temp_player)

		return players[0:40]

	@staticmethod
	def get_player_with_club(player_id):
		# Get player obj
		player_obj = Player.query.get(player_id)

		# Get player club object
		club_obj = player_obj.clubs.all()[0]
		club = {}
		club.update(club_obj.__dict__)
		club.pop('_sa_instance_state', -1)

		player = {}
		player.update(player_obj.__dict__)
		player.pop('_sa_instance_state', -1)
		player['curr_perf'] = round(player['curr_perf'] * 100)

		player.update({ 'club': club })
		return player


	@staticmethod
	def get_goal_keepers():
		players_obj = Player.query.filter(Player.role.contains('Goal Keeper'))
		players = []
		for player in players_obj:
			players.append(PlayerHandler().get_player_with_club(player.id))

		custom = CustomSort(sequence=players)
		return custom.sort_by_rating()[0:40]

	@staticmethod
	def get_defenders():
		players_obj = Player.query.filter(Player.role.contains('Defender'))
		players_obj2 = Player.query.filter(Player.role.contains('Back'))
		players = []
		for player in players_obj:
			players.append(PlayerHandler().get_player_with_club(player.id))
		for player in players_obj2:
			players.append(PlayerHandler().get_player_with_club(player.id))
		
		custom = CustomSort(sequence=players)
		return custom.sort_by_rating()[0:40]

	@staticmethod
	def get_midfielders():
		players_obj = Player.query.filter(Player.role.contains('Midfielder'))
		players = []
		for player in players_obj:
			players.append(PlayerHandler().get_player_with_club(player.id))
		
		custom = CustomSort(sequence=players)
		return custom.sort_by_rating()[0:40]

	@staticmethod
	def get_forwards():
		players_obj = Player.query.filter(Player.role.contains('Forward'))
		players_obj2 = Player.query.filter(Player.role.contains('Striker'))
		players = []
		for player in players_obj:
			players.append(PlayerHandler().get_player_with_club(player.id))
		for player in players_obj2:
			players.append(PlayerHandler().get_player_with_club(player.id))
		
		custom = CustomSort(sequence=players)
		return custom.sort_by_rating()[0:40]


class StatsHandler:
	@staticmethod
	def set_stats(player_id=1, shots_for=0, shots_for_ontarget=0, goals_for=0,
		assists=0, crosses=0, crosses_successful=0, interceptions=0, clearances=0, tackles=0,
		fouls=0, shots_against=0, shots_blocked=0, goals_against=0, saves=0):
		
		player = Player.query.get(player_id)
		stats = Stats(shots_for=shots_for, shots_for_ontarget=shots_for_ontarget,
				goals_for=goals_for, assists=assists, crosses=crosses, crosses_successful=crosses_successful,
				interceptions=interceptions, clearances=clearances, tackles=tackles, fouls=fouls,
				shots_against=shots_against, shots_blocked=shots_blocked,
				goals_against=goals_against, saves=saves
			)
		player.stats.append(stats)
		db.session.add(stats)
		db.session.commit()

	@staticmethod
	def get_highest_saves():
		stat = Stats.query.order_by(Stats.saves.desc()).first()
		return stat.saves if stat is not None else 0

	@staticmethod
	def get_highest_shots_for():
		stat = Stats.query.order_by(Stats.shots_for.desc()).first()
		return stat.shots_for if stat is not None else 0

	@staticmethod
	def get_highest_shots_for_ontarget():
		stat = Stats.query.order_by(Stats.shots_for_ontarget.desc()).first()
		return stat.shots_for_ontarget if stat is not None else 0

	@staticmethod
	def get_highest_goals_for():
		stat = Stats.query.order_by(Stats.goals_for.desc()).first()
		return stat.goals_for if stat is not None else 0

	@staticmethod
	def get_highest_assists():
		stat = Stats.query.order_by(Stats.assists.desc()).first()
		return stat.assists if stat is not None else 0

	@staticmethod
	def get_highest_crosses():
		stat = Stats.query.order_by(Stats.crosses.desc()).first()
		return stat.crosses if stat is not None else 0

	@staticmethod
	def get_highest_crosses_successful():
		stat = Stats.query.order_by(Stats.crosses_successful.desc()).first()
		return stat.crosses_successful if stat is not None else 0

	@staticmethod
	def get_highest_interceptions():
		stat = Stats.query.order_by(Stats.interceptions.desc()).first()
		return stat.interceptions if stat is not None else 0

	@staticmethod
	def get_highest_clearances():
		stat = Stats.query.order_by(Stats.clearances.desc()).first()
		return stat.clearances if stat is not None else 0

	@staticmethod
	def get_highest_tackles():
		stat = Stats.query.order_by(Stats.tackles.desc()).first()
		return stat.tackles if stat is not None else 0

	@staticmethod
	def get_highest_fouls():
		stat = Stats.query.order_by(Stats.fouls.desc()).first()
		return stat.fouls if stat is not None else 0

	@staticmethod
	def get_highest_shots_against():
		stat = Stats.query.order_by(Stats.shots_against.desc()).first()
		return stat.shots_against if stat is not None else 0

	@staticmethod
	def get_highest_shots_blocked():
		stat = Stats.query.order_by(Stats.shots_blocked.desc()).first()
		return stat.shots_blocked if stat is not None else 0

	@staticmethod
	def get_highest_goals_against():
		stat = Stats.query.order_by(Stats.goals_against.desc()).first()
		return stat.goals_against if stat is not None else 0


class PerformanceHandler():
	@staticmethod
	def set_performance(player_id, perf):
		player = Player.query.get(player_id)
		week = player.week
		player.week = week + 1
		player.num_matches = player.num_matches + 1
		performance = Performance(week=week+1, performance=perf)
		player.performance.append(performance)
		db.session.add(performance)
		db.session.commit()

class RatingHandler:
	@staticmethod
	def update_club_rating(club_id=0, home_rating=0, away_rating=0):
		ave_rating = (home_rating + away_rating) / 2
		club = Club.query.get(club_id)
		club.home_rating = home_rating
		club.away_rating = away_rating
		club.ave_rating = round(ave_rating, 4)
		db.session.commit()
	