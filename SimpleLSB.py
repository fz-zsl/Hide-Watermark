import argparse
import LoadData


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, default='P.jpg')  # img_path
    parser.add_argument('--logo', type=str, default='')  # short watermark
    parser.add_argument('--text', type=str, default='law.txt')  # text_path, long watermark
    parser.add_argument('--output', type=str, default='SP.png')  # output file
    args = parser.parse_args()

    img_arr = LoadData.load_image(str(args.img))
    if str(args.logo).__len__() == 0:
        # long watermark
        text_arr = LoadData.load_text(str(args.text))
        if text_arr.__len__() > 65535:
            print("[Warning] Text too long.")
    else:
        # short watermark
        text_arr = []
        for ch in str(args.logo):
            text_arr.append(ord(ch))
    # print(text_arr)

    text_bin = []
    for bit in range (15, -1, -1):
        text_bin.append((text_arr.__len__() >> bit) & 1)
    for ch in text_arr:
        for bit in range (15, -1, -1):
            text_bin.append((ch >> bit) & 1)
    # print(text_bin)

    # print(img_arr)
    height = img_arr.__len__()
    width = img_arr[0].__len__()
    channel = img_arr[0][0].__len__()
    # print(channel, height, width)

    pnt = 0
    for x in range(0, height):
        for y in range(0, width):
            for c in range(0, channel):
                img_arr[x][y][c] = ((img_arr[x][y][c] >> 1) << 1) | text_bin[pnt % text_bin.__len__()]
                pnt += 1

    LoadData.save_img(img_arr, str(args.output))
