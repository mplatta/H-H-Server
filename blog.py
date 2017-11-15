class NewsLogger(object):
    def __init__(self):
        self.news = {}

    def register(self, methods=["POST"]):

        def decorator(f):
            self.news[f.__name__] = (Article(f.__name__, methods))
            return f
        return decorator

    def getArticles(self):
        return self.news


class Article:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods
        self.commentary = []

    @property
    def content(self):
        return "Added new API endpoint as {name} with following methods: {methods}".format(
            name=self.name,
            methods=self.methods)

    def addComment(self, comment):
        self.commentary.append(comment)

    def addURL(self, url):
        self.url = url
