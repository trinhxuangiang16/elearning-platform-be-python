from bisect import bisect_left, bisect_right


def normalize_intervals(intervals):
    if not intervals or not isinstance(intervals, list):
        return []
    cleaned = []
    for item in intervals:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            start_val = int(item[0])
            end_val = int(item[1])
            if end_val > start_val:
                cleaned.append([start_val, end_val])
    cleaned.sort(key=lambda pair: pair[0])
    merged = []
    for start_val, end_val in cleaned:
        if not merged or merged[-1][1] < start_val:
            merged.append([start_val, end_val])
        else:
            merged[-1][1] = max(merged[-1][1], end_val)
    return merged


def merge_new_interval(intervals, new_start, new_end):
    current = normalize_intervals(intervals)
    start_val = max(0, int(new_start))
    end_val = max(start_val, int(new_end))

    if end_val <= start_val:
        return current

    if not current:
        return [[start_val, end_val]]

    starts = [iv[0] for iv in current]
    ends = [iv[1] for iv in current]

    left_idx = bisect_left(ends, start_val)
    right_idx = bisect_right(starts, end_val)

    if left_idx < right_idx:
        merged_start = min(start_val, current[left_idx][0])
        merged_end = max(end_val, current[right_idx - 1][1])
    else:
        merged_start = start_val
        merged_end = end_val

    updated = [list(iv) for iv in current]
    updated[left_idx:right_idx] = [[merged_start, merged_end]]
    return updated


def calculate_watched_seconds(intervals):
    total = 0
    for start_val, end_val in normalize_intervals(intervals):
        if end_val > start_val:
            total += end_val - start_val
    return total


def process_video_progress_ping(
    existing_intervals,
    previous_position,
    existing_completed,
    last_ping_at,
    now_dt,
    lesson_duration,
    payload,
    strict_anticheat=False,
):
    intervals = normalize_intervals(existing_intervals)
    duration = max(0, int(lesson_duration or 0))

    raw_watched = payload.get("thoiGianXem")
    raw_completed = payload.get("daHoanThanh")
    start_time = payload.get("startTime")
    end_time = payload.get("endTime")

    if start_time is not None and end_time is not None:
        new_start = max(0, int(start_time))
        new_end = max(new_start, int(end_time))
        current_pos = int(raw_watched) if raw_watched is not None else new_end

        if strict_anticheat:
            delta_video = new_end - new_start
            delta_real = (now_dt - last_ping_at).total_seconds() if last_ping_at else 0.0
            delta_real = max(0.0, delta_real)
            if delta_video > (delta_real * 2.5 + 15):
                new_start = max(0, new_end - 5)

        if new_end > new_start:
            intervals = merge_new_interval(intervals, new_start, new_end)

    elif (
        not strict_anticheat
        and bool(raw_completed) is True
        and duration > 0
        and (raw_watched is None or int(raw_watched) >= duration)
    ):
        current_pos = int(raw_watched) if raw_watched is not None else duration
        intervals = merge_new_interval(intervals, 0, duration)

    else:
        current_pos = max(0, int(raw_watched or 0))
        prev_pos = max(0, int(previous_position or 0))

        if current_pos > prev_pos:
            new_start = prev_pos
            new_end = current_pos
        else:
            new_start = current_pos
            new_end = current_pos

        delta_video = new_end - new_start
        if last_ping_at is not None:
            delta_real = max(0.0, (now_dt - last_ping_at).total_seconds())
        else:
            delta_real = 0.0 if strict_anticheat else float(delta_video)

        if strict_anticheat or last_ping_at is not None:
            if delta_video > (delta_real * 2.5 + 15):
                new_start = max(0, current_pos - 5)
                new_end = current_pos

        if new_end > new_start:
            intervals = merge_new_interval(intervals, new_start, new_end)

    actual_watched_seconds = calculate_watched_seconds(intervals)
    if duration > 0 and actual_watched_seconds > duration:
        actual_watched_seconds = duration

    if duration > 0:
        if actual_watched_seconds >= 0.8 * duration:
            da_hoan_thanh = True
        elif not strict_anticheat and bool(raw_completed) is True:
            da_hoan_thanh = True
        elif existing_completed and not strict_anticheat:
            da_hoan_thanh = True
        else:
            da_hoan_thanh = False
    else:
        da_hoan_thanh = bool(raw_completed) if raw_completed is not None else bool(existing_completed)

    return {
        "thoi_gian_xem": current_pos,
        "da_hoan_thanh": da_hoan_thanh,
        "watched_intervals": intervals,
        "actual_watched_seconds": actual_watched_seconds,
        "last_ping_at": now_dt,
    }
