# ロト解析用パッケージ
# 作成日: 2023/05/06
# 更新日:

import constants as const
import loto as lt
import numpy as np
import pprint as pp

# 追加予定の機能
# =====+=====+=====+=====+=====+=====
# 過去データに対する解析
# 出現数字の合計値
# 連番の出現回数
# 各数字の出現間隔
# 前後の関係性（直前の数字との関係性）
# =====+=====+=====+=====+=====+=====
# 起こりうる全組合せに対する解析
# 偶数奇数の組合せ
# 出現数字の合計値
# 連番の出現回数

# =====+=====+=====+=====+=====+=====
# 過去データの解析
# =====+=====+=====+=====+=====+=====

# 各数字が最低n回以上出現する回数（nは任意の数字）


def analyze_range_n(n):
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    # ロトの過去データの集計(各数字の出現回数)
    range_index = 0
    loto_num_count = np.zeros((const.LOTO_MAX), dtype=np.uint16)
    for i, numbers in enumerate(loto_num_data):
        for num in numbers:
            loto_num_count[num - 1] += 1
        if np.min(loto_num_count) >= n:
            range_index = i
            break
    # 結果の表示
    print("各数字が最低{}回以上出現する区間は{}回まで".format(n, range_index + 1))
    for i, count in enumerate(loto_num_count):
        print("[{:>2}]:({:>4})".format(i + 1, count), end=" ")
        if (i + 1) % 10 == 0:
            print("")
    else:
        print("")
    print("max: {}".format(np.max(loto_num_count)))
    print("min: {}".format(np.min(loto_num_count)))
    print("Next: {}".format(loto_data[range_index + 1]))
    for num in loto_num_data[range_index + 1]:
        print("[{:>2}]:({:>4})".format(num, loto_num_count[num - 1]), end=" ")
    else:
        print("")


# (固定区間)
def analyze_number_count_range(n):
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    max_count = 0
    min_count = 0
    same_time = 0
    max_min = {}
    sum_count = {}
    sum_rank = {}
    rank_combinations = {}

    print("各数字の出現回数(全区間)")
    for i in range(len(loto_data) - n - 1):
        temp_loto_num_data = loto_num_data[i:i + n, :]

        # ロトの過去データの集計(各数字の出現回数)
        loto_number_count = lt.number_count(temp_loto_num_data)
        # データのチェック
        for j in range(const.LOTO_MAX):
            if j + 1 not in loto_number_count:
                loto_number_count.setdefault(j + 1, 0)
        # データの順位付け
        temp_rank = list(loto_number_count.values())
        rank_loto_number_count = lt.rank(temp_rank)

        # 結果の表示
        print("[{}] - [{}]".format(i + 1, i + n ))
        print("Count")
        for temp_key, temp_value in sorted(loto_number_count.items()):
            print("[{:>2}]:({:>4})".format(temp_key, temp_value), end=" ")
            if temp_key % 10 == 0:
                print("")
        else:
            print("")
            print("max: {}".format(max(loto_number_count.values())))
            print("min: {}".format(min(loto_number_count.values())))
            print("Next: {}".format(loto_data[i + n + 1]))

        print("Rank")
        for temp_key, temp_value in sorted(loto_number_count.items()):
            print("[{:>2}]:({:>4})".format(
                temp_key, rank_loto_number_count[temp_value]), end=" ")
            if temp_key % 10 == 0:
                print("")
        else:
            print("")

        temp_max_count = 0
        temp_min_count = 0
        temp_same_time = 0
        temp_sum = 0
        print("Next Data")
        for num in loto_num_data[i + n + 1]:
            print("[{:>2}]:({:>4})".format(
                num, loto_number_count[num]), end=" ")
            # 出現数の合計値
            temp_sum += loto_number_count[num]
            # 集計の最大値が含まれているか？
            if temp_max_count == 0:
                if max(loto_number_count.values()) == loto_number_count[num]:
                    max_count += 1
                    temp_same_time += 1
                    temp_max_count += 1
            else:
                if max(loto_number_count.values()) == loto_number_count[num]:
                    temp_max_count += 1
            # 集計の最小値が含まれているか？
            if temp_min_count == 0:
                if min(loto_number_count.values()) == loto_number_count[num]:
                    min_count += 1
                    temp_same_time += 1
                    temp_min_count += 1
            else:
                if min(loto_number_count.values()) == loto_number_count[num]:
                    temp_min_count += 1
            if temp_same_time == 2:
                same_time += 1
        else:
            print("")
            if temp_max_count != 0:
                print("max in numbers [{:>2}]".format(temp_max_count))
            if temp_min_count != 0:
                print("min in numbers [{:>2}]".format(temp_min_count))
            max_min.setdefault((temp_max_count, temp_min_count), 1)
            max_min[(temp_max_count, temp_min_count)] += 1
            sum_count.setdefault(temp_sum, 1)
            sum_count[temp_sum] += 1

        temp_sum_rank = 0
        temp_rank_combination = []
        for num in loto_num_data[i + n + 1]:
            temp_rank = rank_loto_number_count[loto_number_count[num]]
            print("[{:>2}]:({:>4})".format(num, temp_rank), end=" ")
            temp_sum_rank += temp_rank
            temp_rank_combination.append(temp_rank)
        else:
            print("")
            sum_rank.setdefault(temp_sum_rank, 1)
            sum_rank[temp_sum_rank] += 1
            temp_rank_combination = sorted(temp_rank_combination)
            rank_combinations.setdefault(tuple(temp_rank_combination), 0)
            rank_combinations[tuple(temp_rank_combination)] += 1
    else:
        print("In Max : ({:>4} / {:>4})".format(max_count,
              len(loto_data) - n - 1))
        print("In Min:  ({:>4} / {:>4})".format(min_count,
              len(loto_data) - n - 1))
        print("In Same: ({:>4} / {:>4})".format(same_time,
              len(loto_data) - n - 1))
        print("Max : Min")
        for key, value in sorted(max_min.items()):
            print("{} : {:>3}".format(key, value))
        print("Sum")
        for key, value in sorted(sum_count.items()):
            print("{:>2} : {:>3}".format(key, value))
        print("Sum Rank")
        for key, value in sorted(sum_rank.items()):
            print("{:>3} : {:>3}".format(key, value))
        print("Rank Combination")
        for key, value in sorted(rank_combinations.items()):
            print("{} : {:>4}".format(key, value))


# 偶数奇数の組合せ
def analyze_even_odd():
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    # len(loto_even_odd_count) == 2 ** LOTO_NUMになる集計範囲を調べる
    for i in range(len(loto_data) - 1):
        # ロトの過去データの集計(偶数奇数)
        loto_even_odd_count = lt.even_odd_count(
            lt.get_even_odd(loto_num_data[0:i + 1, :]))
        if len(loto_even_odd_count) == (2 ** const.LOTO_NUM):
            even_odd_index = i
            break
        print("[{}] - [{}]".format(1, i + 1))
        for temp_key, temp_value in loto_even_odd_count.items():
            print("[{}]:({:>4})".format(temp_key, temp_value))
        else:
            print("Lengs: {}".format(len(loto_even_odd_count)))
    # 最終集計範囲の表示
    print("[{}] - [{}]".format(1, even_odd_index + 1))
    for temp_key, temp_value in loto_even_odd_count.items():
        print("[{}]:({:>4})".format(temp_key, temp_value))
    else:
        print("Lengs: {}".format(len(loto_even_odd_count)))

    rank_count = {}
    print("偶数奇数の組合せ")
    for i in range(len(loto_data) - even_odd_index - 1):
        # ロトの過去データの集計(偶数奇数)
        loto_even_odd_count = lt.even_odd_count(
            lt.get_even_odd(loto_num_data[0:even_odd_index + i, :]))
        # データの順位付け
        temp_rank = list(loto_even_odd_count.values())
        rank_loto_number_count = lt.rank(temp_rank)

        # 結果の表示
        print("[{}] - [{}]".format(1, (even_odd_index + 1) + i))
        loto_even_odd_count = sorted(loto_even_odd_count.items())
        loto_even_odd_count = dict((x, y)
                                   for x, y in loto_even_odd_count)  # 追加
        for temp_key, temp_value in loto_even_odd_count.items():
            print("[{}]:({:>4}):{:>3}".format(temp_key, int(
                temp_value), rank_loto_number_count[temp_value]))
        else:
            print("Next: {}".format(loto_data[even_odd_index + i + 1]))
            print("{} :".format(lt.get_even_odd(
                loto_num_data[even_odd_index + i + 1, :])), end=" ")
            temp_rank = rank_loto_number_count[loto_even_odd_count[tuple(
                lt.get_even_odd(loto_num_data[even_odd_index + i + 1, :]))]]
            print("({})".format(temp_rank))
            # Rankの集計
            rank_count.setdefault(temp_rank, 0)
            rank_count[temp_rank] += 1

    print("Rank")
    for key, value in sorted(rank_count.items()):
        print("{:>2} : {:>3}".format(key, value))


def analyze_number_in_number():
    import loto as lt
    import constants as const
    import numpy as np

    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    much_count = {}
    for i in range(len(loto_data) - const.LOTO_MAX):
        temp_loto_num_data = loto_num_data[0 : const.LOTO_MAX + i, :]
        
        # 最終結果の表示
        print("Next:{}".format(loto_data[len(temp_loto_num_data)]))
        # print("{}".format(loto_data[len(temp_loto_num_data) - 1]))

        # 最終結果の数字をインデックスにして過去のデータを取得
        # 最終データを取り出す
        next_numbers = []
        temp_loto_index = temp_loto_num_data[-1, :]
        # print("{}".format(temp_loto_index))
        for j, temp_num in enumerate(temp_loto_index):
            # print("{}".format(loto_data[len(temp_loto_num_data) - temp_num - 1]))
            # print("{}".format(temp_loto_num_data[len(temp_loto_num_data) - temp_num - 1, :]))
            # print("{}".format(temp_loto_num_data[len(temp_loto_num_data) - temp_num - 1, j]))
            next_numbers.append(temp_loto_num_data[len(temp_loto_num_data) - temp_num - 1, j])
        else:
            print("{}".format(next_numbers))
        
        # 最終結果と同じ数字がいくつあったかを数える
        temp_much = len(set(next_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        print("{}".format(temp_much))
        much_count.setdefault(temp_much, 0)
        much_count[temp_much] += 1
    else:
        print("Count")
        for key, value in sorted(much_count.items()):
            print("{:>2} : {:>3}".format(key, value))
    
