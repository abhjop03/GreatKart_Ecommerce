from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.redis_helper import RedisHelper

redis = RedisHelper()

class RedisOperations(APIView):

    def post(self, request):
        data = request.data
        dtype = data.get("type")

        if dtype == "string":
            redis.set_string(data["key"], data["value"])
            return Response({"message": "String set successfully"})
        
        elif dtype == "hash":
            redis.set_hash(data["key"], data["value"])
            return Response({"message": "Hash set successfully"})

        elif dtype == "list":
            redis.push_list(data["key"], data["value"])
            return Response({"message": "List pushed successfully"})

        return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        key = request.query_params.get("key")
        dtype = request.query_params.get("type")
        field = request.query_params.get("field")

        if dtype == "string":
            return Response({"value": redis.get_string(key)})
        
        elif dtype == "hash":
            if field:
                return Response({field: redis.get_hash_field(key, field)})
            return Response(redis.get_hash(key))
        
        elif dtype == "list":
            return Response({"list": redis.get_list(key)})

        return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        key = request.query_params.get("key")
        dtype = request.query_params.get("type")
        field = request.query_params.get("field")

        if dtype == "string" or dtype == "list":
            redis.delete_key(key)
            return Response({"message": "Key deleted"})

        elif dtype == "hash" and field:
            redis.delete_hash_field(key, field)
            return Response({"message": f"Field '{field}' deleted from hash"})

        return Response({"error": "Invalid delete operation"}, status=status.HTTP_400_BAD_REQUEST)
