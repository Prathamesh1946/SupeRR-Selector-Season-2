from pathlib import Path
import re
import pandas as pd
import streamlit as st
# ============================================================
# SUPERR SELECTOR SEASON 2
# Rajasthan Royals Auction Intelligence Dashboard
# ============================================================
ROOT = Path(__file__).resolve().parent
NOTEBOOKS = ROOT / "notebooks"
SUBMISSION = NOTEBOOKS / "ROUND1_SUBMISSION"
CHARTS = NOTEBOOKS / "Round1_Report_Charts"
# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="SupeRR Analytics | Rajasthan Royals",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ------------------------------------------------------------
# CUSTOM DESIGN
# ------------------------------------------------------------
st.markdown("""
<style>
/* ===== GLOBAL ===== */
.stApp {
    background: #F5F6FA;
    color: #17233B;
}
.block-container {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
/* ===== TYPOGRAPHY ===== */
html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}
h1, h2, h3, h4 {
    color: #17233B !important;
    letter-spacing: -0.5px;
}
p, li, label, .stMarkdown {
    color: #35445D;
}
/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #101D35;
    border-right: 1px solid #263550;
}
section[data-testid="stSidebar"] * {
    color: #E8EDF5 !important;
}
section[data-testid="stSidebar"] h1 {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    border-radius: 8px;
    padding: 7px 9px;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #253550;
}
/* ===== HERO ===== */
.hero {
    background: linear-gradient(
        120deg,
        #101D35 0%,
        #1C3152 65%,
        #293C5C 100%
    );
    padding: 38px 40px;
    border-radius: 20px;
    color: #FFFFFF;
    margin-bottom: 30px;
    border: 1px solid #304463;
    box-shadow: 0 12px 30px rgba(16, 29, 53, 0.10);
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 12px 0 8px 0;
}
.hero h3 {
    color: #F3B6CD !important;
    font-size: 22px;
    font-weight: 650;
    margin: 0 0 15px 0;
}
.hero p {
    color: #D7E0EE !important;
    font-size: 14px;
    line-height: 1.7;
}
.hero-kicker {
    color: #F3B6CD;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}
/* ===== METRICS ===== */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E9F1;
    border-radius: 15px;
    padding: 18px 20px;
    box-shadow: 0 4px 14px rgba(22, 35, 59, 0.035);
}
div[data-testid="stMetricLabel"] {
    color: #66748B !important;
    font-size: 13px !important;
}
div[data-testid="stMetricLabel"] p {
    color: #66748B !important;
}
div[data-testid="stMetricValue"] {
    color: #17233B !important;
    font-size: 30px !important;
    font-weight: 750 !important;
}
/* ===== CARDS ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #E5E9F1;
    border-radius: 15px;
}
/* ===== TABS ===== */
button[data-baseweb="tab"] {
    color: #66748B;
    font-weight: 650;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #D83F78;
}
/* ===== TABLES ===== */
div[data-testid="stDataFrame"] {
    border: 1px solid #E5E9F1;
    border-radius: 12px;
    overflow: hidden;
}
/* ===== BUTTONS ===== */
.stDownloadButton button,
.stButton button {
    background: #D83F78;
    color: #FFFFFF;
    border: none;
    border-radius: 9px;
    font-weight: 650;
    padding: 9px 18px;
}
.stDownloadButton button:hover,
.stButton button:hover {
    background: #B82D63;
    color: #FFFFFF;
    border: none;
}
/* ===== SELECT BOX ===== */
div[data-baseweb="select"] > div {
    background: #FFFFFF;
    border-color: #DCE2EC;
    border-radius: 9px;
}
/* ===== ALERTS ===== */
div[data-testid="stAlert"] {
    border-radius: 11px;
}
/* ===== DIVIDERS ===== */
hr {
    border-color: #E1E6EF;
}
/* ===== FOOTER ===== */
.footer {
    text-align: center;
    padding: 25px 10px;
    color: #7B879A;
    font-size: 12px;
    border-top: 1px solid #E1E6EF;
    margin-top: 35px;
}
/* ===== MOBILE ===== */
@media (max-width: 768px) {
    .hero {
        padding: 25px 22px;
    }
    .hero h1 {
        font-size: 30px;
    }
    .hero h3 {
        font-size: 18px;
    }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# FILE DISCOVERY
# ------------------------------------------------------------
@st.cache_data
def find_file(filename):
    locations = [
        SUBMISSION / filename,
        NOTEBOOKS / filename,
        CHARTS / filename,
        ROOT / filename
    ]
    for path in locations:
        if path.is_file():
            return path
    if NOTEBOOKS.exists():
        matches = list(NOTEBOOKS.rglob(filename))
        if matches:
            return matches[0]
    return None
@st.cache_data
def read_csv(filename):
    path = find_file(filename)
    if path is None:
        return None
    try:
        return pd.read_csv(path)
    except Exception as error:
        st.error(f"Could not read {filename}: {error}")
        return None
def first_available(*filenames):
    for filename in filenames:
        path = find_file(filename)
        if path is not None:
            return pd.read_csv(path), path.name
    return None, None
def display_table(df, title=None):
    if df is None:
        st.warning("This output file was not found.")
        return
    if title:
        st.subheader(title)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
def normalize_column(column):
    return re.sub(
        r"[^a-z0-9]",
        "",
        str(column).lower()
    )
def find_column(df, candidates):
    if df is None:
        return None
    normalized = {
        normalize_column(col): col
        for col in df.columns
    }
    for candidate in candidates:
        key = normalize_column(candidate)
        if key in normalized:
            return normalized[key]
    for candidate in candidates:
        key = normalize_column(candidate)
        for existing, original in normalized.items():
            if key in existing or existing in key:
                return original
    return None
def safe_value(value, default="Not available"):
    if pd.isna(value) or str(value).strip().lower() in ["", "nan", "none"]:
        return default
    return str(value)

def get_number(row, *column_names, default=None):
    """Return the first available numeric value from a row."""
    for column in column_names:
        if column in row.index:
            value = pd.to_numeric(row[column], errors="coerce")
            if pd.notna(value):
                return float(value)
    return default

def metric_text(row, *column_names, digits=2, suffix=""):
    value = get_number(row, *column_names)
    return "N/A" if value is None else f"{value:.{digits}f}{suffix}"

def metric_int_text(row, *column_names):
    value = get_number(row, *column_names)
    return "N/A" if value is None else f"{int(value):,}"
def show_player_explorer(df, title):
    if df is None or df.empty:
        st.warning(f"{title} data is not available.")
        return
    name_col = find_column(
        df,
        [
            "player_name",
            "striker_name",
            "batter_name",
            "bowler_name",
            "player",
            "name"
        ]
    )
    if name_col is None:
        st.info("Player-name column not detected. Showing source table.")
        display_table(df)
        return
    st.subheader(title)
    players = sorted(
        df[name_col].dropna().astype(str).unique().tolist()
    )
    if not players:
        st.info("No player records found.")
        return
    selected = st.selectbox(
        "Select a player",
        players,
        key=title
    )
    row = df[
        df[name_col].astype(str) == selected
    ].iloc[0]
    st.markdown(f"### {selected}")
    # Show all available evidence for the selected player.
    st.dataframe(
        row.to_frame("Value"),
        use_container_width=True
    )

def show_rr_scouting_profile(
    ranking_df,
    evidence_df,
    player_type="Batter"
):
    """Display a player scouting profile using actual RR and
    official Round 1 evidence columns."""

    if ranking_df is None or ranking_df.empty:
        st.warning("RR ranking data unavailable.")
        return

    name_col = "player_name"
    rank_col = "category_fit_rank"

    if rank_col in ranking_df.columns:
        ranking_df = ranking_df.sort_values(rank_col)

    players = ranking_df[name_col].dropna().tolist()

    if not players:
        st.warning("No players found in ranking data.")
        return

    st.markdown("### Select a player to scout")

    selected = st.selectbox(
        "Player",
        players,
        key=f"rr_scout_{player_type}"
    )

    player = ranking_df[
        ranking_df[name_col] == selected
    ].iloc[0]

    # Match official pressure evidence
    evidence = None

    if evidence_df is not None:
        evidence_name = find_column(
            evidence_df,
            ["striker_name", "batter_name", "player_name"]
            if player_type == "Batter"
            else ["bowler_name", "player_name"]
        )

        if evidence_name is not None:
            matched = evidence_df[
                evidence_df[evidence_name].astype(str).str.strip()
                == str(selected).strip()
            ]

            if not matched.empty:
                evidence = matched.iloc[0]

    st.divider()

    # Player heading
    st.markdown(f"# {selected}")

    role = player.get("playing_role", "Role not available")
    st.caption(f"{player_type} · {role}")

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "RR Fit Rank",
        f"#{int(player['category_fit_rank'])}"
        if pd.notna(player.get("category_fit_rank"))
        else "N/A"
    )

    fit_score = pd.to_numeric(
        pd.Series([player.get("preliminary_fit_score")]),
        errors="coerce"
    ).iloc[0]

    c2.metric(
        "RR Fit Score",
        f"{fit_score:.2f}" if pd.notna(fit_score) else "N/A"
    )

    historical_rank = pd.to_numeric(
        pd.Series([player.get("original_rank")]),
        errors="coerce"
    ).iloc[0]

    c3.metric(
        "Historical Rank",
        f"#{int(historical_rank)}"
        if pd.notna(historical_rank)
        else "N/A"
    )

    historical_score = pd.to_numeric(
        pd.Series([player.get("original_score")]),
        errors="coerce"
    ).iloc[0]

    c4.metric(
        "Historical Score",
        f"{historical_score:.2f}"
        if pd.notna(historical_score)
        else "N/A"
    )

    # Squad fit
    st.markdown("## Why this player is considered")

    left, right = st.columns(2)

    with left:
        st.markdown("**Playing role**")
        st.write(role)

        st.markdown("**RR squad requirement**")
        st.write(
            safe_value(
                player.get("rr_squad_gap"),
                "Not available"
            )
        )

    with right:
        st.markdown("**Fit assessment**")
        st.write(
            safe_value(
                player.get("fit_assessment"),
                "Assessment pending"
            )
        )

        st.markdown("**Fit reasoning**")
        st.write(
            safe_value(
                player.get("rr_fit_reason"),
                "Reasoning pending verification"
            )
        )

    st.divider()

    # ==========================================
    # HISTORICAL PRESSURE-PERFORMANCE EVIDENCE
    # ==========================================

    st.markdown("## Historical pressure-performance evidence")

    if evidence is None:
        st.warning(
            "No matching official pressure evidence was found. "
            "Check that the detailed batter or bowler evidence CSV "
            "is inside the project data folder."
        )

    elif player_type == "Batter":

        # Top batter metrics
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Pressure strike rate",
            metric_text(evidence, "strike_rate_pressure")
        )

        c2.metric(
            "Normal strike rate",
            metric_text(evidence, "strike_rate_normal")
        )

        c3.metric(
            "Pressure balls",
            metric_int_text(
                evidence,
                "balls_pressure",
                "format_pressure_balls"
            )
        )

        c4.metric(
            "Pressure matches",
            metric_int_text(evidence, "matches_pressure")
        )

        st.markdown("### Pressure vs normal performance")

        # Row 1: Strike Rate and Dot-Ball Percentage
        chart1, chart2 = st.columns(2)

        pressure_sr = get_number(
            evidence, "strike_rate_pressure"
        )
        normal_sr = get_number(
            evidence, "strike_rate_normal"
        )

        with chart1:
            if pressure_sr is not None and normal_sr is not None:
                show_comparison_chart(
                    "Strike Rate",
                    pressure_sr,
                    normal_sr,
                    "Runs per 100 balls"
                )
            else:
                st.info("Strike-rate comparison is unavailable.")

        pressure_dot = get_number(
            evidence, "dot_ball_pct_pressure"
        )
        normal_dot = get_number(
            evidence, "dot_ball_pct_normal"
        )

        with chart2:
            if pressure_dot is not None and normal_dot is not None:
                show_comparison_chart(
                    "Dot-Ball Percentage",
                    pressure_dot,
                    normal_dot,
                    "Dot balls (%)",
                    lower_is_better=True
                )
            else:
                st.info("Dot-ball comparison is unavailable.")

        # Row 2: Boundary Percentage and Normal Sample Size
        chart3, chart4 = st.columns(2)

        pressure_boundary = get_number(
            evidence, "boundary_pct_pressure"
        )
        normal_boundary = get_number(
            evidence, "boundary_pct_normal"
        )

        with chart3:
            if (
                pressure_boundary is not None
                and normal_boundary is not None
            ):
                show_comparison_chart(
                    "Boundary Percentage",
                    pressure_boundary,
                    normal_boundary,
                    "Boundary balls (%)"
                )
            else:
                st.info("Boundary comparison is unavailable.")

        with chart4:
            st.metric(
                "Normal balls",
                metric_int_text(evidence, "balls_normal")
            )

            st.metric(
                "Normal matches",
                metric_int_text(evidence, "matches_normal")
            )

    else:

        # Top bowler metrics
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Pressure economy",
            metric_text(evidence, "economy_pressure")
        )

        c2.metric(
            "Normal economy",
            metric_text(evidence, "economy_normal")
        )

        c3.metric(
            "Pressure wickets",
            metric_int_text(evidence, "wickets_pressure")
        )

        c4.metric(
            "Pressure legal balls",
            metric_int_text(
                evidence,
                "legal_balls_pressure",
                "pressure_balls"
            )
        )

        st.markdown("### Pressure vs normal performance")

        # Row 1: Economy Rate and Wicket Rate
        chart1, chart2 = st.columns(2)

        pressure = get_number(
            evidence, "economy_pressure"
        )
        normal = get_number(
            evidence, "economy_normal"
        )

        with chart1:
            if pressure is not None and normal is not None:
                show_comparison_chart(
                    "Economy Rate",
                    pressure,
                    normal,
                    "Runs per over",
                    lower_is_better=True
                )
            else:
                st.info("Economy data unavailable.")

        pressure = get_number(
            evidence, "wicket_rate_pressure"
        )
        normal = get_number(
            evidence, "wicket_rate_normal"
        )

        with chart2:
            if pressure is not None and normal is not None:
                show_comparison_chart(
                    "Wicket Rate",
                    pressure,
                    normal,
                    "Wickets per 100 legal balls"
                )
            else:
                st.info("Wicket-rate data unavailable.")

        # Row 2: Dot-Ball Percentage and Boundary Percentage
        chart3, chart4 = st.columns(2)

        pressure = get_number(
            evidence, "dot_ball_pct_pressure"
        )
        normal = get_number(
            evidence, "dot_ball_pct_normal"
        )

        with chart3:
            if pressure is not None and normal is not None:
                show_comparison_chart(
                    "Dot-Ball Percentage",
                    pressure,
                    normal,
                    "Dot balls (%)",
                    lower_is_better=True
                )
            else:
                st.info("Dot-ball data unavailable.")

        pressure = get_number(
            evidence, "boundary_pct_pressure"
        )
        normal = get_number(
            evidence, "boundary_pct_normal"
        )

        with chart4:
            if pressure is not None and normal is not None:
                show_comparison_chart(
                    "Boundary Percentage",
                    pressure,
                    normal,
                    "Batter boundaries (%)",
                    lower_is_better=True
                )
            else:
                st.info("Boundary data unavailable.")

        # Bowler sample size
        st.markdown("### Sample size")

        st.write(
            f"Pressure: "
            f"{metric_int_text(evidence, 'legal_balls_pressure', 'pressure_balls')} "
            f"legal balls across "
            f"{metric_int_text(evidence, 'matches_pressure')} matches."
        )

        st.write(
            f"Normal: "
            f"{metric_int_text(evidence, 'legal_balls_normal')} "
            f"legal balls across "
            f"{metric_int_text(evidence, 'matches_normal')} matches."
        )

    st.divider()

    # ==========================================
    # AUCTION ELIGIBILITY AND VERIFICATION
    # ==========================================

    st.markdown("## Auction eligibility and verification")

    v1, v2, v3 = st.columns(3)

    v1.metric(
        "Retention status",
        str(player.get("2027_retention_status", "Unknown"))
    )

    v2.metric(
        "Auction registration",
        str(player.get("auction_registration", "Unknown"))
    )

    v3.metric(
        "Availability",
        str(player.get("auction_availability", "Unknown"))
    )

    st.warning(
        "This is a preliminary squad-fit assessment, not a "
        "confirmed auction recommendation. Retention, registration "
        "and auction availability require official verification."
    )

def show_comparison_chart(title, pressure, normal, ylabel,
                          lower_is_better=False):
    import matplotlib.pyplot as plt
    import numpy as np
    labels = ["Pressure", "Normal"]
    values = [pressure, normal]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    colors = ["#D83F78", "#263F65"]
    bars = ax.bar(
        labels,
        values,
        color=colors,
        width=0.48,
        edgecolor="white"
    )
    ax.set_title(
        title,
        fontsize=13,
        fontweight="bold",
        color="#17233B",
        pad=15
    )
    ax.set_ylabel(ylabel, color="#66748B")
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.bar_label(
        bars,
        fmt="%.2f",
        padding=4,
        fontsize=10,
        fontweight="bold"
    )
    ax.tick_params(axis="both", labelsize=10)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
def show_chart(filename, caption):
    path = find_file(filename)
    if path is not None:
        st.image(
            str(path),
            caption=caption,
            use_container_width=True
        )
# ------------------------------------------------------------
# LOAD OFFICIAL ROUND 1 DATA
# ------------------------------------------------------------
official_batters, _ = first_available(
    "ROUND1_OFFICIAL_TOP10_BATTERS.csv",
    "Official_Top10_Batters.csv"
)
official_bowlers, _ = first_available(
    "ROUND1_OFFICIAL_TOP10_BOWLERS.csv",
    "Official_Top10_Bowlers.csv"
)
batter_evidence, _ = first_available(
    "Detailed_Batter_Evidence.csv",
    "ROUND1_DETAILED_TOP10_BATTER_EVIDENCE.csv",
    "ROUND1_FINAL_BATTER_EVIDENCE.csv"
)
bowler_evidence, _ = first_available(
    "Detailed_Bowler_Evidence.csv",
    "ROUND1_DETAILED_TOP10_BOWLER_EVIDENCE.csv",
    "ROUND1_FINAL_BOWLER_EVIDENCE.csv"
)
validation, _ = first_available(
    "ROUND1_RECALCULATED_MODEL_VALIDATION.csv",
    "Model_Validation.csv"
)
coverage, _ = first_available(
    "ROUND1_MODEL_DATASET_COVERAGE.csv",
    "Model_Dataset_Coverage.csv"
)
pressure_robustness, _ = first_available(
    "ROUND1_PRESSURE_THRESHOLD_ROBUSTNESS.csv",
    "Pressure_Threshold_Robustness.csv"
)
weight_robustness, _ = first_available(
    "ROUND1_COMPONENT_WEIGHT_ROBUSTNESS.csv",
    "Component_Weight_Robustness.csv"
)
methodology, _ = first_available(
    "ROUND1_METHODOLOGY_REFERENCE.csv",
    "Methodology_Reference.csv"
)
# ------------------------------------------------------------
# LOAD RAJASTHAN ROYALS ANALYSIS
# ------------------------------------------------------------
rr_batters, rr_batter_filename = first_available(
    "RR_2027_Batter_Fit_Ranking.csv",
    "RR_Batter_Candidate_Ranking.csv"
)
rr_bowlers, rr_bowler_filename = first_available(
    "RR_2027_Bowler_Fit_Ranking.csv",
    "RR_Bowler_Candidate_Ranking.csv"
)
rr_preliminary = read_csv(
    "RR_2027_Preliminary_Fit_Ranking.csv"
)
# Load Player Verification Tracking CSV if available
rr_verification_path = (
    next(ROOT.rglob("RR_2027_Player_Verification_Track*.csv"), None)
)
rr_verification = (
    pd.read_csv(rr_verification_path)
    if rr_verification_path is not None
    else None
)
rr_squad_verification = read_csv(
    "RR_2027_Squad_Fit_Verification.csv"
)
rr_squad_gaps = read_csv(
    "RR_2027_Squad_Gap_Analysis.csv"
)
rr_candidates = read_csv(
    "rr_potential_auction_candidates.csv"
)
# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.markdown("# 🏏 SupeRR")
st.sidebar.caption("SELECTOR SEASON 2")
st.sidebar.divider()
page = st.sidebar.radio(
    "DASHBOARD NAVIGATION",
    [
        "Overview",
        "Rajasthan Royals Strategy",
        "RR Batter Recommendations",
        "RR Bowler Recommendations",
        "Official Round 1 Rankings",
        "Pressure Methodology & Validation"
    ]
)
st.sidebar.divider()
st.sidebar.caption(
    "Historical dataset: IPL and T20I, 2022 onwards"
)
st.sidebar.caption(
    "Data-driven player reliability analysis"
)
# ============================================================
# PAGE 1: OVERVIEW
# ============================================================
if page == "Overview":
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">
            SUPERR SELECTOR · SEASON 2 · ROUND 1
        </div>
        <h1>SupeRR Analytics</h1>
        <h3>Pressure. Performance. Precision.</h3>
        <p>
            Identifying the most reliable T20 players under pressure
            through match-context modelling, performance analytics
            and evidence-based evaluation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## The analysis at a glance")
    st.caption(
        "Historical IPL and T20 International data from 2022 onwards"
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Deliveries analysed", "192,270")
    c2.metric("Matches analysed", "815")
    c3.metric("Eligible batters", "98")
    c4.metric("Eligible bowlers", "135")
    st.write("")
    st.markdown("## From pressure detection to player selection")
    a, b, c = st.columns(3)
    with a:
        with st.container(border=True):
            st.markdown("### 01 · Detect")
            st.markdown("**Identify pressure situations**")
            st.write(
                "Model first-innings scoring pressure and "
                "high-risk run chases using match-state information."
            )
            st.caption("Random Forest · Logistic Regression")
    with b:
        with st.container(border=True):
            st.markdown("### 02 · Evaluate")
            st.markdown("**Measure player reliability**")
            st.write(
                "Compare pressure and normal performance using "
                "batting and bowling indicators."
            )
            st.caption("Sample eligibility · Shrinkage · Composite scores")
    with c:
        with st.container(border=True):
            st.markdown("### 03 · Recommend")
            st.markdown("**Translate evidence into RR strategy**")
            st.write(
                "Evaluate player performance alongside Rajasthan "
                "Royals' squad requirements and role suitability."
            )
            st.caption("Squad fit · Candidate ranking · Verification")
    st.write("")
    st.markdown("## Historical pressure leaderboard")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("#### 🏏 Leading batter")
            if official_batters is not None and not official_batters.empty:
                row = official_batters.iloc[0]
                name_col = find_column(
                    official_batters,
                    ["striker_name", "player_name"]
                )
                score_col = find_column(
                    official_batters,
                    ["final_batter_score"]
                )
                if name_col and score_col:
                    st.markdown(f"### {row[name_col]}")
                    st.metric(
                        "Final batter score",
                        f"{float(row[score_col]):.2f}"
                    )
                st.dataframe(
                    official_batters.head(5),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Official batter ranking unavailable.")
    with right:
        with st.container(border=True):
            st.markdown("#### 🎯 Leading bowler")
            if official_bowlers is not None and not official_bowlers.empty:
                row = official_bowlers.iloc[0]
                name_col = find_column(
                    official_bowlers,
                    ["bowler_name", "player_name"]
                )
                score_col = find_column(
                    official_bowlers,
                    ["bowler_score"]
                )
                if name_col and score_col:
                    st.markdown(f"### {row[name_col]}")
                    st.metric(
                        "Final bowler score",
                        f"{float(row[score_col]):.2f}"
                    )
                st.dataframe(
                    official_bowlers.head(5),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Official bowler ranking unavailable.")
    st.write("")
    st.markdown("## Two distinct analytical outputs")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("### Official Round 1 rankings")
            st.write(
                "Historical top-10 batter and bowler rankings "
                "based on the supplied challenge datapack."
            )
            st.caption(
                "All eligible players are retained irrespective "
                "of nationality."
            )
    with right:
        with st.container(border=True):
            st.markdown("### Rajasthan Royals squad fit")
            st.write(
                "A supplementary player-selection strategy "
                "combining pressure evidence and squad requirements."
            )
            st.caption(
                "Pakistan-national players excluded from this "
                "separate actionable shortlist."
            )
    st.markdown("""
    <div class="footer">
        <b>SUPERR SELECTOR · SEASON 2</b><br>
        Identify the Most Reliable Players Under Pressure<br>
        Historical performance analysis · Rajasthan Royals squad-fit research
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE 2: RAJASTHAN ROYALS STRATEGY
# ============================================================
elif page == "Rajasthan Royals Strategy":

    # --------------------------------------------------------
    # 1. HERO
    # --------------------------------------------------------
    st.markdown("""
    <div class="hero">
        <p>SUPPLEMENTARY TEAM ANALYSIS · ROUND 1</p>
        <h1>Rajasthan Royals Auction Intelligence</h1>
        <h3>Build a pressure-resistant squad</h3>
        <p>
        Translating historical pressure performance into
        evidence-based squad-fit recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # 2. IMPORTANT DISTINCTION
    # --------------------------------------------------------
    st.markdown("## From performance to recruitment")

    st.write(
        "This analysis separates historical player performance "
        "from Rajasthan Royals squad suitability. A high historical "
        "rank does not automatically mean a player is an auction target."
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 01 · Performance")
        st.write(
            "Identify players who have demonstrated strong "
            "performance in high-pressure situations."
        )

    with b:
        st.markdown("### 02 · Squad fit")
        st.write(
            "Evaluate playing role, squad requirements and "
            "potential gaps that a candidate could address."
        )

    with c:
        st.markdown("### 03 · Verification")
        st.write(
            "Check retention, registration, nationality and "
            "auction availability before making a decision."
        )

    st.divider()

    # --------------------------------------------------------
    # 3. PREPARE ACTIONABLE CANDIDATE DATA
    # --------------------------------------------------------
    rr_actionable = (
        rr_preliminary.copy()
        if rr_preliminary is not None
        else pd.DataFrame()
    )

    # Pakistan-national players are excluded from the RR
    # actionable shortlist, but retained in official rankings.
    excluded_rr_players = {
        "Shadab Khan",
        "Abrar Ahmed",
        "Mohammad Nawaz",
        "Shaheen Afridi"
    }

    if not rr_actionable.empty and "player_name" in rr_actionable.columns:
        rr_actionable = rr_actionable[
            ~rr_actionable["player_name"].astype(str).isin(
                excluded_rr_players
            )
        ].copy()

        # Also exclude players explicitly identified as Pakistani
        # in the nationality field. Do not treat pending verification
        # as proof of nationality.
        if "nationality" in rr_actionable.columns:
            rr_actionable = rr_actionable[
                ~rr_actionable["nationality"].astype(str).str.contains(
                    r"\bPakistan\b",
                    case=False,
                    na=False,
                    regex=True
                )
            ].copy()

    # --------------------------------------------------------
    # 4. SUMMARY METRICS
    # --------------------------------------------------------
    st.markdown("## Candidate pool overview")

    total_candidates = len(rr_actionable)

    batter_count = 0
    bowler_count = 0

    if (
        not rr_actionable.empty
        and "analysis_category" in rr_actionable.columns
    ):
        categories = rr_actionable["analysis_category"].astype(str).str.lower()
        batter_count = int(categories.str.contains("batter").sum())
        bowler_count = int(categories.str.contains("bowler").sum())

    k1, k2, k3 = st.columns(3)

    k1.metric("Actionable candidates", total_candidates)
    k2.metric("Batter candidates", batter_count)
    k3.metric("Bowler candidates", bowler_count)

    st.caption(
        "These counts represent the current preliminary RR candidate "
        "dataset, not confirmed auction availability."
    )

    st.divider()

    # --------------------------------------------------------
    # 5. PRELIMINARY RR FIT RANKING
    # --------------------------------------------------------
    st.markdown("## RR preliminary fit ranking")

    st.write(
        "The following candidates are drawn from the supplementary "
        "RR squad-fit analysis. Historical rank and preliminary fit "
        "are separate measures."
    )

    if not rr_actionable.empty:

        display_table(
            rr_actionable,
            "Preliminary RR Candidate Ranking"
        )

    else:
        st.warning(
            "No actionable candidates are available in the "
            "preliminary fit dataset."
        )

    st.divider()

    # --------------------------------------------------------
    # 6. INTERACTIVE PLAYER SCOUTING
    # --------------------------------------------------------
    st.markdown("## Explore a candidate")

    if (
        not rr_actionable.empty
        and "player_name" in rr_actionable.columns
    ):

        candidate_names = sorted(
            rr_actionable["player_name"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_name = st.selectbox(
            "Select a player to evaluate",
            candidate_names,
            key="rr_strategy_candidate"
        )

        selected_rows = rr_actionable[
            rr_actionable["player_name"].astype(str) == selected_name
        ]

        if not selected_rows.empty:

            player = selected_rows.iloc[0]

            def rr_value(row, column, default="Not available"):
                if column not in row.index:
                    return default

                value = row[column]

                if pd.isna(value) or str(value).strip() == "":
                    return default

                return value

            st.markdown("---")
            st.markdown(f"# {selected_name}")

            role = rr_value(
                player,
                "playing_role",
                rr_value(player, "analysis_category")
            )

            st.caption(f"Playing role: {role}")

            # Separate historical rank and fit score
            historical_rank = rr_value(player, "original_rank")
            historical_score = rr_value(player, "original_score")

            fit_score = rr_value(
                player,
                "preliminary_fit_score",
                rr_value(player, "rr_fit_score")
            )

            m1, m2, m3 = st.columns(3)

            m1.metric(
                "Historical pressure rank",
                str(historical_rank)
            )

            m2.metric(
                "Historical pressure score",
                (
                    f"{float(historical_score):.2f}"
                    if pd.notna(pd.to_numeric(
                        pd.Series([historical_score]),
                        errors="coerce"
                    ).iloc[0])
                    else str(historical_score)
                )
            )

            m3.metric(
                "Preliminary RR fit score",
                (
                    f"{float(fit_score):.2f}"
                    if pd.notna(pd.to_numeric(
                        pd.Series([fit_score]),
                        errors="coerce"
                    ).iloc[0])
                    else str(fit_score)
                )
            )

            st.markdown("## Why this player is being evaluated")

            left, right = st.columns(2)

            with left:
                st.markdown("**Playing role**")
                st.write(role)

                st.markdown("**Squad requirement**")
                st.write(
                    rr_value(
                        player,
                        "rr_squad_gap",
                        "Squad-gap assessment not available"
                    )
                )

            with right:
                st.markdown("**Fit assessment**")
                st.write(
                    rr_value(
                        player,
                        "fit_assessment",
                        "Preliminary candidate for further evaluation"
                    )
                )

                st.markdown("**Fit reasoning**")
                st.write(
                    rr_value(
                        player,
                        "fit_reasoning",
                        "Detailed reasoning pending verification"
                    )
                )

            # Show matching squad-gap record, if available
            if (
                rr_squad_gaps is not None
                and not rr_squad_gaps.empty
                and "player_name" in rr_squad_gaps.columns
            ):

                gap_rows = rr_squad_gaps[
                    rr_squad_gaps["player_name"].astype(str)
                    == selected_name
                ]

                if not gap_rows.empty:
                    st.markdown("### Squad-gap evidence")
                    display_table(
                        gap_rows,
                        f"Squad Requirement: {selected_name}"
                    )

    else:
        st.info(
            "Candidate exploration requires a preliminary "
            "ranking file with a player_name column."
        )

    st.divider()

    # --------------------------------------------------------
    # 7. SQUAD GAP VS PLAYER STRENGTH
    # --------------------------------------------------------
    st.divider()

    st.markdown("## Squad Gap vs Player Strength")

    st.write(
        "Compare the preliminary RR candidate scores across "
        "batting and bowling roles. This helps identify which "
        "candidates deserve further scouting attention."
    )

    if (
        not rr_actionable.empty
        and "analysis_category" in rr_actionable.columns
        and "preliminary_fit_score" in rr_actionable.columns
    ):

        comparison = rr_actionable.copy()

        comparison["preliminary_fit_score"] = pd.to_numeric(
            comparison["preliminary_fit_score"],
            errors="coerce"
        )

        comparison = comparison.dropna(
            subset=["preliminary_fit_score"]
        )

        if not comparison.empty:

            # Separate batting and bowling candidates
            batters = comparison[
                comparison["analysis_category"]
                .astype(str).str.lower().str.contains("batter")
            ].sort_values(
                "preliminary_fit_score",
                ascending=False
            )

            bowlers = comparison[
                comparison["analysis_category"]
                .astype(str).str.lower().str.contains("bowler")
            ].sort_values(
                "preliminary_fit_score",
                ascending=False
            )

            left, right = st.columns(2)

            with left:
                st.markdown("### Batting candidates")

                if not batters.empty:
                    st.bar_chart(
                        batters.set_index("player_name")[
                            ["preliminary_fit_score"]
                        ]
                    )
                else:
                    st.info("No batter scores available.")

            with right:
                st.markdown("### Bowling candidates")

                if not bowlers.empty:
                    st.bar_chart(
                        bowlers.set_index("player_name")[
                            ["preliminary_fit_score"]
                        ]
                    )
                else:
                    st.info("No bowler scores available.")

            st.caption(
                "Scores represent the preliminary RR fit assessment, "
                "not confirmed auction value or player availability."
            )

        else:
            st.info("No valid preliminary fit scores are available.")

    else:
        st.info(
            "The candidate dataset does not contain the required "
            "category and preliminary fit score columns."
        )


    # --------------------------------------------------------
    # 7. PLAYER VERIFICATION
    # --------------------------------------------------------
    st.markdown("## Auction eligibility and verification")

    st.write(
        "A player may have strong historical performance and "
        "potential squad fit without being confirmed as available."
    )

    # Player Verification Tracking
    if rr_verification is not None:

        verification_columns = [
            col for col in [
                "analysis_category",
                "player_name",
                "original_rank",
                "2027_retention_status",
                "auction_registration",
                "nationality"
            ]
            if col in rr_verification.columns
        ]

        if verification_columns:
            display_table(
                rr_verification[verification_columns],
                "Player Verification Tracking"
            )
        else:
            st.info(
                "No matching verification columns were found."
            )

    else:
        st.info(
            "Player Verification Tracking CSV is not available."
        )

    # Squad-Fit Verification
    if rr_squad_verification is not None:

        squad_verification_columns = [
            col for col in [
                "analysis_category",
                "player_name",
                "original_rank",
                "2026_franchise",
                "2027_retention_status",
                "auction_registration",
                "nationality"
            ]
            if col in rr_squad_verification.columns
        ]

        if squad_verification_columns:
            display_table(
                rr_squad_verification[squad_verification_columns],
                "Squad-Fit Verification"
            )
        else:
            st.info(
                "No matching squad-fit verification columns were found."
            )

    else:
        st.info(
            "Separate squad-fit verification file is not available."
        )

    # Important warning
    st.warning(
        "Do not interpret a preliminary fit score as confirmation "
        "of auction registration, retention status or availability. "
        "These require independent official verification."
    )


    # --------------------------------------------------------
    # 8. ELIGIBILITY DISTINCTION
    # --------------------------------------------------------
    st.markdown("## Important eligibility distinction")

    st.info(
        "Pakistan-national players are retained in the official "
        "historical rankings because they are included in the "
        "supplied datapack. They are excluded only from the "
        "separate Rajasthan Royals actionable auction shortlist. "
        "This distinction does not alter the official Round 1 rankings."
    )

    st.markdown("""
    <div class="note">
        <b>Decision principle</b><br>
        Historical pressure performance identifies proven
        performers. Squad-fit analysis identifies potential
        recruitment value. Official availability verification
        determines whether a candidate can actually be pursued.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE 3: RR BATTER RECOMMENDATIONS
# ============================================================
elif page == "RR Batter Recommendations":
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">RAJASTHAN ROYALS · BATTER ANALYSIS</div>
        <h1>RR Batter Scouting</h1>
        <h3>Find the next pressure performer</h3>
        <p>
        Evaluate historical pressure performance, preliminary
        squad fit and auction verification.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if rr_batters is not None:
        st.markdown("## RR Batter Fit Leaderboard")
        ranked = rr_batters.sort_values("category_fit_rank")
        display_columns = [
            "category_fit_rank",
            "player_name",
            "playing_role",
            "original_rank",
            "preliminary_fit_score",
            "rr_squad_gap",
            "auction_availability"
        ]
        st.dataframe(
            ranked[display_columns],
            use_container_width=True,
            hide_index=True
        )
        st.divider()
        show_rr_scouting_profile(
            rr_batters,
            batter_evidence,
            "Batter"
        )
    else:
        st.error("RR batter ranking data not found.")
# ============================================================
# PAGE 4: RR BOWLER RECOMMENDATIONS
# ============================================================
elif page == "RR Bowler Recommendations":
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">RAJASTHAN ROYALS · BOWLING ANALYSIS</div>
        <h1>RR Bowler Scouting</h1>
        <h3>Build a pressure-resistant bowling attack</h3>
        <p>
        Evaluate economy, wicket-taking ability, dot-ball
        performance and squad requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if rr_bowlers is not None:
        st.markdown("## RR Bowler Fit Leaderboard")
        ranked = rr_bowlers.sort_values("category_fit_rank")
        display_columns = [
            "category_fit_rank",
            "player_name",
            "playing_role",
            "original_rank",
            "preliminary_fit_score",
            "rr_squad_gap",
            "auction_availability"
        ]
        st.dataframe(
            ranked[display_columns],
            use_container_width=True,
            hide_index=True
        )
        st.divider()
        show_rr_scouting_profile(
            rr_bowlers,
            bowler_evidence,
            "Bowler"
        )
    else:
        st.error("RR bowler ranking data not found.")
# ============================================================
# PAGE 5: OFFICIAL ROUND 1 RANKINGS
# ============================================================
elif page == "Official Round 1 Rankings":
    st.markdown("""
    <div class="hero">
        <p>OFFICIAL CHALLENGE OUTPUT</p>
        <h1>Round 1 Player Rankings</h1>
        <h3>Most Reliable Players Under Pressure</h3>
        <p>
        Historical IPL and T20I performance rankings
        based on the supplied challenge datapack.
        </p>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2 = st.tabs([
        "Top 10 Batters",
        "Top 10 Bowlers"
    ])
    with tab1:
        display_table(
            official_batters,
            "Official Top 10 Batters"
        )
        if official_batters is not None:
            st.download_button(
                "Download Batter Rankings",
                official_batters.to_csv(index=False),
                file_name="Official_Top10_Batters.csv",
                mime="text/csv"
            )
    with tab2:
        display_table(
            official_bowlers,
            "Official Top 10 Bowlers"
        )
        if official_bowlers is not None:
            st.download_button(
                "Download Bowler Rankings",
                official_bowlers.to_csv(index=False),
                file_name="Official_Top10_Bowlers.csv",
                mime="text/csv"
            )
    st.divider()
    st.markdown("""
    <div class="note">
    <b>Historical ranking policy</b><br>
    These official rankings retain eligible players from the
    supplied datapack irrespective of nationality. The
    Pakistan-national player exclusion applies only to the
    separate Rajasthan Royals auction shortlist.
    </div>
    """, unsafe_allow_html=True)
# ============================================================
# PAGE 6: PRESSURE METHODOLOGY AND VALIDATION
# ============================================================
elif page == "Pressure Methodology & Validation":
    st.markdown("""
    <div class="hero">
        <p>MODEL TRANSPARENCY</p>
        <h1>Pressure Methodology</h1>
        <h3>How Reliability Was Measured</h3>
        <p>
        Separate pressure models, composite scoring,
        validation and ranking robustness.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 1. First-Innings Pressure")
    st.markdown("**Model: Random Forest Regressor**")
    st.write(
        "The model estimates expected score using innings progress, "
        "wickets remaining, balls remaining, maximum legal balls "
        "and match format."
    )
    st.markdown("**Scoring deficit**")
    st.latex(
        r"\text{Scoring Deficit}_{t}"
        r" = \text{Expected Score}_{t}"
        r" - \text{Actual Score}_{t}"
    )
    st.markdown("**Standardisation within match format and innings-progress bands**")
    st.latex(r"z_t = \frac{D_t-\mu_{f,b}}{\sigma_{f,b}}")
    st.success("Pressure condition: standardised scoring deficit z ≥ 1")
    st.caption(
        "D is the scoring deficit; f denotes match format and b denotes "
        "the 10%-wide innings-progress band."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("MAE", "12.9227")
    c2.metric("RMSE", "18.0928")
    c3.metric("R²", "0.8925")
    st.divider()
    st.markdown("## 2. Chase Pressure")
    st.markdown("**Model: Logistic Regression**")
    st.write(
        "The model estimates the batting team's win probability using "
        "required run rate, balls remaining, wickets remaining and match format."
    )
    st.markdown("**Chase win-probability pressure rule**")
    st.latex(
        r"\text{Pressure}_t = "
        r"\mathbb{1}\left(\widehat{P}(\text{Win}_t)\leq 0.20\right)"
    )
    st.success("Pressure condition: predicted chase win probability ≤ 20%")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ROC-AUC", "0.8935")
    c2.metric("Accuracy", "0.8088")
    c3.metric("Brier Score", "0.1349")
    c4.metric("Log Loss", "0.4182")
    st.warning(
        "The two pressure definitions are intentionally different. "
        "Chase-model probabilities are not perfectly calibrated."
    )
    st.divider()
    st.markdown("## 3. Batter Reliability Weights")
    st.caption(
        "40% pressure strike rate + 25% strike-rate improvement + "
        "20% dot-ball avoidance + 15% boundary contribution."
    )
    batter_weights = pd.DataFrame({
        "Weight (%)": [40, 25, 20, 15]
    }, index=[
        "Pressure strike rate",
        "Strike-rate improvement",
        "Dot-ball avoidance",
        "Boundary contribution"
    ])
    st.bar_chart(batter_weights, horizontal=True)
    st.dataframe(
        batter_weights.reset_index(names="Component"),
        hide_index=True,
        use_container_width=True
    )
    st.markdown("## 4. Bowler Reliability Weights")
    st.caption(
        "30% economy performance + 35% wicket-taking performance + "
        "20% dot-ball percentage + 15% boundary control."
    )
    bowler_weights = pd.DataFrame({
        "Weight (%)": [30, 35, 20, 15]
    }, index=[
        "Economy performance",
        "Wicket-taking performance",
        "Dot-ball percentage",
        "Boundary control"
    ])
    st.bar_chart(bowler_weights, horizontal=True)
    st.dataframe(
        bowler_weights.reset_index(names="Component"),
        hide_index=True,
        use_container_width=True
    )
    st.divider()
    st.markdown("## 5. Validation Results")
    display_table(
        validation,
        "Model Validation"
    )
    display_table(
        coverage,
        "Dataset Coverage"
    )
    display_table(
        pressure_robustness,
        "Pressure Threshold Robustness"
    )
    display_table(
        weight_robustness,
        "Component Weight Robustness"
    )
    display_table(
        methodology,
        "Methodology Reference"
    )
    st.divider()
    st.markdown("## Interpretation and Limitations")
    st.write(
        "Minimum sample-size requirements and statistical "
        "shrinkage reduce the influence of small samples. "
        "Sensitivity analysis tests whether the leading "
        "players remain competitive under alternative settings."
    )
    st.write(
        "Composite scores are relative model outputs, not "
        "probabilities of future success. Player rankings "
        "should be interpreted alongside sample sizes, "
        "format differences and the limitations of the data."
    )
# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<div style="text-align:center; color:#64748B; padding:15px;">
    <b>SupeRR Selector Season 2</b><br>
    Identify the Most Reliable Players Under Pressure<br>
    <span style="font-size:12px;">
    Data-driven historical performance analysis ·
    Rajasthan Royals supplementary squad-fit analysis
    </span>
</div>
""", unsafe_allow_html=True)
