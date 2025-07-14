import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO

# Title and intro
st.title("Wage Convergence Explorer")
st.write("""
Welcome! This app will help you explore wage convergence projections.
Use the sidebar to select a country, growth scenario, and convergence threshold.
""")

# Load both convergers and divergers files
df_conv = pd.read_csv("Result/V30_convergers_low70.csv")
df_div = pd.read_csv("Result/V30_divergers_low70.csv")
df = pd.concat([df_conv, df_div], ignore_index=True)
df['country'] = df['country'].str.strip()

# === Country Selection (Grouped Dropdown with Filter) ===
st.sidebar.subheader("Country selection mode")
country_group = st.sidebar.radio("Filter by group:", ['All', 'Convergers only', 'Divergers only'])

if country_group == 'Convergers only':
    filtered_countries = sorted(df_conv['country'].unique())
elif country_group == 'Divergers only':
    filtered_countries = sorted(df_div['country'].unique())
else:
    filtered_countries = sorted(df['country'].unique())

selected_country = st.sidebar.selectbox("Select a country:", filtered_countries)

# === Scenario Selection ===
growth = st.sidebar.selectbox("Select growth scenario:", ['Low', 'Medium', 'High'])
threshold = st.sidebar.selectbox("Select convergence threshold:", ['70', '80', '90'])
column = f"{growth[0]}-{threshold}"

# === Main Output ===
row = df[df['country'] == selected_country]

if row.empty:
    st.warning(f"No data found for {selected_country}.")
else:
    result = row.iloc[0][column]
    gap_2080 = row.iloc[0]['gap_low_2080']
    best_model = row.iloc[0]['best_model']
    mse = row.iloc[0]['cv_mse']

    if result == 'X':
        st.error(f"❌ {selected_country} does **not** converge under {growth} growth with {threshold}% threshold.")
    else:
        st.success(f"✅ {selected_country} is projected to converge in **{int(result)}** under {growth} growth with {threshold}% threshold.")

    st.markdown(f"""
    - **Gap to OECD in 2080**: {gap_2080}
    - **Best model**: {best_model}
    - **Cross-validated MSE**: {mse}
    """)

    # Load and display plot
    img_path = f"Result/Plots/{selected_country}.png"
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, caption=f"Projected convergence for {selected_country}", use_column_width=True)

        # Convert image to bytes and offer download
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        st.download_button(
            label="📥 Download this chart as PNG",
            data=img_bytes,
            file_name=f"{selected_country}_convergence_plot.png",
            mime="image/png"
        )
    else:
        st.info("No convergence plot available for this country.")

# === Compare Countries Mode ===
st.markdown("---")
st.subheader("📊 Compare Multiple Countries")

compare_mode = st.checkbox("Enable comparison mode")

if compare_mode:
    compare_list = st.multiselect(
        "Select up to 4 countries to compare:",
        sorted(df['country'].unique()),
        max_selections=4
    )

    col1, col2 = st.columns(2)
    for i, country in enumerate(compare_list):
        img_path = f"Result/Plots/{country}.png"
        if os.path.exists(img_path):
            image = Image.open(img_path)
            with (col1 if i % 2 == 0 else col2):
                st.image(image, caption=country, use_column_width=True)
        else:
            st.warning(f"No plot available for {country}")
