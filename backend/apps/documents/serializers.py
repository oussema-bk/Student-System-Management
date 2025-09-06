from rest_framework import serializers
from .models import Document, Bulletin, BulletinSubject, Attestation


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class BulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulletin
        fields = '__all__'


class BulletinSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletinSubject
        fields = '__all__'


class AttestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attestation
        fields = '__all__'
