# bitrate_plot

Plot bitrate graph of video file.

## Requirements

- `ffmpeg` is installed and `ffprobe` is added to `PATH`.
- Run `pip install -r requirements.txt` to install dependencies.

## Run

```
usage: plot_bitrate.py [-h] [-o OUTPUT] [-f {png,jpg}] input

Plot bitrate of all streams in video/audio files

positional arguments:
  input                 Path to input file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to output folder. Default: current folder
  -f {png,jpg}, --format {png,jpg}
                        Format of plot file. Default: png
```
