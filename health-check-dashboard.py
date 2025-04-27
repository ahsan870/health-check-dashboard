import streamlit as st
import asyncio
import httpx
import time
import json
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import urljoin

# Load .env file
load_dotenv()

# Load config.json
with open("config.json") as f:
    config = json.load(f)

base_urls = config["base_urls"]
env_urls = config["env_urls"]

# Customize tab names here
env_display_names = {
    "dev": "DEV",
    "sit": "SIT",
    "uat": "UAT",
    "prod": "PROD",
    # Add more if you have more environments
}

# Set Streamlit page config
st.set_page_config(page_title="🩺 Health Check Dashboard", layout="wide")
st.title("🩺 Health Check Dashboard")
status_placeholder = st.empty()

# Async function to fetch service status
async def fetch_status(client, env, svc):
    url = urljoin(base_urls[env], svc["path"])  # Safe URL joining

    # Fetch credentials from environment variables
    username = os.getenv(f"{env.upper()}_USERNAME")
    password = os.getenv(f"{env.upper()}_PASSWORD")
    auth = (username, password) if username and password else None

    try:
        response = await client.get(
            url,
            timeout=5.0,
            follow_redirects=False,
            auth=auth,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        is_up = response.status_code == 200
    except Exception as e:
        print(f"Error checking {url}: {e}")
        is_up = False

    return {
        "Environment": env,
        "Service Name": svc["name"],
        "Endpoints": url,
        "Status": "🟢 UP" if is_up else "🔴 DOWN"
    }

# Async function to check all services
async def check_services_async():
    async with httpx.AsyncClient() as client:
        tasks = []
        for env, services in env_urls.items():
            for svc in services:
                tasks.append(fetch_status(client, env, svc))
        result = await asyncio.gather(*tasks)
    return result

# Main health check loop
def run_health_check_loop():
    while True:
        check_time = time.strftime('%Y-%m-%d %H:%M:%S')
        statuses = asyncio.run(check_services_async())

        df = pd.DataFrame(statuses)

        with status_placeholder.container():
            st.write(f"Last Checked: {check_time}")

            # Prepare tabs with custom display names
            environments = df["Environment"].unique().tolist()
            tab_labels = [env_display_names.get(env, env.upper()) for env in environments]
            tabs = st.tabs(tab_labels)

            for env, tab in zip(environments, tabs):
                env_df = df[df["Environment"] == env].copy()

                # Optional: Sort DOWN first
                env_df["SortOrder"] = env_df["Status"].apply(lambda x: 0 if "DOWN" in x else 1)
                env_df = env_df.sort_values("SortOrder").drop(columns=["SortOrder"]).reset_index(drop=True)

                # Color the 'Status' column
                def color_status(val):
                    if "UP" in val:
                        return 'background-color: #d4edda; color: green; font-weight: bold'
                    else:
                        return 'background-color: #f8d7da; color: red; font-weight: bold'

                styled_env_df = env_df.style.applymap(color_status, subset=["Status"])

                with tab:
                    st.subheader(f"Environment: {env_display_names.get(env, env.upper())}")
                    st.dataframe(styled_env_df, use_container_width=True)

                    # 🎯 Download CSV for this environment
                    csv_text = f"Last Checked: {check_time}\n\n"
                    csv_text += env_df.to_csv(index=False)

                    st.download_button(
                        label=f"⬇️ Download {env_display_names.get(env, env.upper())} Report CSV",
                        data=csv_text.encode('utf-8'),
                        file_name=f'{env}_health_check_report_{check_time.replace(" ", "_").replace(":", "-")}.csv',
                        mime='text/csv',
                    )

        time.sleep(60)

# Streamlit session state trick
if 'started' not in st.session_state:
    st.session_state.started = True
    run_health_check_loop()
