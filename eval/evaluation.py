from  typing import List

import numpy as np
import pandas as pd

class Eval:
    def rate_calculation(data: any, calc_kind: int, delta_x: int) -> List[int]:
        rate = []
        for n in range(11):
            cnt = 0
            for i in range(15, 150):
                x = i // 3 + 1
                y = i % 3 + 1
                decode_image = ae.predict(data[i].reshape(1, 150))
                error = (data[i] - decode_image)**2
                obs_flag = (error > (error.mean() + error.std() * n))\
                    .reshape(3, 50)[y-1][x-delta_x+1:x-1]
                if(calc_kind == 'TP' or calc_kind == 'FP'):
                    if obs_flag:
                        cnt += 1
                else:
                    if not obs_flag:
                        cnt += 1
            rate.append(cnt)
        return rate


    def rate_calculations(data: any) -> pd.DataFrame:
        _rates = pd.DataFrame()
        matrix_kinds = ['TP', 'FP', 'TN', 'FN']
        for kind in matrix_kinds:
            tmp = []
            for delta_x in range(1, 6):
                tmp.append(rate_calculation(data, kind, delta_x))
            _rates[matrix_kinds] = tmp

        return _rates


    def accuracy(TP, FP, TN, FN):
        try:
            return TP + TN / (TP + FP + TN + FN)
        except ZeroDivisionError:
            return 0


    def recall(TP, FN):
        try:
            return TP / (TP + FN)
        except ZeroDivisionError:
            return 0


    def precision(TP, FP):
        try:
            return TP / (TP + FP)
        except ZeroDivisionError:
            return 0


    def fscore(recall, precision):
        try:
            return (2 * recall * precision) / (recall + precision)
        except ZeroDivisionError:
            return 0


    def fmeasure(recall, precision, beta=2):
        weight = beta**2
        try:
            return ((1 + weight) * recall * precision) / \
                (recall + weight * precision)
        except ZeroDivisionError:
            return 0

    def matrix_gen(rates: pd.DataFrame) -> pd.DataFrame:
        matrix = pd.DataFrame()
        matrix['recall'] = recall(rates["TP"], rates["FN"])
        matrix['precision'] = precision(rates["TP"], rates["FP"])
        matrix['fmeasure'] = fmeasure(matrix['recall'], matrix['prcision'])
        return matrix
        
