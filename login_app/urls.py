from django.urls import path     
from . import views

urlpatterns = [

    path('', views.index),                  # localhost:8000
    path('register', views.register),       # localhost:8000/register
    path('logout', views.logout),
    path('login', views.login),
    path('recipes', views.recipes),
    path('favRecipes', views.favoriteRecipes),
    path('addRecipe', views.addRecipe),
    path('editRecipe/<int:recipe_id>', views.editRecipe),
    path('updateRecipe/<int:recipe_id>', views.updateRecipe),
    path('viewRecipe/<int:recipe_id>', views.viewRecipe),
    path('newRecipe', views.newRecipe),
    path('recipe/<int:recipe_id>/like', views.like),
    path('recipe/<int:recipe_id>/unlike', views.unlike),
    path('recipe/<int:recipe_id>/addFavorite', views.addFavorite),
    path('recipe/<int:recipe_id>/removeFavorite', views.removeFavorite),
    path('addIngredient', views.addIngredient),
    path('removeIngredient/<int:recipe_id>/<int:ingredient_id>/', views.removeIngredient),
    path('addStep', views.addStep),
    path('removeStep/<int:recipe_id>/<int:step_id>/', views.removeStep),
    path('deleteRecipe/<int:recipe_id>', views.deleteRecipe),
]
