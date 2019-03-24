import json

class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.data = dict()

    def configure(self, min_threshold, max_threshold, matrix_blur_size):
        data = self.data
        data['first_time'] = False
        data['min_threshold'] = min_threshold
        data['max_threshold'] = max_threshold
        data['matrix_blur_size'] = matrix_blur_size

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

    def get_data(self):
        return self.data

if __name__ == "__main__":
    config = Config()
    config.configure(15, 255, (3,3))
    config.save()
    config.load()
    print(config.get_data())
