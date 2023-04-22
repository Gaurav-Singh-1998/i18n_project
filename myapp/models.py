from django.db import models
from .fields import I18nJSONField

class Article(models.Model):
    # The title field will be used for internationalization.
    title = I18nJSONField('Article title', default=dict)

    # A text field to hold the content of the article.
    content = models.TextField()

    # The name of the author of the article.
    author = models.CharField(max_length=255)

    # The date when the article was published.
    publication_date = models.DateField()

    class Meta:
        # The name of the database table to use for this model.
        db_table = "article"

        # A human-readable name for the model, used in the Django admin.
        verbose_name = "article"

    # A string representation of the Article object.
    def __str__(self):
        return str(self.title)
