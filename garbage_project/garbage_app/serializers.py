from rest_framework import serializers
from .models import Post,Vote,Garbage_User,checkpoint,driver_checkpoint,checkpoint_dustbin

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    votes=VoteSerializer(many=True,required=False)

    class Meta:
        model=Post
        fields="__all__"


class Garbage_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Garbage_User
        fields="__all__"

class checkpoint_Serializer(serializers.ModelSerializer):

    class Meta:
        model=checkpoint
        fields="__all__"

class driver_checkpoint_Serializer(serializers.ModelSerializer):
    class Meta:
        model=driver_checkpoint
        fields="__all__"


class checkpoint_dustbin_Serializer(serializers.ModelSerializer):
     class Meta:
        model=checkpoint_dustbin
        fields="__all__"