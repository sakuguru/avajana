import random
import asyncio
from inspect import iscoroutine
from time import sleep
from typing import Awaitable, Callable


async def call_a_function(func: Callable):
    return_ = func()
    if iscoroutine(return_):
        await return_


class Bubbling:
    def __init__(self, word_per_min=168):
        # https://humanbenchmark.com/tests/typing, https://www.reddit.com/r/MechanicalKeyboards/comments/6gqblx/typeracer_wpm_percentiles/
        # a 80 percentile typing speed but we are better than HUMAN isn't it? 555
        # and Thai contain more character than Eng
        self.word_per_min = word_per_min

    @property
    def charactor_per_min(self):
        # English Estimate
        return self.word_per_min * 5

    @property
    def gap_between_seen_and_start_typing(self):
        """
        in milisecond
        """
        return random.normalvariate(100, 100)

    async def act_typing(
        self, text, typing_func: Callable, stop_typing_func: Callable, *, non_stop=False
    ):
        """
        This function simulates typing with a resonable pause in a given text.

        :param text:
        :param typing_func:
        :param stop_typing_func:
        :return:
        """
        duration_min = len(text) / self.charactor_per_min
        num_of_word = len(text) / 5
        num_of_sentence = num_of_word // 5
        duration_sec = duration_min * 60

        # this pareto dist. aims to make 2/3 = 0
        num_of_pause = min(
            round(random.paretovariate(2.64)) - 1, max(num_of_sentence, 3)
        )
        remain_pause = num_of_pause if not non_stop else 0
        remain_time = duration_sec
        while True:
            await asyncio.sleep(0.3)
            await call_a_function(typing_func)
            if remain_pause == 0:
                await asyncio.sleep(remain_time)
                await call_a_function(typing_func)
                break
            else:
                type_for = random.random() * remain_time
                remain_time -= type_for
                await asyncio.sleep(type_for)
                remain_pause -= 1
            await call_a_function(stop_typing_func)

    def act_typing_simple_sync(
        self, text, typing_func: callable, stop_typing_func: callable
    ):
        duration_min = len(text) / self.charactor_per_min
        duration_sec = duration_min * 60
        typing_func()
        sleep(duration_sec)
        stop_typing_func()
