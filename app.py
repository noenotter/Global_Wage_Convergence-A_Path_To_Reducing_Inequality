import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO

# --- Configuration ---
MODE_OPTIONS = ['Linear only', 'Best-model (original)']
SCENARIOS = ['Low', 'Medium', 'High']
THRESHOLDS = ['70', '80', '90']

# --- Sidebar ---
st.sidebar.title("Settings")
mode = st.sidebar.radio("Select mode:", MODE_OPTIONS)

# Determine file suffixes based on mode
suffix = '_linear' if mode == 'Linear only' else ''

# --- Load Data ---
conv_path = f"Result/V30_convergers_low70{suffix}.csv"
div_path  = f"Result/V30_divergers_low70{suffix}.csv"
df_conv = pd.read_csv(conv_path)
df_div  = pd.read_csv(div_path)
df = pd.concat([df_conv, df_div], ignore_index=True)
df['country'] = df['country'].str.strip()

# --- Country Selection ---
st.sidebar.subheader("Country Group")
group = st.sidebar.radio("Filter by group:", ['All', 'Convergers only', 'Divergers only'])
if group == 'Convergers only':
    countries = sorted(df_conv['country'].unique())
elif group == 'Divergers only':
    countries = sorted(df_div['country'].unique())
else:
    countries = sorted(df['country'].unique())
selected_country = st.sidebar.selectbox("Select a country:", countries)

# --- Scenario & Threshold ---
st.sidebar.subheader("Scenario & Threshold")
growth = st.sidebar.selectbox("Growth scenario:", SCENARIOS)
threshold = st.sidebar.selectbox("Threshold (%):", THRESHOLDS)
col_key = f"{growth[0]}-{threshold}"

# --- Main ---
st.title("Wage Convergence Explorer")
st.write(f"**Mode:** {mode}")
row = df[df['country'] == selected_country]
if row.empty:
    st.warning(f"No data for {selected_country} in this mode.")
else:
    result = row.iloc[0][col_key]
    gap_2080 = row.iloc[0]['gap_low_2080']
    if mode == 'Best-model (original)':
        best_model = row.iloc[0]['best_model']
        mse = row.iloc[0]['cv_mse']
    
    if result == 'X':
        st.error(f"❌ {selected_country} does not converge under {growth}/{threshold}%.")
    else:
        st.success(f"✅ Converges in **{int(result)}** under {growth}/{threshold}%.")
    
    st.markdown(f"- **Gap in 2080**: {gap_2080}")
    if mode == 'Best-model (original)':
        st.markdown(f"- **Best model**: {best_model}")
        st.markdown(f"- **CV MSE**: {mse}")

    # Display plot
    plot_name = f"{selected_country.replace(' ', '_')}{suffix}.png"
    plot_path = os.path.join('Result', plot_name)
    if os.path.exists(plot_path):
        image = Image.open(plot_path)
        st.image(image, caption=selected_country, use_column_width=True)
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        st.download_button("Download chart", data=buf,
                            file_name=f"{selected_country}_convergence{suffix}.png",
                            mime="image/png")
    else:
        st.info("Plot not available.")

# --- Comparison Mode ---
st.markdown("---")
compare = st.checkbox("Enable comparison mode")
if compare:
    mult = st.multiselect("Select up to 4 countries:", countries, max_selections=4)
    cols = st.columns(2)
    for idx, country in enumerate(mult):
        name = f"{country.replace(' ', '_')}{suffix}.png"
        path = os.path.join('Result', name)
        col = cols[idx % 2]
        if os.path.exists(path):
            img = Image.open(path)
            col.image(img, caption=country, use_column_width=True)
        else:
            col.warning(f"No plot for {country}")
