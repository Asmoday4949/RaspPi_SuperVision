import json
import os

class Config:
    def __init__(self, filename="config.json", data=dict()):
        self.filename = filename
        self.set_data(data)

    def set_data(self, data):
        self.data = data

    def save(self):
        data_json = json.dumps(self.data)
        file = open(self.filename, 'w')
        file.write(data_json)
        file.close()

    def load(self):
        file = open(self.filename, 'r')
        data_json = file.read()
        file.close()
        self.data = json.loads(data_json)

    def exist(self):
        return os.path.isfile(self.filename)

    def get_data(self):
        return self.data

if __name__ == "__main__":
    config = Config()
    config.save()
    config.load()
    print(config.get_data())
