

import model
import loader

import codecs
import sys
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class CUIApp:
    """
    CUI Application.
    use command module?

    """
    def __init__(self):
        self.bs = []
        self.filename = "test.csv"

    def load(self):
        with file(self.filename) as f:
            self.bs = loader.read_csv(f)

    def save(self):
        with file(self.filename, 'w') as f:
            loader.write_csv(self.bs, f)

    def listall(self):
        for b in self.bs:
            print "=" * 60
            print "ISBN:", b.isbn
            print "title:", b.title

    def add(self, isbn, title):
        try:
            b = model.Book(isbn, title)
        except libisbn.BadISBNException:
            pass


app = CUIApp()

app.load()
app.listall()


