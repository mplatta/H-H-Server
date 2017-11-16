class NewsLogger(object):
    def __init__(self):
        self.news = {}

    def register(self, app):
        rules = app.url_map._rules
        for rule in rules:
            if rule.rule.startswith("/api/"):
                self.news[rule.endpoint] = Article(rule.endpoint, rule.rule, rule.methods)

    def getArticles(self):
        return self.news


class Article:
    def __init__(self, name, path, methods):
        self.name = name
        self.path = path
        self.methods = methods
        self.commentary = []

    @property
    def content(self):
        return "Methods: {methods}".format(methods=", ".join(self.methods))

    def addComment(self, comment):
        self.commentary.append(comment)
