from main.app import db
import datetime



scout_messages = db.Table('scout_messages',
		db.Column('scout_id', db.Integer, db.ForeignKey('scout.id')),
		db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
	)

class Scout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	username = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	image_name = db.Column(db.String(400), default='avatar.png')
	messages = db.relationship('Message', secondary=scout_messages,
			backref=db.backref('scouts', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Scout, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Scout: %s >' % self.username


manager_messages = db.Table('manager_messages',
		db.Column('manager_id', db.Integer, db.ForeignKey('manager.id')),
		db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
	)


class Manager(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	image_name = db.Column(db.String(400), default='avatar.png')
	messages = db.relationship('Message', secondary=manager_messages,
			backref=db.backref('managers', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Manager, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Manager; First Name: %s >' % self.first_name


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String(100))
	sender_status = db.Column(db.String(100))
	receiver_status = db.Column(db.String(100))
	receiver_id = db.Column(db.Integer)
	sender_id = db.Column(db.Integer)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(Message, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Message: %s>' % self.body


player_stats = db.Table('player_stats',
		db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
		db.Column('stats_id', db.Integer, db.ForeignKey('stats.id')),
	)


player_performance = db.Table('player_performance',
		db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
		db.Column('performance_id', db.Integer, db.ForeignKey('performance.id'))
	)


class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	role = db.Column(db.String(100), nullable=False)
	curr_perf = db.Column(db.Float, default=0.00)
	photo_name = db.Column(db.String(400), unique=True, nullable=False)
	date_of_birth = db.Column(db.DateTime, nullable=False)
	week = db.Column(db.Integer, default=0)
	num_matches = db.Column(db.Integer, default=0)
	stats = db.relationship('Stats', secondary=player_stats,
			backref=db.backref('players', lazy='dynamic')
		)
	performance = db.relationship('Performance', secondary=player_performance,
			backref=db.backref('players', lazy='dynamic'),
		)

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Player: %s >' % self.first_name


class Stats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	shots_for = db.Column(db.Integer, default=0)
	shots_for_ontarget = db.Column(db.Integer, default=0)
	goals_for = db.Column(db.Integer, default=0)
	assists = db.Column(db.Integer, default=0)
	crosses = db.Column(db.Integer, default=0)
	crosses_successful = db.Column(db.Integer, default=0)
	interceptions = db.Column(db.Integer, default=0)
	clearances = db.Column(db.Integer, default=0)
	tackles = db.Column(db.Integer, default=0)
	fouls = db.Column(db.Integer, default=0)
	shots_against = db.Column(db.Integer, default=0)
	shots_blocked = db.Column(db.Integer, default=0)
	goals_against = db.Column(db.Integer, default=0)
	saves = db.Column(db.Integer, default=0)

	def __init__(self, *args, **kwargs):
		super(Stats, self).__init__(*args, **kwargs)


class Performance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	week = db.Column(db.Integer, default=0)
	performance = db.Column(db.Float)

	def __init__(self, *args, **kwargs):
		super(Performance, self).__init__(*args, **kwargs)


	def __repr__(self):
		return '<Performance: %s>' % self.week



club_manager = db.Table('club_manager',
		db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
		db.Column('manager_id', db.Integer, db.ForeignKey('manager.id')),
	)


club_players = db.Table('club_players',
		db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
		db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
	)


class Club(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	league = db.Column(db.String(100), default='Uganda Premier League')
	logo_name = db.Column(db.String(200), default='avatar.png')
	home_rating = db.Column(db.Float, default=0.0)
	away_rating = db.Column(db.Float, default=0.0)
	ave_rating = db.Column(db.Float, default=0.0)
	manager = db.relationship('Manager', secondary=club_manager,
			backref=db.backref('clubs', lazy='dynamic')
		)
	players = db.relationship('Player', secondary=club_players,
			backref=db.backref('clubs', lazy='dynamic'),
		)

	def __init__(self, *args, **kwargs):
		super(Club, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Club: %s >' % self.name


class FeedbackComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(1000), default='Edit this text to add your own feedback comment')
	created_time = db.Column(db.DateTime, default=datetime.datetime.now)
	updated_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(FeedbackComment, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Feedback Comment: %s >' % self.body
