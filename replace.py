f = open('sample3.txt', 'r', encoding='UTF-8')
data = f.read()
data = data.replace("...", "")
data = data.replace("◯", "X")
with open("sample4.txt", mode="a") as k:
    k.write(data)
f.close()