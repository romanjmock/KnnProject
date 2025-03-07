from csv import DictReader, DictWriter

file = open("insurance.csv", "r")
dictionary = DictReader(file)
data = list(dictionary)

print(data[5]["charges"])

for item in data:
    if (item["sex"] == "female"):
        item["sex"] = 1
    if (item["sex"] == "male"):
        item["sex"] = 0
    
    if (item["children"] == "no"):
        item["children"] = 0
    if (item["children"] == "yes"):
        item["children"] = 1
    
    if (item["smoker"] == "no"):
        item["smoker"] = 0
    if (item["smoker"] == "yes"):
        item["smoker"] = 1

    if (item["region"] == "northeast"):
        item["region"] = 0
    if (item["region"] == "northwest"):
        item["region"] = 1
    if (item["region"] == "southeast"):
        item["region"] = 2
    if (item["region"] == "southwest"):
        item["region"] = 3

print(data)
prepared = open("prepared.csv", "a", newline = "")
keys = data[0]
fileWriter = DictWriter(prepared, fieldnames = keys)
fileWriter.writeheader()

rows = []
for row in data:
    fileWriter.writerow(row)