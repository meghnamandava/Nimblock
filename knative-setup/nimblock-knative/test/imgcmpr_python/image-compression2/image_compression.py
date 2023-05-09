import numpy as np
import random

IMAGE_MAX_M = 1920
IMAGE_MAX_N = 1080
IMAGE_MAX = IMAGE_MAX_M*IMAGE_MAX_N


dctMat = [
    [0.353553, 0.353553, 0.353553, 0.353553, 0.353553, 0.353553, 0.353553, 0.353553],
    [0.490393, 0.41574, 0.277797, 0.097565, -0.0975196, -0.277759, -0.415714, -0.490384],
    [0.461942, 0.191358, -0.191315, -0.461924, -0.46196, -0.191401, 0.191272, 0.461907],
    [0.41574, -0.0975196, -0.490384, -0.277836, 0.27772, 0.490411, 0.0976559, -0.415662],
    [0.353562, -0.353529, -0.353594, 0.353496, 0.353627, -0.353463, -0.35366, 0.353431],
    [0.277797, -0.490384, 0.0974742, 0.415791, -0.415662, -0.0977013, 0.490429, -0.277605],
    [0.191358, -0.46196, 0.461907, -0.191229, -0.191486, 0.462013, -0.461853, 0.191101],
    [0.097565, -0.277836, 0.415791, -0.49042, 0.490357, -0.415611, 0.277566, -0.097247]
]

# Transposed
dctMatT = [
    [0.353553, 0.490393, 0.461942, 0.41574, 0.353562, 0.277797, 0.191358, 0.097565],
    [0.353553, 0.41574, 0.191358, -0.0975196, -0.353529, -0.490384, -0.46196, -0.277836],
    [0.353553, 0.277797, -0.191315, -0.490384, -0.353594, 0.0974742, 0.461907, 0.415791],
    [0.353553, 0.097565, -0.461924, -0.277836, 0.353496, 0.415791, -0.191229, -0.49042],
    [0.353553, -0.0975196, -0.46196, 0.27772, 0.353627, -0.415662, -0.191486, 0.490357],
    [0.353553, -0.277759, -0.191401, 0.490411, -0.353463, -0.0977013, 0.462013, -0.415611],
    [0.353553, -0.415714, 0.191272, 0.0976559, -0.35366, 0.490429,-0.461853, 0.277566 ],
    [0.353553, -0.490384, 0.461907, -0.415662, 0.353431, -0.277605, 0.191101, -0.097247 ]
    ]

def padImage(src, dst, srcm, srcn, dstm, dstn):
    for i in range(IMAGE_MAX_M):
        if i < dstm:
            for j in range(IMAGE_MAX_N):
                if j < dstn:
                    image = (i < srcm) and (j < srcn)
                    if image:
                        dst[(i*dstn) + j] = src[(i*srcn) + j]
                    else:
                        dst[(i*dstn) + j] = DZERO
    return dst


def extractBlockD(src, dst, srcm, srcn):
    buffer0 = [0] * 8
    buffer1 = [0] * 8
    buffer2 = [0] * 8
    buffer3 = [0] * 8
    buffer4 = [0] * 8
    buffer5 = [0] * 8
    buffer6 = [0] * 8
    buffer7 = [0] * 8
    count = 0
    loc = 0

    for i in range(0, IMAGE_MAX_M, 8):
        if i < srcm:
            for j in range(0, IMAGE_MAX_N, 8):
                if j < srcn:
                    for k in range(8):
                        loc = ((i+k)*srcn + j)
                        buffer0[k] = src[((i+0)*srcn + j) + k]
                        buffer1[k] = src[((i+1)*srcn + j) + k]
                        buffer2[k] = src[((i+2)*srcn + j) + k]
                        buffer3[k] = src[((i+3)*srcn + j) + k]
                        buffer4[k] = src[((i+4)*srcn + j) + k]
                        buffer5[k] = src[((i+5)*srcn + j) + k]
                        buffer6[k] = src[((i+6)*srcn + j) + k]
                        buffer7[k] = src[((i+7)*srcn + j) + k]

                    for k in range(8):
                        dst[count + 8*0 + k] = buffer0[k]
                        dst[count + 8*1 + k] = buffer1[k]
                        dst[count + 8*2 + k] = buffer2[k]
                        dst[count + 8*3 + k] = buffer3[k]
                        dst[count + 8*4 + k] = buffer4[k]
                        dst[count + 8*5 + k] = buffer5[k]
                        dst[count + 8*6 + k] = buffer6[k]
                        dst[count + 8*7 + k] = buffer7[k]

                    count += 64

    return dst


def bundle1(dummy_data, buf1, buf2, srcm, srcn, dstm, dstn):
    buf2 = padImage(buf1, buf2, srcm, srcn, dstm, dstn)
    buf1 = extractBlockD(buf2, buf1, dstm, dstn)
    return buf1

def matmul_fast(srcA, srcB, dst):
    DZERO = 0

    for i in range(8):
        sum0 = sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = sum7 = DZERO

        for j in range(8):
            sum0 = srcA[i][0] * srcB[0][j]
            sum1 = srcA[i][1] * srcB[1][j]
            sum2 = srcA[i][2] * srcB[2][j]
            sum3 = srcA[i][3] * srcB[3][j]
            sum4 = srcA[i][4] * srcB[4][j]
            sum5 = srcA[i][5] * srcB[5][j]
            sum6 = srcA[i][6] * srcB[6][j]
            sum7 = srcA[i][7] * srcB[7][j]

            tmp = sum0 + sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7

            dst[i][j] = tmp

    return dst

def dct(dummy_data, src, dst, srcm, srcn, dstm, dstn):

    for m in range(0, IMAGE_MAX_M*IMAGE_MAX_N, 64):
        if(m < (srcm*srcn)):
            srcBlk = [[src[m + (i*8) + j] for j in range(8)] for i in range(8)]
            tmpBlk = [[0 for j in range(8)] for i in range(8)]
            dstBlk = [[0 for j in range(8)] for i in range(8)]

            # perform matrix multiplication using matmul_fast
            for i in range(8):
                for j in range(8):
                    sum0 = srcBlk[i][0] * dctMat[0][j]
                    sum1 = srcBlk[i][1] * dctMat[1][j]
                    sum2 = srcBlk[i][2] * dctMat[2][j]
                    sum3 = srcBlk[i][3] * dctMat[3][j]
                    sum4 = srcBlk[i][4] * dctMat[4][j]
                    sum5 = srcBlk[i][5] * dctMat[5][j]
                    sum6 = srcBlk[i][6] * dctMat[6][j]
                    sum7 = srcBlk[i][7] * dctMat[7][j]

                    tmpBlk[i][j] = sum0 + sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7

            for i in range(8):
                for j in range(8):
                    sum0 = tmpBlk[i][0] * dctMatT[0][j]
                    sum1 = tmpBlk[i][1] * dctMatT[1][j]
                    sum2 = tmpBlk[i][2] * dctMatT[2][j]
                    sum3 = tmpBlk[i][3] * dctMatT[3][j]
                    sum4 = tmpBlk[i][4] * dctMatT[4][j]
                    sum5 = tmpBlk[i][5] * dctMatT[5][j]
                    sum6 = tmpBlk[i][6] * dctMatT[6][j]
                    sum7 = tmpBlk[i][7] * dctMatT[7][j]

                    dstBlk[i][j] = sum0 + sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7

            for i in range(8):
                for j in range(8):
                    dst[m + (i*8) +j] = dstBlk[i][j]

    return dst

def quantize(dummy_data, src, dst, srcm, srcn, dstm, dstn):
    
    srcBlk = [[0 for j in range(8)] for i in range(8)]
    dstBlk = [[0 for j in range(8)] for i in range(8)]
    
    stdQuantizationMatrixInv = [[ 0.063, 0.091, 0.100, 0.063, 0.042, 0.025, 0.020, 0.016 ],
                                [ 0.083, 0.082, 0.071, 0.053, 0.038, 0.017, 0.017, 0.018 ],
                                [ 0.071, 0.077, 0.063, 0.042, 0.025, 0.018, 0.014, 0.018 ],
                                [ 0.071, 0.059, 0.045, 0.034, 0.020, 0.011, 0.013, 0.016 ],
                                [ 0.056, 0.045, 0.027, 0.018, 0.015, 0.009, 0.010, 0.013 ],
                                [ 0.042, 0.029, 0.018, 0.016, 0.012, 0.010, 0.009, 0.011 ],
                                [ 0.020, 0.016, 0.013, 0.011, 0.010, 0.008, 0.008, 0.010 ],
                                [ 0.014, 0.011, 0.011, 0.010, 0.009, 0.010, 0.010, 0.010 ]]

    for m in range(0, IMAGE_MAX_M*IMAGE_MAX_N, 64):
        if m < (srcm*srcn):
            for i in range(8):
                for j in range(8):
                    srcBlk[i][j] = src[m + (i*8) + j]
            
            for i in range(8):
                tmpD0 = srcBlk[i][0] * stdQuantizationMatrixInv[i][0]
                tmpD1 = srcBlk[i][1] * stdQuantizationMatrixInv[i][1]
                tmpD2 = srcBlk[i][2] * stdQuantizationMatrixInv[i][2]
                tmpD3 = srcBlk[i][3] * stdQuantizationMatrixInv[i][3]
                tmpD4 = srcBlk[i][4] * stdQuantizationMatrixInv[i][4]
                tmpD5 = srcBlk[i][5] * stdQuantizationMatrixInv[i][5]
                tmpD6 = srcBlk[i][6] * stdQuantizationMatrixInv[i][6]
                tmpD7 = srcBlk[i][7] * stdQuantizationMatrixInv[i][7]

                tmpQ0 = int(tmpD0)
                tmpQ1 = int(tmpD1)
                tmpQ2 = int(tmpD2)
                tmpQ3 = int(tmpD3)
                tmpQ4 = int(tmpD4)
                tmpQ5 = int(tmpD5)
                tmpQ6 = int(tmpD6)
                tmpQ7 = int(tmpD7)

                dstBlk[i][0] = tmpQ0
                dstBlk[i][1] = tmpQ1
                dstBlk[i][2] = tmpQ2
                dstBlk[i][3] = tmpQ3
                dstBlk[i][4] = tmpQ4
                dstBlk[i][5] = tmpQ5
                dstBlk[i][6] = tmpQ6
                dstBlk[i][7] = tmpQ7

            for i in range(8):
                for j in range(8):
                    dst[m + (i*8) +j] = dstBlk[i][j]

    return dst


def dequantize(dummy_data, src, dst, srcm, srcn, dstm, dstn):
    stdQuantizationMatrix = np.array([[16.00, 11.00, 10.00, 16.00, 24.00, 40.00, 51.00, 61.00],
                                    [12.00, 12.00, 14.00, 19.00, 26.00, 58.00, 60.00, 55.00],
                                    [14.00, 13.00, 16.00, 24.00, 40.00, 57.00, 69.00, 56.00],
                                    [14.00, 17.00, 22.00, 29.00, 51.00, 87.00, 80.00, 62.00],
                                    [18.00, 22.00, 37.00, 56.00, 68.00, 109.00, 103.00, 77.00],
                                    [24.00, 35.00, 55.00, 64.00, 81.00, 104.00, 113.00, 92.00],
                                    [49.00, 64.00, 78.00, 87.00, 103.00, 121.00, 120.00, 101.00],
                                    [72.00, 92.00, 95.00, 98.00, 112.00, 100.00, 103.00, 99.00]])

    srcBlk = np.zeros((8, 8), dtype=np.int16)
    dstBlk = np.zeros((8, 8), dtype=np.float32)

    for m in range(0, srcm*srcn, 64):
        if m < srcm*srcn:
            for i in range(8):
                for j in range(8):
                    srcBlk[i, j] = src[m + (i*8) + j]

            for i in range(8):
                for j in range(8):
                    tmpD = srcBlk[i, j] * stdQuantizationMatrix[i, j]
                    tmpQ = int(tmpD)
                    dstBlk[i, j] = tmpQ

            for i in range(8):
                for j in range(8):
                    dst[m + (i*8) + j] = dstBlk[i, j]

    return dst


def idct(dummy_data, src, dst, srcm, srcn, dstm, dstn):

    srcBlk = [[0 for j in range(8)] for i in range(8)]
    tmpBlk = [[0 for j in range(8)] for i in range(8)]
    dstBlk = [[0 for j in range(8)] for i in range(8)]

    for m in range(0, srcm * srcn, 64):
        if m < (srcm * srcn):
            for i in range(8):
                for j in range(8):
                    srcBlk[i][j] = src[m + (i * 8) + j]

            matmul_fast(dctMatT, srcBlk, tmpBlk)
            matmul_fast(tmpBlk, dctMat, dstBlk)

            for i in range(8):
                for j in range(8):
                    dst[m + (i * 8) + j] = dstBlk[i][j]

    return dst

def reconstructBlockD(dummy_data, src, dst, srcm, srcn, dstm, dstn):
    buffer0 = [0] * 8
    buffer1 = [0] * 8
    buffer2 = [0] * 8
    buffer3 = [0] * 8
    buffer4 = [0] * 8
    buffer5 = [0] * 8
    buffer6 = [0] * 8
    buffer7 = [0] * 8
    count = 0
    loc = 0

    for i in range(0, IMAGE_MAX_M, 8):
        if i < srcm:
            for j in range(0, IMAGE_MAX_N, 8):
                if j < srcn:
                    for k in range(8):
                        buffer0[k] = src[(count) + (8*0) + k]
                        buffer1[k] = src[(count) + (8*1) + k]
                        buffer2[k] = src[(count) + (8*2) + k]
                        buffer3[k] = src[(count) + (8*3) + k]
                        buffer4[k] = src[(count) + (8*4) + k]
                        buffer5[k] = src[(count) + (8*5) + k]
                        buffer6[k] = src[(count) + (8*6) + k]
                        buffer7[k] = src[(count) + (8*7) + k]

                    count += 64

                    for k in range(8):
                        dst[((i+0)*srcn + j) + k] = buffer0[k]
                        dst[((i+1)*srcn + j) + k] = buffer1[k]
                        dst[((i+2)*srcn + j) + k] = buffer2[k]
                        dst[((i+3)*srcn + j) + k] = buffer3[k]
                        dst[((i+4)*srcn + j) + k] = buffer4[k]
                        dst[((i+5)*srcn + j) + k] = buffer5[k]
                        dst[((i+6)*srcn + j) + k] = buffer6[k]
                        dst[((i+7)*srcn + j) + k] = buffer7[k]

    return 0






srcn = 250 #IMAGE_MAX_N
srcm = 250 #IMAGE_MAX_M
dstn = 250 #IMAGE_MAX_N
dstm = 250 #IMAGE_MAX_M

#buf1 = [random.randint(0, 1000)]*IMAGE_MAX
#buf2 = [0]*IMAGE_MAX
#dummy_data = [0]*IMAGE_MAX

#buf1 = bundle1(dummy_data, buf1, buf2, srcm, srcn, dstm, dstn)
#dst1 = dct(dummy_data, buf1, buf2, srcm, srcn, dstm, dstn)
#dst2 = quantize(dummy_data, dst1, buf2, srcm, srcn, dstm, dstn)
#dst3 = dequantize(dummy_data, dst2, buf2, srcm, srcn, dstm, dstn)
#dst4 = idct(dummy_data, dst3, buf2, srcm, srcn, dstm, dstn)
#dst5 = reconstructBlockD(dummy_data, dst4, buf2, srcm, srcn, dstm, dstn)

def run_img_compression(batch_size):
    for i in range(batch_size):
        buf1 = [random.randint(0, 1000)]*IMAGE_MAX 
        buf2 = [0]*IMAGE_MAX
        dummy_data = [0]*IMAGE_MAX

        buf1 = bundle1(dummy_data, buf1, buf2, srcm, srcn, dstm, dstn)
        dst1 = dct(dummy_data, buf1, buf2, srcm, srcn, dstm, dstn)
        dst2 = quantize(dummy_data, dst1, buf2, srcm, srcn, dstm, dstn)
        dst3 = dequantize(dummy_data, dst2, buf2, srcm, srcn, dstm, dstn)
        dst4 = idct(dummy_data, dst3, buf2, srcm, srcn, dstm, dstn)
        dst5 = reconstructBlockD(dummy_data, dst4, buf2, srcm, srcn, dstm, dstn)
    return "Complete"



