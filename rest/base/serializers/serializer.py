
from base.models import Person
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
    
    def validate(self, data):
        if any(char.isdigit() for char in data['name']):
            raise serializers.ValidationError({'error':'Name should not contain numbers'})
        
        return data