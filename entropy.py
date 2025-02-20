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
    st.title("クラシックギター曲のエントロピーとスコア計算")
    
    entropy_file_path = "total-entropy.csv"
    
    if os.path.exists(entropy_file_path):
        st.write("### すべてのエントロピーとスコア")
        saved_entropy_df = pd.read_csv(entropy_file_path)
        st.write(saved_entropy_df)
    
    st.write("### 新しいCSVファイルをアップロード")
    uploaded_file = st.file_uploader("CSVファイルを選択", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### アップロードされたデータ")
        st.write(df.head())
        
        columns_to_analyze = ["absolute_pitch", "pitch_class", "duration", "fingering", "string", "fret"]
        entropy_values = {}
        score_values = {}
        
        for col in columns_to_analyze:
            entropy, num_variations, _ = calculate_entropy(df[col].dropna())
            entropy_values[col] = entropy
            score_values[col] = calculate_score(entropy, num_variations)
        
        # スコア計算
        MDS = (score_values["absolute_pitch"] + score_values["pitch_class"] + score_values["duration"]) / 3
        TDS = (score_values["fingering"] + score_values["string"] + score_values["fret"]) / 3
        OverallScore = MDS + TDS
        
        entropy_values.update({
            "file_name": uploaded_file.name,
            "unique_id": str(uuid.uuid4()),
            "MDS": MDS,
            "TDS": TDS,
            "OverallScore": OverallScore
        })
        
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

if __name__ == "__main__":
    main()
