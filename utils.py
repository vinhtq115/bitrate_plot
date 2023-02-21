from typing import Tuple
import json
import os
import subprocess


def get_framerate(input_path: str, stream_index: int = 0) -> float:
    with subprocess.Popen(
        [
            "ffprobe",
            "-select_streams", f"v:{stream_index}",
            "-print_format", "json",
            "-count_frames",
            "-threads", f"{os.cpu_count()}",
            "-show_entries", "format=duration:stream=nb_read_frames",
            input_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ) as p:
        lines = [line.decode('utf-8').strip() for line in p.stdout]
    data = json.loads("".join(lines))

    duration = float(data['format']['duration'])
    n_frames = int(data['streams'][0]['nb_read_frames'])
    return n_frames / duration


def count_streams(input_path: str) -> Tuple[int, int]:
    """Get number of video and audio streams from a file.

    Args:
        input_path (str): Path to input file

    Returns:
        Tuple[int, int]: Number of video and audio streams
    """
    with subprocess.Popen(
        [
            "ffprobe",
            "-hide_banner",
            "-print_format", "json",
            "-show_streams",
            input_path
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    ) as p:
        lines = [line.decode('utf-8').strip() for line in p.stdout]
    data = json.loads("".join(lines))
    if data.get('streams') is None:
        return 0, 0

    audio_count = 0
    video_count = 0
    for stream in data['streams']:
        if stream['codec_type'] not in ['audio', 'video']:
            # Skip data stream
            continue

        if stream['codec_type'] == 'audio':
            audio_count += 1
        else:
            video_count += 1

    return video_count, audio_count
