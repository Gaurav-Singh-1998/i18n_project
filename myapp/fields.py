from django.core.exceptions import ValidationError
from django.db.models import JSONField
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# I18nJSONField is a custom JSONField that supports internationalization.
# It ensures that there's a value for the default language and automatically
# adds fields for any other languages specified in the project's settings.
class I18nJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Override the validate method to add custom validation rules
    def validate(self, value, model_instance):
        # Call the parent class's validate method
        super().validate(value, model_instance)

        # Check if the default language field is present in the JSON value
        default_lang_code = settings.LANGUAGE_CODE

        # If the default language field is not present, raise a ValidationError
        if default_lang_code not in value:
            raise ValidationError(
                _("The default language (%(language)s) field is required."),
                params={"language": default_lang_code},
            )

        # For each language specified in the project settings,
        # add an empty field in the JSON value if it doesn't already exist
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code not in value:
                value[lang_code] = ""

        # Remove any extra keys in the JSON value that are not part of the project's languages
        extra_keys = set(value.keys()) - set(lang[0] for lang in settings.LANGUAGES)
        for key in extra_keys:
            del value[key]

    # Override the formfield method to use the default form field for JSONField
    def formfield(self, **kwargs):
        return super().formfield(**kwargs)
