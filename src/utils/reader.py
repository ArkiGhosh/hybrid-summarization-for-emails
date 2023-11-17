import os

class DataReader:

    def __init__(self, object):
        self.path = object

    def read_file(self):
        all_file = []

        for filename in os.listdir(self.path):
            file_content = ""
            file = os.path.join(self.path, filename)
            
            if os.path.isfile(file):
                f = open(file, "r")
                for line in f:
                    file_content += line
                f.close()
                all_file.append(file_content)

        return all_file


                







