from .models import Token


class TokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Middleware start!")

        if 'HTTP_AUTHORIZATION' in request.META:
            header_value = request.META['HTTP_AUTHORIZATION']
            token_key = header_value[6:]
            token = Token.objects.get(key=token_key)
            request.user = token.user
            request.auth = token_key

        print("Middleware done! user=", request.user)

        response = self.get_response(request)

        return response
