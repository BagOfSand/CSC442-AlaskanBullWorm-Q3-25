def conv(fileName):
    f = open(fileName, "r")
    txt = f.read()
    txt = txt.replace("zero", "0").replace("one", "1")

    print(txt)

conv("itallbeginshere")