class MainHello:
    def __init__(self):
        pass

    def out(self):
        print("hello world")


class Service:
    """interconnecting class must be builded"""

    main = MainHello()
