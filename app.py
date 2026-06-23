"""
IPL 2026 Batting Analytics Dashboard
=====================================
A professional, interactive, and visually stunning dashboard built with
Streamlit, Pandas, and Plotly for analysing IPL 2026 batting statistics.

Features:
  - KPI cards (Total Runs, Players, Highest Scorer, Highest Strike Rate)
  - Sidebar filters (Team, Player, Runs Range, Strike Rate Range)
  - Top Run Scorers horizontal bar chart
  - Team-wise Runs bar chart
  - Runs vs Strike Rate scatter plot
  - Orange Cap leaderboard table
  - Individual player analysis with radar chart
  - Downloadable filtered data (CSV)
  - Modern dark-themed responsive UI with glassmorphism effects

Author : Dashboard Analytics
Date   : June 2026
"""

# ──────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL 2026 · Batting Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# IPL TEAM COLOUR PALETTE  (official-ish hex colours)
# ──────────────────────────────────────────────────────────────────────────────
TEAM_COLORS = {
    "CSK": "#FCCA06",   # Chennai Super Kings – Gold
    "MI":  "#005DA0",   # Mumbai Indians – Blue
    "RCB": "#D4213D",   # Royal Challengers Bengaluru – Red
    "KKR": "#3A225D",   # Kolkata Knight Riders – Purple
    "DC":  "#0078BC",   # Delhi Capitals – Blue
    "PBKS":"#DD1F2D",   # Punjab Kings – Red
    "RR":  "#EA1A85",   # Rajasthan Royals – Pink
    "SRH": "#FF822A",   # Sunrisers Hyderabad – Orange
    "GT":  "#1B2133",   # Gujarat Titans – Navy
    "LSG": "#A72056",   # Lucknow Super Giants – Magenta
}

# Consistent colour list for Plotly
TEAM_COLOR_SEQUENCE = list(TEAM_COLORS.values())

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS – Dark Theme · Glassmorphism · Animations
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* ── Global ── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
}

/* ── Hide default Streamlit elements for cleaner look ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e0e0ff !important;
}

/* ── KPI Card ── */
.kpi-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.25);
    border-color: rgba(99, 102, 241, 0.4);
}
.kpi-icon {
    font-size: 2rem;
    margin-bottom: 6px;
    display: block;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #818cf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.kpi-label {
    font-size: 0.78rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-top: 4px;
    font-weight: 600;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e0e0ff;
    margin: 2.2rem 0 0.8rem 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Orange Cap Table ── */
.orange-row {
    background: linear-gradient(90deg, rgba(255,165,0,0.15), rgba(255,165,0,0.04));
    border-radius: 8px;
}

/* ── Badge / Chip ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ── Player Profile Card ── */
.player-profile {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 28px 24px;
    margin-bottom: 1rem;
}

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stMultiSelect label, .stSlider label {
    color: #c4b5fd !important;
    font-weight: 600 !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #6366f1, #818cf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────
def render_kpi(icon: str, value, label: str, accent: str = "#6366f1"):
    """Render a single glassmorphism KPI card."""
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid {accent};">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, text: str):
    """Render a styled section header."""
    st.markdown(
        f'<div class="section-header">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


def divider():
    """Render a subtle gradient divider."""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


def dark_plotly_layout(fig, height: int = 460):
    """Apply a consistent dark theme to every Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#cbd5e1"),
        height=height,
        margin=dict(l=40, r=30, t=50, b=40),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.05)",
            font=dict(size=11),
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# DATA LOADING (cached)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Load the IPL 2026 batting CSV and perform basic cleaning.

    Returns
    -------
    pd.DataFrame  Cleaned DataFrame ready for analysis.
    """
    try:
        df = pd.read_csv("ipl_2026_batting.csv")
    except FileNotFoundError:
        st.error("❌ Dataset file `ipl_2026_batting.csv` not found in the app directory.")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("❌ The CSV file is empty. Please provide a valid dataset.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error loading data: {e}")
        st.stop()

    # Normalise column names (lowercase, stripped)
    df.columns = df.columns.str.strip().str.lower()

    # Ensure essential numeric columns exist and coerce types
    numeric_cols = ["runs", "mat", "inns", "sr", "avg", "4s", "6s", "100", "50", "no", "bf"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill NaN numerics with 0
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Strip whitespace from string columns
    for col in ["player", "team", "hs"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


df = load_data()


# ──────────────────────────────────────────────────────────────────────────────
# DASHBOARD HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1.2rem 0 0.2rem 0;">
    <h1 style="
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #c084fc, #818cf8, #6366f1, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
    ">🏏 IPL 2026 Batting Analytics</h1>
    <p style="color:#94a3b8; font-size:1rem; font-weight:500; margin-top:0;">
        Complete Player &amp; Team Performance Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

# Timestamp
st.markdown(
    f'<p style="text-align:center;color:#64748b;font-size:0.75rem;">🕒 Last refreshed: '
    f'{datetime.now().strftime("%d %b %Y  •  %I:%M %p")}</p>',
    unsafe_allow_html=True,
)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem 0;">
        <span style="font-size:2.2rem;">🏏</span>
        <h2 style="
            font-size:1.15rem; font-weight:800;
            background: linear-gradient(135deg,#c084fc,#818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin:6px 0 0 0;
        ">Dashboard Filters</h2>
        <p style="color:#94a3b8;font-size:0.72rem;margin-top:2px;">
            Refine data across all visualisations
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Team Filter ──
    all_teams = sorted(df["team"].unique().tolist())
    selected_teams = st.multiselect(
        "🏟️ Select Team(s)",
        options=all_teams,
        default=all_teams,
        help="Filter players by their IPL franchise.",
    )
    # Guard: at least one team
    if not selected_teams:
        st.warning("⚠️ Please select at least one team.")
        st.stop()

    # ── Player Filter ──
    players_in_teams = sorted(
        df[df["team"].isin(selected_teams)]["player"].unique().tolist()
    )
    selected_players = st.multiselect(
        "👤 Select Player(s)",
        options=players_in_teams,
        default=[],
        help="Leave blank to include all players from selected teams.",
    )

    st.markdown("---")

    # ── Runs Slider ──
    min_runs, max_runs = int(df["runs"].min()), int(df["runs"].max())
    runs_range = st.slider(
        "🏏 Runs Range",
        min_value=min_runs,
        max_value=max_runs,
        value=(min_runs, max_runs),
        help="Filter players by total runs scored.",
    )

    # ── Strike Rate Slider ──
    min_sr, max_sr = float(df["sr"].min()), float(df["sr"].max())
    sr_range = st.slider(
        "⚡ Strike Rate Range",
        min_value=min_sr,
        max_value=max_sr,
        value=(min_sr, max_sr),
        step=0.5,
        help="Filter players by strike rate.",
    )

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center;color:#475569;font-size:0.65rem;">'
        "Built with ❤️ using Streamlit &amp; Plotly</p>",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ──────────────────────────────────────────────────────────────────────────────
filtered_df = df[
    (df["team"].isin(selected_teams))
    & (df["runs"].between(runs_range[0], runs_range[1]))
    & (df["sr"].between(sr_range[0], sr_range[1]))
].copy()

# If specific players selected, narrow down further
if selected_players:
    filtered_df = filtered_df[filtered_df["player"].isin(selected_players)]

# Guard: empty result set
if filtered_df.empty:
    st.warning("⚠️ No players match the current filter criteria. Please adjust the filters.")
    st.stop()


# ──────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────────────────────────────────────
total_runs = int(filtered_df["runs"].sum())
total_players = int(filtered_df["player"].nunique())
top_scorer_name = filtered_df.loc[filtered_df["runs"].idxmax(), "player"]
top_scorer_runs = int(filtered_df["runs"].max())
highest_sr_val = round(filtered_df["sr"].max(), 2)
highest_sr_player = filtered_df.loc[filtered_df["sr"].idxmax(), "player"]
total_centuries = int(filtered_df["100"].sum())
total_fifties = int(filtered_df["50"].sum())

k1, k2, k3, k4 = st.columns(4)

with k1:
    render_kpi("🏏", f"{total_runs:,}", "Total Runs", "#6366f1")
with k2:
    render_kpi("👥", total_players, "Players", "#8b5cf6")
with k3:
    render_kpi("👑", top_scorer_name, f"Highest Scorer • {top_scorer_runs}", "#f59e0b")
with k4:
    render_kpi("⚡", highest_sr_val, f"Highest SR • {highest_sr_player}", "#10b981")

# Secondary KPI row
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
k5, k6, k7, k8 = st.columns(4)

with k5:
    render_kpi("💯", total_centuries, "Centuries", "#ef4444")
with k6:
    render_kpi("5️⃣0️⃣", total_fifties, "Half Centuries", "#f97316")
with k7:
    total_fours = int(filtered_df["4s"].sum())
    render_kpi("4️⃣", f"{total_fours:,}", "Total Fours", "#06b6d4")
with k8:
    total_sixes = int(filtered_df["6s"].sum())
    render_kpi("6️⃣", f"{total_sixes:,}", "Total Sixes", "#ec4899")

divider()


# ──────────────────────────────────────────────────────────────────────────────
# CHART 1 – TOP 10 RUN SCORERS
# ──────────────────────────────────────────────────────────────────────────────
section_header("📊", "Top 10 Run Scorers")

top_runs = filtered_df.nlargest(10, "runs").sort_values("runs", ascending=True)
color_map = {t: TEAM_COLORS.get(t, "#6366f1") for t in top_runs["team"].unique()}

fig_top_runs = px.bar(
    top_runs,
    x="runs",
    y="player",
    color="team",
    color_discrete_map=color_map,
    orientation="h",
    text="runs",
    hover_data={"team": True, "avg": True, "sr": True, "mat": True},
)
fig_top_runs.update_traces(
    textposition="outside",
    textfont=dict(size=12, color="#cbd5e1"),
    marker_line_width=0,
)
fig_top_runs = dark_plotly_layout(fig_top_runs, height=480)
fig_top_runs.update_layout(
    title=dict(text="Top 10 Highest Run Scorers", font=dict(size=16)),
    xaxis_title="Runs",
    yaxis_title="",
)
st.plotly_chart(fig_top_runs, use_container_width=True)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# CHART 2 – TEAM-WISE TOTAL RUNS
# ──────────────────────────────────────────────────────────────────────────────
section_header("🏟️", "Team-wise Total Runs")

team_runs = (
    filtered_df.groupby("team")["runs"]
    .sum()
    .reset_index()
    .sort_values("runs", ascending=False)
)
color_map_team = {t: TEAM_COLORS.get(t, "#6366f1") for t in team_runs["team"].unique()}

fig_team = px.bar(
    team_runs,
    x="team",
    y="runs",
    color="team",
    color_discrete_map=color_map_team,
    text="runs",
    hover_data={"runs": True},
)
fig_team.update_traces(
    textposition="outside",
    textfont=dict(size=12, color="#cbd5e1"),
    marker_line_width=0,
)
fig_team = dark_plotly_layout(fig_team, height=440)
fig_team.update_layout(
    title=dict(text="Total Runs by Franchise", font=dict(size=16)),
    xaxis_title="",
    yaxis_title="Runs",
    showlegend=False,
)
st.plotly_chart(fig_team, use_container_width=True)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# CHART 3 – RUNS vs STRIKE RATE  (Scatter)
# ──────────────────────────────────────────────────────────────────────────────
section_header("🎯", "Runs vs Strike Rate Analysis")

# Filter for meaningful scatter: only players with ≥ 50 runs for clarity
scatter_df = filtered_df[filtered_df["runs"] >= 20].copy()

if not scatter_df.empty:
    # Use boundary count as bubble size
    scatter_df["boundaries"] = scatter_df["4s"] + scatter_df["6s"]
    scatter_df["boundaries"] = scatter_df["boundaries"].clip(lower=1)  # avoid zero-size

    color_map_scatter = {t: TEAM_COLORS.get(t, "#6366f1") for t in scatter_df["team"].unique()}

    fig_scatter = px.scatter(
        scatter_df,
        x="runs",
        y="sr",
        size="boundaries",
        color="team",
        color_discrete_map=color_map_scatter,
        hover_name="player",
        hover_data={"runs": True, "sr": True, "team": True, "avg": True, "mat": True},
        size_max=28,
    )
    fig_scatter = dark_plotly_layout(fig_scatter, height=520)
    fig_scatter.update_layout(
        title=dict(text="Runs vs Strike Rate (bubble = boundaries)", font=dict(size=16)),
        xaxis_title="Runs Scored",
        yaxis_title="Strike Rate",
    )
    # Add quadrant reference lines (mean values)
    avg_runs = scatter_df["runs"].mean()
    avg_sr = scatter_df["sr"].mean()
    fig_scatter.add_hline(y=avg_sr, line_dash="dot", line_color="rgba(148,163,184,0.3)",
                          annotation_text=f"Avg SR {avg_sr:.1f}")
    fig_scatter.add_vline(x=avg_runs, line_dash="dot", line_color="rgba(148,163,184,0.3)",
                          annotation_text=f"Avg Runs {avg_runs:.0f}")

    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Not enough data points for the scatter plot with current filters.")

divider()


# ──────────────────────────────────────────────────────────────────────────────
# CHART 4 – BOUNDARY ANALYSIS  (Stacked)
# ──────────────────────────────────────────────────────────────────────────────
section_header("💥", "Top 10 Boundary Hitters")

boundary_df = filtered_df.copy()
boundary_df["total_boundaries"] = boundary_df["4s"] + boundary_df["6s"]
top_boundary = boundary_df.nlargest(10, "total_boundaries").sort_values(
    "total_boundaries", ascending=True
)

fig_boundary = go.Figure()
fig_boundary.add_trace(go.Bar(
    y=top_boundary["player"],
    x=top_boundary["4s"],
    name="Fours",
    orientation="h",
    marker_color="#06b6d4",
    text=top_boundary["4s"],
    textposition="inside",
))
fig_boundary.add_trace(go.Bar(
    y=top_boundary["player"],
    x=top_boundary["6s"],
    name="Sixes",
    orientation="h",
    marker_color="#ec4899",
    text=top_boundary["6s"],
    textposition="inside",
))
fig_boundary.update_layout(barmode="stack")
fig_boundary = dark_plotly_layout(fig_boundary, height=460)
fig_boundary.update_layout(
    title=dict(text="Top 10 Boundary Hitters (4s + 6s)", font=dict(size=16)),
    xaxis_title="Boundaries",
    yaxis_title="",
)
st.plotly_chart(fig_boundary, use_container_width=True)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# ORANGE CAP LEADERBOARD
# ──────────────────────────────────────────────────────────────────────────────
section_header("🧡", "Orange Cap Leaderboard")

orange_cap = (
    filtered_df[["pos", "player", "team", "runs", "mat", "inns", "avg", "sr", "100", "50", "hs"]]
    .sort_values("runs", ascending=False)
    .head(15)
    .reset_index(drop=True)
)
orange_cap.index = orange_cap.index + 1  # 1-based rank
orange_cap.index.name = "Rank"

# Rename for display
display_orange = orange_cap.rename(columns={
    "player": "Player",
    "team": "Team",
    "runs": "Runs",
    "mat": "Matches",
    "inns": "Innings",
    "avg": "Average",
    "sr": "Strike Rate",
    "100": "100s",
    "50": "50s",
    "hs": "High Score",
    "pos": "Pos",
})

st.dataframe(
    display_orange.style
    .background_gradient(cmap="YlOrRd", subset=["Runs"])
    .format({"Average": "{:.2f}", "Strike Rate": "{:.2f}", "Matches": "{:.0f}",
             "Innings": "{:.0f}", "100s": "{:.0f}", "50s": "{:.0f}"}),
    use_container_width=True,
    height=560,
)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# PLAYER ANALYSIS SECTION
# ──────────────────────────────────────────────────────────────────────────────
section_header("🔍", "Individual Player Analysis")

pa_col1, pa_col2 = st.columns([1, 2])

with pa_col1:
    selected_player = st.selectbox(
        "Choose a player",
        options=sorted(df["player"].unique().tolist()),
        index=0,
        help="Select a player to view detailed batting profile.",
    )

player_data = df[df["player"] == selected_player]

if not player_data.empty:
    p = player_data.iloc[0]

    with pa_col1:
        st.markdown(f"""
        <div class="player-profile">
            <h3 style="color:#e0e0ff; margin:0 0 4px 0; font-size:1.4rem;">{p['player']}</h3>
            <span class="badge" style="background:{TEAM_COLORS.get(p['team'],'#6366f1')}; color:#fff;">
                {p['team']}
            </span>
            <div style="margin-top:18px; display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">Runs</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{int(p['runs'])}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">Strike Rate</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{p['sr']}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">Average</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{p['avg']}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">Matches</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{int(p['mat'])}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">Innings</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{int(p['inns'])}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">High Score</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{p['hs']}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">100s / 50s</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{int(p['100'])} / {int(p['50'])}</div>
                </div>
                <div>
                    <div style="color:#94a3b8; font-size:0.7rem; text-transform:uppercase;">4s / 6s</div>
                    <div style="color:#e0e0ff; font-size:1.3rem; font-weight:700;">{int(p['4s'])} / {int(p['6s'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with pa_col2:
        # ── Radar Chart ──
        # Normalise each metric to 0-100 for a balanced radar
        max_vals = {
            "Runs":   df["runs"].max() if df["runs"].max() > 0 else 1,
            "Average": df["avg"].max() if df["avg"].max() > 0 else 1,
            "SR":      df["sr"].max() if df["sr"].max() > 0 else 1,
            "4s":      df["4s"].max() if df["4s"].max() > 0 else 1,
            "6s":      df["6s"].max() if df["6s"].max() > 0 else 1,
            "Innings": df["inns"].max() if df["inns"].max() > 0 else 1,
        }
        radar_vals = [
            (p["runs"]  / max_vals["Runs"])   * 100,
            (p["avg"]   / max_vals["Average"]) * 100,
            (p["sr"]    / max_vals["SR"])       * 100,
            (p["4s"]    / max_vals["4s"])       * 100,
            (p["6s"]    / max_vals["6s"])       * 100,
            (p["inns"]  / max_vals["Innings"])  * 100,
        ]
        radar_cats = ["Runs", "Average", "Strike Rate", "Fours", "Sixes", "Innings"]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_vals + [radar_vals[0]],  # close the polygon
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            fillcolor="rgba(99,102,241,0.15)",
            line=dict(color="#818cf8", width=2.5),
            marker=dict(size=6, color="#a78bfa"),
            name=p["player"],
        ))
        fig_radar = dark_plotly_layout(fig_radar, height=440)
        fig_radar.update_layout(
            title=dict(text=f"{p['player']} – Performance Radar", font=dict(size=15)),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    gridcolor="rgba(255,255,255,0.06)",
                    tickfont=dict(size=9, color="#64748b"),
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.08)",
                    tickfont=dict(size=11, color="#94a3b8"),
                ),
            ),
        )
        st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("No data available for the selected player.")

divider()


# ──────────────────────────────────────────────────────────────────────────────
# TEAM CONTRIBUTION TREEMAP
# ──────────────────────────────────────────────────────────────────────────────
section_header("🗺️", "Team Contribution Treemap")

fig_treemap = px.treemap(
    filtered_df,
    path=["team", "player"],
    values="runs",
    color="runs",
    color_continuous_scale="Viridis",
    hover_data={"sr": True, "avg": True},
)
fig_treemap = dark_plotly_layout(fig_treemap, height=520)
fig_treemap.update_layout(
    title=dict(text="Runs Contribution by Team & Player", font=dict(size=16)),
    coloraxis_colorbar=dict(title="Runs", tickfont=dict(color="#94a3b8")),
)
st.plotly_chart(fig_treemap, use_container_width=True)

divider()


# ──────────────────────────────────────────────────────────────────────────────
# DOWNLOADABLE FILTERED DATA
# ──────────────────────────────────────────────────────────────────────────────
section_header("📥", "Download Filtered Data")

st.markdown(
    '<p style="color:#94a3b8; font-size:0.85rem;">Export the currently filtered dataset as CSV.</p>',
    unsafe_allow_html=True,
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 2])
with dl_col1:
    st.download_button(
        label="📥  Download CSV",
        data=csv_data,
        file_name=f"ipl_2026_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

with dl_col2:
    st.markdown(
        f'<p style="color:#64748b;font-size:0.78rem;margin-top:10px;">'
        f'{len(filtered_df)} players · {len(filtered_df["team"].unique())} teams</p>',
        unsafe_allow_html=True,
    )

divider()


# ──────────────────────────────────────────────────────────────────────────────
# COMPLETE DATASET TABLE
# ──────────────────────────────────────────────────────────────────────────────
section_header("📋", "Complete Filtered Dataset")

display_df = filtered_df.rename(columns={
    "pos": "Pos", "player": "Player", "team": "Team", "runs": "Runs",
    "mat": "Matches", "inns": "Innings", "no": "Not Outs", "hs": "High Score",
    "avg": "Average", "bf": "Balls Faced", "sr": "Strike Rate",
    "100": "100s", "50": "50s", "4s": "Fours", "6s": "Sixes",
}).reset_index(drop=True)

st.dataframe(
    display_df.style.background_gradient(cmap="Blues", subset=["Runs"]),
    use_container_width=True,
    height=500,
)


# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem 0; border-top:1px solid rgba(255,255,255,0.05);">
    <p style="color:#475569; font-size:0.75rem; margin:0;">
        IPL 2026 Batting Analytics Dashboard · Built with
        <span style="color:#ef4444;">❤</span> using Streamlit &amp; Plotly
    </p>
    <p style="color:#334155; font-size:0.65rem; margin-top:4px;">
        © 2026 Dashboard Analytics · Data sourced from official IPL statistics
    </p>
</div>
""", unsafe_allow_html=True)