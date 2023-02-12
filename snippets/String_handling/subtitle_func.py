import os
import pathlib
import json
from collections import deque

from snippets.Built_in.datetime_ import second_to_timecode

PRJ_ROOT_PATH = pathlib.Path(__file__).parent.parent.absolute()
APP_PATH = os.path.join(PRJ_ROOT_PATH, "app")


def json2sub(session_id: str, json_str: str, fps=10, save: bool = True, ext: str = "vtt"):
    break_ = "\r\n" if ext == "srt" else "\n"
    vtt_header = "WEBVTT\n"
    frame_time_in_sec = 1/fps
    subtitle_arr = [] if ext == "srt" else [vtt_header]
    js_dict = json.loads(json_str)
    caption_queue = deque()
    for frame_no, frame_items in sorted(js_dict.items(), key=lambda x: x[0], reverse=False):
        if len(frame_items):
            caption_line_arr = []
            for obj_id, obj_data in sorted(frame_items.items(), key=lambda x: x[0], reverse=False):
                tmp_caption_line = "INSERT CAPTION LINE"
                if len(tmp_caption_line.strip()):
                    caption_line_arr.append(tmp_caption_line)
            if len(caption_line_arr):
                caption_line = break_.join(caption_line_arr)
                caption_queue.append((int(frame_no), caption_line))

    while len(caption_queue) > 1:
        caption_idx = 1
        first_frame, caption_line = caption_queue.popleft()
        second_frame, _ = caption_queue[0]
        ts_start = (first_frame - 1) * frame_time_in_sec
        duration = (second_frame - first_frame) * frame_time_in_sec
        ts_end = (ts_start + duration) if duration <= 1 else (ts_start + 1)
        time_line = f"{second_to_timecode(ts_start)} --> {second_to_timecode(ts_end)}"
        subtitle_arr.append("\n".join([str(caption_idx), time_line, caption_line, ""]))
        caption_idx += 1
        if len(caption_queue) == 1:
            last_frame, caption_line = caption_queue.popleft()
            ts_start = (last_frame - 1) * frame_time_in_sec
            ts_end = ts_start + 1
            time_line = f"{second_to_timecode(ts_start)} --> {second_to_timecode(ts_end)}"
            subtitle_arr.append("\n".join([str(caption_idx), time_line, caption_line, ""]))

    parsed_str = "\n".join(subtitle_arr)
    if save:
        save_path = os.path.join(APP_PATH, "result", session_id)
        with open(os.path.join(save_path, f"result.{ext}"), 'w+', encoding='utf-8') as f:
            f.writelines(parsed_str)
    return parsed_str
