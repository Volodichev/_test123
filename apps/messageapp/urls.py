from django.urls import path, re_path
from .views import homepageview, MessageApiViewDetail, MessageConfirmApiView, MessageApiViewList

urlpatterns = [
    path('', homepageview, name="message_list"),
    re_path(r'v1/message/', MessageApiViewDetail.as_view(), name="message_detail"),
    re_path(r'v1/messages/', MessageApiViewList.as_view(), name="message_list"),
    re_path(r'v1/message_confirmation/', MessageConfirmApiView.as_view(), name="message_confirmation")
]
