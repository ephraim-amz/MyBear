import numpy as np
from typing import List, Dict, Callable, Any


class DataFrame:
    @property
    def iloc(self):
        raise NotImplementedError

    @property
    def max(self):
        raise NotImplementedError

    @property
    def min(self) -> np.int64:
        raise NotImplementedError

    @property
    def mean(self) -> np.float64:
        raise NotImplementedError

    @property
    def std(self) -> np.float64:
        raise NotImplementedError

    @property
    def count(self) -> np.int64:
        raise NotImplementedError

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]):
        raise NotImplementedError

    def read_csv(path: str, delimiter: str = ","):
        raise NotImplementedError

    def read_json(path: str, orient: str = "records"):
        raise NotImplementedError

    def join(self, other, left_on: List[str] | str, right_on: List[str] | str, how: str = "left"):
        raise NotImplementedError
