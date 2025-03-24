import matplotlib.pyplot as plt
import numpy as np

graph = 1
if (graph == 0):
    xAxis = []
    yAxis = []
    for x in range(2, 11):
        xAxis.append(x)
        yAxis.append(0)
    print(xAxis)
    xAxis = np.array(xAxis)

    file = open("buckets.txt", "r")
    lines = file.readlines()
    for line in lines:
        index = (int)(line[0:line.index(",")])
        accuracy = (float)(line[line.index(" "):line.index("\n")])
        yAxis[index - 2] = accuracy
    plt.xlabel("Buckets")
    plt.ylabel("accuracy")
    yAxis = np.array(yAxis)
    plt.plot(xAxis, yAxis)
    plt.show()

if (graph == 1):
    data = []
    labels = []
    file = open("distribution.txt", "r")
    lines = file.readlines()
    for x in range(len(lines)):
        data.append(int(lines[x][lines[x].index(" ") + 1:lines[x].index("\n")]))
        labels.append(x + 1)
    plt.bar(labels, data)
    plt.xlabel("bucket")
    plt.ylabel("amount")
    plt.show()
    
    