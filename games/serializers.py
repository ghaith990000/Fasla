from rest_framework import serializers
from .models import GameSession, Player, Team

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

class GameSessionSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = GameSession
        fields = "__all__"