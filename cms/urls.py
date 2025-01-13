from django.contrib import admin
from django.urls import path, include
from project import urls as project_urls
from company import urls as company_urls
from department import urls as department_urls
from employee import urls as employee_urls
from user import urls as user_urls
from performance_review import urls as performance_review_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', include(project_urls)),
    path('company/', include(company_urls)),
    path('department/', include(department_urls)),
    path('employee/', include(employee_urls)),
    path('user/', include(user_urls)),
    path('performance_review/', include(performance_review_urls))
]
