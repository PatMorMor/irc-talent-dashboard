"""
IRC Talent Dashboard
Run with: streamlit run dashboard.py
"""
import streamlit as st
import sqlite3
import pandas as pd
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "talentmap.db")
PHOTOS_DIR = os.path.join(BASE_DIR, "Our people __ IRC_files")

st.set_page_config(
    page_title="IRC Talent Dashboard",
    page_icon="💧",
    layout="wide",
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .person-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid #0077b6;
    }
    .person-name { font-size: 1.1rem; font-weight: 700; color: #0077b6; }
    .person-title { font-size: 0.9rem; color: #444; margin-top: 2px; }
    .person-meta { font-size: 0.8rem; color: #888; margin-top: 4px; }
    .bio-text { font-size: 0.85rem; color: #333; margin-top: 8px; line-height: 1.5; }
    .tag { display: inline-block; background: #e0f0ff; color: #0077b6;
           border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; margin: 2px; }
    .highlight { background-color: #fff3cd; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM people ORDER BY name", conn)
    conn.close()
    return df

df = load_data()

DIVISIONS = {
    100: "Netherlands (HQ)",
    200: "Ghana",
    300: "Sahel",
    400: "Uganda",
    500: "Ethiopia",
}

def division_label(d):
    try:
        d = int(d)
        return f"Div {d} — {DIVISIONS.get(d, 'Other')}"
    except (TypeError, ValueError):
        return "Unknown"

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("💧 IRC Talent Dashboard")
st.sidebar.markdown("---")

search = st.sidebar.text_input("🔍 Search (name, bio, expertise...)", "")

st.sidebar.markdown("**Filter by Division**")
div_options = ["All"] + [f"Div {k} — {v}" for k, v in DIVISIONS.items()]
selected_div = st.sidebar.selectbox("Division", div_options)

st.sidebar.markdown("**Filter by Level**")
LEVEL_ORDER = ["Leader", "Senior Expert", "Junior Expert", "Support"]
level_options = [l for l in LEVEL_ORDER if l in df['level'].values]
selected_level_groups = st.sidebar.multiselect("Level (leave blank = all)", level_options)

st.sidebar.markdown("**Filter by Category**")
all_cats = sorted([c for c in df['category'].dropna().unique()])
selected_cats = st.sidebar.multiselect("Category (leave blank = all)", all_cats)

st.sidebar.markdown("**Filter by Source**")
source_opt = st.sidebar.radio("Show", ["All", "Staff only (in organigram)", "Staff and Associates", "Board"])

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(df)} people total** in database")

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()

# Source filter
is_board = filtered['web_title'].fillna('').str.contains('Supervisory Board', case=False)
if source_opt == "Staff only (in organigram)":
    filtered = filtered[filtered['in_excel'] == 1]
elif source_opt == "Staff and Associates":
    filtered = filtered[(filtered['in_excel'] == 1) | ((filtered['in_excel'] == 0) & ~is_board)]
elif source_opt == "Board":
    filtered = filtered[is_board]

# Division filter
if selected_div != "All":
    div_num = int(selected_div.split(" ")[1])
    filtered = filtered[filtered['division'] == div_num]

# Category filter
if selected_cats:
    filtered = filtered[filtered['category'].isin(selected_cats)]

# Level filter
if selected_level_groups:
    filtered = filtered[filtered['level'].isin(selected_level_groups)]

# Search filter — split into tokens so each word matched independently
# "water resource management" matches "water resources management" etc.
if search:
    tokens = [t for t in search.lower().split() if t]
    for token in tokens:
        mask = (
            filtered['name'].fillna('').str.lower().str.contains(token) |
            filtered['bio'].fillna('').str.lower().str.contains(token) |
            filtered['function'].fillna('').str.lower().str.contains(token) |
            filtered['role'].fillna('').str.lower().str.contains(token) |
            filtered['web_title'].fillna('').str.lower().str.contains(token) |
            filtered['category'].fillna('').str.lower().str.contains(token) |
            filtered['unit'].fillna('').str.lower().str.contains(token)
        )
        filtered = filtered[mask]

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("IRC Talent Finder")

col_summary, col_space = st.columns([3, 1])
with col_summary:
    st.markdown(f"Showing **{len(filtered)}** people" +
                (f" matching **'{search}'**" if search else ""))

st.markdown("---")

if filtered.empty:
    st.info("No people match your current filters.")
else:
    # Two-column layout for cards
    cols = st.columns(2)
    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 2]:
            # Photo
            photo_col, text_col = st.columns([1, 3])
            with photo_col:
                photo_path = None
                if pd.notna(row.get('photo_file')) and row['photo_file']:
                    candidate = os.path.join(PHOTOS_DIR, row['photo_file'])
                    if os.path.exists(candidate):
                        photo_path = candidate
                if photo_path:
                    try:
                        img = Image.open(photo_path)
                        st.image(img, width=80)
                    except Exception:
                        st.markdown("👤")
                else:
                    st.markdown("<div style='font-size:3rem;text-align:center'>👤</div>",
                                unsafe_allow_html=True)

            with text_col:
                # Name (highlighted if search match)
                name = row['name'] or ''
                st.markdown(f"<div class='person-name'>{name}</div>", unsafe_allow_html=True)

                # Title: prefer Excel function, fall back to web title
                title = row.get('function') or row.get('web_title') or ''
                if title:
                    st.markdown(f"<div class='person-title'>{title}</div>", unsafe_allow_html=True)

                # Meta: division + level
                meta_parts = []
                if pd.notna(row.get('division')):
                    meta_parts.append(division_label(row['division']))
                if pd.notna(row.get('level')):
                    meta_parts.append(str(row['level']))
                if pd.notna(row.get('unit')) and row['unit']:
                    meta_parts.append(str(row['unit']))
                if meta_parts:
                    st.markdown(f"<div class='person-meta'>{' · '.join(meta_parts)}</div>",
                                unsafe_allow_html=True)

                # Source badges
                badges = []
                if row.get('in_excel'): badges.append("📋 Organigram")
                if row.get('on_web'): badges.append("🌐 Web profile")
                if badges:
                    st.markdown(" ".join(f"<span class='tag'>{b}</span>" for b in badges),
                                unsafe_allow_html=True)

            # Bio (expandable)
            bio = row.get('bio') or ''
            if bio and len(bio) > 20:
                with st.expander("Bio"):
                    # Highlight search term in bio
                    if search:
                        import re
                        highlighted = re.sub(
                            f'({re.escape(search)})',
                            r'<mark>\1</mark>',
                            bio[:1500],
                            flags=re.IGNORECASE
                        )
                        st.markdown(highlighted, unsafe_allow_html=True)
                    else:
                        st.write(bio[:1500])
                    if row.get('profile_url'):
                        st.markdown(f"[Full profile on IRC website]({row['profile_url']})")

            st.markdown("<hr style='margin:8px 0;border:none;border-top:1px solid #eee'>",
                        unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("IRC Talent Dashboard · Data from organigram (Organigram 2026_v2.xlsx) + ircwash.org profiles · April 2026")
