from rest_framework import serializers
from .models import Post,Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    votes=VoteSerializer(many=True,required=False)

    class Meta:
        model=Post
        fields="__all__"