class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = title

        if not isinstance(author, Author):
            raise TypeError("Author must be an instance of Author.")
        self.author = author

        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be an instance of Magazine.")
        self.magazine = magazine

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    def __str__(self):
        return "<Immutable title: {}>".format(self._title)

    def __setattr__(self, key, value):
        if key == "_title" and not isinstance(value, str):
            raise TypeError("Title must be a string.")
        super().__setattr__(key, value)

    @title.setter
    def title(self, new_title):
        self._title = new_title


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    @property
    def name(self):
        return self._name

    def articles(self, magazine=None):
        if magazine:
            return [article for article in Article.all if article.author == self and article.magazine == magazine]
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        topics = list(set(magazine.category for magazine in self.magazines()))
        return topics if topics else None


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = name

        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self.category = category

        Magazine.all.append(self)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = new_name

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str) or len(new_category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = new_category

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        return [article.title for article in self.articles()] if self.articles() else None

    def contributing_authors(self):
        contributing_authors = []
        for author in self.contributors():
            if len([article for article in author.articles(self) if article.magazine == self]) > 2:
                contributing_authors.append(author)

        return contributing_authors if contributing_authors else None

    @classmethod
    def top_publisher(cls):
        if not cls.all:
            return None

        article_counts = {magazine: len(magazine.articles()) for magazine in cls.all}
        top_magazine = max(article_counts, key=article_counts.get)

        return top_magazine if article_counts[top_magazine] > 0 else None
