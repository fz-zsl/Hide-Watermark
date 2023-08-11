import argparse
import string

import cv2
import HammingCode
import LoadData
import math
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
self_info_len = 11


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


def check_utf8(index):
    ch = chr(index)
    return ch == ch.encode('utf-8', 'replace').decode('utf-8')


def vote(num_arr):
    cnt = np.zeros((16, 2), dtype=int)
    for num in num_arr:
        for bit in range(16):
            cnt[bit][int(num) >> bit & 1] += 1
    num = 0
    prob = 1.0
    unsure = 0
    for bit in range(16):
        if (cnt[bit][1] > cnt[bit][0]):
            num |= 1 << bit
            prob *= cnt[bit][1] / (cnt[bit][0] + cnt[bit][1])
        elif (cnt[bit][1] < cnt[bit][0]):
            prob *= cnt[bit][0] / (cnt[bit][0] + cnt[bit][1])
        else:
            unsure |= 1 << bit
            prob *= 0.5
    if check_utf8(num):
        return num, prob
    comp = unsure
    while comp > 0:
        if check_utf8(num | comp):
            return (num | comp), prob
        comp = (comp - 1) & unsure
    return 63, prob


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, default='SP-Task2-0812.png')  # image with watermark
    args = parser.parse_args()

    is_jpg = str(args.img).endswith('.jpg') or str(args.img).endswith('.jpeg')
    if is_jpg:
        info_begin = 6
        info_end = 21
        eps = 5
    else:
        info_begin = 21  # 13
        info_end = 36  # 28
        eps = 3
    info_len = info_end - info_begin

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

    best_prob = -10 ** 6
    good_prob = -10 ** 6
    watermark = []
    for test_len in range(1, int(text_arr.__len__() * 0.5)):
        test_arr = []
        test_prob = 0
        flag = False
        for x in range(test_len):
            buc = []
            for y in range(x, text_arr.__len__(), test_len):
                buc.append(text_arr[y])
            test_uni, uni_prob = vote(buc)
            if uni_prob < (0.0007 if is_jpg else 0.1):
                flag = True
                break
            test_prob += math.log(uni_prob)
            test_arr.append(chr(test_uni))
        if flag:
            continue
        test_prob /= test_len
        if test_prob > best_prob:
            good_prob = best_prob
            best_prob = test_prob
            watermark = test_arr
        elif test_prob > good_prob:
            good_prob = test_prob
        if test_len > 5 and best_prob - good_prob > 2:
            break
    if watermark.__len__() == 0:
        for uni in text_arr:
            watermark.append(chr(uni))

    if watermark.__len__() <= 100:
        print("Watermark: ", end='')
        for ch in watermark:
            print(ch, end='')
    else:
        print('[Note] Watermark is long, please view in \'./output/watermark.txt\'.')
        watermark_str = ''.join(str(ch) for ch in watermark)
        with open('output/watermark.txt', 'w') as file_output:
            print(watermark_str, file=file_output)
