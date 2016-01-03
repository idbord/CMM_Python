# -*- coding: utf-8 -*-
__author__ = 'idbord'


class BiIterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return result

    def hasNext(self):
        try:
            if self.index < len(self.collection):
                return True
            return False
        except IndexError:
            raise StopIteration

    def prev(self):
        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self
