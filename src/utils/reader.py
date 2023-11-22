import os
import re

class DataReader:

    def __init__(self, object):
        self.path = object

    def read_file(self):
        #first should be content and second should id extracted from file name, in the 2D list
        all_file = []
        pattern = re.compile(r'[0-9]+')

        for filename in os.listdir(self.path):
            file_content = ""
            file = os.path.join(self.path, filename)
            #extract id from file name
            
            file_id = pattern.findall(filename)[0]

            if os.path.isfile(file):
                f = open(file, "r")
                for line in f:
                    file_content += line
                f.close()
                # change to all_file.append([file_content, extracted_id])
                all_file.append([file_content, file_id])

        return all_file


                







