from django.urls import path
from . import views
#from blog.views import ListView
app_name="blog"

urlpatterns = [
	path('list/', views.user_blogs, name='user_blogs'),

	path('index/', views.index, name='home'),
	path('register/', views.register, name='register'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('<slug:username>/', views.list_view, name='list'),
	#path('dashboard/create/', views.formset_view, name='formset_view'),
	# path('list/', views.list_view, name='list'),
	path('dashboard/<int:user_id>/', views.detail_view, name="detail" ),
    path('dashboard/<int:user_id>/delete', views.post_model_delete_view, name="delete" ),
    path('dashboard/<int:user_id>/edit', views.post_model_update_view, name="update" ),
    path('dashboard/create/', views.post_model_create_view, name="create" ),

	#path('blog/create/', views.post_model_create_view, name='create'),
	# path('blogs/', BlogList.as_view(), name='list'),
	# path('index/', MyView.as_view(template_name='A1/index.html'), name='index'),
	# path('blog/<slug:slug>/', BlogDetail.as_view(), name='blog_detail'),
	# path('blog/<slug:slug>/delete/', BlogDeleteView.as_view(), name='delete'),
	# path('blog/<slug:slug>/update/', BlogUpdateView.as_view(), name='update'),
]