from main.app import db
import datetime


scout_views = db.Table('scout_views',
		db.Column('scout_id', db.Integer, db.ForeignKey('scout.id')),
		db.Column('view_id', db.Integer, db.ForeignKey('view.id'))
	)


class Scout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), unique=True, nullable=False)
	image_name = db.Column(db.String(400), default='avatar')
	date_of_birth = db.Column(db.DateTime, default=datetime.datetime.now)
	views = db.relationship('View', secondary=scout_views,
		backref=db.backref('scouts', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Scout, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Scout: %s >' % self.username


manager_views = db.Table('manager_views',
		db.Column('manager_id', db.Integer, db.ForeignKey('manager.id')),
		db.Column('view_id', db.Integer, db.ForeignKey('view.id'))
	)


class Manager(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), unique=True, nullable=False)
	image_name = db.Column(db.String(400), default='avatar.png')
	date_of_birth = db.Column(db.DateTime, default=datetime.datetime.now)
	views = db.relationship('View', secondary=manager_views,
		backref=db.backref('managers', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(Manager, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Manager: %s >' % self.username


class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	date_of_birth = db.Column(db.DateTime, default=datetime.datetime.now)
	goals = db.Column(db.Integer, default=0)
	assists = db.Column(db.Integer, default=0)
	yellow_cards = db.Column(db.Integer, default=0)
	red_cards = db.Column(db.Integer, default=0)
	role = db.Column(db.String(100), nullable=False)
	image_name = db.Column(db.String(400), unique=True, nullable=False)

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Player: %s >' % self.name


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

view_replies = db.Table('view_replies',
		db.Column('view_id', db.Integer, db.ForeignKey('view.id')),
		db.Column('reply_id', db.Integer, db.ForeignKey('reply.id'))
	)


class View(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text, nullable=False)
	created_time = db.Column(db.DateTime, default=datetime.datetime.now)
	image_name = db.Column(db.String(400), nullable=True)
	replies = db.relationship('Reply', secondary=view_replies,
		backref=db.backref('views', lazy='dynamic')
		)

	def __init__(self, *args, **kwargs):
		super(View, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<View: %s >' % self.body
	

class Reply(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	creator = db.Column(db.String(100), nullable=False)
	body = db.Column(db.Text, nullable=False)
	created_time = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(Reply, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Reply: %s >' % self.body


class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	league = db.Column(db.Integer, default=1)
	competition = db.Column(db.String(100))
	home = db.Column(db.String(100), nullable=False)
	away = db.Column(db.String(100), nullable=False)
	home_score = db.Column(db.Integer)
	away_score = db.Column(db.Integer)
	done = db.Column(db.String(100), default=0)
	stadium = db.Column(db.String(100), nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	def __init__(self, *args, **kwargs):
		super(Match, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Match: Home - %s >' % self.home


class NonleagueMatch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	league = db.Column(db.Integer, default=0)
	competition = db.Column(db.String(100))
	home = db.Column(db.String(100), nullable=False)
	away = db.Column(db.String(100), nullable=False)
	home_score = db.Column(db.Integer)
	away_score = db.Column(db.Integer)
	done = db.Column(db.String(100), default=0)
	stadium = db.Column(db.String(100), nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	def __init__(self, *args, **kwargs):
		super(NonleagueMatch, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Match: Home - %s >' % self.home


class FeedbackComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(1000), default='Edit this text to add your own feedback comment')
	created_time = db.Column(db.DateTime, default=datetime.datetime.now)
	updated_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

	def __init__(self, *args, **kwargs):
		super(FeedbackComment, self).__init__(*args, **kwargs)

	def __repr__(self):
		return '<Feedback Comment: %s >' % self.body
