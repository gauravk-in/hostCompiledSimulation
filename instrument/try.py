import sys

if __name__ == "__main__":
    fileName = "./abc.txt"
    file = open(fileName, "w")
    str = "Hello\nWorld!"
    file.write(str)
    file.close()
    
    