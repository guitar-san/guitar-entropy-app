# 再計算のための関数
def compute_entropy_debug(series):
    value_counts = series.value_counts(normalize=True)
    entropy = -np.sum(value_counts * np.log2(value_counts))
    return entropy, value_counts  # 各カテゴリの確率分布も確認

# 各カラムのエントロピーを再計算
entropy_debug = {}
value_distributions = {}

for col in ["absolute_pitch", "pitch_class"]:
    entropy_debug[col], value_distributions[col] = compute_entropy_debug(df[col].dropna())

# 結果を表示
entropy_debug
