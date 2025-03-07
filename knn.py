from sklearn.neighbors import KNeighborsClassifier
from csv import DictReader

dictionary = list(DictReader(open("prepared.csv", "r")))

data = []
target = [[0] for x in range (len(dictionary))]
i = 0
for item in dictionary:
    current = []
    for key in dictionary[0].keys():
        if (key != "charges"):
            current.append((float)(item[key]))
    data.append(current)
    if ((float)(item["charges"]) < 10000):
        target[i] = 0
    elif ((float)(item["charges"]) < 20000):
        target[i] = 1
    elif ((float)(item["charges"]) < 30000):
        target[i] = 2
    elif ((float)(item["charges"]) < 40000):
        target[i] = 3
    elif ((float)(item["charges"]) < 50000):
        target[i] = 4
    elif ((float)(item["charges"]) < 60000):
        target[i] = 5
    elif ((float)(item["charges"]) < 70000):
        target[i] = 6
    i += 1

print(target)

print("starting classification")

# testData = data[0:(int)(len(data) / 2)]
# testTarget = target[0:(int)(len(target) / 2)]

testData = data
testTarget = target
accuracies = {}
#3 neighbors gives best accuracy default
#cosine says 1 neightbors
for i in range (1, 20):
    
    classifier = KNeighborsClassifier(n_neighbors = i, metric = "cosine")
    classifier.fit(testData, testTarget)

    results = classifier.predict(data)

    errorCount = 0
    total = 0
    for x in range(len(results)):
        #print(f"{results[x]}, {target[x]}")
        if (results[x] != target[x]):
            errorCount += 1
            #print(f"{results[x]}, {target[x]}")
        total += 1

    print(errorCount)
    print(f"total {len(results)}")
    error = errorCount * 100 / total
    accuracy = 100 - error
    print(accuracy)
    accuracies[i] = accuracy

print(accuracies)