import dataclasses
import typing as T

from .mp4_sample_parser import RawSample


def filter_samples(
    filter_func: T.Callable[[int], bool], samples: T.Sequence[RawSample]
) -> T.List[RawSample]:
    new_samples = []
    first_timedelta = 0
    expected_duration = 0
    for idx, sample in enumerate(samples):
        expected_duration += sample.timedelta
        if filter_func(idx):
            new_samples.append(
                dataclasses.replace(
                    sample, timedelta=sample.timedelta + first_timedelta
                )
            )
            first_timedelta = 0
        else:
            if new_samples:
                new_samples[-1].timedelta += sample.timedelta
            else:
                first_timedelta += sample.timedelta
    assert expected_duration == sum(s.timedelta for s in new_samples)
    return new_samples


# def filter_max_one_keyframe_per_range(
#     samples: T.Sequence[RawSample], ranges: T.Sequence[T.Tuple[int, int]]
# ) -> T.List[RawSample]:
#     for idx, sample in enumerate(samples):
#         if sample.is_sync:
#             pass
#             # for start, end in ranges:
#             #     if start <= idx < end:
#             #         break
#             # else:
#             #     raise ValueError(f"sample {sample} at index {idx} is a keyframe but not in any range")


# filter_samples(lambda x: x.is_sync, [])
