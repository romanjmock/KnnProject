from sklearn.neighbors import KNeighborsClassifier
from csv import DictReader
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from csv import DictReader, DictWriter
import random

dictionary = list(DictReader(open("prepared.csv", "r")))

data = []
highest = (float)(dictionary[0]["charges"])
lowest = (float)(dictionary[0]["charges"])
for item in dictionary:
    current = (float)(item["charges"])
    if (current > highest):
        highest = current
    if (current < lowest):
        lowest = current

#buckets = (int)(input("number of buckets "))
buckets = 10

groupCounts = [0 for x in range(buckets)]
target = [[0] for x in range (len(dictionary))]
i = 0
step = 0
for item in dictionary:
    current = []
    for key in dictionary[0].keys():
        if (key != "charges"):
            current.append((float)(item[key]))
    data.append(current)
    step = (highest - lowest) / (buckets - 1)
    price = (float)(item["charges"])
    index = (int)((price - lowest) / step)
    #print(f"{i}, {index}")
    target[i]  = index
    groupCounts[index] += 1
    i += 1

distribution = open("distribution.txt", "a")
for x in range(len(groupCounts)):
    distribution.write(f"{x + 1}, {groupCounts[x]}\n")

print()

grouping = lowest
while (grouping <= highest):
    grouping += step
    print(grouping)
print(f"{target[34]}, {dictionary[34]["charges"]}")

# groupCounts = [0 for x in range(8)]
# target = [[0] for x in range (len(dictionary))]
# i = 0
# for item in dictionary:
#     current = []
#     for key in dictionary[0].keys():
#         if (key != "charges"):
#             current.append((float)(item[key]))
#     data.append(current)
#     if ((float)(item["charges"]) < 2000):
#         target[i] = 0
#         groupCounts[0] += 1
#     elif ((float)(item["charges"]) < 3000):
#         groupCounts[1] += 1
#         target[i] = 1
#     elif ((float)(item["charges"]) < 5000):
#         groupCounts[2] += 1
#         target[i] = 2
#     elif ((float)(item["charges"]) < 7000):
#         groupCounts[3] += 1
#         target[i] = 3
#     elif ((float)(item["charges"]) < 9000):
#         groupCounts[4] += 1
#         target[i] = 4
#     elif ((float)(item["charges"]) < 15000):
#         groupCounts[5] += 1
#         target[i] = 5
#     elif ((float)(item["charges"]) < 30000):
#         groupCounts[6] += 1
#         target[i] = 6
#     elif ((float)(item["charges"]) < 70000):
#         groupCounts[7] += 1
#         target[i] = 7
#     i += 1

#print(groupCounts)
#stop = input("continue? ")

#methods = ['mahalanobis', 'correlation', 'infinity', 'hamming', 'dice', 'jaccard', 'nan_euclidean', 'russellrao', 'l1', 'euclidean', 'sokalmichener', 'manhattan', 'chebyshev', 'canberra', 'yule', 'minkowski', 'p', 'sqeuclidean', 'cityblock', 'pyfunc', 'l2', 'rogerstanimoto', 'braycurtis', 'haversine', 'cosine', 'sokalsneath', 'seuclidean', 'precomputed']
methods = ['correlation', 'infinity', 'hamming', 'dice', 'jaccard', 'nan_euclidean', 'russellrao', 'l1', 'euclidean', 'sokalmichener', 'manhattan', 'chebyshev', 'canberra', 'yule', 'minkowski', 'p', 'sqeuclidean', 'cityblock', 'l2', 'rogerstanimoto', 'braycurtis', 'cosine', 'sokalsneath']

#print(target)

print("starting classification")

testData = data[0:(int)(len(data) / 2)]
testTarget = target[0:(int)(len(target) / 2)]

totalAccuracy = []
bestk = {}
bestAccuracy = {}
totalListAccuracy = []
#3 neighbors gives best accuracy default
#cosine says 1 neightbors
maxN = 20
#testAll = input("testAll? ")
testAll = "n"
if(testAll[0].lower() == 'y'):
    for m in range (len(methods)):
        accuracies = {}
        accuraciesList = [0 for x in range(maxN + 1)]
        highestAccuracy = 0
        accuratei = 0
        for i in range (1, maxN):
            error = False
            print(f"{methods[m]} {m}, {i}")
            
            classifier = KNeighborsClassifier(n_neighbors = i, metric = methods[m])
            try:
                classifier.fit(testData, testTarget)
            except (ValueError) as e:
                print(e)
                #pause = input()
                error = True

            if (error):
                print("error")
                results = [-1 for x in range (len(testData))]
            else:
                results = classifier.predict(data)

            errorCount = 0
            total = 0
            for x in range((int)(len(results) / 2), len(results)):
                #print(f"{results[x]}, {target[x]}")
                if (results[x] != target[x]):
                    errorCount += 1
                    #print(f"{results[x]}, {target[x]}")
                total += 1

            #print(errorCount)
            #print(f"total {len(results)}")
            error = errorCount * 100 / total
            accuracy = 100 - error
            #print(accuracy)
            accuracies[i] = accuracy
            accuraciesList[i] = accuracy

            if (accuracy > highestAccuracy):
                highestAccuracy = accuracy
                accuratei = i

            # if (i == 1):
            #     for result in results:
            #         print(result)
            #     sleep(5)
            #print(f"accuracy {accuracies}")
        totalAccuracy.append(accuracies)
        totalListAccuracy.append(accuraciesList)
        bestk[methods[m]] = accuratei
        bestAccuracy[methods[m]] = highestAccuracy

    print(bestk)
    print(bestAccuracy)

    keys = (list)(bestAccuracy.keys())
    best = 0
    for x in range(len(keys)):
        if bestAccuracy[keys[x]] > bestAccuracy[keys[best]]:
            best = x

    print(f"best accuracy is using the method {keys[best]}, with an accuracy of {bestAccuracy[keys[best]]}")

    visualAccuracies = []
    for method in methods:
        visualAccuracies.append(bestAccuracy[method])

    plt.bar(methods, visualAccuracies)
    plt.title("best distance type")
    plt.xlabel("method")
    plt.ylabel("accuracy")
    plt.xticks(range(len(methods)), methods, rotation = "vertical")
    plt.show()

    xAxis = []
    for x in range(0, maxN):
        xAxis.append(x)
    xAxis = np.array(xAxis)
    minimum = max(totalListAccuracy[0])
    maximum = min(totalListAccuracy[0])
    for x in range(len(totalListAccuracy)):
        totalListAccuracy[x].pop()
        print(totalListAccuracy[x])
        print(xAxis)
        plt.plot(xAxis, totalListAccuracy[x])
        for value in totalListAccuracy[x]:
            print(f"value is {value}")
            if value != 0 and value < minimum:
                minimum = value
            if value != 0 and value > maximum:
                maximum = value
        print(f"max {max(totalListAccuracy[x])}")
    # plt.axis([0, maxN, minimum, maximum])
    # plt.show()

    # prepared = open("methods.csv", "a", newline = "")
    # fileWriter = DictWriter(prepared, fieldnames = )
    # fileWriter.writeheader()

    # rows = []
    # print(totalAccuracy)
    # for row in (list)(totalAccuracy):
    #     fileWriter.writerow(row)



classifier = KNeighborsClassifier(n_neighbors = 1, metric = "canberra")
classifier.fit(testData, testTarget)

errorCount = 0

errorTest = classifier.predict(data)
totalError = 0
for x in range (len(errorTest)):
    #print(x)
    if (errorTest[x] != target[x]):
        #print(f"error {errorTest[x]} {target[x]}")
        errorCount += 1
        totalError += abs(errorTest[x] - target[x])

if (errorCount != 0):
    averageError = totalError / errorCount
    print(f"average error {averageError}")


print(f"Error Count {errorCount}")
accuracy = (1 - (errorCount / len(errorTest))) * 100
print(f"accuracy {accuracy}, {len(errorTest)}")

bucketFile = open("buckets.txt", "a")
bucketFile.write(f"{buckets}, {accuracy}\n")

while False:
    number = input("enter the number ")
    predict = []
    predict.append(data[(int)(number)])
    print(classifier.predict((predict)))
    print(target[(int)(number)])

#prediction test
for i in range(10):
    randomData = [[0 for x in range(6)] for y in range(1000)]
    minItems = [0 for x in range(6)]
    maxItems = [(int)(data[0][x]) for x in range(6)]

    for item in data:
        for x in range(len(item)):
            if (item[x] < minItems[x]):
                minItems[x] = (int)(item[x])
            if (item[x] > maxItems[x]):
                maxItems[x] = (int)(item[x])

    for x in range(len(randomData)):
        for y in range(len(randomData[0])):
            randomData[x][y] = random.randint(minItems[y], maxItems[y])

    xAxis = [x for x in range(len(randomData))]
    swap = True
    choiceItem = 4
    while (swap):
        swap = False
        for x in range(len(randomData) - 1):
            if (randomData[x][choiceItem] > randomData[x + 1][choiceItem]):
                current = randomData[x][choiceItem]
                randomData[x][choiceItem] = randomData[x + 1][choiceItem]
                randomData[x + 1][choiceItem] = current
                swap = True
    # for x in range(len(randomData)):
    #     print(randomData[x][choiceItem])
    predict = classifier.predict(randomData)
    xAxis = np.array(xAxis)
    # plt.plot(xAxis, predict)
    # plt.show()

    xAxis = [(x + 1) for x in range(10)]
    yAxis = []
    for x in range(10):
        average = 0
        for y in range(100):
            average += predict[x * 100 + y]
        average /= 100
        yAxis.append(average)
    plt.plot(xAxis, yAxis)
    print(predict[500])
plt.show()
