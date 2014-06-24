import os

class FileNotepad:

    def __init__(self, filepath=None):
        self.filepath = filepath

    def setFilepath(self, filepath):
        self.filepath = filepath

    def readRawFile(self):
        if self.filepath != None:
            fileContent = []
            with open(self.filepath, 'rb') as myfile:
                for line in myfile:
                    fileContent.append(line)
            return fileContent

    def processRawFile(self, contentlist):
        newlist=[]
        for line in contentlist:
            newlist.append("<div>"+line+"</div>")
        filecontent = "".join(newlist)
        return filecontent

		

    def readFile(self):
        if self.filepath != None:
            fileContent = []
            with open(self.filepath, 'rb') as myfile:
                fileContent = myfile.read()
            return fileContent

    def writeExistingFile(self, fileContent):
        if self.filepath != None:
            with open(self.filepath, 'wb') as myfile:
                myfile.write(fileContent)

    def writeNewFile(self, fileContent):
        if self.filepath != None:
            dir = os.path.dirname(self.filepath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(self.filepath, 'w+') as myfile:
                myfile.write(fileContent)