from rest_framework import serializers
from trade.models import Bar, Instrument


class BarSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    instrument = serializers.StringRelatedField()

    class Meta:
        model = Bar
        fields = ['id', 'time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume', 'instrument', 'timeframe', 'created_by']


class InstrumentSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Instrument
        fields = ['id', 'name', 'desc', 'created_by']

    # id = serializers.IntegerField(read_only=True)
    # time = serializers.DateTimeField()
    # open = serializers.FloatField()
    # high = serializers.FloatField()
    # low = serializers.FloatField()
    # close = serializers.FloatField()
    # tick_volume = serializers.BigIntegerField(blank=True, null=True)
    # spread = serializers.IntegerField(blank=True, null=True)
    # real_volume = serializers.BigIntegerField(blank=True, null=True)
    # instrument = serializers.ForeignKey(Instrument, on_delete=models.CASCADE)
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Snippet.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
