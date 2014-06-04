
class FileNotepad:

    def __init__(self, filepath=None):
        self.filepath = filepath

    def setFilepath(self, filepath):
        self.filepath = filepath

    def readFile(self):
        if self.filepath != None:
            with open(self.filepath, 'rb') as myfile:
                fileContent = myfile.read()
            return fileContent

    def writeExistingFile(self, fileContent):
        if self.filepath != None:
            with open(self.filepath, 'wb') as myfile:
                myfile.write(fileContent)

    def writeNewFile(self, fileContent):
        if self.filepath != None:
            with open(self.filepath, 'w+') as myfile:
                myfile.write(fileContent)