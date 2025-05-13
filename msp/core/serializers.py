from rest_framework import serializers
from .models import MarkingCode, MovementLog, Location, ProductBatch


class MovementLogSerializer(serializers.ModelSerializer):
    timestamp_formatted = serializers.SerializerMethodField()

    class Meta:
        model = MovementLog
        fields = ['location', 'timestamp', 'timestamp_formatted']

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime('%d.%m.%Y %H:%M:%S')


class MarkingCodeSerializer(serializers.ModelSerializer):
    movements = MovementLogSerializer(many=True, read_only=True)

    class Meta:
        model = MarkingCode
        fields = ['code', 'product', 'movements']


class MovementCreateSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class ProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = ['id', 'name', 'product', 'quantity']


class MarkingCodeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingCode
        fields = ['id', 'code']
