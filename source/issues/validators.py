from django.core.exceptions import ValidationError


def validate_summary_length(value):
    if len(value.strip()) < 10:
        raise ValidationError("Краткое описание должно содержать не менее 10 символов.")


def validate_forbidden_words(value):
    forbidden_words = ['слово', 'взлом', 'атака']
    lowered = value.lower()
    for word in forbidden_words:
        if word in lowered:
            raise ValidationError(f"Описание содержит запрещённое слово: '{word}'.")
