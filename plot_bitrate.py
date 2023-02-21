from argparse import ArgumentParser
from pathlib import Path
import json
import os
import subprocess

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np


from utils import count_streams, get_framerate


def plot_bitrate(bitrates: np.ndarray, title: str = None) -> Figure:
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))

    ax.plot(bitrates)

    if title:
        ax.set_title(title)

    ax.set_xlabel('Time (s)')
    ax.set_xticks(np.arange(0, len(bitrates), 60))

    ax.set_ylabel('Bitrate (B)')

    return fig


def main(args):
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_format = args.format

    if not input_path.exists():
        # TODO: throw error here
        pass

    output_path.mkdir(parents=True, exist_ok=True)

    filename = input_path.stem
    video_streams, audio_streams = count_streams(input_path.as_posix())

    for stream in range(video_streams):
        print(f'Processing video stream #{stream}')

        fps = int(np.ceil(get_framerate(input_path.as_posix(), stream)))
        print(f'FPS: {fps}')

        with subprocess.Popen(
            [
                "ffprobe",
                "-hide_banner",
                "-threads", f"{os.cpu_count()}",
                "-print_format", "json",
                "-select_streams", f"v:{stream}",
                "-show_entries", "frame=pict_type,pkt_pts_time,best_effort_timestamp_time,pkt_size",
                input_path.as_posix()
            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        ) as p:
            lines = [line.decode('utf-8') for line in p.stdout]
        data = json.loads("".join(lines))

        frames_bitrate = []
        for frame in data['frames']:
            frame_size = int(frame['pkt_size'])
            frames_bitrate.append(frame_size)
        print('Number of frames:', len(frames_bitrate))

        per_second_bitrates = []
        i = 0
        while i < len(frames_bitrate):
            sliced_bitrates = frames_bitrate[i:i+fps]
            per_second_bitrates.append(sum(sliced_bitrates) / len(sliced_bitrates))
            i += fps
        per_second_bitrates = np.array(per_second_bitrates)

        fig = plot_bitrate(per_second_bitrates, input_path.name)

        fig.savefig(output_path / f'{filename}_video_{stream}.{output_format}')


if __name__ == '__main__':
    parser = ArgumentParser(description='Plot bitrate of all streams in video/audio files')
    parser.add_argument('input', type=str, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, help='Path to output folder. Default: current folder', default='.')
    parser.add_argument('-f', '--format', type=str, help='Format of plot file. Default: png',
        choices=['png', 'jpg'], default='png')

    main(parser.parse_args())
