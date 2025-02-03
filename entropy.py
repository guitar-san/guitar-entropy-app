import streamlit as st
import pandas as pd
import numpy as np
import os

# エントロピー計算関数
def calculate_entropy(series):
    value_counts = series.value_counts(normalize=True)
    return -np.sum(value_counts * np.log2(value_counts))

# メイン関数
def main():
    st.title("クラシックギター曲のエントロピー計算")
    st.write("CSVファイルをアップロードしてください。")
    
    # ファイルアップロード
    uploaded_file = st.file_uploader("CSVファイルをドロップまたは選択", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### アップロードされたデータ")
        st.write(df.head())
        
        # 計算対象のカラム
        columns_to_analyze = ["absolute_pitch", "pitch_class", "duration", "fingering", "string"]
        entropy_values = {col: calculate_entropy(df[col].dropna()) for col in columns_to_analyze}
        entropy_df = pd.DataFrame([entropy_values])
        
        # 結果の表示
        st.write("### 計算されたエントロピー値")
        st.write(entropy_df)
        
        # ファイルの保存
        entropy_file_path = "total-entropy.csv"
        if os.path.exists(entropy_file_path):
            existing_entropy_df = pd.read_csv(entropy_file_path)
            updated_entropy_df = pd.concat([existing_entropy_df, entropy_df], ignore_index=True)
        else:
            updated_entropy_df = entropy_df
        
        updated_entropy_df.to_csv(entropy_file_path, index=False)
        st.success("エントロピー値を `total-entropy.csv` に保存しました！")
        
        # ダウンロードリンク
        st.download_button(
            label="エントロピーCSVをダウンロード",
            data=updated_entropy_df.to_csv(index=False).encode("utf-8"),
            file_name="total-entropy.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
