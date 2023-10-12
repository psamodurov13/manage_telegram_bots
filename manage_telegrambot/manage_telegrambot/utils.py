class CustomStr:
    def __str__(self):
        if self.__class__.__name__ == 'Post':
            return f'{self.bot} / {self.name} (ID {self.id} / Custom ID {self.count})'
        elif hasattr(self, 'title'):
            return self.title
        elif hasattr(self, 'name'):
            return self.name
        else:
            return str(self.id)