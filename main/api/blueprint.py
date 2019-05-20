from flask import Blueprint, jsonify, redirect, url_for, request
from main.app import app
from main.api.access_control.account_manager import AccountSet, MockAccount
from main.api.access_control.logger import Logger
from main.api.data.data import *
from main.api.data.structured_date import structure_date
from main.api.data.statistics import *


api = Blueprint('api', __name__, static_folder='uploads')

@api.route('/')
def index():
    return jsonify({ 'state': {} })

@api.route('/create_account', methods=['GET', 'POST'])
def create_account():
    invalid_email = 'INVALID_EMAIL'
    invalid_username = 'INVALID_USERNAME'
    all_valid = 'TRUE'
    error = 'ERROR'

    try:
        email, username, password = request.form['email'], request.form['username'], request.form['password']
        _account = MockAccount(email, username, password)
        if not _account.is_email_valid():
            return jsonify({ 'validity': invalid_email })

        elif not _account.is_username_valid():
            return jsonify({ 'validity': invalid_username })

        else:
            _account.send_verification()
            return jsonify({ 'validity': all_valid })

    except:
        return jsonify({ 'validity': error })


@api.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    code = request.form['code']
    account_set = AccountSet()
    returnCode = account_set.is_code_valid(code)

    if returnCode == 0:
        return jsonify({'code': 0})

    elif returnCode == 1:
        account_cred = account_set.get_credentials()
        return jsonify({'code': 1, 'account_cred': account_cred })

    elif returnCode == -1:
        return jsonify({'code': -1 })


@api.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        try:
            username, password = request.form['username'], request.form['password']
            manager_obj = Logger().login_manager(username, password)
            return jsonify({ 'username': manager_obj.username })
        except Exception as e:
            return jsonify({ 'fail': 1 })
    else:
        return jsonify({ 'fail': 1 })


@api.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        try:
            username = request.form['username']
            user_obj = Logger().logout(username)
            user = { 'id': user_obj.id }
            return jsonify({ 'user': user })
        except:
            return jsonify({ 'user': {} })
    else:
        return jsonify({ 'user': {} })


@api.route('/post_view', methods=['GET', 'POST'])
def post_view():
    if request.method == 'POST':
        try:
            username, body = request.form['username'], request.form['body']
            if Logger().is_logged_in(username):
                view = UserHandler().set_view(user_id, body)
                return jsonify({'view': True})
            else:
                return jsonify({'not_loggedin': True})

        except:
            return jsonify({'view': 0})

    else:
        return  jsonify({'view': 0})


@api.route('/get_all_views')
def get_all_views():
    try:
        views_list = UserHandler().get_all_views()
        return jsonify({'views': views_list})
    except:
        return jsonify({'views': [] })


@api.route('/get_all_replies')
def get_all_replies():
    try:
        return jsonify({ 'replies': UserHandler().get_replies(view_id) })
    except Exception as e:
        return jsonify({ 'replies': [] })


@api.route('/set_reply', methods=['GET', 'POST'])
def set_reply():
    if request.method == 'POST':
        try:
            view_id, creator_id, body = request.form['view_id'], request.form['creator_id'], request.form['body']
            if Logger().is_logged_in(creator_id) :
                reply = UserHandler().set_reply(view_id, creator_id, body)
                return jsonify({ 'reply': reply })
            else:
                return jsonify({ 'reply': -1 })
        except:
            return jsonify({ 'reply': {} })
    else:
        return jsonify({ 'reply': {} })


@api.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        try:
            username, name, role = request.form['username'], request.form['name'], request.form['role']
            photo = request.files['photo']
            player_obj = PlayerHandler().set_player(name, role, photo)
            player = { 'id': player_obj.id }
            return jsonify({ 'player': player })
        except:
            return jsonify({ 'player': {} })
    else:
        return jsonify({ 'player': {} })


@api.route('/get_all_players')
def get_all_players():
    try:
        season_obj, players_obj = PlayerHandler().get_all_players()
        season = { 'id': season_obj.id, 'name': season_obj.name, 'year': season_obj.year }
        players = [
            {'id': player.id, 'name': player.name, 'role': player.role, 'image_name': player.image_name }
            for player in players_obj
        ]
        return jsonify({ 'season': season, 'players': players })
    except:
        return jsonify({ 'players': [] })


@api.route('/get_player', methods=['GET', 'POST'])
def get_player():
    if request.method == 'POST':
        try:
            player_id = request.form['player_id']
            player_obj = PlayerHandler().get_player(player_id)
            player = {'id': player_obj.id, 'name': player_obj.name, 'role': player_obj.role,
            'image_name': player_obj.image_name }
            return jsonify({ 'player': player })

        except:
            return jsonify({'player': {} })

    else:
        return jsonify({'player': {} })


@api.route('/edit_player', methods=['GET', 'POST'])
def edit_player():
    if request.method == 'POST':
        try:
            try:
                player_id, name, role = request.form['player_id'], request.form['name'], request.form['role']
                photo = request.files['photo']
                player_obj = PlayerHandler().edit_player_with_photo(player_id, name, role, photo)
                player = {'id': player_obj.id, 'name': player_obj.name, 'role': player_obj.role,
                            'image_name': player_obj.image_name }
                return jsonify({ 'player': player })

            except:
                player_id, name, role = request.form['player_id'], request.form['name'], request.form['role']
                player_obj = PlayerHandler().edit_player(player_id, name, role)
                player = {'id': player_obj.id, 'name': player_obj.name, 'role': player_obj.role,
                            'image_name': player_obj.image_name }
                return jsonify({ 'player': player })

        except:
            return jsonify({ 'player': {} })

    else:
        return jsonify({ 'player': {} })


@api.route('/delete_player', methods=['GET', 'POST'])
def delete_player():
    if request.method == 'POST':
        try:
            player_id = request.form['player_id']
            PlayerHandler().delete_player(player_id)
            season_obj, players_obj = PlayerHandler().get_all_players()
            season = { 'id': season_obj.id, 'name': season_obj.name, 'year': season_obj.year }
            players = [
                {'id': player.id, 'name': player.name, 'role': player.name, 'image_name': player.image_name }
                for player in players_obj
            ]
            return jsonify({ 'season': season, 'players': players })

        except:
            return jsonify({'player': {} })

    else:
        return jsonify({'player': {} })




@api.route('/get_all_matches')
def get_all_matches():
    matches_obj = MatchHandler().get_all_matches()
    matches = [
        { 'id': match.id, 'league': match.league, 'competition': match.competition, 'home': match.home, 
        'away': match.away,
        'done': match.done, 'home_score': match.home_score, 'away_score': match.away_score,
        'stadium': match.stadium, 'date': structure_date(match.date)} for match in  matches_obj
    ]
    return jsonify({ 'matches': matches })


@api.route('/add_league_match', methods=['GET', 'POST'])
def add_league_match():
    season_id = request.form['season_id']
    home_id, away_id, stadium = request.form['home_id'], request.form['away_id'], request.form['stadium']
    year, month, date = request.form['year'], request.form['month'], request.form['date']
    hour, minutes = request.form['hour'], request.form['mins']
    year, month, date, hour, minutes = int(year), int(month), int(date), int(hour), int(minutes)
    match_obj = MatchHandler().add_league_match(season_id, home_id, away_id, stadium, year, month, date,
        hour, minutes)
    match = { 'id': match_obj.id }
    return jsonify({ 'match': match })


@api.route('/add_nonleague_match', methods=['GET', 'POST'])
def add_nonleague_match():
    competition = request.form['competition']
    home, away, stadium = request.form['other_home'], request.form['other_away'], request.form['other_stadium']
    year, month, date = request.form['other_year'], request.form['other_month'], request.form['other_date']
    hour, minutes = request.form['other_hour'], request.form['other_mins']
    year, month, date, hour, minutes = int(year), int(month), int(date), int(hour), int(minutes)
    match_obj = MatchHandler().add_nonleague_match(competition, home, away, stadium, year, month,
        date, hour, minutes)
    match = { 'id': match_obj.id }
    return jsonify({ 'match': match })


@api.route('/delete_league_match', methods=['GET', 'POST'])
def delete_league_match():
    match_id = request.form['match_id']
    MatchHandler().delete_league_match(match_id)
    matches_obj = MatchHandler().get_all_matches()
    matches = [
        { 'id': match.id, 'league': match.league, 'competition': match.competition, 'home': match.home,
        'away': match.away,
        'done': match.done, 'home_score': match.home_score, 'away_score': match.away_score,
        'stadium': match.stadium, 'date': structure_date(match.date)} for match in  matches_obj
    ]
    return jsonify({ 'matches': matches })


@api.route('/delete_nonleague_match', methods=['GET', 'POST'])
def delete_nonleague_match():
    match_id = request.form['match_id']
    MatchHandler().delete_nonleague_match(match_id)
    matches_obj = MatchHandler().get_all_matches()
    matches = [
        { 'id': match.id, 'league': match.league, 'competition': match.competition, 'home': match.home,
        'away': match.away,
        'done': match.done, 'home_score': match.home_score, 'away_score': match.away_score,
        'stadium': match.stadium, 'date': structure_date(match.date)} for match in  matches_obj
    ]
    return jsonify({ 'matches': matches })


@api.route('/add_club', methods=['GET', 'POST'])
def add_club():
    if request.method == 'POST':
        try:
            name, league = request.form['name'], request.form['league']
            logo = request.files['logo']
            ClubHandler().set_club(name, league, logo)
            return jsonify({ 'success': 1 })

        except Exception as e:
            return jsonify({'fail': 1})

    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_all_clubs')
def get_all_clubs():
    try:
        clubs_obj = ClubHandler().get_all_clubs()
        clubs = [ { 'id': club.id, 'name': club.name, 'logo_name': club.logo_name,
            'league': club.league, 'num_players': len(club.players)
        } for club in clubs_obj]
        return jsonify({ 'clubs': clubs })

    except Exception as e:
        return jsonify({ 'fail': 1 })


@api.route('/get_club_by_manager', methods=['GET', 'POST'])
def get_club_by_manager():
    if request.method == 'POST':
        try:
            manager = request.form['manager']
            club_obj = ClubHandler().get_club_by_manager(manager)
            club = { 'id': club_obj.id, 'name': club_obj.name, 'league': club_obj.league }
            return jsonify({ 'club': club })

        except Exception as e:
            return jsonify({ 'fail': str(e)})

    else:
        return jsonify({ 'fail': 1 })


@api.route('/delete_club', methods=['GET', 'POST'])
def delete_club():
    if request.method == 'POST':
        try:
            club_id = request.form['club_id']
            ClubHandler().delete_club(club_id)
            table_obj = TableHandler().get_table()[1]
            table = [
                {'id': club.id, 'name': club.name, 'wins': club.wins, 'plays': club.plays, 'draws': club.draws, 
                'losses': club.losses, 'goals_for': club.goals_for, 'goals_against': club.goals_against, 
                'goal_diff': club.goal_diff, 'points': club.points }
                for club in table_obj
            ]
            return jsonify({'table': table})

        except:
            return jsonify({'data': [] })

    else:
        return jsonify({'data': [] })


'''
    Urls for getting statistcal values
'''
@api.route('/get_top_scorers')
def get_top_scorers():
    top_scorers_list = [
        { 'id': player.id, 'name': player.name, 'value': player.goals }
        for player in top_scorers()
    ]
    return jsonify({ 'top_scorers_list': top_scorers_list })


@api.route('/get_top_assists')
def get_top_assists():
    top_assists_list = [
        { 'id': player.id, 'name': player.name, 'value': player.assists }
        for player in top_assists()
    ]
    return jsonify({ 'top_assists_list': top_assists_list })


@api.route('/get_top_yellow')
def get_top_yellow():
    top_yellow_list = [
        { 'id': player.id, 'name': player.name, 'value': player.yellow_cards }
        for player in top_yellow()
    ]
    return jsonify({ 'top_yellow_list': top_yellow_list })


@api.route('/get_top_red')
def get_top_red():
    top_red_list = [
        { 'id': player.id, 'name': player.name, 'value': player.red_cards }
        for player in top_red()
    ]
    return jsonify({ 'top_red_list': top_red_list })


@api.route('/get_statistics')
def get_statistics():
    top_scorers_list = [
        { 'id': player.id, 'name': player.name, 'value': player.goals }
        for player in top_scorers()
    ]

    top_assists_list = [
        { 'id': player.id, 'name': player.name, 'value': player.assists }
        for player in top_assists()
    ] 
    
    top_yellow_list = [
        { 'id': player.id, 'name': player.name, 'value': player.yellow_cards }
        for player in top_yellow()
    ] 

    top_red_list = [
        { 'id': player.id, 'name': player.name, 'value': player.red_cards }
        for player in top_red()
    ]

    return jsonify({ 'top_scorers_list': top_scorers_list, 'top_assists_list': top_assists_list,
        'top_yellow_list': top_yellow_list, 'top_red_list': top_red_list })


'''
    urls for exact ( non cumulative ) raw statistical values
'''
@api.route('/persist_goals', methods=['GET', 'POST'])
def persist_goals():
    player_id, goals = request.form['player_id'], request.form['goals']
    PlayerHandler().persist_player_goals(player_id, goals)
    top_scorers_list = [
        { 'id': player.id, 'name': player.name, 'value': player.goals }
        for player in top_scorers()
    ]
    return jsonify({ 'top_scorers_list': top_scorers_list })


@api.route('/persist_assists', methods=['GET', 'POST'])
def persist_assists():
    player_id, assists = request.form['player_id'], request.form['assists']
    PlayerHandler().persist_player_assists(player_id, assists)
    top_assists_list = [
        { 'id': player.id, 'name': player.name, 'value': player.assists }
        for player in top_assists()
    ]
    return jsonify({ 'top_assists_list': top_assists_list })


@api.route('/persist_yellow_cards', methods=['GET', 'POST'])
def persist_yellow_cards():
    player_id, yellow_cards = request.form['player_id'], request.form['yellow_cards']
    PlayerHandler().persist_player_yellow_cards(player_id, yellow_cards)
    top_yellow_list = [
        { 'id': player.id, 'name': player.name, 'value': player.yellow_cards }
        for player in top_yellow()
    ]
    return jsonify({ 'top_yellow_list': top_yellow_list })


@api.route('/persist_red_cards', methods=['GET', 'POST'])
def persist_red_cards():
    player_id, red_cards = request.form['player_id'], request.form['red_cards']
    PlayerHandler().persist_player_red_cards(player_id, red_cards)
    top_red_list = [
        { 'id': player.id, 'name': player.name, 'value': player.red_cards }
        for player in top_red()
    ]
    return jsonify({ 'top_red_list': top_red_list })


'''
    urls for cumulative raw statistical values
'''
@api.route('/cumulate_goals', methods=['GET', 'POST'])
def cumulative_goals():
    return jsonify({'playerObj': {} })


@api.route('/cumulate_assists', methods=['GET', 'POST'])
def cumulate_assists():
    return jsonify({'playerObj': {} })


@api.route('/cumulate_yellow_cards', methods=['GET', 'POST'])
def cumulate_yellow_cards():
    return jsonify({'playerObj': {} })


@api.route('/cumulate_red_cards', methods=['GET', 'POST'])
def cumulate_red_cards():
    return jsonify({'playerObj': {} })

@api.route('/get_feedback_comment')
def get_feedback_comment():
    try:
        feedback_obj = FeedbackHandler().get_feedback_comment()
        feedback = { 'id': feedback_obj.id, 'body': feedback_obj.body }
        print('here')
        return jsonify({ 'feedback': feedback })

    except:
        return jsonify({ 'feedback': {} })

@api.route('/update_feedback', methods=['GET', 'POST'])
def update_feedback():
    if request.method == 'POST':
        try:
            feedback_id, feedback_body = request.form['feedback_id'], request.form['feedback_body']
            feedback_obj = FeedbackHandler().update_feedback(feedback_id, feedback_body)
            feedback = { 'id': feedback_obj.id, 'body': feedback_obj.body }
            return jsonify({ 'feedback': feedback })

        except:
            return jsonify({ 'feedback': {} })

    else:
        return jsonify({ 'feedback': {} })


@api.route('/set_new_feedback', methods=['GET', 'POST'])
def set_new_feedback():
    if request.method == 'POST':
        try:
            feedback_body = request.form['feedback_body']
            feedback_obj = FeedbackHandler().set_feedback(feedback_body)
            feedback = { 'id': feedback_obj.id, 'body': feedback_obj.body }
            return jsonify({ 'feedback': feedback })

        except:
            return jsonify({ 'feedback': {} })

    else:
        return jsonify({ 'feedback': {} })
