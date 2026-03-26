from rest_framework.serializers import ValidationError


def validate_habit(data):

    if data.get("reward") and data.get("related_habit"):
        raise ValidationError("Нельзя указывать и reward и related_habit")

    if data.get("execution_time") > 120:
        raise ValidationError("Время выполнения > 120 секунд")

    if data.get("period_days") > 7:
        raise ValidationError("Нельзя выполнять реже чем 1 раз в 7 дней")

    related = data.get("related_habit")
    if related and not related.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной")

    if data.get("is_pleasant"):
        if data.get("reward") or data.get("related_habit"):
            raise ValidationError("У приятной привычки не может быть награды")
