from ast import alias
from asyncore import write
from rest_framework import viewsets, permissions, status
from .models import Player, Game
from .serializers import CreateGameSerializer, JoinGameSerializer, GetGameDataSerializer
from rest_framework.response import Response
from .utils import GenerateInviteCode
from django.shortcuts import get_object_or_404


# Create your views here.

class CreateGameView(viewsets.ModelViewSet):
    # *************** do I really need this serializer here? I am not using it *****************
    serializer_class = CreateGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        inviteCode = GenerateInviteCode()
        myPlayerName = Player.objects.get(alias=user.username)
        Game.objects.create(
            playerX=myPlayerName,
            xState = Player.JOINED,
            oState = Player.NOT_READY,
            inviteCode = inviteCode,
            status = Game.WAITING
        )

        return Response({
                'message': 'game created',
                'invite_code': inviteCode
            }, status.HTTP_201_CREATED)

class JoinGameView(viewsets.ModelViewSet):
    serializer_class = JoinGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    #this is not working. it should update game model and make it ready to start the game. 
    # ********* the logic I have to use is witten on board! :) ********* #
    def update(self, request, *args, **kwargs):
        # ******** question?? why do write queryset. how it helps us???? *******
        # queryset = Game.objects.all()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        inviteCode = request.data.get('inviteCode')
        myPlayerName = Player.objects.get(alias=user.username)

        targetGame = get_object_or_404(Game, inviteCode=inviteCode)

        # ******** question?? there should be a way to handle this way find it *******
        # Game.objects.update(
        #     id = targetGame,
        #     playerO=myPlayerName,
        #     oState = 'joined',
        #     status = 'ready',
        # )
        targetGame.playerO = myPlayerName
        targetGame.oState = Player.JOINED
        targetGame.status = Game.READY

        targetGame.save()
        
        # ******** question?? how to send game data in response??? *******
        return Response({
            'message': 'game started!',
            # 'data': targetGame.playerX
        }, status.HTTP_200_OK)

class GameStateView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        inviteCode = kwargs.get("code", None)
        targetGame = get_object_or_404(Game, inviteCode=inviteCode)

        return Response({
            "status": targetGame.status
        }, status.HTTP_200_OK)

class GetGameDataView(viewsets.ModelViewSet):
    serializer_class = GetGameDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        inviteCode = kwargs.get("code", None)
        targetGame = get_object_or_404(Game, inviteCode=inviteCode)
        serializer = self.get_serializer(targetGame)
        return Response(serializer.data, status=status.HTTP_200_OK)


