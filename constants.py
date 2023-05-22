# miniLOTO次回予測プログラム用定数定義
# 作成日: 2023/04/30
# 更新日: 2023/05/06

# くじのタイプ
LOTO = "MLOTO"

# miniLOTOの過去データファイル
LOTO_DATA_FILE = "miniloto.csv"

# miniLOTOの最大値
LOTO_MAX = 31

# miniLOTOの最小値
LOTO_MIN = 1

# miniLOTOの数字の個数
LOTO_NUM = 5

# miniLOTOのボーナス数字の個数
LOTO_B_NUM = 1

# miniLOTOの曜日
LOTO_WEEKDAY = 1

# miniLOTO購入金額
LOTO_PRICE = 200

# miniLOTO当選等級の個数
LOTO_MAX_PRIZE = 4

# miniLOTO当選金額
LOTO_1ST_PRIZE = 10000000
LOTO_2ND_PRIZE = 150000
LOTO_3RD_PRIZE = 10000
LOTO_4TH_PRIZE = 1000

# PandasのDataFrameの列名
LOTO_COL_NAME = ["TIMES", "DATE", "N1", "N2", "N3", "N4", "N5", "BN"]