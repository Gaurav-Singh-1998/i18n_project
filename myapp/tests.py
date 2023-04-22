from django.test import TestCase
from django.core.exceptions import ValidationError
from myapp.models import Article
from myapp.fields import I18nJSONField
from datetime import datetime

class I18nJSONFieldTest(TestCase):
    def test_default_language_required(self):
        # Test that a ValidationError is raised when the default language is not provided
        field = I18nJSONField()
        with self.assertRaises(ValidationError):
            field.validate({}, None)

    def test_extra_languages_added(self):
        # Test that extra languages are added to the JSON value
        field = I18nJSONField()
        value = {"en": "Title in English"}
        field.validate(value, None)
        self.assertIn("fr", value)

    def test_extra_keys_removed(self):
        # Test that extra keys not in the LANGUAGES setting are removed
        field = I18nJSONField()
        value = {
            "en": "Title in English",
            "es": "Título en español",
            "fr": "Titre en français",
            "de": "Titel auf Deutsch",
            "it": "Titolo in italiano",
        }
        field.validate(value, None)
        self.assertNotIn("it", value)

    def test_article_creation(self):
        # Test creating an Article instance with I18nJSONField
        title_data = {
            "en": "Title in English",
            "fr": "Titre en français",
        }
        article = Article(title=title_data, author="Gaurav Singh", content="This is the article content", publication_date=datetime.now())
        article.save()
        self.assertEqual(article.title, title_data)
