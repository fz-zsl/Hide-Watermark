import argparse
import cv2
import HammingCode
import LoadData
import numpy as np


zigzag_ord = [[0, 1, 5, 6, 14, 15, 27, 28],
              [2, 4, 7, 13, 16, 26, 29, 42],
              [3, 8, 12, 17, 25, 30, 41, 43],
              [9, 11, 18, 24, 31, 40, 44, 53],
              [10, 19, 23, 32, 39, 45, 52, 54],
              [20, 22, 33, 38, 46, 51, 55, 60],
              [21, 34, 37, 47, 50, 56, 59, 61],
              [35, 36, 48, 49, 57, 58, 62, 63]]
zigzag_pos = np.zeros((64, 2), dtype=int)
info_begin = 21 # 13
info_end = 36 # 28
info_len = info_end - info_begin
self_info_len = 11
eps = 3


def calc(val, bit):
    neg = False
    if val < 0:
        neg = True
        val = -val
    if val < 10 ** -6:
        val = eps * (1 if bit == 1 else 2)
    else:
        val = int(np.floor(val / eps))
        if val & 1 != bit:
            val += 1
        val *= eps
    return val if not neg else -val


def blk_dct(img):
    height, width = img.shape[:2]
    blk_height = height >> 3
    blk_width = width >> 3
    dct_height = blk_height << 3
    dct_width = blk_width << 3
    img_cut = img[: dct_height, : dct_width]
    img_dct = np.zeros((dct_height, dct_width), dtype=np.float32)
    for blk_h in range(blk_height):
        for blk_w in range(blk_width):
            img_blk = img_cut[blk_h << 3: (blk_h + 1) << 3, blk_w << 3: (blk_w + 1) << 3]
            img_blk2 = cv2.dct(np.float32(img_blk))
            code11 = 0
            for self_info_index in range(self_info_len):
                code11 = code11 << 1 | self_info[blk_h][blk_w][self_info_index]
            code15 = HammingCode.hamming_code_gen[code11]
            for info_index in range(info_begin, info_end):
                img_blk2[zigzag_pos[info_index][0]][zigzag_pos[info_index][1]] \
                    = calc(img_blk2[zigzag_pos[info_index][0]][zigzag_pos[info_index][1]],
                           (code15 >> (14 - info_index + info_begin)) & 1)
            img_dct[blk_h << 3: (blk_h + 1) << 3, blk_w << 3: (blk_w + 1) << 3] = cv2.idct(img_blk2)
    return img_dct


def get_arr(arr, l, r):
    if l % arr.__len__() < r % arr.__len__():
        return arr[l % arr.__len__(): r % arr.__len__()]
    return arr[l % arr.__len__():] + arr[: r % arr.__len__()]


if __name__ == "__main__":
    # set arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, default='P.jpg')  # img_path
    parser.add_argument('--logo', type=str, default='深圳杯数学建模挑战赛')  # short watermark
    parser.add_argument('--text', type=str, default='law.txt')  # text_path, long watermark
    parser.add_argument('--output', type=str, default='SP.png')  # output file
    args = parser.parse_args()

    # size of image
    img_arr = LoadData.load_image(str(args.img))
    height, width, channel = img_arr.shape
    capacity = (height >> 3) * (width >> 3) * channel * self_info_len

    # put watermark into text_arr
    if str(args.logo).__len__() == 0:
        # long watermark
        text_arr = LoadData.load_text(str(args.text))
        if text_arr.__len__() > capacity:
            print("[Error] Text too long.")
            exit(101)
    else:
        # short watermark
        text_arr = []
        for ch in str(args.logo):
            text_arr.append(ord(ch))

    # transform text_arr into binary code array text_bin
    text_bin = []
    for bit in range(15, -1, -1):
        text_bin.append((text_arr.__len__() >> bit) & 1)
    for ch in text_arr:
        for bit in range(15, -1, -1):
            text_bin.append((ch >> bit) & 1)

    # pre-process zigzag order
    for x in range(8):
        for y in range(8):
            zigzag_pos[zigzag_ord[x][y]] = [x, y]

    # flatten image to 1-channel form
    blk_height = height >> 3
    blk_width = width >> 3
    img_arr2 = np.zeros(((blk_height << 3) * channel, blk_width << 3), dtype=np.float32)
    for ch in range(channel):
        for blk_h in range(blk_height):
            for hh in range(8):
                for ww in range(blk_width << 3):
                    img_arr2[(blk_h * channel + ch) << 3 | hh][ww] = img_arr[blk_h << 3 | hh][ww][ch]

    # pre-process self_info
    self_info = np.zeros((blk_height * channel, blk_width, self_info_len), dtype=int)
    for blk_h in range(blk_height * channel):
        for blk_w in range(blk_width):
            blk_index = blk_h * blk_width + blk_w
            self_info[blk_h][blk_w] = get_arr(text_bin, blk_index * self_info_len, (blk_index + 1) * self_info_len)

    HammingCode.__init__()
    img_res2 = blk_dct(img_arr2)

    # restore image into 3-channel form
    img_res = np.zeros((blk_height << 3, blk_width << 3, channel), dtype=np.float32)
    for ch in range(channel):
        for blk_h in range(blk_height):
            for hh in range(8):
                for ww in range(blk_width << 3):
                    img_res[blk_h << 3 | hh][ww][ch] = img_res2[(blk_h * channel + ch) << 3 | hh][ww]

    # surrounding completion
    img_res_full = img_arr.copy().astype(np.float32)
    img_res_full[: blk_height << 3, : blk_width << 3, :] = img_res

    img_res_full_int = np.zeros_like(img_res_full, dtype=np.uint8)
    for x in range(img_res_full_int.shape[0]):
        for y in range(img_res_full_int.shape[1]):
            for c in range(channel):
                img_res_full_int[x][y][c] = max(min(int(np.rint(img_res_full[x][y][c])), 255), 0)
    LoadData.save_img(img_res_full_int, str(args.output))
