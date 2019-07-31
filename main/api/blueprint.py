from flask import Blueprint, jsonify, redirect, url_for, request
from main.app import app
from main.api.access_control.account_manager import AccountSet, ScoutAccount, ManagerAccount
from main.api.data.generic import Generic
from main.api.data.custom import Custom
from main.api.access_control.logger import Logger
from main.api.data.data import *
from main.api.data.structured_date import structure_date
from main.api.data.player_performance import SetPerformance
from main.api.data.stat import Stat


api = Blueprint('api', __name__, static_folder='uploads')

@api.route('/')
def index():
    return jsonify({ 'state': {} })

@api.route('/create_manager_account', methods=['GET', 'POST'])
def create_manager_account():
    invalid_email = 'INVALID_EMAIL'
    invalid_username = 'INVALID_USERNAME'
    all_valid = 'TRUE'
    error = 'ERROR'

    try:
        email, first_name, last_name = request.form['email'], request.form['first_name'], request.form['last_name']
        club_id, password = request.form['club_id'], request.form['password']
        _account = ManagerAccount(club_id, first_name, last_name, email, password)
        if not _account.is_manager_email_valid():
            return jsonify({ 'validity': invalid_email })

        else:
            _account.send_verification()
            return jsonify({ 'success': 1 })

    except Exception as e:
        return jsonify({ 'fail': 1 })


@api.route('/create_scout_account', methods=['GET', 'POST'])
def create_scout_account():
    invalid_email = 'INVALID_EMAIL'
    invalid_username = 'INVALID_USERNAME'
    all_valid = 'TRUE'
    error = 'ERROR'

    try:
        first_name, last_name = request.form['first_name'], request.form['last_name']
        email, password = request.form['email'], request.form['password']
        _account = ScoutAccount(first_name=first_name, last_name=last_name, email=email,
                password=password
            )
        if not _account.is_scout_email_valid():
            return jsonify({ 'validity': invalid_email })

        else:
            _account.send_verification()
            return jsonify({ 'success': 1 })

    except Exception as e:
        return jsonify({ 'fail': 1 })


@api.route('/verify_manager_code', methods=['GET', 'POST'])
def verify_manager_code():
    code = request.form['code']
    account_set = AccountSet()
    returnCode = account_set.is_manager_code_valid(code)

    if returnCode == 0:
        return jsonify({'code': 0})

    elif returnCode == 1:
        user_id = account_set.get_user_id()
        return jsonify({'code': 1, 'user_id': user_id })

    elif returnCode == -1:
        return jsonify({'code': -1 })


@api.route('/verify_scout_code', methods=['GET', 'POST'])
def verify_scout_code():
    code = request.form['code']
    account_set = AccountSet()
    returnCode = account_set.is_scout_code_valid(code)

    if returnCode == 0:
        return jsonify({'code': 0})

    elif returnCode == 1:
        user_id = account_set.get_user_id()
        return jsonify({'code': 1, 'user_id': user_id })

    elif returnCode == -1:
        return jsonify({'code': -1 })


@api.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        try:
            email, password = request.form['email'], request.form['password']
            if Logger().is_manager(email):
                manager = Logger().login_manager(email, password)
                return jsonify({ 'user_id': manager['id'] })

            else:
                return jsonify({ 'user_id': '' })

        except Exception as e:
            return jsonify({ 'fail': 1 })
    else:
        return jsonify({ 'fail': 1 })


@api.route('/login_scout', methods=['GET', 'POST'])
def login_scout():
    if request.method == 'POST':
        try:
            email, password = request.form['email'], request.form['password']
            if Logger().is_scout(email):
                scout = Logger().login_scout(email, password)
                return jsonify({ 'user_id': scout['id'] })

            else:
                return jsonify({ 'fail': 1 })

        except Exception as e:
            return jsonify({ 'fail': 1 })
    else:
        return jsonify({ 'fail': 1 })


@api.route('/logout', methods=['GET', 'POST'])
def logout():
    username = request.form['username']
    Logger().logout(username)
    return jsonify({ 'success': 1 })
    if request.method == 'POST':
        try:
            username = request.form['username']
            Logger().logout(username)
            return jsonify({ 'success': 1 })
        except Exception as e:
            return jsonify({ 'fail': str(e) })
    else:
        return jsonify({ 'fail': 1 })


@api.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        try:
            user_id, user_status = int(request.form['user_id']), request.form['user_status']
            Logger().delete_account(user_id, user_status)
            return jsonify({ 'success': True })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/update_photo', methods=['GET', 'POST'])
def update_photo():
    if request.method == 'POST':
        try:
            user_id, user_status = request.form['user_id'], request.form['user_status']
            image = request.files['image']

            if user_status == 'scout':
                ScoutHandler().update_photo(scout_id=user_id, image=image )
                user = ScoutHandler().get_scout(user_id)
                return jsonify({ 'user': user })

            else:
                ManagerHandler().update_photo(manager_id=user_id, image=image)
                user = ManagerHandler().get_manager(user_id)
                return jsonify({ 'user': user })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/get_all_managers')
def get_all_managers():
    try:
        managers = ManagerHandler().get_all_managers_with_clubs()
        return jsonify({ 'managers': managers })

    except:
        return jsonify({ 'fail': 1 })


@api.route('/get_scout', methods=['GET', 'POST'])
def get_scout():
    if request.method == 'POST':
        try:
            scout_id = request.form['scout_id']
            scout = ScoutHandler().get_scout(scout_id)
            return jsonify({ 'user': scout })

        except:
            return jsonify({ 'fail': 1})

    else:
        return jsonify({'fail': 1})


@api.route('/get_manager', methods=['GET', 'POST'])
def get_manager():
    if request.method == 'POST':
        try:
            manager_id = request.form['manager_id']
            manager = ManagerHandler().get_manager(manager_id)
            return jsonify({ 'user': manager })

        except:
            return jsonify({ 'fail': 1})

    else:
        return jsonify({'fail': 1})


@api.route('/get_all_scouts', methods=['GET', 'POST'])
def get_all_scouts():
    if request.method == 'POST':
        try:
            user_id, user_status = int(request.form['user_id']), request.form['user_status']
            scouts = ScoutHandler().filter_scouts(user_id, user_status)
            return jsonify({ 'scouts': scouts })

        except:
            return jsonify({ 'fail': 1 })

    else:
        return jsonify({ 'fail': 1 })


@api.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        try: 
            first_name, last_name = request.form['first_name'], request.form['last_name']
            role, year, month = request.form['role'], request.form['year'], request.form['month']
            date, club_name = request.form['date'], request.form['club_name']
            photo = request.files['photo']
            player_obj = PlayerHandler().set_player(club_name, first_name, last_name, role, photo, year, month, date)
            return jsonify({ 'success': True, 'player_id': player_obj.id })
        except Exception as e:
            return jsonify({ 'fail': str(e) })
    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_custom_players', methods=['GET', 'POST'])
def get_custom_players():
    if request.method == 'POST':
        try:
            username = request.form['username']
            custom = Custom(username)
            players = custom.get_custom_players()
            return jsonify({ 'players': players })

        except Exception as e:
            return jsonify({ 'fail': str(e) })

    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_goal_keepers')
def get_goal_keepers():
    players = PlayerHandler().get_goal_keepers()
    return jsonify({ 'players': players })

@api.route('/get_defenders')
def get_defenders():
    players = PlayerHandler().get_defenders()
    return jsonify({ 'players': players })


@api.route('/get_midfielders')
def get_midfielders():
    players = PlayerHandler().get_midfielders()
    return jsonify({ 'players': players })


@api.route('/get_forwards')
def get_forwards():
    players = PlayerHandler().get_forwards()
    return jsonify({ 'players': players })



@api.route('/get_generic_players', methods=['GET', 'POST'])
def get_generic_players():
    if request.method == 'POST':
        try:
            generic = Generic()
            players = generic.get_generic_players()
            return jsonify({ 'players': players })

        except Exception as e:
            return jsonify({ 'fail': str(e) })

    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_my_players', methods=['GET', 'POST'])
def get_my_players():
    
    if request.method == 'POST':
        try:
            manager_id = int(request.form['manager_id'])
            club_name, players = PlayerHandler().get_my_players(manager_id)
            return jsonify({ 'players': players, 'club_name': club_name })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/get_player', methods=['GET', 'POST'])
def get_player():
    if request.method == 'POST':
        try:
            player_id = request.form['player_id']
            player = PlayerHandler().get_player(player_id)
            return jsonify({ 'player': player })

        except:
            return jsonify({'fail': 1 })

    else:
        return jsonify({'fail': 1 })


@api.route('/update_player', methods=['GET', 'POST'])
def update_player():
    if request.method == 'POST':
        try:
            player_id, role = int(request.form['player_id']), request.form['role']
            first_name, last_name = request.form['first_name'], request.form['last_name']
            player = PlayerHandler().update_player(player_id=player_id, first_name=first_name,
                    last_name=last_name, role=role
                )
            return jsonify({ 'player_id': player.id })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/update_player_with_photo', methods=['GET', 'POST'])
def update_player_with_photo():
    if request.method == 'POST':
        try:
            player_id, role = int(request.form['player_id']), request.form['role']
            first_name, last_name = request.form['first_name'], request.form['last_name']
            photo = request.files['photo']
            player = PlayerHandler().update_player_with_photo(player_id=player_id, first_name=first_name,
                    last_name=last_name, role=role, photo=photo
                )
            return jsonify({ 'player_id': player.id })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })




@api.route('/delete_player', methods=['GET', 'POST'])
def delete_player():
    if request.method == 'POST':
        try:
            player_id = int(request.form['player_id'])
            player = PlayerHandler().delete_player(player_id)
            return jsonify({ 'player_id': player.id })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/get_player_with_stats', methods=['GET', 'POST'])
def get_player_with_stats():   
    if request.method == 'POST':
        try:
            player_id = request.form['player_id']
            stat = Stat(player_id=player_id)
            player = stat.get_player_stats()
            return jsonify({ 'player': player })
        except Exception as e:
            return jsonify({ 'fail': 1 })

    else:
        return jsonify({ 'fail': 1 })


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


@api.route('/add_club', methods=['GET', 'POST'])
def add_club():
    if request.method == 'POST':
        try:
            name, league = request.form['name'], request.form['league']
            logo = request.files['logo']
            club = ClubHandler().set_club(name, league, logo)
            return jsonify({ 'success': 1, 'club_id': club.id })

        except Exception as e:
            return jsonify({'fail': 1})

    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_all_clubs')
def get_all_clubs():
    try:
        clubs_obj = ClubHandler().get_all_clubs()
        clubs = [ { 'id': club.id, 'name': club.name, 'logo_name': club.logo_name,
            'league': club.league, 'ave_rating': round(club.ave_rating * 100), 'num_players': len(club.players)
        } for club in clubs_obj]
        return jsonify({ 'clubs': clubs })

    except Exception as e:
        return jsonify({ 'fail': 1 })


@api.route('/get_clubs_without_managers')
def get_clubs_without_managers():
    try:
        clubs = ClubHandler().get_clubs_without_managers()
        return jsonify({ 'clubs': clubs })
    except Exception as e:
        return jsonify({ 'fail': 1 })


@api.route('/get_detailed_club', methods=['GET', 'POST'])
def get_detailed_club():
    if request.method == 'POST':
        try:
            club_id = request.form['club_id']
            club = ClubHandler().get_detailed_club(club_id)
            return jsonify({ 'club': club })

        except Exception as e:
            return jsonify({ 'fail': True })

    else:
        return jsonify({ 'fail': True })


@api.route('/get_club_by_manager', methods=['GET', 'POST'])
def get_club_by_manager():
    if request.method == 'POST':
        try:
            manager_id = int(request.form['manager_id'])
            club = ClubHandler().get_club_by_manager(manager_id)
            return jsonify({ 'club': club })

        except Exception as e:
            return jsonify({ 'fail': str(e)})

    else:
        return jsonify({ 'fail': 1 })


@api.route('/get_clubs_with_players')
def get_clubs_with_players():
    try:
        clubs = ClubHandler().get_clubs_with_players()
        return jsonify({ 'clubs': clubs })

    except Exception as e:
        return jsonify({ 'fail': 1})



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


@api.route('/add_stats', methods=['GET', 'POST'])
def add_stats():
    if request.method == 'POST':
        player_id, player_status = request.form['player_id'], request.form['player_status']
        home_id, away_id = request.form['home_id'], request.form['away_id']
        home_score, away_score = request.form['home_score'], request.form['away_score']

        shots_for, shots_for_ontarget = request.form['shots_for'], request.form['shots_for_ontarget']
        goals_for, assists = request.form['goals_for'], request.form['assists']
        crosses, crosses_successful = request.form['crosses'], request.form['crosses_successful']

        interceptions, clearances = request.form['interceptions'], request.form['clearances']
        tackles, fouls = request.form['tackles'], request.form['fouls']
        shots_against, shots_blocked = request.form['shots_against'], request.form['shots_against_blocked']
        goals_against, saves = request.form['goals_against'], request.form['saves']
        set_performance = SetPerformance(player_id=player_id, player_status=player_status,
                home_id=home_id, away_id=away_id, home_score=home_score, away_score=away_score,
                shots_for=shots_for, shots_for_ontarget=shots_for_ontarget,
                goals_for=goals_for, assists=assists, crosses=crosses,
                crosses_successful=crosses_successful, interceptions=interceptions,
                clearances=clearances, tackles=tackles, fouls=fouls, shots_against=shots_against,
                shots_blocked=shots_blocked, goals_against=goals_against, saves=saves
            )
        return jsonify({ 'success': True, 'player_id': player_id })

    else:
        return jsonify({ 'success': False })

