from django.conf.urls import url

from coup.positions.views import PositionOverview

urlpatterns = [
    url(
        regex = r'^$',\
        view = PositionOverview.as_view(),\
        name = 'DashBoardView'
    ),
]

