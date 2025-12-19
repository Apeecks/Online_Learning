from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials import views


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', views.LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path("courses/subscription/", views.CourseSubscriptionAPIView.as_view(), name="course_subscription"),
] + router.urls
