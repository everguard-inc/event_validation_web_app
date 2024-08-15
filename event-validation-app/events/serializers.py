from rest_framework import serializers

from events.models import Event, Tag, Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('slug', 'name', 'validation_guide_link')


class TagSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Tag
        fields = ('name', 'project')


class EventSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    major_tag = TagSerializer()
    minor_tag1 = TagSerializer()
    minor_tag2 = TagSerializer()

    class Meta:
        model = Event
        fields = '__all__'
