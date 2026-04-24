# records/models.py
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

# Static Encryption Key for AES-like approach using Fernet
ENCRYPTION_KEY = b'6t-WwXpPZ9_Vf8PkWl3bK_Y-t_8oG36H-d6bS3mU5G0='
cipher = Fernet(ENCRYPTION_KEY)

class StudentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    year_level = models.IntegerField()

    def __str__(self):
        return f"{self.full_name} - {self.course}"

class PaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    encrypted_card_number = models.CharField(max_length=255)

    def set_card_number(self, raw_card):
        """Encrypts raw text string before storage."""
        self.encrypted_card_number = cipher.encrypt(raw_card.encode()).decode()

    def get_card_number(self):
        """Decrypts database ciphertext back to plain text."""
        return cipher.decrypt(self.encrypted_card_number.encode()).decode()

    def __str__(self):
        return f"{self.item_name} - ${self.amount}"