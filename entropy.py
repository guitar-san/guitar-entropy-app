import streamlit as st
import pandas as pd
import numpy as np
import os
import uuid

# エントロピー計算関数
def calculate_entropy(series):
    value_counts = series.value_counts()
    total_count = len(series)
    probabilities = value_counts / total_count
    
    # 情報量を算出
    information_values = -probabilities * np.log2(probabilities)
    entropy = information_values.sum()
    
    return entropy, len(value_counts), information_values.sum()

# スコア計算関数
def calculate_score(entropy, num_variations):
    return entropy * np.log(1 + num_variations)

# メイン関数
def main():
    st.title("楽曲の平均情報量及び音楽的・技術的スコアの算出アプリ")
    
    entropy_file_path = "total-entropy.csv"
    
    # データ破損時のリカバリ用
    if "reset" in st.query_params:
        if os.path.exists(entropy_file_path):
            os.remove(entropy_file_path)
        st.experimental_rerun()
    
    if os.path.exists(entropy_file_path):
        st.write("### すべてのエントロピーとスコア")
        try:
            saved_entropy_df = pd.read_csv(entropy_file_path)
            st.write(saved_entropy_df)
        except Exception:
            st.error("保存されたデータが壊れています。リセットしてください。")
            if st.button("データをリセット"):
                os.remove(entropy_file_path)
                st.experimental_rerun()
            return
    
        # 削除したいデータの選択
        if not saved_entropy_df.empty:
            file_names = saved_entropy_df["file_name"].unique().tolist()
            selected_file = st.selectbox("削除するデータを選択", file_names)
            if st.button("選択したデータを削除"):
                saved_entropy_df = saved_entropy_df[saved_entropy_df["file_name"] != selected_file]
                saved_entropy_df.to_csv(entropy_file_path, index=False)
                st.success(f"{selected_file} のデータを削除しました。")
                st.experimental_rerun()
    
    st.write("### 新しいCSVファイルをアップロード")
    uploaded_file = st.file_uploader("CSVファイルを選択", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### アップロードされたデータ")
            st.write(df.head())
        except Exception:
            st.error("ファイルの読み込みに失敗しました。正しいCSVファイルをアップロードしてください。")
            return
        
        columns_to_analyze = ["absolute_pitch", "pitch_class", "duration", "fingering", "string", "fret"]
        existing_columns = [col for col in columns_to_analyze if col in df.columns]
        missing_columns = [col for col in columns_to_analyze if col not in df.columns]
        
        if missing_columns:
            st.warning(f"以下のカラムがデータに存在しません: {', '.join(missing_columns)}")
        
        entropy_values = {"file_name": uploaded_file.name, "unique_id": str(uuid.uuid4())}
        score_values = {}
        
        for col in existing_columns:
            entropy_col_name = col + "_entropy"
            if entropy_col_name not in df.columns:
                entropy, num_variations, _ = calculate_entropy(df[col].dropna())
                entropy_values[entropy_col_name] = entropy
                score_values[col] = calculate_score(entropy, num_variations)
        
        # スコア計算（存在するカラムのみ）
        if all(k in score_values for k in ["absolute_pitch", "pitch_class", "duration"]):
            entropy_values["MDS"] = (score_values["absolute_pitch"] + score_values["pitch_class"] + score_values["duration"]) / 3
        else:
            entropy_values["MDS"] = None
        
        if all(k in score_values for k in ["fingering", "string", "fret"]):
            entropy_values["TDS"] = (score_values["fingering"] + score_values["string"] + score_values["fret"]) / 3
        else:
            entropy_values["TDS"] = None
        
        if entropy_values["MDS"] is not None and entropy_values["TDS"] is not None:
            entropy_values["OverallScore"] = entropy_values["MDS"] + entropy_values["TDS"]
        else:
            entropy_values["OverallScore"] = None
        
        entropy_df = pd.DataFrame([entropy_values])
        
        # 既存データと統合
        if os.path.exists(entropy_file_path):
            existing_entropy_df = pd.read_csv(entropy_file_path)
            updated_entropy_df = pd.concat([existing_entropy_df, entropy_df], ignore_index=True)
        else:
            updated_entropy_df = entropy_df
        
        updated_entropy_df.to_csv(entropy_file_path, index=False)
        st.success("エントロピーとスコアを保存しました！")
        st.write(updated_entropy_df)
    
    if os.path.exists(entropy_file_path):
        st.download_button(
            label="エントロピーとスコアCSVをダウンロード",
            data=pd.read_csv(entropy_file_path).to_csv(index=False).encode("utf-8"),
            file_name="total-entropy.csv",
            mime="text/csv"
        )

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if __name__ == "__main__":
    main()
