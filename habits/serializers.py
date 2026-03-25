from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):

        reward = data.get("reward")
        related = data.get("related_habit")
        pleasant = data.get("is_pleasant")
        execution_time = data.get("execution_time")
        frequency = data.get("frequency")

        # нельзя reward + related
        if reward and related:
            raise serializers.ValidationError(
                "Нельзя указывать reward и related_habit вместе"
            )

        # execution_time <= 120
        if execution_time > 120:
            raise serializers.ValidationError(
                "Время выполнения > 120 секунд"
            )

        # related только pleasant
        if related and not related.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть pleasant"
            )

        # pleasant нельзя reward и related
        if pleasant and (reward or related):
            raise serializers.ValidationError(
                "У pleasant не может быть reward или related"
            )

        # frequency <= 7
        if frequency > 7:
            raise serializers.ValidationError(
                "Нельзя реже чем раз в 7 дней"
            )

        return data
