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
    
    # 情報量を算出（底2の対数を使用）
    information_values = -probabilities * np.log2(probabilities)
    entropy = information_values.sum()
    
    return entropy, len(value_counts)

# スコア計算関数（S = I * log₂(1 + V)）
def calculate_score(entropy, num_variations):
    return entropy * np.log2(1 + num_variations)

# メイン関数
def main():
    st.title("楽曲の定量スコア算出アプリ")
    
    entropy_file_path = "total-entropy.csv"
    
    # 全データを削除するボタン
    if st.button("全データを削除"):
        if os.path.exists(entropy_file_path):
            os.remove(entropy_file_path)
            st.success("全てのデータを削除しました！")
            st.experimental_rerun()
        else:
            st.warning("削除するデータがありません。")
    
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
    
        # 個別データ削除ボタン
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
                entropy, num_variations = calculate_entropy(df[col].dropna())
                entropy_values[entropy_col_name] = entropy
                score_values[col] = calculate_score(entropy, num_variations)
        
        # スコア計算（S = I × log₂(1 + V) を正しく適用）
        entropy_values["MDS"] = sum(score_values.get(col, 0) for col in ["absolute_pitch", "pitch_class", "duration"]) / 3
        entropy_values["TDS"] = sum(score_values.get(col, 0) for col in ["fingering", "string", "fret"]) / 3
        entropy_values["OverallScore"] = entropy_values["MDS"] + entropy_values["TDS"]
        
        entropy_df = pd.DataFrame([entropy_values])
        
        # カラムの順序を統一（エントロピー → スコア）
        ordered_columns = ["file_name", "unique_id"] + [col + "_entropy" for col in columns_to_analyze] + ["MDS", "TDS", "OverallScore"]
        entropy_df = entropy_df.reindex(columns=ordered_columns)
        
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
