from threading import Thread

class MyThread(Thread):
    def __init__(self,target,args):
        super().__init__()
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)

    def get_args(self):
        return str(self.args[3])

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None