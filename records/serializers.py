# records/serializers.py
from rest_framework import serializers
from .models import StudentRecord, PaymentTransaction

class StudentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ['id', 'owner', 'full_name', 'course', 'year_level']
        read_only_fields = ['owner']

class PaymentTransactionSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PaymentTransaction
        fields = ['id', 'item_name', 'amount', 'card_number', 'encrypted_card_number']
        read_only_fields = ['encrypted_card_number']

    def create(self, validated_data):
        raw_card = validated_data.pop('card_number')
        transaction = PaymentTransaction.objects.create(**validated_data)
        transaction.set_card_number(raw_card)
        transaction.save()
        return transaction