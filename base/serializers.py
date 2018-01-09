from rest_framework import serializers


class BaseHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    modified_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    created_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        # exclude = ('owner', 'created_by', 'modified_by')
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at',
                            'modified_by', 'modified_at',
                            'own', 'deleted')
        extra_kwargs = {
            'owner': {'lookup_field': 'username'},
            'modified_by': {'lookup_field': 'username'},
            'created_by': {'lookup_field': 'username'}
        }

