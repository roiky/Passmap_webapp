import streamlit as st
import soccerdata as sd
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import logging
import io
import numpy as np

st.set_page_config(page_title="⚽ Tactical Dashboard", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CUSTOM LOG HANDLER FOR STREAMLIT PROGRESS
# ==========================================
class StreamlitLogHandler(logging.Handler):
    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder

    def emit(self, record):
        msg = self.format(record)
        self.placeholder.info(f"⏳ **Fetching Data:** {msg}")

# ==========================================
# CONFIGURATION & COLORS
# ==========================================
TEAM_COLORS = {
 'Arsenal': '#ef0107', 'Aston Villa': '#95bfe5', 'Bournemouth': '#da291c', 'Brentford': '#e30613',
 'Brighton': '#0057b8', 'Chelsea': '#034694', 'Crystal Palace': '#1b458f', 'Everton': '#003399',
 'Fulham': '#ffffff', 'Burnley': '#6C1D45', 'Leicester': '#003090', 'Liverpool': '#c8102e',
 'Manchester City': '#6caddf', 'Man City': '#6caddf', 'Manchester United': '#da291c', 'Man Utd': '#da291c',
 'Newcastle': '#241f20', 'Nottingham Forest': '#dd0000', 'Southampton': '#d71920', 'Tottenham': '#ffffff','Tottenham Hotspur': '#ffffff',
 'West Ham': '#7a263a','West Ham United': '#7a263a', 'Wolves': '#fdb913', 'Sunderland': '#d71920',
 'Alaves': '#005599', 'Athletic Club': '#ff0000', 'Atletico Madrid': '#cb3524', 'Barcelona': '#a50044',
 'Celta Vigo': '#8ec0e4', 'Espanyol': '#00529f', 'Getafe': '#0000ab', 'Girona': '#e23237',
 'Las Palmas': '#ffe600', 'Leganes': '#005599', 'Mallorca': '#e20612', 'Osasuna': '#ab1a2d',
 'Real Betis': '#00965e', 'Real Madrid': '#ffffff', 'Real Sociedad': '#0067b1', 'Sevilla': '#f0f0f0',
 'Valencia': '#ffffff', 'Valladolid': '#6d2d91', 'Villarreal': '#ffe600', 'Rayo Vallecano': '#ffffff',
 'AC Milan': '#ff2e2e', 'Atalanta': '#1e90ff', 'Bologna': '#162b4c', 'Cagliari': '#002350',
 'Como': '#3498db', 'Empoli': '#00579c', 'Fiorentina': '#4b0082', 'Genoa': '#a61111',
 'Inter': '#0053a0', 'Juventus': '#f0f0f0', 'Lazio': '#87ceeb', 'Lecce': '#ffed00',
 'Monza': '#e30613', 'Napoli': '#00bfff', 'Parma': '#ffffff', 'AS Roma': '#8b0000',
 'Torino': '#5a1313', 'Udinese': '#ffffff', 'Venezia': '#006633', 'Verona': '#ffd700',
 'Augsburg': '#ba3733', 'Bayer Leverkusen': '#e32221', 'Bayern Munich': '#dc052d','Bayern': '#dc052d','Bayern München': '#dc052d', 'Bochum': '#005ca9',
 'Borussia Dortmund': '#fde100', 'Borussia M.Gladbach': '#ffffff', 'Eintracht Frankfurt': '#ff0000', 
 'Freiburg': '#d11a1a', 'Heidenheim': '#e2001a', 'Hoffenheim': '#1c63b7', 'Holstein Kiel': '#004a99',
 'Mainz': '#c3121d', 'RB Leipzig': '#ffffff','RBL': '#ffffff', 'St. Pauli': '#6d4c41', 'Stuttgart': '#ffffff', 
 'Union Berlin': '#ff0000', 'Werder Bremen': '#1d9053', 'Wolfsburg': '#65ae7c',
 'Angers': '#ffffff', 'Auxerre': '#ffffff', 'Brest': '#e5001a', 'Le Havre': '#10203f',
 'Lens': '#ffcc00', 'Lille': '#e01e13', 'Lyon': '#ffffff', 'Marseille': '#2faee0',
 'Monaco': '#ff0000', 'Montpellier': '#003366', 'Nantes': '#fdf200', 'Nice': '#d40000',
 'Paris Saint-Germain': '#004170','PSG': '#004170', 'Reims': '#d71920', 'Rennes': '#e40032', 'Saint-Etienne': '#009344',
 'Strasbourg': '#0097d7', 'Toulouse': '#4c2471',
 'Maccabi Tel Aviv': '#f6c400',     'Maccabi Haifa': '#008f43',     'Hapoel Beer Sheva': '#d40000', 
 'Beitar Jerusalem': '#fff200',    'Hapoel Haifa': '#d40000',    'Hapoel Tel Aviv': '#d40000',    
 'Maccabi Netanya': '#ffff00',    'Bnei Sakhnin': '#d40000',    'Ashdod': '#d40000', 
 'Hapoel Jerusalem': '#d40000',     'Maccabi Petah Tikva': '#0066cc',    'Hapoel Hadera': '#d40000',
 'Maccabi Bnei Reineh': '#f6c400',    'Ironi Tiberias': '#0066cc',    'Ironi Kiryat Shmona': '#0066cc',
 'Benfica': '#e30613', 'Porto': '#004289', 'Sporting CP': '#008000',
 'Ajax': '#d2122e', 'PSV': '#ff0000', 'Feyenoord': '#ff0000',
 'Celtic': '#008000', 'Galatasaray': '#a32638'
}
DEFAULT_COLORS = ['#ff0000', '#0053a0'] 

st.title("⚽ Tactical Dashboard")
st.markdown("Generate beautiful passing networks, shot maps, and heatmaps using WhoScored data.")

# ==========================================
# DATA FETCHING FUNCTIONS
# ==========================================
def fetch_events(match_id, league, season, log_placeholder):
    handler = StreamlitLogHandler(log_placeholder)
    handler.setFormatter(logging.Formatter('%(message)s'))
    
    sd_logger = logging.getLogger('soccerdata')
    sd_logger.setLevel(logging.INFO)
    sd_logger.addHandler(handler)
    
    try:
        ws = sd.WhoScored(leagues=[league], seasons=season)
        events = ws.read_events(match_id=[int(match_id)])
        
        sd_logger.removeHandler(handler)
        return events
    except Exception as e:
        sd_logger.removeHandler(handler)
        st.error(f"Error fetching events: {e}")
        return None

# ==========================================
# SIDEBAR UI
# ==========================================
with st.sidebar:
    st.header("1. Match Selection")
    league = st.selectbox("League", [
        'ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 
        'GER-Bundesliga', 'ITA-Serie A', 'INT-UEFA Champions League', 
        'INT-Europa League', 'ISR-Ligat HaAl'
    ], index=1)
    season = st.text_input("Season", "2526")
    match_id = st.text_input("Match ID (WhoScored)", "1914207")
    
    st.divider()
    st.header("2. Settings & Filters")
    time_range = st.slider("Time Range (Minutes)", 0, 120, (0, 90))
    theme = st.selectbox("Map Theme", ["Dark", "Light"])
    node_scale = st.slider("Node Size Scale", 0.5, 3.0, 1.0)
    arrow_scale = st.slider("Arrow Thickness Scale", 0.1, 1.0, 0.4)
    
    generate_btn = st.button("Generate Dashboard", type="primary", use_container_width=True)

# Helper function to save plot to memory
def get_image_download_link(fig, filename="map.png"):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)
    buf.seek(0)
    return buf

# ==========================================
# MAIN EXECUTION
# ==========================================
if generate_btn:
    if not match_id:
        st.error("Please enter a Match ID.")
    else:
        log_placeholder = st.empty()
        
        with st.spinner("Processing match data..."):
            events = fetch_events(match_id, league, season, log_placeholder)
            log_placeholder.empty()
            
            if events is None or events.empty:
                st.error("Error: Could not find event data for this match ID. It may not have detailed data yet.")
            else:
                # Setup Theme Colors
                bg_color = '#1a1a1a' if theme == "Dark" else '#f4f4f4'
                line_color = '#cfcfcf' if theme == "Dark" else '#121212'
                text_color = 'white' if theme == "Dark" else 'black'
                
                events['team'] = events['team'].astype(str).str.strip()
                unique_teams_in_data = list(events['team'].unique())

                if len(unique_teams_in_data) < 2:
                    st.error("Error: Less than 2 teams found in data.")
                else:
                    game_header = events.index.get_level_values('game')[0]
                    match_date = game_header.split(' ')[0]
                    teams_part = game_header.replace(match_date + " ", "")

                    pos0 = teams_part.find(unique_teams_in_data[0])
                    pos1 = teams_part.find(unique_teams_in_data[1])

                    if pos0 < pos1:
                        home_team, away_team = unique_teams_in_data[0], unique_teams_in_data[1]
                    else:
                        home_team, away_team = unique_teams_in_data[1], unique_teams_in_data[0]

                    # Basic filtering for total match score before time filter
                    home_score_full = len(events[(events['team'] == home_team) & (events['is_goal'] == True)])
                    away_score_full = len(events[(events['team'] == away_team) & (events['is_goal'] == True)])
                    st.success(f"**Match Identified:** {home_team} {home_score_full} - {away_score_full} {away_team} ({match_date})")

                    # Apply time filter
                    filtered_events = events[(events['minute'] >= time_range[0]) & (events['minute'] <= time_range[1])].copy()
                    
                    if filtered_events.empty:
                        st.warning("No events found in the selected time range.")
                        st.stop()

                    filtered_events['pass_recipient'] = filtered_events['player'].shift(-1)
                    
                    # Create Tabs
                    tab_net, tab_shot, tab_heat, tab_stats = st.tabs(["Passing Networks", "Shot Maps", "Heatmaps", "Match Stats"])
                    
                    teams = [home_team, away_team]
                    
                    # -----------------------------------------------------
                    # TAB 1: PASSING NETWORKS
                    # -----------------------------------------------------
                    with tab_net:
                        cols = st.columns(2)
                        for i, team in enumerate(teams):
                            team_events = filtered_events[filtered_events['team'] == team].copy()
                            starters = team_events.groupby('player')['minute'].min().nsmallest(11).index.tolist()
                            team_events_starters = team_events[team_events['player'].isin(starters)]
                            
                            avg_locs = team_events_starters.groupby(['player', 'player_id']).agg({'x': 'mean', 'y': 'mean'}).reset_index()
                            
                            team_passes = team_events_starters[
                                (team_events_starters['type'] == 'Pass') & 
                                (team_events_starters['outcome_type'] == 'Successful') &
                                (team_events_starters['pass_recipient'].isin(starters))
                            ].copy()
                            
                            if team_passes.empty:
                                cols[i].warning(f"No successful passes found for {team} in this timeframe.")
                                continue

                            pass_vol = team_passes.groupby('player').size().reset_index(name='pass_count')
                            nodes = pd.merge(avg_locs, pass_vol, on='player')
                            
                            pair_stats = team_passes.groupby(['player', 'pass_recipient']).size().reset_index(name='pair_count')
                            top_3 = pair_stats.sort_values(['player', 'pair_count'], ascending=[True, False]).groupby('player').head(3)

                            fig, ax = plt.subplots(figsize=(10, 7))
                            fig.set_facecolor(bg_color)
                            
                            pitch = Pitch(pitch_type='opta', pitch_color=bg_color, line_color=line_color)
                            pitch.draw(ax=ax)
                            
                            for _, row in top_3.iterrows():
                                p = nodes[nodes['player'] == row['player']]
                                r = nodes[nodes['player'] == row['pass_recipient']]
                                if not p.empty and not r.empty:
                                    ax.annotate("", xy=(r.x.values[0], r.y.values[0]), xytext=(p.x.values[0], p.y.values[0]),
                                                arrowprops=dict(arrowstyle="-|>", color=text_color, alpha=0.4, shrinkA=8, shrinkB=8, 
                                                                lw=row['pair_count'] * arrow_scale, connectionstyle="arc3,rad=0.1"))

                            t_color = TEAM_COLORS.get(team, DEFAULT_COLORS[i])
                            pitch.scatter(nodes.x, nodes.y, s=nodes.pass_count * 15 * node_scale, color=t_color, edgecolors=text_color, linewidth=1.5, ax=ax, zorder=2)
                            
                            for _, row in nodes.iterrows():
                                pitch.annotate(row.player.split(' ')[-1], xy=(row.x, row.y + 4), c=text_color, size=9, weight='bold', va='center', ha='center', ax=ax)
                                
                            ax.set_title(f"{team} Tactical Network\n{time_range[0]}'-{time_range[1]}'", color=text_color, fontsize=16, pad=10)
                            
                            cols[i].pyplot(fig)
                            img_buf = get_image_download_link(fig)
                            cols[i].download_button(label=f"Download {team} Network", data=img_buf, file_name=f"{team}_network.png", mime="image/png", use_container_width=True)
                            plt.close(fig)

                    # -----------------------------------------------------
                    # TAB 2: SHOT MAPS
                    # -----------------------------------------------------
                    with tab_shot:
                        cols = st.columns(2)
                        for i, team in enumerate(teams):
                            team_events = filtered_events[filtered_events['team'] == team]
                            
                            # Identify shots
                            if 'is_shot' in team_events.columns:
                                shots = team_events[team_events['is_shot'] == True]
                            else:
                                shots = team_events[team_events['type'].isin(['SavedShot', 'MissedShots', 'Goal', 'ShotOnPost'])]

                            fig, ax = plt.subplots(figsize=(10, 7))
                            fig.set_facecolor(bg_color)
                            pitch = Pitch(pitch_type='opta', pitch_color=bg_color, line_color=line_color, half=True)
                            pitch.draw(ax=ax)
                            
                            if shots.empty:
                                cols[i].info(f"No shots recorded for {team} in this timeframe.")
                            else:
                                goals = shots[shots['is_goal'] == True]
                                non_goals = shots[shots['is_goal'] != True]
                                
                                t_color = TEAM_COLORS.get(team, DEFAULT_COLORS[i])
                                
                                # Plot non-goals
                                pitch.scatter(non_goals.x, non_goals.y, s=100, color=bg_color, edgecolors=t_color, linewidth=2, alpha=0.7, marker='o', ax=ax, label="Shot")
                                # Plot goals
                                pitch.scatter(goals.x, goals.y, s=200, color=t_color, edgecolors='gold', linewidth=2, marker='*', ax=ax, label="Goal")
                                
                                ax.legend(loc='lower left', frameon=False, labelcolor=text_color)
                            
                            ax.set_title(f"{team} Shots\n{time_range[0]}'-{time_range[1]}'", color=text_color, fontsize=16, pad=10)
                            cols[i].pyplot(fig)
                            img_buf = get_image_download_link(fig)
                            cols[i].download_button(label=f"Download {team} Shots", data=img_buf, file_name=f"{team}_shots.png", mime="image/png", use_container_width=True)
                            plt.close(fig)

                    # -----------------------------------------------------
                    # TAB 3: HEATMAPS
                    # -----------------------------------------------------
                    with tab_heat:
                        cols = st.columns(2)
                        for i, team in enumerate(teams):
                            team_events = filtered_events[filtered_events['team'] == team]
                            
                            fig, ax = plt.subplots(figsize=(10, 7))
                            fig.set_facecolor(bg_color)
                            pitch = Pitch(pitch_type='opta', pitch_color=bg_color, line_color=line_color)
                            pitch.draw(ax=ax)
                            
                            if not team_events.empty:
                                try:
                                    pitch.kdeplot(team_events.x, team_events.y, ax=ax, fill=True, cmap='plasma', n_levels=100, alpha=0.6)
                                except Exception as e:
                                    # Fallback if seaborn/scipy is missing
                                    pitch.hexbin(team_events.x, team_events.y, ax=ax, edgecolors=bg_color, gridsize=(10, 5), cmap='plasma', alpha=0.8)
                            
                            ax.set_title(f"{team} Action Heatmap\n{time_range[0]}'-{time_range[1]}'", color=text_color, fontsize=16, pad=10)
                            cols[i].pyplot(fig)
                            img_buf = get_image_download_link(fig)
                            cols[i].download_button(label=f"Download {team} Heatmap", data=img_buf, file_name=f"{team}_heatmap.png", mime="image/png", use_container_width=True)
                            plt.close(fig)

                    # -----------------------------------------------------
                    # TAB 4: MATCH STATS
                    # -----------------------------------------------------
                    with tab_stats:
                        st.subheader(f"Match Statistics ({time_range[0]}'-{time_range[1]}')")
                        
                        stats_data = []
                        for team in teams:
                            team_events = filtered_events[filtered_events['team'] == team]
                            
                            passes = team_events[team_events['type'] == 'Pass']
                            total_passes = len(passes)
                            succ_passes = len(passes[passes['outcome_type'] == 'Successful'])
                            pass_pct = round((succ_passes / total_passes * 100), 1) if total_passes > 0 else 0
                            
                            if 'is_shot' in team_events.columns:
                                shots = len(team_events[team_events['is_shot'] == True])
                            else:
                                shots = len(team_events[team_events['type'].isin(['SavedShot', 'MissedShots', 'Goal', 'ShotOnPost'])])
                                
                            goals = len(team_events[team_events['is_goal'] == True])
                            
                            fouls = len(team_events[team_events['type'] == 'Foul'])
                            
                            stats_data.append({
                                "Team": team,
                                "Goals": goals,
                                "Shots": shots,
                                "Total Passes": total_passes,
                                "Pass Completion": f"{pass_pct}%",
                                "Fouls": fouls
                            })
                            
                        stats_df = pd.DataFrame(stats_data)
                        st.dataframe(stats_df, use_container_width=True, hide_index=True)
                        
                        # Add quick metric cards
                        cols = st.columns(2)
                        for i, team in enumerate(teams):
                            with cols[i]:
                                st.markdown(f"### {team}")
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Goals", stats_data[i]["Goals"])
                                col2.metric("Shots", stats_data[i]["Shots"])
                                col3.metric("Total Passes", stats_data[i]["Total Passes"])
