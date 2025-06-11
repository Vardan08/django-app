from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import Serializers
from .Serializers import UsersSerializer, FriendRequestSerializer
from .models import MyUser, FriendRequest
from .throttles import MillisecondThrottle


class TestThrottleView(APIView):
    throttle_classes = [MillisecondThrottle]

    def get(self, request):
        return Response({"message": "Allowed"})

class UserDetailsView(APIView):
    throttle_classes = [MillisecondThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UsersSerializer(user)
        data = serializer.data

        fields = request.query_params.get('field') or request.query_params.get('fields')

        if fields:
            field_list = [f.strip() for f in fields.split(',')]
            filtered_data = {key: data[key] for key in field_list if key in data}
            return Response(filtered_data)

        return Response(data)

class UserUpdateView(APIView):
    throttle_classes = [MillisecondThrottle]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UsersSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    throttle_classes = [MillisecondThrottle]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "User account deleted."}, status=status.HTTP_204_NO_CONTENT)

class UsersAPIList(generics.ListAPIView):
    throttle_classes = [MillisecondThrottle]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

class UsersAPICreate(generics.CreateAPIView):
    throttle_classes = [MillisecondThrottle]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

class UsersAPIUpdate(generics.UpdateAPIView):
    throttle_classes = [MillisecondThrottle]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

class UsersAPIDelete(generics.DestroyAPIView):
    throttle_classes = [MillisecondThrottle]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
#
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser

class UsersAPIDetail(generics.RetrieveAPIView):
    throttle_classes = [MillisecondThrottle]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Get query parameter `fields` or `field`
        fields = request.query_params.get('field') or request.query_params.get('fields')

        if fields:
            requested_fields = [f.strip() for f in fields.split(',')]
            filtered_data = {k: data[k] for k in requested_fields if k in data}
            return Response(filtered_data)

        # Return all fields if no specific field is requested
        return Response(data)

class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [MillisecondThrottle]

    def perform_create(self, serializer):
        receiver = self.request.data.get('receiver')
        if not receiver:
            raise Serializers.ValidationError({"receiver": "This field is required."})
        serializer.save(sender=self.request.user)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [MillisecondThrottle]

    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        friend_request.is_accepted = True
        friend_request.save()
        return Response({"success": "Friend request accepted."})

class ReceivedFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [MillisecondThrottle]

    def get_queryset(self):
        # Show all friend requests received by the logged-in user
        return FriendRequest.objects.filter(receiver=self.request.user)



class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [MillisecondThrottle]

    def get(self, request):
        user = request.user

        # Get users the current user sent requests to AND were accepted
        sent = FriendRequest.objects.filter(sender=user, is_accepted=True).values_list('receiver', flat=True)
        # Get users who sent requests to current user AND were accepted
        received = FriendRequest.objects.filter(receiver=user, is_accepted=True).values_list('sender', flat=True)

        # Combine all friend IDs
        friend_ids = list(sent) + list(received)

        # Get user instances for all friends
        friends = MyUser.objects.filter(id__in=friend_ids)
        serializer = UsersSerializer(friends, many=True)
        return Response(serializer.data)