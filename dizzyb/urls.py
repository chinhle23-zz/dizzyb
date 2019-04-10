"""dizzyb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', core_views.index, name='index'),
    path('tasks/<int:task_id>/', core_views.edit_task, name='edit_task'),
    # path('tasks/<hashid:task_id>/', core_views.edit_task, name='edit_task')
    path('tasks/<int:task_id>/notes/', core_views.new_note, name='new_note'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
