from GAME_PLANNER_LOGIC import *
import streamlit as st
import pandas as pd

st.title("POLO GAME PLANNER")
st.image("polo image.jpeg")

st.sidebar.header("ADD NEW PLAYER OR USE PREDEFINED LIST")

use_predefined = st.sidebar.checkbox("Use Predefined Player List")

if use_predefined:
    predefined_players = [ 
        Player("SSS", 8, 4, "pro", "6:00"),
        Player("VSS", 2, -2, "amateur", "6:00"),
        Player("RS", 2, -1, "amateur", "6:30"),
        Player("SID", 8, 4, "pro", "6:00"),
        Player("RANSHAY", 6, 1, "amateur", "6:00"),
        Player("AQ", 2, -2, "patron", "5:30"),
        Player("SA", 8, 2, "pro", "6:00"),
        Player("KI", 8, 1, "pro", "5:30"),
        Player("MS", 2, 0, "amateur", "6:00"),
        Player("GS", 2, -2, "amateur", "5:30"),
        Player("AM", 2, 0, "amateur", "6:30"),
        Player("MKS", 2, -1, "amateur", "6:00")
    ]
    if 'players' not in st.session_state:
        st.session_state.players = predefined_players
    st.sidebar.success("Using predefined player list")
else:
    name = st.sidebar.text_input("Name")
    chakkus = st.sidebar.number_input("Chakkus", min_value=0, value=2)
    handicap = st.sidebar.number_input("Handicap", min_value=-2, max_value=6, value=0)
    role = st.sidebar.selectbox("Role", ["patron", "pro", "amateur"])
    arrival_time = st.sidebar.selectbox("Arrival Time", ["5:30", "6:00", "6:30", "7:00"])
    preferred_teammates = st.sidebar.text_input("Preferred Teammates (comma separated)").split(",")
    avoid_teammates = st.sidebar.text_input("Avoid Teammates (comma separated)").split(",")

    if st.sidebar.button("Add Player"):
        new_player = Player(name, chakkus, handicap, role, arrival_time, preferred_teammates, avoid_teammates)
        if 'players' not in st.session_state:
            st.session_state.players = []
        st.session_state.players.append(new_player)
        st.sidebar.success(f"Added {name}")

if 'players' in st.session_state:
    players = st.session_state.players

    st.subheader("Player List")
    for player in players:
        st.write(f"{player.name}, Chakkus: {player.chakkus}, Handicap: {player.handicap}, Role: {player.role}, Arrival: {player.arrival_time}")

    arrival_times = ["5:30", "6:00", "6:30", "7:00"]
    
    players = prioritize_players(players)
    player_queue = deque(players)
    
    for time in arrival_times:
        st.subheader(f"Time: {time}")
        arrived_players = []
        while player_queue and player_queue[0].arrival_time <= time:
            arrived_players.append(player_queue.popleft())

        st.write(f"Arrived Players at {time}: {[p.name for p in arrived_players]}")

        arrived_players = filter_active_players(arrived_players)

        st.write(f"Active Players at {time}: {[p.name for p in arrived_players]}")

        if len(arrived_players) >= 4:
            team1, team2 = form_teams(arrived_players)
            if team1 and team2:
                st.write("Teams formed:")

                team1_names = [p.name for p in team1]
                team2_names = [p.name for p in team2]

                # Create a DataFrame for display
                team_data = {
                    "Team 1": team1_names,
                    "Team 2": team2_names
                }
                max_length = max(len(team1_names), len(team2_names))
                team_data["Team 1"].extend([""] * (max_length - len(team1_names)))
                team_data["Team 2"].extend([""] * (max_length - len(team2_names)))

                team_df = pd.DataFrame(team_data)
                st.table(team_df)

                update_player_chakkus(team1 + team2, 2)  # EACH GAME HAVING 2 CHAKKUS.
            else:
                st.write("Not enough players to form balanced teams.")
        else:
            st.write("Not enough players to start a game.")

        players = prioritize_players(players)
        player_queue = deque(players)
