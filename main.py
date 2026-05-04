import cv2
import numpy as np
from tqdm import tqdm
from numba import njit


@njit(fastmath=True)
def max_sum_rectangle(matrix):
    rows, cols = matrix.shape
    max_sum = -1e18

    final_top = 0
    final_bottom = 0
    final_left = 0
    final_right = 0

    temp = np.zeros(cols, dtype=np.float32)

    for top in range(rows):
        temp[:] = 0

        for bottom in range(top, rows):
            for c in range(cols):
                temp[c] += matrix[bottom, c]

            current_sum = 0.0
            start_col = 0

            for col in range(cols):
                current_sum += temp[col]

                if current_sum > max_sum:
                    max_sum = current_sum
                    final_top = top
                    final_bottom = bottom
                    final_left = start_col
                    final_right = col

                if current_sum < 0:
                    current_sum = 0.0
                    start_col = col + 1

    return max_sum, final_top, final_bottom, final_left, final_right


def process_video(input_path, output_path, rect_log_path):
    cap = cv2.VideoCapture(input_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = 20   # updated width
    height = 16  # updated height

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), False)

    canvas = np.zeros((height, width), dtype=np.float32)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(rect_log_path, "w") as log_file:

        for frame_index in tqdm(range(total_frames)):
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)

            current_error = np.abs(gray - canvas)

            white_improve = current_error - np.abs(gray - 255.0)
            black_improve = current_error - np.abs(gray - 0.0)

            white_gain, wt, wb, wl, wr = max_sum_rectangle(white_improve)
            black_gain, bt, bb, bl, br = max_sum_rectangle(black_improve)

            if white_gain > black_gain:
                canvas[wt:wb+1, wl:wr+1] = 255.0
                x1, y1, x2, y2, colour = wl, wt, wr, wb, 1
            else:
                canvas[bt:bb+1, bl:br+1] = 0.0
                x1, y1, x2, y2, colour = bl, bt, br, bb, 0

            # Save rectangle data
            log_file.write(f"{x1} {y1} {x2} {y2} {colour}\n")

            out.write(canvas.astype(np.uint8))

    cap.release()
    out.release()
    print("Done.")


if __name__ == "__main__":
    process_video(
        r"C:\Users\theSEAT\Desktop\Coding\Python_projects\Bad_Apple_256x256_rectangle\output.mp4",
        "badapple_rectangles_fast_64x32.mp4",
        "rectangles.txt"
    )

