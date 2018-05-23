WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 710

VIDEO_PREVIEW_WIDTH = int(640 * 3 / 4)
VIDEO_PREVIEW_HEIGHT = int(480 * 3 / 4)

VIDEO_SR_SELECT_PREVIEW_WIDTH = int(640 * 0.625)
VIDEO_SR_SELECT_PREVIEW_HEIGHT = int(480 * 0.625)

SCREENS_REL_X = 0.5
SCREENS_REL_Y = 0.45

VIDEO_SELECT_SCREEN_REL_Y = 0.47

LEFT = "left"
RIGHT = "right"
FRAME_NUM_LABEL = "frame_num"

# Video Selection Screen
VIDEOS_SELECTED_TMP_FILENAME = "videos_selected.cache"

# Video Progress Screen
LEFT_FRAMES_COUNT_PREFIX = "Frames read for left video: "
RIGHT_FRAMES_COUNT_PREFIX = "Frames read for right video: "

# SR Frame Selection
SR_FRAME_SELECTION_TITLE = "Chessboard Frame Suggestion"

# SR Progress Screen
SR_PROGRESS_SCREEN_TITLE = "Finding frames valid for stereo rectification..."

SR_MAP_LABEL = "sr_map"

VALID_FRAMES_FOUND_PREFIX = "Valid frames found: "
FRAMES_READ_PREFIX = "Number of frames scanned: "

# Apply SR Screen
APPLY_SR_SCREEN_TITLE = "Video Stereo Rectification"

# Apply SR Progress Screen
APPLY_SR_PROGRESS_SCREEN_TITLE = "Applying stereo rectification to your videos..."
FRAMES_STEREO_RECTIFIED_PREFIX = "Number of frames stereo rectified: "