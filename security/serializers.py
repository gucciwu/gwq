from .models import Type, Security
from base.serializers import BaseHyperlinkedModelSerializer


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
        model = Type

    def create(self, validated_data):
        return Type.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance