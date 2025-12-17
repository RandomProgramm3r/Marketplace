import http

import django.http
import django.views


class Coffee(django.views.View):
    def get(self, request):
        return django.http.HttpResponse(
            "I'm a Teapot",
            status=http.HTTPStatus.IM_A_TEAPOT,
        )
