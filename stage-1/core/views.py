"""
=====================
core/views.py
====================


Contains validation, flow logic
"""
from rest_framework.decorators import api_view
from rest_framework import status
from core.serializers import StringreadSerializer
from rest_framework.response import Response
# from django.core.exceptions import ValidationError
from core.models import AnalyzedString
from core.utils import analyze_string
import hashlib
from core.nlp_parser import parse_natural_query

@api_view(['POST'])
def create_strings(request):
    value = request.data.get('value')

    if value.strip() == "" or not isinstance(value, str) or value is None:
        return Response(
            # {"value": 'Invalid request body or missing "value" field'},
            'Invalid request body or missing "value" field',
            status=status.HTTP_400_BAD_REQUEST
        )
    
    computed_string = analyze_string(value)

    if AnalyzedString.objects.filter(
        id=computed_string['sha256_hash']
    ).exists():
        return Response(
            # {"value": "String already exists in this system"},
            "String already exists in this system",
            status=status.HTTP_409_CONFLICT
        )
    
    try:
        obj = AnalyzedString.objects.create(
            id=computed_string['sha256_hash'],
            value=value,
            length=computed_string['length'],
            is_palindrome=computed_string['is_palindrome'],
            unique_characters=computed_string['unique_characters'],
            word_count=computed_string['word_count'],
            sha256_hash=computed_string['sha256_hash'],
            character_frequency_map=computed_string[
                'character_frequency_map'
            ],
        )
    except Exception as e:
        return Response(
            # {"error": f"Unprocessable Entity: {str(e)}"},
            "Invalid data type for \"value\" (must be string)",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    serializer = StringreadSerializer(obj)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(["GET", "DELETE"])
def get_string(request, string_value):
    try:
        obj = AnalyzedString.objects.get(id=hashlib.sha256(string_value.encode('utf-8')).hexdigest())
    except AnalyzedString.DoesNotExist:
        return Response(
            "String does not exist in the system",
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        return Response(
            StringreadSerializer(obj).data,
            status=status.HTTP_200_OK
        )
    else:
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_string_by_filtering(request):
    is_palindrome = request.query_params.get('is_palindrome')
    min_length = request.query_params.get('min_length')
    max_length = request.query_params.get('max_length')
    word_count = request.query_params.get('word_count')
    contains_character = request.query_params.get('contains_character')

    queryset = AnalyzedString.objects.all()

    if is_palindrome and is_palindrome.lower() == 'true':
        queryset = queryset.filter(is_palindrome=True)
    if min_length:
        queryset = queryset.filter(length__gte=int(min_length))
    if max_length:
        queryset = queryset.filter(length__lte=int(max_length))
    if word_count:
        queryset = queryset.filter(word_count=int(word_count))
    if contains_character:
        queryset = queryset.filter(value__icontains=contains_character)
    
    serializer = StringreadSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def filter_by_natural(request):
    query = request.query_params.get('query')


    if not query:
        return Response(
            {
                "error": "Missing \'query\' parameter"
            }, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        filters = parse_natural_query(query)
    except ValueError as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    
    if not filters:
        return Response(
            {"error": "Unable to parse Natural Language query"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    results = AnalyzedString.objects.filter(**filters)
    serializer = StringreadSerializer(results, many=True)

    return Response({
        "data": serializer.data,
        "count": len(serializer.data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": filters
        }
    }, status=status.HTTP_200_OK)
