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


def calc(val):
    return int(np.rint(abs(val) / eps)) & 1


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
            img_dct[blk_h << 3: (blk_h + 1) << 3, blk_w << 3: (blk_w + 1) << 3] = img_blk2
            code15 = 0
            for info_index in range(info_begin, info_end):
                code15 = (code15 << 1) | calc(img_blk2[zigzag_pos[info_index][0]][zigzag_pos[info_index][1]])
            self_info[blk_h][blk_w] = HammingCode.gen11(HammingCode.hamming_code_near[code15])


def vote(num_arr):
    cnt = np.zeros((16, 2), dtype=int)
    for num in num_arr:
        for bit in range(16):
            cnt[bit][int(num) >> bit & 1] += 1
    num = 0
    for bit in range(16):
        num |= (1 if cnt[bit][1] > cnt[bit][0] else 0) << bit
    return num


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, default='SP.png')  # image with watermark
    args = parser.parse_args()

    # size of image
    img_arr = LoadData.load_image_inv(str(args.img))
    height, width, channel = img_arr.shape
    # print(img_arr)

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

    # extract self_info
    HammingCode.__init__()
    self_info = np.zeros((blk_height * channel, blk_width, self_info_len), dtype=int)
    blk_dct(img_arr2)

    pnt = 0
    num = 0
    text_arr = []
    for x in range(blk_height * channel):
        for y in range(blk_width):
            for self_info_index in range(self_info_len):
                num = num << 1 | self_info[x][y][self_info_index]
                pnt += 1
                if (pnt & 15) == 0:
                    text_arr.append(num)
                    num = 0

    watermark_len = vote(text_arr[: 10])
    watermark = []
    for x in range(watermark_len):
        buc = []
        for y in range(10 + x, text_arr.__len__(), watermark_len):
            buc.append(text_arr[y])
        watermark.append(chr(vote(buc)))

    if watermark_len <= 100:
        print("Watermark: ", end='')
        for ch in watermark:
            print(ch, end='')
    else:
        print('[Note] Watermark is long, please view in \'./output/watermark.txt\'.')
        watermark_str = ''.join(str(ch) for ch in watermark)
        with open('output/watermark.txt', 'w') as file_output:
            print(watermark_str, file=file_output)
