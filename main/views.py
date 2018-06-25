from parsing_tools import parse, stringify_parsed_json
from rest_framework.views import APIView
from rest_framework.response import Response


class OpeningHours(APIView):
    """
    Parse opening hours into nice human readable representation.
    """
    def post(self, request, format=None):
        return Response(parse(request.data))
