from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    message = serializers.CharField(allow_blank=False)
    class Meta:
        fields = ['message']
