from rest_framework import serializers
from core.models import AnalyzedString
from core.utils import analyze_string


class StringreadSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AnalyzedString
        fields = [
            'id', 'value', 'properties', 'created_at'
        ]
    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'character_frequency_map': obj.character_frequency_map,
            'sha256_hash': obj.sha256_hash
        }


# class StringCreateSerializer(serializers.ModelSerializer):
#     value = serializers.CharField(
#         required=True,
#         allow_blank=False,
#         validators=[], # Disable unique and built-ins
#     )
#     class Meta:
#         model = AnalyzedString
#         fields = [
#             'value'
#         ]
#     def validate(self, attrs):
#         value = attrs['value']
#         if value.strip() is None:
#             raise serializers.ValidationError(
#                 {"value": "Invalid request body or missing \"value\" field"},
#                 code="bad_request"
#             )
#         if not isinstance(value, str):
#             raise serializers.ValidationError(
#                 {"value": "Invalid data type for \"value\" (must be string)"},
#                 code="unprocessable"
#             )
                
#         return super().validate(attrs)
#     def create(self, validated_data):
#         value = validated_data['value']
#         cleaned_value_ppt = analyze_string(value)

#         if AnalyzedString.objects.filter(
#             id=cleaned_value_ppt['sha256_hash']
#         ).exists():
#             raise serializers.ValidationError(
#                 {"value": "String already exists in this system"},
#                 code="conflict"
#             )
        
#         return AnalyzedString.objects.create(
#             id=cleaned_value_ppt['sha256_hash'],
#             value=value,
#             length=cleaned_value_ppt['length'],
#             is_palindrome=cleaned_value_ppt['is_palindrome'],
#             unique_characters=cleaned_value_ppt['unique_characters'],
#             word_count=cleaned_value_ppt['word_count'],
#             sha256_hash=cleaned_value_ppt['sha256_hash'],
#             character_frequency_map=cleaned_value_ppt[
#                 'character_frequency_map'
#             ],
#         )
        
    
