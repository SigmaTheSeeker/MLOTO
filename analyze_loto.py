# ロト解析用パッケージ
# 作成日: 2023/05/06
# 更新日:

import constants as const
import loto as lt
import numpy as np
import pprint as pp
import itertools
import math

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
    max_list = {}
    min_list = {}
    ave_list = {}

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
            max_list.setdefault(max(loto_number_count.values()), 0)
            max_list[max(loto_number_count.values())] += 1
            min_list.setdefault(min(loto_number_count.values()), 0)
            min_list[min(loto_number_count.values())] += 1
            ave_list.setdefault(np.average(list(loto_number_count.values())), 0)
            ave_list[np.average(list(loto_number_count.values()))] += 1

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
        print("Max List")
        for key, value in sorted(max_list.items()):
            print("{:>3} : {:>3}".format(key, value))
        print("Min List")
        for key, value in sorted(min_list.items()):
            print("{:>3} : {:>3}".format(key, value))
        print("Ave List")
        for key, value in sorted(ave_list.items()):
            print("{:>3} : {:>3}".format(key, value))


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


def analyze_serial_calculator():
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[:, 2:const.LOTO_NUM + 2].astype(np.uint8)

    match_count = {}
    without_self_match_count = {}
    length_serial_numbers = {}
    length_without_self_serial_numbers = {}
    length_serial_numbers_max = 0
    length_serial_numbers_min = 999999
    length_without_self_serial_numbers_max = 0
    length_without_self_serial_numbers_min = 999999
    for i in range(len(loto_data) - 1):
        temp_loto_num_data = loto_num_data[i : i + 1, :]
        print("{}".format(temp_loto_num_data))
        
        # 最終結果の表示
        print("Next:{}".format(loto_data[i + 1]))

        # ±1,2,3の数字を取得
        serial_numbers = lt.serial_calculator(temp_loto_num_data[0])
        without_self_serial_numbers = set(serial_numbers) - set(temp_loto_num_data[0])
    
        print("Serial:({}){}".format(len(serial_numbers), serial_numbers))
        print("Combinations:({})".format(math.comb(len(serial_numbers), 5)))
        length_serial_numbers.setdefault(len(serial_numbers), 0)
        length_serial_numbers[len(serial_numbers)] += 1
        if len(serial_numbers) > length_serial_numbers_max:
            length_serial_numbers_max = len(serial_numbers)
        if len(serial_numbers) < length_serial_numbers_min:
            length_serial_numbers_min = len(serial_numbers)
    
        print("Without Self Serial:({}){}".format(len(without_self_serial_numbers), without_self_serial_numbers))
        print("Combinations:({})".format(math.comb(len(without_self_serial_numbers), 5)))
        length_without_self_serial_numbers.setdefault(len(without_self_serial_numbers), 0)
        length_without_self_serial_numbers[len(without_self_serial_numbers)] += 1
        if len(without_self_serial_numbers) > length_without_self_serial_numbers_max:
            length_without_self_serial_numbers_max = len(without_self_serial_numbers)
        if len(without_self_serial_numbers) < length_without_self_serial_numbers_min:
            length_without_self_serial_numbers_min = len(without_self_serial_numbers)

        # 最終結果と同じ数字がいくつあったかを数える
        temp_match = sorted(list(set(serial_numbers) & set(loto_data[i + 1][2:const.LOTO_NUM + 2])))
        print("({:>2}){}".format(len(temp_match), temp_match))
        temp_without_self_match = sorted(list(set(without_self_serial_numbers) & set(loto_data[i + 1][2:const.LOTO_NUM + 2])))
        print("({:>2}){}".format(len(temp_without_self_match), temp_without_self_match))

        match_count.setdefault(len(temp_match), 0)
        match_count[len(temp_match)] += 1
        without_self_match_count.setdefault(len(temp_without_self_match), 0)
        without_self_match_count[len(temp_without_self_match)] += 1


    print("Count")
    for key, value in sorted(match_count.items()):
        print("{:>2} : {:>3}".format(key, value))
    print("Length Serial Numbers")
    for key, value in sorted(length_serial_numbers.items()):
        print("{:>2} : {:>3}".format(key, value))
    print("Max: {:>3}  Min: {:>3}".format(length_serial_numbers_max, length_serial_numbers_min))
    print("Without Self Count")
    for key, value in sorted(without_self_match_count.items()):
        print("{:>2} : {:>3}".format(key, value))
    print("Length Without Self Serial Numbers")
    for key, value in sorted(length_without_self_serial_numbers.items()):
        print("{:>2} : {:>3}".format(key, value))
    print("Max: {:>3}  Min: {:>3}".format(length_without_self_serial_numbers_max, length_without_self_serial_numbers_min))


def analyze_english_calculator():
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    match_count = {}
    for i in range(len(loto_data) - 1):
        temp_loto_num_data = loto_num_data[i : i + 1, :]
        print("{}".format(temp_loto_num_data))
        
        # 最終結果の表示
        print("Next:{}".format(loto_data[i + 1]))

        # english_calculatorの数字を取得
        english_numbers = lt.english_calculator(temp_loto_num_data[0])
        print("English:({}){}".format(len(english_numbers), english_numbers))

        # 最終結果と同じ数字がいくつあったかを数える
        temp_match = len(set(english_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        print("{}".format(temp_match))

        match_count.setdefault(temp_match, 0)
        match_count[temp_match] += 1

    print("Count")
    for key, value in sorted(match_count.items()):
        print("{:>2} : {:>3}".format(key, value))


def analyze_combinations():
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    match_count = {}
    for i in range(len(loto_data) - 1):
        temp_loto_num_data = loto_num_data[i : i + 1, :]
        print("{}".format(temp_loto_num_data))
        
        # 最終結果の表示
        print("Next:{}".format(loto_data[i + 1]))

        # ±1,2,3の数字を取得
        serial_numbers = lt.serial_calculator(temp_loto_num_data[0])

        # english_calculatorの数字を取得
        english_numbers = lt.english_calculator(temp_loto_num_data[0])

        # 共通部分の抽出
        common_loto_numbers = set(serial_numbers) & set(english_numbers)
        common_loto_numbers = sorted(list(common_loto_numbers))

        # 差集合の作成
        serial_numbers = set(serial_numbers) - set(common_loto_numbers)
        serial_numbers = sorted(list(serial_numbers))
        english_numbers = set(english_numbers) - set(common_loto_numbers)
        english_numbers = sorted(list(english_numbers))

        # common_loto_numbers, serial_numbers, english_numbersに含まれない数字を抽出
        out_of_numbers = set(range(1, const.LOTO_MAX + 1)) - set(common_loto_numbers) - set(serial_numbers) - set(english_numbers)

        # common_loto_numbers, serial_numbers, english_numbersの表示
        print("Common:({}){}".format(len(common_loto_numbers), common_loto_numbers))
        print("Serial:({}){}".format(len(serial_numbers), serial_numbers))
        print("English:({}){}".format(len(english_numbers), english_numbers))
        print("Out of:({}){}".format(len(out_of_numbers), out_of_numbers))


        # 最終結果と同じ数字がいくつあったかを数える
        temp_match_common = len(set(common_loto_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_serial = len(set(serial_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_english = len(set(english_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_out_of = len(set(out_of_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        print("({:>2}):({:>2}):({:>2}):({:>2})".format(temp_match_common, temp_match_serial, temp_match_english, temp_match_out_of))

        temp_key = (temp_match_common, temp_match_serial, temp_match_english, temp_match_out_of)
        match_count.setdefault(temp_key, 0)
        match_count[temp_key] += 1

    print("Count")
    for key, value in sorted(match_count.items()):
        print("{} : {:>3}".format(key, value))
    temp_average = sum(match_count.values()) / len(match_count)
    print("Average: {}".format(temp_average))
    print("Than Anverage")
    for key, value in sorted(match_count.items()):
        if value > temp_average:
            print("{} : {:>3}".format(key, value))


def analyze_mix():
    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[
        :, 2:const.LOTO_NUM + 2].astype(np.uint8)

    index_list = []    
    # 各数字が1回以上出現する範囲を調べる 
    range_index = 0
    loto_num_count = np.zeros((const.LOTO_MAX), dtype=np.uint16)
    for i, numbers in enumerate(loto_num_data):
        for num in numbers:
            loto_num_count[num - 1] += 1
        if np.min(loto_num_count) >= 1:
            range_index = i
            break
    # 結果の表示
    print("range_index: {}".format(range_index))
    index_list.append(range_index)

    # len(loto_even_odd_count) == 2 ** LOTO_NUMになる集計範囲を調べる
    for i in range(len(loto_data) - 1):
        # ロトの過去データの集計(偶数奇数)
        loto_even_odd_count = lt.even_odd_count(
            lt.get_even_odd(loto_num_data[0:i + 1, :]))
        if len(loto_even_odd_count) == (2 ** const.LOTO_NUM):
            even_odd_index = i
            break
    # 結果の表示
    print("even_odd_index: {}".format(even_odd_index))
    index_list.append(even_odd_index)

    # 数字の組合せの集計範囲を平均以上のデータにしたときにデータが1つ以上残る範囲
    match_count ={}
    for i in range(len(loto_data) - 1):
        temp_loto_num_data = loto_num_data[0 : i + 1, :]
        
        # 数字の組合せを作成
        common_loto_numbers, serial_numbers, english_numbers, out_of_numbers = lt.generate_combinations(temp_loto_num_data[-1])

        # 最終結果と同じ数字がいくつあったかを数える
        temp_match_common = len(set(common_loto_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_serial = len(set(serial_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_english = len(set(english_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_out_of = len(set(out_of_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_key = (temp_match_common, temp_match_serial, temp_match_english, temp_match_out_of)
        match_count.setdefault(temp_key, 0)
        match_count[temp_key] += 1

         # 各集計結果を平均値以上の値をもつものだけを残す
        than_average_match_count = {}
        temp_average = sum(match_count.values()) / len(match_count)
        for key, value in sorted(match_count.items()):
            if value > temp_average:
                than_average_match_count.setdefault(key, value)

       # データの個数が1以上になる範囲を調べる
        if len(than_average_match_count) > 0:
            combinations_index = i
            break

    # 結果の表示
    print("combinations_index: {}".format(combinations_index))
    index_list.append(combinations_index)
   
    # 解析範囲のインデクスを作成する
    main_index = max(index_list)
   
    rank_count = {}
    match_count = {}
    hit_count = {}
    for i in range(len(loto_data) - main_index - 1):
        temp_loto_num_data = loto_num_data[0 : main_index + i + 1, :]
        
        # ロトの過去データの集計(偶数奇数)
        loto_even_odd_count = lt.even_odd_count(
            lt.get_even_odd(temp_loto_num_data))
        # データの順位付け
        temp_rank = list(loto_even_odd_count.values())
        rank_loto_number_count = lt.rank(temp_rank)

        # 結果の表示
        print("[{}] - [{}]".format(1, (even_odd_index + 1) + i))
        loto_even_odd_count = sorted(loto_even_odd_count.items())
        loto_even_odd_count = dict((x, y)
                                   for x, y in loto_even_odd_count)  # 追加
        print("Next:{}".format(loto_data[even_odd_index + i + 1]))
        print("Current: {}".format(loto_data[even_odd_index + i]))
        print("{} :".format(temp_loto_num_data[-1]))
        print("{} :".format(lt.get_even_odd(
            temp_loto_num_data[-1])), end=" ")

        # 数字の組合せを作成
        common_loto_numbers, serial_numbers, english_numbers, out_of_numbers = lt.generate_combinations(temp_loto_num_data[-1])

        # common_loto_numbers, serial_numbers, english_numbersの表示
        print("Common:({}){}".format(len(common_loto_numbers), common_loto_numbers))
        print("Serial:({}){}".format(len(serial_numbers), serial_numbers))
        print("English:({}){}".format(len(english_numbers), english_numbers))
        print("Out of:({}){}".format(len(out_of_numbers), out_of_numbers))

        # 最終結果と同じ数字がいくつあったかを数える
        temp_match_common = len(set(common_loto_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_serial = len(set(serial_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_english = len(set(english_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        temp_match_out_of = len(set(out_of_numbers) & set(loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]))
        print("({:>2}):({:>2}):({:>2}):({:>2})".format(temp_match_common, temp_match_serial, temp_match_english, temp_match_out_of))

        temp_key = (temp_match_common, temp_match_serial, temp_match_english, temp_match_out_of)
        match_count.setdefault(temp_key, 0)
        match_count[temp_key] += 1

        # 合計値の集計
        sum_count = lt.sum_count(temp_loto_num_data)

        # 24回分の各数字の出現数をカウントする
        n = 24
        sum_rank ={}
        for j in range(len(temp_loto_num_data)  - n - 1):
            temp_n_loto_num_data = temp_loto_num_data[j:j + n, :]

            # ロトの過去データの集計(各数字の出現回数)
            loto_number_count = lt.number_count(temp_n_loto_num_data)
            # データのチェック
            for k in range(const.LOTO_MAX):
                if k + 1 not in loto_number_count:
                    loto_number_count.setdefault(k + 1, 0)
            # データの順位付け
            temp_rank = list(loto_number_count.values())
            rank_loto_number_count = lt.rank(temp_rank)

            temp_sum_rank = 0
            temp_rank_combination = []
            for num in temp_loto_num_data[i + n + 1]:
                temp_rank = rank_loto_number_count[loto_number_count[num]]
                # print("[{:>2}]:({:>4})".format(num, temp_rank), end=" ")
                temp_sum_rank += temp_rank
                temp_rank_combination.append(temp_rank)
            else:
                # print("")
                sum_rank.setdefault(temp_sum_rank, 1)
                sum_rank[temp_sum_rank] += 1

        # 最新の24回分の各数字の出現数をカウントする
        n = 24
        temp_n_loto_num_data = temp_loto_num_data[-n:, :]
        # ロトの過去データの集計(各数字の出現回数)
        loto_number_count = lt.number_count(temp_n_loto_num_data)
        # データのチェック
        for j in range(const.LOTO_MAX):
            if j + 1 not in loto_number_count:
                loto_number_count.setdefault(j + 1, 0)
        # データの順位付け
        temp_rank = list(loto_number_count.values())
        rank_loto_number_count = lt.rank(temp_rank)

        for num in loto_data[len(temp_loto_num_data)][2:const.LOTO_NUM + 2]:
            temp_rank = rank_loto_number_count[loto_number_count[num]]
            # print("[{:>2}]:({:>4})".format(num, temp_rank), end=" ")
            temp_sum_rank += temp_rank

        # 各集計結果を平均値以上の値をもつものだけを残す
        than_average_match_count = {}
        temp_average = sum(match_count.values()) / len(match_count)
        for key, value in sorted(match_count.items()):
            if value > temp_average:
                than_average_match_count.setdefault(key, value)

        than_average_even_odd_count = {}
        temp_average = sum(loto_even_odd_count.values()) / len(loto_even_odd_count)
        for key, value in sorted(loto_even_odd_count.items()):
            if value > temp_average:
                than_average_even_odd_count.setdefault(key, value)

        than_average_sum_count = {}
        temp_average = sum(sum_count.values()) / len(sum_count)
        for key, value in sorted(sum_count.items()):
            if value > temp_average:
                than_average_sum_count.setdefault(key, value)

        than_average_sum_rank = {}
        temp_average = sum(sum_rank.values()) / len(sum_rank)
        for key, value in sorted(sum_rank.items()):
            if value > temp_average:
                than_average_sum_rank.setdefault(key, value)

        # 平均以上の値をもつ集計結果の表示
        print("Than Average Match")
        for key, value in sorted(than_average_match_count.items()):
            print("{} : {:>3}".format(key, value))
        print("Than Average Even Odd")
        for key, value in sorted(than_average_even_odd_count.items()):
            print("{} : {:>3}".format(key, value))
        print("Than Average Sum")
        for key, value in sorted(than_average_sum_count.items()):
            print("{} : {:>3}".format(key, value))
        print("Than Sum Rank")
        for key, value in sorted(than_average_sum_rank.items()):
            print("{} : {:>3}".format(key, value))
        print(len(sum_rank))


        # 平均以上の値をもつ集計表に次回結果が含まれているかを確認
        temp_match_flag = 0
        tmp_even_odd_flag = 0
        temp_sum_flag = 0
        temp_rank_flag = 0
        if temp_key in than_average_match_count:
            print("Match: {}".format(temp_key))
            temp_match_flag = 1
        if tuple(list(lt.get_even_odd(temp_loto_num_data[-1]))) in than_average_even_odd_count:
            print("Even Odd: {}".format(lt.get_even_odd(temp_loto_num_data[-1])))
            tmp_even_odd_flag = 1
        if sum(temp_loto_num_data[-1]) in than_average_sum_count:
            print("Sum: {}".format(sum(temp_loto_num_data[-1])))
            temp_sum_flag = 1
        if temp_sum_rank in than_average_sum_rank:
            print("Sum Rank: {}".format(temp_sum_rank))
            temp_rank_flag = 1

        hit_count.setdefault((temp_match_flag, tmp_even_odd_flag, temp_sum_flag, temp_rank_flag), 0)
        hit_count[(temp_match_flag, tmp_even_odd_flag, temp_sum_flag, temp_rank_flag)] += 1


        # 条件に合う数字の組合せを作成
        numbars = range(1, const.LOTO_MAX + 1)
        all_loto = lt.all_loto_combinations(numbers)
        selected_loto = []
        for temp_all_loto in all_loto:
            # 合計値の確認
            if sum(temp_all_loto) not in than_average_sum_count:
                continue
            # 偶数奇数の確認
            if tuple(list(lt.get_even_odd(temp_all_loto))) not in than_average_even_odd_count:
                continue
            # ランクの合計
            if temp_sum_rank in than_average_sum_rank:
                continue
            # 数字の組合せの確認
            for temp_key in than_average_match_count:
                # common_loto_numbers
                if len(set(temp_all_loto) & set(common_loto_numbers)) != temp_key[0]:
                    continue
                # serial_numbers
                if len(set(temp_all_loto) & set(serial_numbers)) != temp_key[1]:
                    continue
                # english_numbers
                if len(set(temp_all_loto) & set(english_numbers)) != temp_key[2]:
                    continue
                # out_of_numbers
                if len(set(temp_all_loto) & set(out_of_numbers)) != temp_key[3]:
                    continue
                selected_loto.append(temp_all_loto)
    
        # 選択された数字の組合せの表示
        print("Selected Loto")
        print("{}".format(len(selected_loto)))

    print("Hit Count")
    for key, value in sorted(hit_count.items()):
        print("{} : {:>3}".format(key, value))


# 前後の組み合わの集計
def analyze_columns():
    from collections import Counter

    counter = Counter()

    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[:, 2:const.LOTO_NUM + 2].astype(np.uint8)

    # 前後の組み合わせを作成
    # loto_num_data[0] = [1, 2, 3, 4, 5, 6]
    # loto_num_data[1] = [2, 3, 4, 5, 6, 7]
    # combination = [(loto_num_data[0][i], j, loto_num_data[1][j]) for j in range(len(loto_num_data[0]))]
    for i in range(len(loto_num_data) - 1):
        for j in range(const.LOTO_NUM):
            temp_combination = [(loto_num_data[i][j], k, loto_num_data[i + 1][k]) for k in range(const.LOTO_NUM)]
            counter.update(temp_combination)

    # キー順にソートして出力
    # (key[0], key[1])の値が変わるごとに合計と平均を出力する
    temp_key0 = 1
    temp_key1 = 0
    temp_sum = 0
    temp_count = 0
    average_list = {}
    for key, value in sorted(counter.items()):
        if temp_key0 != key[0] or temp_key1 != key[1]:
            print("({:>2}, {:>1}) : {:>3} : {:>3}".format(temp_key0, temp_key1, temp_sum, temp_sum / temp_count))
            average_list.setdefault((temp_key0, temp_key1), temp_sum / temp_count)
            temp_key0 = key[0]
            temp_key1 = key[1]
            temp_sum = 0
            temp_count = 0
        print("({:>2}, {:>1}, {:>2}) : {:>3}".format(key[0], key[1], key[2], value))
        temp_sum += value
        temp_count += 1
    else:
        print("({:>2}, {:>1}) : {:>3} : {:>3}".format(temp_key0, temp_key1, temp_sum, temp_sum / temp_count))
        average_list.setdefault((temp_key0, temp_key1), temp_sum / temp_count)



    # # (key[0], key[1])の値ごのと平均値を参照して、平均値以上の値をもつものだけを残す
    than_average_counter = {}
    for key, value in sorted(counter.items()):
        if value > average_list[(key[0], key[1])]:
            than_average_counter.setdefault(key, value)
    # キー順にソートして出力
    for key, value in sorted(than_average_counter.items()):
        print("({:>2}, {:>1}, {:>2}) : {:>3}".format(key[0], key[1], key[2], value))

# 過去データの解析
def analyze_loto_data():

    # ロトの過去データファイルの読み込み
    loto_data = lt.read_loto_data(const.LOTO_DATA_FILE)

    # ロトの過去データを本数字のみのnumpy配列に変換
    loto_num_data = np.array(loto_data)[:, 2:const.LOTO_NUM + 2].astype(np.uint8)

    # 過去データに同じ抽選結果があるかを確認
    for i in range(len(loto_data) - 1):
        for j in range(i + 1, len(loto_data)):
            if np.all(loto_num_data[i] == loto_num_data[j]):
                print("Same: {} - {}".format(i + 1, j + 1))
                print("{}".format(loto_data[i]))
                print("{}".format(loto_data[j]))

    # 前後のデータに同じ数字があるかを確認
    # いくつ同じ数字があったかを数え、集計表を出力する
    match_count = {}
    for i in range(len(loto_data) - 1):
        temp_match_count = 0
        for j in range(const.LOTO_NUM):
            if loto_num_data[i][j] in loto_num_data[i + 1]:
                temp_match_count += 1
        match_count.setdefault(temp_match_count, 0)
        match_count[temp_match_count] += 1
    for key, value in sorted(match_count.items()):
        print("{} : {:>3}".format(key, value))

    # 25回分の数字の出現数をカウントする
    n = 25
    for i in range(len(loto_data) - n - 1):
        temp_loto_num_data = loto_num_data[i:i + n, :]
        # ロトの過去データの集計(各数字の出現回数)
        loto_number_count = lt.number_count(temp_loto_num_data)
        # 集計結果の表示
        # 集計区間を表示して、出現数のカウントをキーでソートして表示する
        print("[{}] - [{}]".format(i + 1, i + n))
        print("{}".format(sorted(loto_number_count.items(), key=lambda x: x[0])))

        # # データのチェック
        # for j in range(const.LOTO_MAX):
        #     if j + 1 not in loto_number_count:
        #         loto_number_count.setdefault(j + 1, 0)
        # # データの順位付け
        # temp_rank = list(loto_number_count.values())
        # rank_loto_number_count = lt.rank(temp_rank)

        # temp_sum_rank = 0
        # temp_rank_combination = []
        # for num in temp_loto_num_data[-1]:
        #     temp_rank = rank_loto_number_count[loto_number_count[num]]
        #     print("[{:>2}]:({:>4})".format(num, temp_rank), end=" ")
        #     temp_sum_rank += temp_rank
        #     temp_rank_combination.append(temp_rank)
        # else:
        #     print("")
        #     print("Sum Rank: {}".format(temp_sum_rank))
        #     print("{}".format(temp_rank_combination))