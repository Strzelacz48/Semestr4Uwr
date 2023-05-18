from time import time
from functools import wraps


class Pos:
    def __init__(self, a, b=None):
        self.x, self.y = a if b is None else (a, b)

    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Pos(self.x-other.x, self.y-other.y)

    def __neg__(self):
        return Pos(-self.x, -self.y)

    def __eq__(self, other):
        return other is not None and self.x == other.x and self.y == other.y

    def __getitem__(self, num):
        return self.x if num == 0 else self.y

    def copy(self):
        return Pos(self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def timeit(func, runs={}, times={}):
    if func == 'START':
        times['START'] = time()
        return
    if func == 'SHOW':
        if 'START' in times:
            total_time = time() - times['START']
            del times['START']
            started = True
            sum_times = sum(times[k] for k in times)
        else:
            sum_times = sum(times[k] for k in times)
            total_time = sum_times
            started = False
        for fun, t in times.items():
            print(
                f'{fun:16} took {t*1.0:>5.1f} seconds in {runs[fun]:8} runs which is {t/total_time:>6.2%} total time')
        if started:
            print(
                f'The rest took {total_time-sum_times:>5.1f} seconds which is {(total_time-sum_times)/total_time:>6.2%} total time')
        print(f'Total time: {total_time:>5.1f} seconds')
        return
    name = func.__name__
    if name not in runs:
        runs[name] = 0
        times[name] = 0

    @wraps(func)
    def timed(*args, silent=True, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        runs[name] += 1
        times[name] += end-start
        if not silent:
            print(f'{end-start}')
        return result
    return timed


def deepcopy(thing):
    try:
        if type(thing) == dict:
            return {k: deepcopy(v) for k,v in thing.items()}
        return [deepcopy(el) for el in thing.copy()]
    except AttributeError:
        return thing

