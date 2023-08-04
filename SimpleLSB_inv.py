import argparse

import LoadData

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='SP.png')  # output file
    args = parser.parse_args()

    img_arr = LoadData.load_image_inv(str(args.output))
    height = img_arr.__len__()
    width = img_arr[0].__len__()
    channel = img_arr[0][0].__len__()

    pnt = 0
    num = 0
    text_arr = []
    for x in range(0, height):
        for y in range(0, width):
            for c in range(0, channel):
                num <<= 1
                num |= (img_arr[x][y][c] & 1)
                pnt += 1
                if (pnt & 15) == 0:
                    # print(num, end=" ")
                    text_arr.append(num)
                    num = 0

    print("Watermark:")
    # print(text_arr[0])
    for i in range (1, text_arr[0] + 1):
        print(chr(text_arr[i]), end="")
