import django.http

import oauth2_provider.views.generic

class OauthApiEndpoint(oauth2_provider.views.generic.ProtectedResourceView):

    def get(self, request, *args, **kwargs):

        return django.http.HttpResponse('Hello, OAuth2!')
