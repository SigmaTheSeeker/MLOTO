# MLOTO,LOTO6,LOTO7共通の関数を定義する

import constants as const
import csv
import datetime
import numpy as np
import collections
import itertools
import pprint as pp

def read_loto_data(loto_data_file):
    # ロト6の過去データを読み込む
    # 引数: ロト6の過去データファイル(csv)
    # 戻り値: ロト6の過去データ（list)
    # データ形式:回号,抽選日,N1,N2,N3,N4,N5,N6,B1
    # 読込時に、型を変換する
    # 回号はシーケンシャルであることを確認する
    # シーケンシャルでない場合は、処理中のデータとメッセージを表示して終了する
    # 回号が1−543までは正しい日付であることを確認して、曜日が木曜日であることを確認する
    # 回号が543以降は正しい日付であることを確認して、曜日が月曜か木曜日であることを確認する
    # 日付が正しくない場合は、処理中のデータとメッセージを表示して終了する
    # 曜日が正しくない場合は、処理中のデータとメッセージを表示して終了する
    # 抽選数字が1-43の間であることを確認する
    # 抽選数字が重複していないことを確認する
    # 抽選数字が正しくない場合は、処理中のデータとメッセージを表示して終了する
    # ボーナス数字が1-43の間であることを確認する
    # ボーナス数字が本数字と重複していないことを確認する
    # ボーナス数字が正しくない場合は、処理中のデータとメッセージを表示して終了する
    # 回号 -> int
    # 抽選日 -> datetime,
    # N1 -> int
    # N2 -> int
    # N3 -> int
    # N4 -> int
    # N5 -> int
    # N6 -> int
    # B1 -> int
    # ファイルが存在する場合は、データを読み込んで上記の処理を行い変換されたデータを返す
    # ファイルが存在しない場合は、メッセージを表示して終了する

    try:
        loto_data = []
        temp_times = 0
        date_format = "%Y/%m/%d"
        with open(loto_data_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                temp_data = []
                # 回号のチェック
                if not row[0].isdecimal():
                    print("本数字に数字以外のデータが含まれています。")
                    print("処理中のデータ:{}".format(row))
                    exit()
                    break
                temp_data.append(int(row[0]))
                if temp_data[0] != temp_times + 1:
                    print("回号がシーケンシャルではありません。")
                    print("処理中のデータ:{}".format(row))
                    exit()
                    break
                # 抽選日
                temp_data.append(row[1])
                # 日付のチェック
                try:
                    temp_date = datetime.datetime.strptime(row[1], date_format)
                except ValueError:
                    print("日付が正しくありません。")
                    print("処理中のデータ:{}".format(row))
                    exit()
                    break
                # 曜日のチェック
                if const.LOTO == "LOTO6":
                    if temp_data[0] < const.LOTO_CHECK_TIMES:
                        if temp_date.weekday() != const.LOTO_WEEKDAY[1]:
                            print("曜日が正しくありません。")
                            print("処理中のデータ:{}".format(row))
                            exit()
                            break
                    else:
                        if temp_date.weekday() not in const.LOTO_WEEKDAY:
                            print("曜日が正しくありません。")
                            print("処理中のデータ:{}".format(row))
                            exit()
                            break
                else:
                        if temp_date.weekday() != const.LOTO_WEEKDAY:
                            print("曜日が正しくありません。")
                            print("処理中のデータ:{}".format(row))
                            exit()
                            break
                # 本数字
                # 数字以外のデータが含まれていないかチェック
                for num in row[2:const.LOTO_NUM + 2]:
                    if not num.isdecimal():
                        print("本数字に数字以外のデータが含まれています。")
                        print("処理中のデータ:{}".format(row))
                        exit()
                        break
                # 数字の範囲チェック
                for num in row[2:const.LOTO_NUM + 2]:
                    if not (const.LOTO_MIN <= int(num) <= const.LOTO_MAX):
                        print("本数字の範囲が正しくありません。")
                        print("処理中のデータ:{}".format(row))
                        exit()
                        break
                # 重複チェック
                if len(set(row[2:const.LOTO_NUM + 2])) != const.LOTO_NUM:
                    print("本数字が重複しています。")
                    print("処理中のデータ:{}".format(row))
                    exit()
                    break
                # ボーナス数字
                # 数字以外のデータが含まれていないかチェック
                for i in range(const.LOTO_B_NUM):
                    if const.LOTO == "LOTO7":
                        num = row[const.LOTO_NUM + const.LOTO_B_NUM + i]
                    else:
                        num = row[const.LOTO_NUM + const.LOTO_B_NUM + i + 1]
                    if not num.isdecimal():
                        print("ボーナス数字に数字以外のデータが含まれています。")
                        print("処理中のデータ:{}".format(row))
                        exit()
                        break
                # 数字の範囲チェック
                    if not (const.LOTO_MIN <= int(num) <= const.LOTO_MAX):
                        print("ボーナス数字の範囲が正しくありません。")
                        print("処理中のデータ:{}".format(row))
                        exit()
                        break
                # 重複チェック
                if num in row[2:const.LOTO_NUM + 2]:
                    print("ボーナス数字が本数字と重複しています。")
                    print("処理中のデータ:{}".format(row))
                    exit()
                    break
                temp_data.extend([int(num) for num in row[2:const.LOTO_NUM + const.LOTO_B_NUM + 2]])
                temp_times += 1
                loto_data.append(temp_data)
        return loto_data
    except FileNotFoundError:
        print("ファイル({})が存在しません。".format(const.LOTO_DATA_FILE))
        exit()
        return None


def all_loto_combinations():
    # 1から43までの数字を持つ配列を作成
    numbers = np.arange(1, const.LOTO_MAX + 1, dtype=np.uint8)

    # 6つの数字の組み合わせを作成
    all_loto_combinations = np.array(list(itertools.combinations(numbers, const.LOTO_NUM))).astype(np.uint8)

    return all_loto_combinations



# 合計値の集計
def sum_count(combinations):
    sum_count = {}
    for combination in combinations:
        sum = np.sum(combination)
        if sum in sum_count:
            sum_count[sum] += 1
        else:
            sum_count[sum] = 1

    # # sum_countを最小-最大スケーリングに変換
    # sum_count = {k: (v - np.min(list(sum_count.values()))) / (np.max(list(sum_count.values())) - np.min(list(sum_count.values()))) for k, v in sum_count.items()}

    return sum_count

def get_even_odd(loto_numbers):
    return loto_numbers % 2

# 偶数奇数の組み合わせをカウントする
def even_odd_count(combinations):
    even_odd_count = {}
    for combination in combinations:
        even_odd_count.setdefault(tuple(combination), 0)
        even_odd_count[tuple(combination)] += 1

    # # even_odd_countを最小-最大スケーリングに変換
    # even_odd_count = {k: (v - np.min(list(even_odd_count.values()))) / (np.max(list(even_odd_count.values())) - np.min(list(even_odd_count.values()))) for k, v in even_odd_count.items()}

    return even_odd_count

def seq_count(combinations):
    # 連番の個数
    total_seq_nums = {}
    for nums in combinations:
        tmp_seq_nums = [list(g) for _, g in itertools.groupby(nums, key=lambda n, c=itertools.count(): n - next(c))]
        tmp_keys = []
        for tmp_seq in tmp_seq_nums:
            tmp_keys.append(len(tmp_seq))

        if tuple(tmp_keys) in total_seq_nums:
            total_seq_nums[tuple(tmp_keys)] += 1
        else:
            total_seq_nums[tuple(tmp_keys)] = 1

    # # seq_countを最小-最大スケーリングに変換
    # total_seq_nums = {k: (v - np.min(list(total_seq_nums.values()))) / (np.max(list(total_seq_nums.values())) - np.min(list(total_seq_nums.values()))) for k, v in total_seq_nums.items()}

    return total_seq_nums

def num_in_past(combinations):
    # 過去n回分のデータからを受け取って、それらのデータに含まれる数字を返す
    num_in_past = []
    for combination in combinations:
        num_in_past.extend(combination)
    # 重複を削除
    num_in_past = list(set(num_in_past))

    return num_in_past


def english_calculator(combinations):
# イングリッシュ式足し算
# LOTOの1回分のデータを受け取り、イングリッシュ式足し算を行って、その数値を返す
    calculated_data = []
    # 出現した数字同士を２つずつ足す
    for i in range(const.LOTO_NUM - 1):
        for j in range(i + 1, const.LOTO_NUM):
            # 足して43を超えるものは除外する
            if (combinations[i] + combinations[j]) <= const.LOTO_MAX:
                calculated_data.append(combinations[i] + combinations[j])

    # 出現した数字同士を2つずつ引く
    for i in reversed(range(1, const.LOTO_NUM)):
        for j in range(0, i):
            calculated_data.append(combinations[i] - combinations[j])


    # 重複するデータを削除し、昇順にソートした結果を返す
    return sorted(list(set(calculated_data)))



# 直前の過去データの数±1,2,3をした数字を生成する
def serial_calculator(combinations):
    calculated_data = []
    # 出現した数字に±1を行う
    max_loop = 3
    for temp_data in combinations:
            for i in range(1, max_loop + 1):
                plus_data = temp_data + i
                # 足してLOTO_MAXを超えるものは除外する
                if plus_data <= const.LOTO_MAX:
                    calculated_data.append(plus_data)
                minus_data = temp_data - i
                # 引いて1を下回るものは除外する
                if minus_data >= 1:
                    calculated_data.append(minus_data)

    # 重複するデータを削除し、昇順にソートした結果を返す
    return sorted(list(set(calculated_data)))


def number_count(combinations):
    # 抽選結果の数字の出現回数をカウントする
    count = {}
    for combination in combinations:
        for number in combination:
            if number in count:
                count[number] += 1
            else:
                count[number] = 1

    return count


def check_result(combinations, result):
    # combinationsで予測結果を受け取る
    # resultで実際の抽選結果を受け取る
    # resultのデータ形式は、[回号, 抽選日, 数字1, 数字2, 数字3, 数字4, 数字5, 数字6, ボーナス数字]
    # 予測結果と実際の抽選結果から当選を調べる
    # len(combinations) * const.LOTO_PRCE購入金額を計算する
    # 当選金額を計算する
    # 1等の当選金額は、resultの数字がcombinationsの数字と一致した場合
    # 2等の当選金額は、resultの数字がcombinationsの数字が4つ一致しており、かつ、combinationsの数字の中にボーナス数字が含まれている場合
    # 3等の当選金額は、resultの数字がcombinationsの数字が4つ一致している場合
    # 4等の当選金額は、resultの数字がcombinationsの数字が3つ一致している場合
    # 上記以外はハズレ
    # 戻り値は、回号、購入金額、当選等数、当選金額
    used_money = len(combinations) * const.LOTO_PRICE
    hit_rank = []
    hit_price = []
    temp_result = result[2:const.LOTO_NUM + 2]
    temp_result_bn = result[const.LOTO_NUM +  const.LOTO_B_NUM +1]
    for combination in combinations:
        hit_number = len(set((temp_result)) & set(combination))
        if hit_number == const.LOTO_NUM:
            hit_rank.append(1)
            hit_price.append(const.LOTO_1ST_PRIZE)

        elif hit_number == (const.LOTO_NUM - 1) and (temp_result_bn in combination):
            hit_rank.append(2)
            hit_price.append(const.LOTO_2ND_PRIZE)

        elif hit_number == (const.LOTO_NUM - 1) and (temp_result_bn not in combination):
            hit_rank.append(3)
            hit_price.append(const.LOTO_3RD_PRIZE)

        elif hit_number == (const.LOTO_NUM - 2):
            hit_rank.append(4)
            hit_price.append(const.LOTO_4TH_PRIZE)

        else:
            hit_rank.append(5)
            hit_price.append(0)


    return used_money, hit_rank, hit_price


# ランキングを作成する
def rank(source_data):
    rank = {}
    # 入力されたデータに対して、順位を付ける
    temp_rank = [1 for n in range(len(source_data))]
    for i in range(len(source_data)):
         for j in range(len(source_data)):
             if source_data[i] < source_data[j]:
                 temp_rank[i] += 1

    # 順位とデータを辞書に登録する
    for temp_key, temp_value in zip(source_data, temp_rank):
        rank.setdefault(temp_key, temp_value)
     
    return rank