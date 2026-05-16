from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ScheduleResult:
    next_review_date: date
    interval_days: int
    ease_factor: float
    review_count: int


def calculate_next_review(
    rating: int,
    interval_days: int,
    ease_factor: float,
    review_count: int,
) -> ScheduleResult:
    """SM-2 spaced repetition algorithm. rating: 1-5 (1=forgot, 5=perfect).

    Ratings < 3 reset the item; ratings >= 3 grow the interval.
    Ease factor adjusts so hard items come back sooner, easy ones space out further.
    """
    if rating < 3:
        return ScheduleResult(
            next_review_date=date.today() + timedelta(days=1),
            interval_days=1,
            ease_factor=ease_factor,
            review_count=0,
        )

    if review_count == 0:
        new_interval = 1
    elif review_count == 1:
        new_interval = 6
    else:
        new_interval = round(interval_days * ease_factor)

    # SM-2 formula: EF += 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
    # rating 5 -> EF increases, rating 4 -> no change, rating 3 -> EF decreases
    q = rating
    new_ease = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ease = max(1.3, round(new_ease, 4))

    return ScheduleResult(
        next_review_date=date.today() + timedelta(days=new_interval),
        interval_days=new_interval,
        ease_factor=new_ease,
        review_count=review_count + 1,
    )
