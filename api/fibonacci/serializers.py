from rest_framework import serializers

class FibonacciSerializer(serializers.Serializer):
    n = serializers.IntegerField(max_value=10000, min_value=0)

    def validate_n(self, n):
        if n < 0:
            raise serializers.ValidationError("Value must be positve")
        return n