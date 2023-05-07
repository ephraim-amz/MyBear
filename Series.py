from typing import Any

import numpy as np


class Series:
    def __init__(self, data, index, dtype, name):
        self.index = index
        self.data = data
        self.dtype = dtype
        self.name = name

    @property
    def iloc(self) -> Any:
        raise NotImplementedError

    def min(self) -> Any:
        raise min(self.data)

    def max(self) -> Any:
        max(self.data)

    def count(self) -> Any:
        return len(self.data)

    def std(self) -> Any:
        return np.std(list(self.data.values()))

    def mean(self) -> Any:
        return np.mean(list(self.data.values()))

    def __repr__(self):
        return f"Data : {self.data} "
