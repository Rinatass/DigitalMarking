from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MarkingCode, Location, MovementLog, ProductBatch
from .serializers import MarkingCodeSerializer, MovementCreateSerializer, LocationSerializer, ProductBatchSerializer, \
    MarkingCodeShortSerializer


class MarkingCodeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code):
        marking_code = get_object_or_404(MarkingCode, code=code)
        serializer = MarkingCodeSerializer(marking_code)
        return Response(serializer.data)


class AddMovementView(APIView):

    def post(self, request, code):
        marking_code = get_object_or_404(MarkingCode, code=code)
        serializer = MovementCreateSerializer(data=request.data)
        if serializer.is_valid():
            location = get_object_or_404(Location, id=serializer.validated_data['location_id'])
            MovementLog.objects.create(
                code=marking_code,
                location=location.name,
                moved_by=request.user if request.user.is_authenticated else None
            )
            return Response({'status': 'movement recorded'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]


class ProductBatchListView(ListAPIView):
    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer
    permission_classes = [IsAuthenticated]

class BatchCodesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        batch = get_object_or_404(ProductBatch, id=batch_id)
        codes = batch.codes.all()
        serializer = MarkingCodeShortSerializer(codes, many=True)
        return Response(serializer.data)
