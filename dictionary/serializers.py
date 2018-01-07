from .models import Dictionary
from rest_framework import serializers


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('entry', 'key', 'value')

    def create(self, validated_data):
        return Dictionary.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.entry = validated_data.get('entry', instance.entry)
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance


