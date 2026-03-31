from rest_framework import serializers
from .models import GameSession, Player, Team, GameTurn
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "score"]

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "user", "team", "score", "joined_at"]

class GameTurnSerializer(serializers.ModelSerializer):
    current_player = PlayerSerializer(read_only=True)

    class Meta:
        model = GameTurn
        fields = ["id", "current_player", "created_at"]

class GameSessionSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    turns = GameTurnSerializer(many=True, read_only=True)

    class Meta:
        model = GameSession
        fields = [
            "id",
            "host",
            "mode",
            "status",
            "config",
            "players",
            "teams",
            "turns",
            "created_at",
            "started_at",
            "ended_at",
        ]