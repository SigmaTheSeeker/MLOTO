#  MiniLOTO次回予測プログラム
# 作成日: 2024/05/01

import loto as lt
import constants as const
import numpy as np
import pprint as pp
import itertools


def main():
    # 全組合せの作成
    all_loto = lt.all_loto_combinations()
    # 全組合せの集計(合計値)
    all_sum_count = lt.sum_count(all_loto)
    # 全組合せの集計(偶数奇数)
    all_even_odd = lt.even_odd_count(lt.get_even_odd(all_loto))
    #  全組合せの集計(連番)
    all_seq = lt.seq_count(all_loto)

    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[:, 2:const.LOTO_NUM + 2].astype(np.uint8)

    # ロトの過去データの集計(合計値)
    loto_sum_count = lt.sum_count(loto_num_data)

    # ロトの過去データの集計(偶数奇数)
    loto_even_odd_count = lt.even_odd_count(lt.get_even_odd(loto_num_data))

    # ロトの過去データの集計(連番)
    loto_seq_count = lt.seq_count(loto_num_data)

    # ロトの過去データの集計開始インデックス
    loto_start_index = 25
    n_count_range = 25
    n_past_range = 5

    # 集計領域
    hit_sum_count = {}

    # 集計用のインデックを作成
    hit_combination = {(i, j, k, l, m): 0 for i in range(const.LOTO_NUM + 1) for j in range(const.LOTO_NUM + 1) for k in range(const.LOTO_NUM + 1) for l in range(const.LOTO_NUM + 1) for m in range(const.LOTO_NUM + 1) if i + j + k + l + m == const.LOTO_NUM}

    # 25回分のデータを抽出
    for i in range(loto_start_index, len(loto_data)):
        n25_loto_num_data = loto_num_data[i - n_count_range:i, :]
        n5_loto_num_data = loto_num_data[i - n_past_range:i, :]
        n1_loto_num_data = loto_num_data[i- 1:i, :]
        n1_loto_num_data = n1_loto_num_data[0]
        next_loto_data = loto_num_data[i:i + 1, :]
        next_loto_data = next_loto_data[0]

        # ロトの過去データの集計(各数字の出現回数)
        loto_number_count = lt.number_count(n25_loto_num_data)

        # 抽選用数字の作成
        # 最後から5回分のデータを使用
        num_in_past = lt.num_in_past(n5_loto_num_data)

        english_loto_numbers = lt.english_calculator(n1_loto_num_data)

        serial_loto_numbers = lt.serial_calculator(n1_loto_num_data)

        # 共通部分の抽出
        common_loto_numbers = set(num_in_past) & set(english_loto_numbers)
        common_loto_numbers = set(common_loto_numbers) - set(serial_loto_numbers)
        common_loto_numbers = sorted(list(common_loto_numbers))

        # 差集合の作成
        num_in_past_only = sorted(list(set(num_in_past) - set(english_loto_numbers) - set(serial_loto_numbers)))
        english_loto_numbers_only = sorted(list(set(english_loto_numbers) - set(num_in_past) - set(serial_loto_numbers)))
        serial_loto_numbers_only = set(serial_loto_numbers)


        # 抽出されなかった数字を抽出
        loto_all_numbers = [i for i in range(const.LOTO_MIN, const.LOTO_MAX + 1)]
        loto_numbers_only = sorted(list(set(loto_all_numbers) - set(common_loto_numbers) - set(num_in_past_only) - set(english_loto_numbers_only) - set(serial_loto_numbers_only)))


        # 集計処理
        # 合計値
        temp_sum_count = 0
        for num in next_loto_data:
            if num in loto_number_count:
                temp_sum_count += loto_number_count[num]

        hit_sum_count.setdefault(temp_sum_count, 1)
        hit_sum_count[temp_sum_count] += 1

        # 各集合に数字の含まれる割合
        temp_common = len(set(common_loto_numbers) & set(next_loto_data))
        temp_num_in_past_only = len(set(num_in_past_only) & set(next_loto_data))
        temp_english_loto_numbers_only = len(set(english_loto_numbers_only) & set(next_loto_data))
        temp_serial_loto_numbers_only = len(set(serial_loto_numbers_only) & set(next_loto_data))
        temp_loto_numbers_only = len(set(loto_numbers_only) & set(next_loto_data))

        # 各集合に数字の含まれる割合の集計
        temp_hit_combination = (temp_common, temp_num_in_past_only, temp_english_loto_numbers_only, temp_serial_loto_numbers_only, temp_loto_numbers_only)
        hit_combination.setdefault(temp_hit_combination, 1)
        hit_combination[temp_hit_combination] += 1

    # hit_sun_countを最小-最大スケーリングに変換
    # 例:total_seq_nums = {k: (v - np.min(list(total_seq_nums.values()))) / (np.max(list(total_seq_nums.values())) - np.min(list(total_seq_nums.values()))) for k, v in total_seq_nums.items()}
    hit_sum_count = {k: (v - np.min(list(hit_sum_count.values()))) / (np.max(list(hit_sum_count.values())) - np.min(list(hit_sum_count.values()))) for k, v in hit_sum_count.items()}
    # hit_combinationを最小-最大スケーリングに変換
    hit_combination = {k: (v - np.min(list(hit_combination.values()))) / (np.max(list(hit_combination.values())) - np.min(list(hit_combination.values()))) for k, v in hit_combination.items()}

    print("=========================================")
    print("loto_sum_count")
    pp.pprint(loto_sum_count)
    print("loto_even_odd_count")
    pp.pprint(loto_even_odd_count)
    print("loto_seq_count")
    pp.pprint(loto_seq_count)
    print("hit_sum_count")
    pp.pprint(hit_sum_count)
    print("hit_combination")
    pp.pprint(hit_combination)
    print("=========================================")


    # 次回結果の予測
    # 1. 過去のデータを取得
    last_index = len(loto_num_data)
    # 2. 過去のデータから、n_count_rangeの範囲のデータを取得
    n25_loto_num_data = loto_num_data[last_index - n_count_range:last_index, :]
    # 3. 過去のデータから、n_past_rangeの範囲のデータを取得
    n5_loto_num_data = loto_num_data[last_index - n_past_range:last_index, :]
    # 4. 過去のデータから、n1の範囲のデータを取得
    n1_loto_num_data = loto_num_data[last_index- 1:last_index, :]
    n1_loto_num_data = n1_loto_num_data[0]
    print("n25_loto_num_data")
    print(n25_loto_num_data)
    print("n5_loto_num_data")
    print(n5_loto_num_data)
    print("n1_loto_num_data")
    print(n1_loto_num_data)

    # ====================================================================
    # 5. 予測
    total_calc = np.zeros(len(all_loto), dtype=float)
    for i in range(len(all_loto)):
        # 5-1. 合計値の予測
        if np.sum(all_loto[i]) in all_sum_count:
            total_calc[i] += all_sum_count[np.sum(all_loto[i])]
        if np.sum(all_loto[i]) in loto_sum_count:
            total_calc[i] += loto_sum_count[np.sum(all_loto[i])]

        # 各集計キーの生成
        temp_sum_key = 0
        for num in all_loto[i]:
            temp_sum_key += loto_number_count.get(num, 0)

        # 5-2. 偶数奇数の予測
        temp_even_odd = lt.get_even_odd(all_loto[i])
        if tuple(temp_even_odd) in all_even_odd:
            total_calc[i] += all_even_odd[tuple(temp_even_odd)]
        if tuple(temp_even_odd) in loto_even_odd_count:
            total_calc[i] += loto_even_odd_count[tuple(temp_even_odd)]

        # 5-3. 連番の予測
        tmp_seq_nums = {}
        tmp_seq_nums = [list(g) for _, g in itertools.groupby(all_loto[i], key=lambda n, c=itertools.count(): n - next(c))]
        tmp_keys = []
        for tmp_seq in tmp_seq_nums:
            tmp_keys.append(len(tmp_seq))
        if tuple(tmp_keys) in all_seq:
            total_calc[i] += all_seq[tuple(tmp_keys)]
        if tuple(tmp_keys) in loto_seq_count:
            total_calc[i] += loto_seq_count[tuple(tmp_keys)]

        # 5-4. 過去のデータの予測
        # 共通部分の抽出
        common_loto_numbers = set(num_in_past) & set(english_loto_numbers)
        common_loto_numbers = set(common_loto_numbers) - set(serial_loto_numbers)
        common_loto_numbers = sorted(list(common_loto_numbers))

        # 差集合の作成
        num_in_past_only = sorted(list(set(num_in_past) - set(english_loto_numbers) - set(serial_loto_numbers)))
        english_loto_numbers_only = sorted(list(set(english_loto_numbers) - set(num_in_past) - set(serial_loto_numbers)))
        serial_loto_numbers_only = sorted(list(set(serial_loto_numbers)))


        # 抽出されなかった数字を抽出
        loto_all_numbers = [i for i in range(const.LOTO_MIN, const.LOTO_MAX + 1)]
        loto_numbers_only = sorted(list(set(loto_all_numbers) - set(common_loto_numbers) - set(num_in_past_only) - set(english_loto_numbers_only) - set(serial_loto_numbers_only)))

        temp_common = len(set(all_loto[i]) & set(common_loto_numbers))
        temp_num_in_past_only = len(set(all_loto[i]) & set(num_in_past_only))
        temp_english_loto_numbers_only = len(set(all_loto[i]) & set(english_loto_numbers_only))
        temp_serial_loto_numbers_only = len(set(all_loto[i]) & set(serial_loto_numbers_only))
        temp_loto_numbers_only = len(set(all_loto[i]) & set(loto_numbers_only))

        temp_key = (temp_common, temp_num_in_past_only, temp_english_loto_numbers_only, temp_serial_loto_numbers_only, temp_loto_numbers_only)
        if temp_key in hit_combination:
            total_calc[i] += hit_combination[temp_key]

        # ロトの過去データの集計(各数字の出現回数)
        loto_number_count = lt.number_count(n25_loto_num_data)

        # 25回分のデータとの比較
        if temp_sum_key in hit_sum_count:
            total_calc[i] += hit_sum_count[temp_sum_key]

    # ====================================================================

    # 6. 予測結果の表示
    print("common_loto_numbers")
    print(len(common_loto_numbers), common_loto_numbers)
    print("num_in_past_only")
    print(len(num_in_past_only), num_in_past_only)
    print("english_loto_numbers_only")
    print(len(english_loto_numbers_only), english_loto_numbers_only)
    print("serial_loto_numbers_only")
    print(len(serial_loto_numbers_only), serial_loto_numbers_only)
    print("loto_numbers_only")
    print(len(loto_numbers_only), loto_numbers_only)
    print("予測結果")
    print(all_loto[np.where(total_calc == np.nanmax(total_calc))])
    # print(all_loto[np.where(total_calc == total_calc.max())])

    return None

if __name__ == "__main__":
    main()

