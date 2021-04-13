from django.urls import path
from . import views
# Goal: Navigate to profile page
# User is prompted to input their info
# Check admin to confirm
# Goal2: Store User's list into the database
# Let user access their list by navigating to their profile
# Goal3: Display Popular movies, Highest grossing, High rated, allow user to refresh
# Home page also provides the user a personalized recommendation based on their list
urlpatterns = [
    # Intended Paths: Login <-> (Register if new, or Pass. reset) -> Home <-> (Profile, Search, User Operations, LogOut)
    path("", views.mainpage, name="login"),
    # path("", views.my_form, name="form"),
    path("register/", views.register, name="register"),
    path("home", views.home, name="return"),
    path("my_form", views.my_form, name="form"),
    path("", views.login, name="login"),
    path("display", views.display, name="display"),
    path("home", views.home, name="return"),
    path("aboutus", views.mainpage, name='return')

]