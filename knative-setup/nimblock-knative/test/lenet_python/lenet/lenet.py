import numpy as np

def relu(input): 
    return max(0,input)


def convolution1(input, weights, bias):
    output = np.zeros((6, 28, 28))
    for co in range(6):
        for h in range(28):
            for w in range(28):
                sum = 0
                for i in range(5):
                    for j in range(5):
                        if (i == 0) and (j == 0):
                            sum = 0
                        sum += weights[co, 0, i, j] * input[0, i+h, j+w]
                        if (i == 4) and (j == 4):
                            output[co, h, w] = sum + bias[co]
    return output

def relu_3d(input):
    output = np.zeros_like(input)
    for i in range(input.shape[0]):
        for j in range(input.shape[1]):
            for k in range(input.shape[2]):
                output[i,j,k] = relu(input[i,j,k])
    return output


def max_pooling2(input):
    output = np.zeros((6, 14, 14))
    for c in range(6):
        for h in range(14):
            for w in range(14):
                max_value = -1000000000000.0
                for i in range(h*2, h*2+2):
                    for j in range(w*2, w*2+2):
                        max_value = max(max_value, input[c, i, j])
                output[c,h,w] = max_value
    return output

def convolution3(input, weights, bias):
    output = np.zeros((16, 10, 10))
    for co in range(16):
        for h in range(10):
            for w in range(10):
                sum = 0
                for i in range(5):
                    for j in range(5):
                        for ci in range(6):
                            if (ci == 0) and (i == 0) and (j == 0):
                                sum = 0
                            sum += weights[co, ci, i, j] * input[ci, i+h, j+w]
                            if (ci == 5) and (i == 4) and (j == 4):
                                output[co, h, w] = sum + bias[co]
    return output

def max_pooling4(input):
    output = np.zeros((16, 5, 5))
    for c in range(16):
        for h in range(5):
            for w in range(5):
                max_value = -np.inf
                for i in range(h*2, h*2+2):
                    for j in range(w*2, w*2+2):
                        max_value = max(max_value, input[c,i,j])
                output[c,h,w] = max_value
    return output



def convolution5(input, weights, bias):
    output = np.zeros((120, 1, 1))
    for co in range(120):
        sum = 0
        for i in range(5):
            for j in range(5):
                for ci in range(16):
                    if ci == 0 and i == 0 and j == 0:
                        sum = 0
                    sum += weights[co,ci,i,j] * input[ci,i,j]
                    if ci == 15 and i == 4 and j == 4:
                        output[co,0,0] = sum + bias[co]
    return output

def relu5(input):
    output = np.zeros_like(input)
    for i in range(120):
        output[i,0,0] = relu(input[i,0,0])
    return output

def fc6(input, weights, bias):
    output = np.zeros((10,), dtype=np.float32)
    for n in range(10):
        sum = 0
        for c in range(120):
            sum += weights[n,c,0,0] * input[c,0,0]
        output[n] = sum + bias[n]
    return output

def relu6(input):
    output = np.zeros_like(input)
    for i in range(10):
        output[i] = relu(input[i])
    return output

def run_lenet(batch_size):
    for i in range(batch_size):
        image = np.random.rand(1, 32, 32)
        conv1_weights = np.random.rand(6, 1, 5, 5)
        conv1_bias = np.random.rand(6,)


        conv3_weights = np.random.rand(16, 6, 5, 5)
        conv3_bias = np.random.rand(16,)


        conv5_weights = np.random.rand(120, 16, 5, 5)
        conv5_bias = np.random.rand(120,)

        fc6_weights = np.random.rand(10, 120, 1, 1)
        fc6_bias = np.random.rand(10,)

        conv1_output = convolution1(image, conv1_weights, conv1_bias)
        conv1_output = relu_3d(conv1_output)

        pool2_output = max_pooling2(conv1_output)
        pool2_output = relu_3d(pool2_output)

        conv3_output = convolution3(pool2_output, conv3_weights, conv3_bias)
        conv3_output = relu_3d(conv3_output)

        pool4_output = max_pooling4(conv3_output)
        pool4_output = relu_3d(pool4_output)

        conv5_output = convolution5(pool4_output, conv5_weights, conv5_bias)
        conv5_output = relu5(conv5_output)
        fc6_output = fc6(conv5_output, fc6_weights, fc6_bias)

    return "Complete"











