import django.urls

import homepage.views

app_name = 'homepage'


urlpatterns = [
    django.urls.path(
        'coffee/',
        homepage.views.Coffee.as_view(),
        name='coffee',
    ),
]
