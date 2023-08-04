import argparse
import LoadData

def calLastBitPercentageImage(img_arr):
    height = img_arr.__len__()
    width = img_arr[0].__len__()
    channel = img_arr[0][0].__len__()
    count_zero = 0
    count_one = 0
    for x in range(0, height):
        for y in range(0, width):
            for c in range(0, channel):
                if img_arr[x][y][c] & 1 == 0:
                    count_zero += 1
                else:
                    count_one += 1
    return count_zero / (count_zero + count_one)

def calBitPercentageText(text_bin):
    count_zero = 0
    count_one = 0
    for bit in text_bin:
        if bit == 0:
            count_zero += 1
        else:
            count_one += 1
    return count_zero / (count_zero + count_one)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, default='P.jpg')  # img_path
    parser.add_argument('--logo', type=str, default='')  # short watermark
    parser.add_argument('--text', type=str, default='law.txt')  # text_path, long watermark
    parser.add_argument('--output', type=str, default='SP.png')  # output file
    args = parser.parse_args()

    #将图片转化为数组，将文字转化为数组
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

    #在text_bin中存储text_arr的二进制形式
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

    #将text_bin中的二进制信息嵌入图片中
    #每个位置的像素对应了三个通道，每个通道的最后一位用来嵌入信息
    print(calLastBitPercentageImage(img_arr))
    print(calBitPercentageText(text_bin))
          
    pnt = 0
    for x in range(0, height):
        for y in range(0, width):
            for c in range(0, channel):
                #此处先进行向右移位操作，再进行向左移位并且补位'0'操作，保证text_bin的二进制信息能被存储在最后一位中
                #TODO:但是这里会出现问题，也就是在移位的过程中，若数据量太大，末位的'0''1'比例会发生变化
                img_arr[x][y][c] = ((img_arr[x][y][c] >> 1) << 1) | text_bin[pnt % text_bin.__len__()]
                pnt += 1
                
    print(calLastBitPercentageImage(img_arr))
    
    LoadData.save_img(img_arr, str(args.output))


  