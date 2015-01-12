from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('subject', 'text')

    def create(self, validated_data):
        contact = Contact(**validated_data)
        contact.player = self.context['request'].user
        contact.save()

        return contact
