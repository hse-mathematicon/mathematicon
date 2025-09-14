from app.container import AppContainer


if __name__ == '__main__':
    container = AppContainer()
    container.wire(packages=["app"])
