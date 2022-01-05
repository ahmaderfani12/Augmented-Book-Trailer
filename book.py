class book:
    def __init__(self, name, cover,video_address) :
        self.name = name
        self.cover=cover
        self.video_address=video_address
        self.features=0
        self.last_frame=400
        self.video=None
        self.kp=None
        self.des=None
        