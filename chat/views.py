from rest_framework.views import APIView
from rest_framework.response import Response 
from useraccount.models import User
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from .models import Conversation, Message

class ConversationsListView(APIView):
    def get(self, request):
        serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
        return Response(serializer.data)


class ConversationsDetailsView(APIView):
    def get(self, request, pk):
        conversation = request.user.conversations.get(pk=pk)
        serializer = ConversationDetailSerializer(conversation, many=False)
        message_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
        return Response({
            'conversation': serializer.data,
            'messages': message_serializer.data
        })

class CreateConversationView(APIView):
    def get(self, request, user_id):
        conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

        if conversation.count() > 0:
            conversation = conversations.first()
            return Response({'sucess': True, conversation_id: conversation.id})
        else:
            user = User.objects.get(pk=user_id)
            conversation = Conversation.objects.create()
            conversation.users.add(request.user)
            conversation.users.add(user)
            return Response({'sucess': True, conversation_id: conversation.id})

        