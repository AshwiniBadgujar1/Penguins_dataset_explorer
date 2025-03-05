import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load and clean the data
df = sns.load_dataset('penguins')
df = df.dropna()

# Sidebar filters
st.sidebar.header(' Filter Penguins Data')
species_filter = st.sidebar.multiselect(
    'Select Species:', options=df['species'].unique(), default=df['species'].unique()
)
island_filter = st.sidebar.multiselect(
    'Select Island:', options=df['island'].unique(), default=df['island'].unique()
)

# Apply filters
filtered_df = df[(df['species'].isin(species_filter)) & (df['island'].isin(island_filter))]

# Split into Male and Female after filtering
male_penguins = filtered_df[filtered_df['sex'] == 'Male']
female_penguins = filtered_df[filtered_df['sex'] == 'Female']

male_count = len(male_penguins)
female_count = len(female_penguins)

st.title('🐧  Penguins Dataset Explorer')

st.write(f"###  Number of Male Penguins: {male_count}")
st.write(f"###  Number of Female Penguins: {female_count}")
st.write(f"###  Total Filtered Penguins: {len(filtered_df)}")

# Download buttons
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.download_button("⬇️ Download Male Penguins CSV", convert_df_to_csv(male_penguins), "male_penguins.csv", "text/csv")
st.download_button("⬇️ Download Female Penguins CSV", convert_df_to_csv(female_penguins), "female_penguins.csv", "text/csv")

# Create columns for side-by-side charts
col1, col2 = st.columns(2)

# === First chart: Bar chart === #
with col1:
    fig1, ax1 = plt.subplots(figsize=(8, 6))

    bars = ax1.bar(['Male', 'Female'],
                   [male_count, female_count],
                   color=['skyblue', 'lightcoral'],
                   width=0.5,
                   edgecolor='black')

    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + 1, str(height),
                 ha='center', fontsize=12, fontweight='bold')

    ax1.set_xlabel('Sex', fontsize=14)
    ax1.set_ylabel('Count', fontsize=14)
    ax1.set_title('Penguin Count by Sex', fontsize=16, fontweight='bold')

    ax1.set_facecolor('#f7f7f7')
    fig1.patch.set_facecolor('#eaeaf2')

    st.pyplot(fig1)

# === Second chart: Stacked bar chart === #
with col2:
    species_sex_counts = filtered_df.groupby(['species', 'sex']).size().unstack(fill_value=0)

    fig2, ax2 = plt.subplots(figsize=(8, 6))

    species_sex_counts.plot(kind='bar',
                            stacked=True,
                            color=['skyblue', 'lightcoral'],
                            edgecolor='black',
                            ax=ax2)

    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    ax2.set_xlabel('Species', fontsize=14)
    ax2.set_ylabel('Count', fontsize=14)
    ax2.set_title('Species-wise Sex Distribution (Stacked)', fontsize=16, fontweight='bold')

    ax2.set_facecolor('#f9f9f9')
    fig2.patch.set_facecolor('#eaeaf2')

    ax2.legend(title='Sex', title_fontsize=12, fontsize=10)

    st.pyplot(fig2)

# === Extra chart: Pie chart === #
st.write("###  Pie Chart of Sex Distribution")
fig3, ax3 = plt.subplots(figsize=(6, 6))

labels = ['Male', 'Female']
sizes = [male_count, female_count]
colors = ['skyblue', 'lightcoral']

ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
ax3.set_title('Sex Distribution of Penguins', fontsize=16, fontweight='bold')

fig3.patch.set_facecolor('#eaeaf2')

st.pyplot(fig3)
