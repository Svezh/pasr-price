import os


if os.path.isdir(os.getcwd() + "\refs"):
    print("Путь есть")
else:
    os.mkdir("refs")

