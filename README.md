# 🎬 Screenshot Video

`Screenshot Video` is a Python program that captures a predefined number of screenshots from a video and optionally removes duplicate screenshots based on similarity. It uses OpenCV for video processing and image comparison.

## Features

- Extracts screenshots evenly distributed across the duration of a video.
- Detects and removes duplicate screenshots using ORB (Oriented FAST and Rotated BRIEF) feature matching.
- Ensures screenshots are not pixelated by analyzing gradient variations.

## 📦 Requirements

The program requires Python 3.11 and the following dependencies, which are listed in the [`requirements.txt`](requirements.txt) file:

- `opencv-python`
- `opencv-contrib-python`
- `numpy`
- `cx_Freeze`
- Other dependencies as specified in the `requirements.txt`.

Install the dependencies using:

```bash
pip install -r requirements.txt
```

## 🚀 Usage
Run the program using the command line:

Arguments:

```bash
--path (required): Path to the input video file.

--output (-o): Directory to save the screenshots. Defaults to ./output.

--number-screenshots (--num-sshots): Number of screenshots to capture. Defaults to 200.

--threshold (-t): Similarity threshold for duplicate detection. Defaults to 0.6.

--remove-duplicates (-r): Flag to enable removal of duplicate screenshots.
```

## Building the Executable
To build the program as an executable using cx_Freeze, run:

```bash
python setup.py build
```