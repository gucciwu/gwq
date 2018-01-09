from .models import Dictionary, SecurityType, Security
from base.serializers import BaseHyperlinkedModelSerializer


class DictionarySerializer(BaseHyperlinkedModelSerializer):
    class Meta(BaseHyperlinkedModelSerializer.Meta):
        model = Dictionary

    def create(self, validated_data):
        return Dictionary.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.entry = validated_data.get('entry', instance.entry)
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance


class SecuritySerializer(BaseHyperlinkedModelSerializer):
    class Meta(BaseHyperlinkedModelSerializer.Meta):
        model = Security

    def create(self, validated_data):
        return Security.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.short = validated_data.get('short', instance.short)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class SecurityTypeSerializer(BaseHyperlinkedModelSerializer):
    class Meta(BaseHyperlinkedModelSerializer.Meta):
        model = SecurityType

    def create(self, validated_data):
        return SecurityType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


