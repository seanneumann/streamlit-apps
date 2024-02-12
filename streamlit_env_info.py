"""
Streamlit Environment Info

App to quickly display Streamlit Environment

streamlit_env_info.py
v0.1.0 11 
February 2024

Author:
    @seanneumann : https://github.com/seanneumann

"""

import streamlit as st
import platform
import pandas as pd
import os
import pkg_resources
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_platform_info():
    info = {}
    default_system = platform.system()
    default_release = platform.release()
    default_version = platform.version()

    attributes = [attr for attr in dir(platform) if callable(getattr(platform, attr)) and not attr.startswith('_')]
    for attr in attributes:
        try:
            if attr == 'system_alias':
                value = platform.system_alias(default_system, default_release, default_version)
            else:
                value = getattr(platform, attr)()

            if not value:
                value = "N/A"  # Placeholder for empty values

            if isinstance(value, (str, int, float)) and len(str(value)) < 100:
                info[attr] = value
        except Exception as e:
            logger.error(f"Error processing attribute {attr}: {e}")
            info[attr] = "Error encountered"
    return info

def get_installed_packages():
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def display_data_in_tabs(data, columns, sort_keys=False):
    table_tab, json_tab = st.tabs(["Table", "JSON"])
    
    with table_tab:
        st.dataframe(data, use_container_width=True, hide_index=True)
    
    with json_tab:
        # Convert the DataFrame to a list of dicts, which is serializable
        data_records = data.to_dict('records')
        json_data = json.dumps(data_records, indent=4, sort_keys=sort_keys)
        st.code(json_data, language='json')


st.title('Streamlit Environment Info')

# Display Streamlit version
streamlit_version = st.__version__
st.write(f"Streamlit: {streamlit_version}")

# Platform information
st.header("Platform")
platform_info = get_platform_info()
platform_info_df = pd.DataFrame(list(platform_info.items()), columns=['Property', 'Value'])
display_data_in_tabs(platform_info_df, ['Property', 'Value'])

# Environment variables
st.header("Environment")
env_variables_df = pd.DataFrame(list(os.environ.items()), columns=['Variable', 'Value'])
display_data_in_tabs(env_variables_df, ['Variable', 'Value'])

# Installed packages
st.header("Packages")
installed_packages = get_installed_packages()
packages_df = pd.DataFrame(list(installed_packages.items()), columns=['Package', 'Version'])
display_data_in_tabs(packages_df, ['Package', 'Version'])
