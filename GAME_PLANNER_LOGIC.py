from itertools import combinations
from collections import deque

class Player:
    def __init__(self, name, chakkus, handicap, role, arrival_time, preferred_teammates=None, avoid_teammates=None):
        self.name = name
        self.handicap = handicap
        self.chakkus = chakkus
        self.role = role
        self.arrival_time = arrival_time
        self.preferred_teammates = preferred_teammates or []
        self.avoid_teammates = avoid_teammates or []

def prioritize_players(players):
    """HANDLE THE PRIORITY LEVEL OF PLAYERS. 
    GIVEN PRIORITY : PATRON > PRO > NOOB / AMATEUR. .""" 
    role_priority = {'patron': 1, 'pro': 2, 'amateur': 3}
    return sorted(players, key=lambda x: (x.arrival_time, role_priority[x.role]))

def can_form_team(players, team_size):
    """CHECK IF TEAM FORMATION IS POSSIBLE."""
    return len(players) >= team_size * 2

def handicap_difference(team1, team2):
    """CALCULATE HANDICAP OF TEAMS."""
#     print(abs(sum(player.handicap for player in team1) - sum(player.handicap for player in team2)))
    return abs(sum(player.handicap for player in team1) - sum(player.handicap for player in team2)) <= 2 

def validate_preferences(team, player):
    """CHECK IF ALL PREFERENCES ARE FULFILLED. """
    for teammate in player.preferred_teammates:
        if teammate not in [p.name for p in team]:
            return False
    for avoid in player.avoid_teammates:
        if avoid in [p.name for p in team]:
            return False
    return True

def form_teams(players): 
    """DO ALL THE P & C TO OBTAIN POSSIBLE TEAM FORMATIONS. """
    players = prioritize_players(players)
    for team_size in range(4, 1, -1):  
        if can_form_team(players, team_size):
            for team_combination in combinations(players, team_size):
                team1 = list(team_combination)
                remaining_players = [player for player in players if player not in team1]
                for remaining_team_combination in combinations(remaining_players, team_size):
                    team2 = list(remaining_team_combination)
                    if handicap_difference(team1, team2) and all(validate_preferences(team1, p) for p in team1) and all(validate_preferences(team2, p) for p in team2):
                        return team1, team2
    return None, None

def update_player_chakkus(players, played_chakkus): 
    """UPDATE PLAYER CHAKKURS AFTER EVERY MATCH. """
    for player in players:
        player.chakkus -= played_chakkus

def filter_active_players(players): 
    """FIND PLAYERS WHOSE STILL HAVE CHAKKURS LEFT."""
    return [player for player in players if player.chakkus > 0]