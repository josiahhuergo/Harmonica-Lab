from harmonica import Mixed


class IDGen:
    def __init__(self):
        self._pool: set[int] = {0}

    def get(self) -> int:
        next_id = min(self._pool)

        if len(self._pool) == 1:
            self._pool.add(next_id + 1)

        self._pool.remove(next_id)

        return next_id

    def free(self, freed_id: int):
        id = freed_id

        if id in self._pool:
            return

        if id >= max(self._pool):
            return

        self._pool.add(id)

        if id == max(self._pool) - 1:
            while True:
                self._pool.remove(id + 1)
                if id - 1 not in self._pool:
                    break
                id -= 1


def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))


def quantize(value: Mixed, step: Mixed):
    return Mixed(round(value / step)) * step
