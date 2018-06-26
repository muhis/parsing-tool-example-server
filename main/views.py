import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from parsing_tools import parse, stringify_parsed_json
from rest_framework.response import Response as APIResponse
from rest_framework.views import APIView


class OpeningHours(APIView):
    """
    Parse opening hours into nice human readable representation.
    """
    def post(self, request, format=None):
        return APIResponse(parse(request.data))


@csrf_exempt
def opening_hours_string(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        parsed_json = parse(payload)
        string_response = stringify_parsed_json(parsed_json)
        return HttpResponse(string_response)

    # This here should be an exception.
    return HttpResponse('Only post request accepted')
