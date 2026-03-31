from rest_framework import serializers
from .models import GameBoard, BoardCell, PlayerResponse

class BoardCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCell
        fields = "__all__"


class GameBoardSerializer(serializers.ModelSerializer):
    cells = BoardCellSerializer(many=True, read_only=True)

    class Meta:
        model = GameBoard
        fields = "__all__"


class PlayerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerResponse
        fields = "__all__"