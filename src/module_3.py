# APP TO GET INFO FROM josaa-viz-2.0.py FILE AND INTO THE app_0.py

import streamlit as st
import os
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # current directory
TRUNK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))      # Move up one level to reach the trunk
DATA_FILE = os.path.join(TRUNK_DIR, 'data', 'final_op_cl_seat_info_consolidated_2024_op_cl_with_marks_splitted_coord.csv')
df = pd.read_csv(DATA_FILE)

def filter_data(selected_institutes, selected_institute_category, selected_degrees, selected_clusters, selected_branch, 
                selected_quotas, selected_seat_types, selected_genders):
    
    filtered_df = df.copy()
    
    if 'All' not in selected_institutes:
        filtered_df = filtered_df[filtered_df['Institute'].isin(selected_institutes)]

    if 'All' not in selected_institute_category:
        filtered_df = filtered_df[filtered_df['College Category'].isin(selected_institute_category)]

    if 'All' not in selected_degrees:
        filtered_df = filtered_df[filtered_df['Degree'].isin(selected_degrees)]
    
    if 'All' not in selected_clusters:
        filtered_df = filtered_df[filtered_df['Branch Cluster'].isin(selected_clusters)]
    
    if selected_branch and selected_branch != 'All':
        filtered_df = filtered_df[filtered_df['Branch Name'] == selected_branch]

    if 'All' not in selected_quotas:
        filtered_df = filtered_df[filtered_df['Quota'].isin(selected_quotas)]

    if 'All' not in selected_seat_types:
        filtered_df = filtered_df[filtered_df['Seat Type'].isin(selected_seat_types)]

    if 'All' not in selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    
    return filtered_df

def generate_map(filtered_df):
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7, width='100%', height=800)
    marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"""
            <b>{row['Institute']}</b><br>
            """,
            tooltip=row["Institute"]
        ).add_to(marker_cluster)
    
    return m

def generate_table(filtered_df):
    
    filtered_df = filtered_df.fillna('-')

    features_to_add = ['Institute', 'College Category', 'Program Code', 'Branch Cluster', 'Degree',
                        'Branch Name', 'Degree Duration', 'Seat Capacity (w.r.t. Quota)', 'Aggregated Seats',
                        'Quota', 'Seat Type', 'Gender', 'Rank Range (Mains)', 'Score Range (Mains)', 
                        'Rank Range (Advanced)', 'Score Range (Advanced)', 'View Details']

    return filtered_df[features_to_add].reset_index(drop=True)

def run():

    st.markdown("""
    <div style="border: 2px solid #D0D0D0; padding: 1.5rem; border-radius: 12px; background-color: #F9F9F9; margin-bottom: 1.5rem;">
        <h3 style="margin-top: 0;">Explore Colleges Based on Your Preferences</h3>
        <p>
            Use this tool to discover institutes and branches that align with your <strong>interests, scores, and location preferences</strong>.
        </p>
        <h4 style="margin-bottom: 0.5rem;">How to Use:</h4>
        <ol style="margin-top: 0;">
            <li><strong>Select Filters:</strong> Choose from institute, institute type (IIT/NIT/IIIT/Other GFTIs), degree, branch or branch clusters, quota, and your JEE Mains/Advanced scores or ranks.</li>
            <li><strong>View Results:</strong> You'll get a table of matching institutes and branches based on your filters.</li>
            <li><strong>See on Map:</strong> A dynamic India map shows the locations of these institutes to help you plan better geographically.</li>
        </ol>
        <p style="margin-top: 1rem;"><strong>Start filtering and find the perfect academic fit across India!</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Filters

    institute_options = ['All'] + sorted(list(df['Institute'].unique()))
    institutes = st.multiselect("Select Institute", options=institute_options, default=['All'])

    institute_category_options = ['All'] + sorted(list(df['College Category'].unique()))
    institute_category = st.multiselect("Select Institute Category", options=institute_category_options, default=['All'])

    degree_options = ['All'] + sorted(list(df['Degree'].unique()))
    degrees = st.multiselect("Select Degree", options=degree_options, default=['All'])

    # cluster_options = ['All'] + sorted(list(df['Branch Cluster'].unique()))
    cluster_options = ['All'] + sorted(list(df[df['Degree'].isin(degrees if 'All' not in degrees else df['Degree'].unique())]['Branch Cluster'].unique()))
    clusters = st.multiselect("Select Branch Clusters", options=cluster_options, default=['All'])

    # Filter Branches based on selected Branch Cluster
    branches_under_selected_clusters = ['All'] + sorted(list(df[(df['Branch Cluster'].isin(clusters if 'All' not in clusters else df['Branch Cluster'].unique())) & (df['Degree'].isin(degrees if 'All' not in degrees else df['Degree'].unique()))]['Branch Name'].unique()))
    selected_branch = st.selectbox("Select Branch", options=branches_under_selected_clusters, index=0)

    quota_options = ['All'] + sorted(list(df['Quota'].unique()))
    quotas = st.multiselect("Select Quota", options=quota_options, default=['All'])

    seat_type_options = ['All'] + sorted(list(df['Seat Type'].unique()))
    seat_types = st.multiselect("Select Seat Type", options=seat_type_options, default=['All'])

    gender_options = ['All'] + sorted(list(df['Gender'].unique()))
    genders = st.multiselect("Select Gender", options=gender_options, default=['All'])

    # Convert columns to float, replacing hyphens with NaN
    df.replace('-', np.nan, inplace=True)

    # Define sliders based on available values
    min_rank_mains, max_rank_mains = int(df['Opening Rank (Mains)'].min()), int(df['Closing Rank (Mains)'].max())
    min_score_mains, max_score_mains = int(df['Opening Marks (Mains)'].min()), int(df['Closing Marks (Mains)'].max())

    min_rank_adv, max_rank_adv = int(df['Opening Rank (Advanced)'].min()), int(df['Closing Rank (Advanced)'].max())
    min_score_adv, max_score_adv = int(df['Opening Marks (Advanced)'].min()), int(df['Closing Marks (Advanced)'].max())

    # Mains Filters
    # rank_mains = st.slider("JEE Mains Rank", min_value=min_rank_mains, max_value=max_rank_mains, value=max_rank_mains)
    rank_mains = st.number_input(
        "Enter Rank (Mains):", 
        min_value=min_rank_mains, 
        max_value=max_rank_mains, 
        value=min_rank_mains, 
        step=1
    )
    score_mains = st.number_input(
        "Enter Score (Mains):", 
        min_value=0.0, 
        max_value=100.0, 
        value=float(max_score_mains), 
        step=0.0001
    )

    # Advanced Filters
    # rank_adv = st.slider("JEE Advanced Rank", min_value=min_rank_adv, max_value=max_rank_adv, value=max_rank_adv)
    rank_adv = st.number_input(
        "Enter Rank (Advanced):", 
        min_value=min_rank_adv, 
        max_value=max_rank_adv, 
        value=max_rank_adv, 
        step=1
    )
    score_adv = st.number_input(
        "Enter Score (Advanced):", 
        min_value=min_score_adv, 
        max_value=max_score_adv, 
        value=min_score_adv, 
        step=1
    )

    # Apply filters

    filtered_df_categ = filter_data(institutes, institute_category, degrees, clusters, selected_branch, quotas, seat_types, genders)

    filtered_df = filtered_df_categ[
        ((filtered_df_categ['Closing Rank (Advanced)'] >= rank_adv) | filtered_df_categ['Closing Rank (Advanced)'].isna()) &
        ((filtered_df_categ['Closing Rank (Mains)'] >= rank_mains) | filtered_df_categ['Closing Rank (Mains)'].isna()) &
        ((filtered_df_categ['Opening Marks (Advanced)'] <= score_adv) | filtered_df_categ['Opening Marks (Advanced)'].isna()) &
        ((filtered_df_categ['Opening Marks (Mains)'] <= score_mains) | filtered_df_categ['Opening Marks (Mains)'].isna())
    ]

    unique_colleges = filtered_df[['Institute', 'Latitude', 'Longitude']].drop_duplicates()

    st.subheader("Filtered Colleges")

    st.markdown("**View in Map:**")
    map_button = st.button("Map")

    st.markdown("**Filtered Data Table:**")
    table_button = st.button("Table")

    if map_button:
        folium_static(generate_map(unique_colleges))

    if table_button:
        st.dataframe(generate_table(filtered_df))