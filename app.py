import streamlit as st
import pandas as pd
import os
from pdf_to_images import convert_pdf_to_images
from gpt_image_parser import parse_cbt_problems_from_images

st.set_page_config(page_title="CBT画像解析アプリ", layout="wide")
st.title("🦷 CBT問題 PDF画像解析アプリ（GPT-4o）")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("secrets.toml に OPENAI_API_KEY を設定してください。")
    st.stop()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("📄 2ページ分のCBT問題PDFをアップロード", type="pdf")

if uploaded_file:
    with st.spinner("PDFを画像に変換中..."):
        images = convert_pdf_to_images(uploaded_file.read())

    with st.spinner("ChatGPTで解析中（少し時間がかかります）..."):
        data = parse_cbt_problems_from_images(images)

    if isinstance(data, list) and "エラー" not in data[0]:
        df = pd.json_normalize(data)
        st.success("✅ 問題の解析に成功しました。")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSVをダウンロード", csv, file_name="cbt_output.csv", mime="text/csv")
    else:
        st.error("❌ 解析中にエラーが発生しました。内容をご確認ください。")
        st.json(data)
else:
    st.info("PDFファイルをアップロードしてください。")