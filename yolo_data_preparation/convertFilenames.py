import os

def convertFilenames(folder):
    for filename in os.listdir(folder):
        os.chdir(folder)
        new_name = str(filename)
        new_name = new_name.replace(" ", "_")
        os.rename(filename, new_name)

folder = "C:\\Users\\t-aysing\\Desktop\\test" #specify path
convertFilenames(folder)