from typing import Union, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping


class AutoEncoder:
    def __init__(self, train_data: np.array, test_data: np.array):
        self.__train, self.__val = train_test_split(
            train_data, test_size=0.33, shuffle=True, random_state=0)
        self._test = test_data
        self._pred = List[float]
        self._error = List[float]
        self.__model = Model
        self.__create_mid3_model()

    @property
    def train(self) -> np.array:
        return self._train

    @property
    def val(self) -> np.array:
        return self._val

    @property
    def test(self) -> np.array:
        return self._test

    @property
    def pred(self) -> List[float]:
        return self._pred

    @property
    def error(self) -> List[float]:
        return self._error


    def fit(self, min_delta: int=0, patient: int=3) -> None:
        es_cb = EarlyStopping(
            monitor='val_loss',
            min_delta=min_delta,
            patience=patient,
            verbose=0,
            mode='auto')
        self.__model.fit(
            self._train,
            self._train,
            epochs=100,
            shuffle=True,
            validation_data=(
                self._val,
                self._val),
            callbacks=[es_cb])

    def predict(self) -> None:
        self._pred = self.__model.predict(self._test)


    def fit_predict(self):
        self.fit()
        self.predict()
    

    def calc_error(self):
        for p, t in zip(self._pred, self._test):
            self._error.append((p - t)**2)
            
    def __create_mid3_model(self) -> None:
        dim = len(self.__train.reshape(-1, ))
        self.__model = Sequential()
        self.__model.add(Dense(dim, input_dim=dim, activation='relu'))
        self.__model.add(Dense(100, activation='relu'))
        self.__model.add(Dropout(rate=0.1))
        self.__model.add(Dense(50, activation='relu'))
        self.__model.add(Dropout(rate=0.1))
        self.__model.add(Dense(100, activation='relu'))
        self.__model.add(Dense(dim, activation='linear'))
        self.__model.compile(loss='mse', optimizer='adam')