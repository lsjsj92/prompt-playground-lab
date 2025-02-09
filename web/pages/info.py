import streamlit as st

from PIL import Image

from config import load_config

config = load_config()


st.title("Prompt 관리 서비스 정보")
st.json(config.page_desc)
st.json(config.poc_env_info)
st.json(config.dev_info_desc)
