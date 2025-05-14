import os
import cv2
import moviepy as mp
import argparse

# get resolution of images
def get_image_resolution(image_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    return width, height

# get resolution and framerate of video files
def get_video_info(video_path):
    video = mp.VideoFileClip(video_path)
    width, height = video.size
    framerate = video.fps
    return width, height, framerate

# process the files in a folder and calculate ideal resolution, max framerate, and files matching ideal resolution/framerate
def calculate_ideal_profile(folder_path):
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'jfif', 'webp'))]
    video_files = [f for f in files if f.lower().endswith(('mp4', 'avi', 'mov', 'mkv'))]

    resolutions = []  # all resolutions of images and videos
    max_width = 0
    max_height = 0
    max_framerate = 0
    matching_files = []  # filenames with the same resolution and framerate as the ideal
    all_files_match = False # if all file resolutions are the same

    # process all images
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        width, height = get_image_resolution(img_path)
        resolutions.append((width, height))
        max_width = max(max_width, width)
        max_height = max(max_height, height)

    # process all videos
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        width, height, framerate = get_video_info(video_path)
        resolutions.append((width, height))
        max_width = max(max_width, width)
        max_height = max(max_height, height)
        max_framerate = max(max_framerate, framerate)

    # process images again to check if they match the ideal resolution/framerate
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        width, height = get_image_resolution(img_path)
        if max_framerate == 30 and (width, height) == (max_width, max_height): # 30 fps is the standard framerate for my purposes
            matching_files.append(img_file)

    # process videos again to check if they match the ideal resolution/framerate
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        width, height, framerate = get_video_info(video_path)
        if (width, height) == (max_width, max_height) and framerate == max_framerate:
            matching_files.append(video_file)

    # check if all resolutions are the same
    all_files_match = len(set(resolutions)) == 1

    return max_width, max_height, max_framerate, matching_files, all_files_match

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", nargs="?", default=os.getcwd(), help="Path to the folder containing the image and video files. Default is the current directory.")

    args = parser.parse_args()

    max_width, max_height, max_framerate, matching_files, all_files_match = calculate_ideal_profile(args.folder_path)

    os.system('clear') # moviepy has a bug right now that makes it print a bunch of stuff, fixed in future release: https://github.com/Zulko/moviepy/issues/2376
    print(f"Ideal resolution: {max_width}x{max_height}")
    print(f"Max framerate: {max_framerate}")

    if(all_files_match):
        print("All images/videos have the same resolution.")

    if(len(matching_files)>=1):
        print(f"Files with the same resolution and framerate: {matching_files}")

    # check if the ideal profile fits any normal 720p/1080p profile
    if (max_width <= 1280 and max_height <= 720 and max_framerate <= 30):
        print("Best standard profile: 720p30")
    elif (max_width <= 1280 and max_height <= 720 and max_framerate <= 60):
        print("Best standard profile: 720p60")
    elif (max_width <= 1920 and max_height <= 1080 and max_framerate <= 30):
        print("Best standard profile: 1080p30")
    elif (max_width <= 1920 and max_height <= 1080 and max_framerate <= 60):
        print("Best standard profile: 1080p60")
    else:
        print("The video can't be accommodated by any standard 720p/1080p profile.")

if __name__ == "__main__":
    main()
