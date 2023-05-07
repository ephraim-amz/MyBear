from typing import Any


class Series:
    @property
    def iloc(self) -> Any:
        raise NotImplementedError

    @property
    def min(self) -> Any:
        raise NotImplementedError

    @property
    def max(self) -> Any:
        raise NotImplementedError

    @property
    def count(self) -> Any:
        raise NotImplementedError
