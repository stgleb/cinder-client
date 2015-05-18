class FakeVolume(object):
    def __init__(self, id="1234", name="test"):
        self.id = id
        self.display_name = name

    def delete(self):
        pass

    def attach(self):
        pass

    def detach(self):
        return 202


class FakeServer(object):
    def __init__(self, id="1234", name="test"):
        self.id = id
        self.name = name