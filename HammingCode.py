from queue import Queue
import numpy as np


hamming_code_dist = []
hamming_code_gen = []
hamming_code_near = np.zeros(32768)  # 1 << 15


def gen(index):
    code = []
    for bit in range(11):
        code.append(index & 1)
        index >>= 1
    code0 = code[0] ^ code[1] ^ code[3] ^ code[4] ^ code[6] ^ code[8] ^ code[10] ^ 1
    code1 = code[0] ^ code[2] ^ code[3] ^ code[5] ^ code[6] ^ code[9] ^ code[10] ^ 1
    code2 = code[1] ^ code[2] ^ code[3] ^ code[7] ^ code[8] ^ code[9] ^ code[10] ^ 1
    code3 = code[4] ^ code[5] ^ code[6] ^ code[7] ^ code[8] ^ code[9] ^ code[10] ^ 1
    num3 = (code[10] << 3) | (code[9] << 2) | (code[8] << 1) | code[7]
    num2 = (code[6] << 3) | (code[5] << 2) | (code[4] << 1) | code3
    num1 = (code[3] << 3) | (code[2] << 2) | (code[1] << 1) | code2
    num0 = (code[0] << 2) | (code1 << 1) | code0
    num = (num3 << 11) | (num2 << 7) | (num1 << 3) | num0
    hamming_code_gen.append(num)
    return num


def gen11(code15):
    code = []
    code15 = int(code15)
    for bit in range(15):
        code.append(code15 & 1)
        code15 >>= 1
    return [code[14], code[13], code[12], code[11], code[10], code[9],
            code[8], code[6], code[5], code[4], code[2]]


def __init__():
    que = Queue()
    for index in range(32768):
        hamming_code_dist.append(20)
    for index in range(2048):
        gen_ = gen(index)
        hamming_code_dist[gen_] = 0
        hamming_code_near[gen_] = gen_
        que.put(gen_)
    while not que.empty():
        index = que.get()
        for bit in range(15):
            index2 = index ^ (1 << bit)
            if hamming_code_dist[index2] > hamming_code_dist[index] + 1:
                hamming_code_dist[index2] = hamming_code_dist[index] + 1
                hamming_code_near[index2] = hamming_code_near[index]
                que.put(index2)