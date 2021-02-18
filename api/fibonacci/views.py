from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .serializers import FibonacciSerializer

@api_view(http_method_names=["GET"])
def calculate_fibonacci(request):
    serializer = FibonacciSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    n = serializer.data.get("n")
    fib_1, fib_2 = 0, 1
    for i in range(1, n + 1):
        aux = fib_1 + fib_2
        fib_1, fib_2 = fib_2, aux
    return Response({
        "status": "SUCCESS",
        "value": fib_1
    }, status=status.HTTP_200_OK)