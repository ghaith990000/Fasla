from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from .models import GameSession, Player, Team, GameTurn
from .serializers import GameSessionSerializer

from questions.models import Question, Answer

import random
# Create your views here.
class GameSessionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    # CREATE SESSION
    def create(self, request):
        mode = request.data.get("mode")
        config = request.data.get("config", {})

        if mode not in ["individual", "team"]:
            return Response({"error": "Invalid mode"}, status=400)

        session = GameSession.objects.create(
            host = request.user,
            mode = mode,
            config = config,
        )
        return Response(GameSessionSerializer(session).data)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.status != "waiting":
            return Response({"error": "Game already started"}, status=400)

        if Player.objects.filter(session=session, user=request.user).exists():
            return Response({"error": "Already joined"}, status=400)

        player = Player.objects.create(
            session=session,
            user=request.user
        )

        return Response({
            "player_id": player.id
        })

    # Create a team in team mode
    @action(detail=True, methods=["post"])
    def create_team(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.mode != "team":
            return Response({"error": "Not team mode"}, status=400)

        max_teams = session.config.get("max_teams")

        if max_teams and session.teams.count() >= max_teams:
            return Response({"error": "Max teams reached"}, status=400)
        
        name = request.data.get("name")

        team = Team.objects.create(
            session=session,
            name=name
        )
        
        return Response({
            "team_id": team.id,
            "name": team.name
        })
    
    # Join a team
    @action(detail=True, methods=["post"])
    def join_team(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.mode != "team":
            return Response({"error": "Not team mode"}, status=400)

        team_id = request.data.get("team_id")

        player = get_object_or_404(Player, session=session, user=request.user)
        team = get_object_or_404(Team, id=team_id, session=session)

        player.team = team
        player.save()

        return Response({"message": "Joined team"})
    
    # Start the game session only host can start
    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.host != request.user:
            return Response({"error": "Only host can start"}, status=403)

        if session.mode == "team":
            if Player.objects.filter(session=session, team__isnull=True).exists():
                return Response({"error": "All players must join teams"}, status=400)

        session.status = "in_progress"
        session.started_at = timezone.now()
        session.save()

        GameTurn.objects.create(session=session)

        return Response({"message": "Game started"})
    
    # Get current question for the turn
    @action(detail=True, methods=["get"])
    def question(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.status != "in_progress":
            return Response({"error": "Game not started"}, status=400)

        turn = session.turns.last()

        category_id = session.config.get("category")

        questions = list(Question.objects.filter(category_id=category_id))

        if not questions:
            return Response({"error": "No questions found"}, status=400)

        question = random.choice(questions)

        return Response({
            "turn_id": turn.id,
            "question_id": question.id,
            "text": question.text,
            "answers": [
                {"id": a.id, "text": a.text}
                for a in question.answers.all()
            ]
        })
    
    # Submit answer for the turn
    @action(detail=True, methods=["post"])
    def answer(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        player = get_object_or_404(Player, session=session, user=request.user)

        answer_id = request.data.get("answer_id")
        answer = get_object_or_404(Answer, id=answer_id)

        is_correct = answer.is_correct

        # INDIVIDUAL MODE
        if session.mode == "individual":
            if is_correct:
                player.score += 10
                player.save()

        # TEAM MODE
        elif session.mode == "team":
            if not player.team:
                return Response({"error": "Player not in a team"}, status=400)
            
            if is_correct:
                player.team.score += 10
                player.team.save()

        return Response({
            "correct": is_correct,
            "player_score": player.score,
            "team_score": player.team.score if player.team else None
        })
    
    # Get leaderboard results for the session
    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)

        if session.mode == "individual":
            players = session.players.order_by("-score")

            return Response({
                "leaderboard": [
                    {
                        "username": p.user.username,
                        "score": p.score
                    }
                    for p in players
                ]
            })

        else:
            teams = session.teams.order_by("-score")

            return Response({
                "leaderboard": [
                    {
                        "team": t.name,
                        "score": t.score
                    }
                    for t in teams
                ]
            })
        
    # session state
    @action(detail=True, methods=["get"])
    def state(self, request, pk=None):
        session = get_object_or_404(GameSession, pk=pk)
        return Response(GameSessionSerializer(session).data)