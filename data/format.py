import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class Data:
    def __init__(
            self,
            data: pd.DataFrame,
            distance: int = 1000,
            cell_num: int = 50,
            time: int = 1000):
        self.__data = data
        self.__distance = distance
        self.__cell_num = cell_num
        self.__time = time
        self.__init_format()
        self.__divide_load()
        self.__fill_nancell()
        self.__cum_sum_acceleration()

    @property
    def data(self):
        return self.__data

    '''
    @name: fotmat_data
    @brief: 目的の時刻のデータを抽出し、車線数 x cell数のデータフレームに変換
    @return: 車線数 x cell数に変換したデータフレーム
    '''

    def format_data(
            self,
            time: int = 999,
            standard_scale: bool = True) -> pd.DataFrame:
        __data = self.__data[self.__data['time']
                             == time][['x', 'y', 'acceleration']]
        if(standard_scale):
            __data['acceleration'] = self.__standard_scaler(
                __data['acceleration'])
        __df = pd.DataFrame({'1': np.array(__data[__data['y'] == 1]['acceleration']),
                             '2': np.array(__data[__data['y'] == 2]['acceleration']),
                             '3': np.array(__data[__data['y'] == 3]['acceleration'])})
        __df.index = [i for i in range(1, 51)]
        return __df

    '''
    @name: __init_format
    @brief: 値を分析しやすいように整形
    '''

    def __init_format(self):
        self.__data.columns = [
            'time',
            'acceleration',
            'angle',
            'id',
            'lane',
            'pos',
            'slope',
            'speed',
            'type',
            'x',
            'y']
        self.__data = self.__data[self.__data['type'] == 'Car']
        self.__data = self.__data[['time', 'acceleration', 'lane', 'pos']]
        self.__data = self.__data.rename({'lane': 'y'}, axis=1)
        self.__data['time'] -= 500
        self.__data = self.__data[self.__data['acceleration'] < 0]
        self.__data['acceleration'] = -self.__data['acceleration']

    '''
    @name: __devide_load
    @brief: 入力されたデータフレームを指定の数のcell_numに分割する
    '''

    def __divide_load(self):
        self.__data['pos'] = self.__data['pos'].astype(int)
        self.__data['time'] = self.__data['time'].astype(int)
        self.__data['x'] = 0
        cell_length = self.__distance // self.__cell_num
        for i in range(1, self.__cell_num + 1):
            self.__data.loc[(self.__data['pos'] > self.__distance +
                             cell_length *
                             (i -
                              1)) & (self.__data['pos'] <= self.__distance +
                                     cell_length *
                                     i), 'x'] = i
        self.__data = self.__data[self.__data['x'] != 0]
        self.__data = self.__data.drop(['pos'], axis=1)

    '''
    @name: __fill_nancell
    @brief: 値がないcellを0で埋める
    '''

    def __fill_nancell(self):
        __times = []
        __x_nums = []
        __y_nums = []
        for t in range(0, self.__time):
            for y in range(1, 4):
                for x in range(1, self.__cell_num + 1):
                    __times.append(t)
                    __x_nums.append(x)
                    __y_nums.append(y)
        __df = pd.DataFrame({'time': __times, "x": __x_nums, "y": __y_nums})
        self.__data = pd.merge(
            __df, self.__data, on=[
                'time', 'y', 'x'], how='left')
        self.__data = self.__data.fillna(0)

    '''
    @name: __cum_sum_acceleration
    @brief: 加速度の累計値を取る
    '''

    def __cum_sum_acceleration(self):
        self.__data = self.__data.groupby(
            ['time', 'y', 'x']).sum().reset_index()
        __target_data = pd.DataFrame(
            index=[], columns=[
                'time', 'y', 'x', 'acceleration'])
        for y in range(1, 4):
            for x in range(1, self.__cell_num + 1):
                __target_cell = self.__data[(
                    self.__data['y'] == y) & (self.__data['x'] == x)]
                __target_cell['acceleration'] = __target_cell['acceleration'].cumsum()
                __target_data = __target_data.append(__target_cell)
        self.__data = __target_data

    '''
    @brief: データの標準化
    @params: 標準化したいデータ
    '''

    def __standard_scaler(self, data: pd.Series) -> pd.Series:
        __sc = StandardScaler()
        __data_std = __sc.fit_transform(
            np.array(data).reshape(-1, 1)).reshape(-1, )
        return __data_std
