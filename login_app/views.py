from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# other imports
from .models import Recipe, User, Ingredient, Step

# `Create` your views here.

def index(request):
    print(f'Index - Login Request method:{request.method}')

    return render(request, "loginReg.html",)

def register(request):
    print(f'Register User Request method:{request.method}')

    if request.method == "GET":
        return redirect('/')

    errors = User.objects.register_validation(request.POST)

    if errors:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        request.session['user_first_name'] = new_user.first_name
        # return redirect('/recipes')
        return redirect('/recipes')

def logout(request):
    request.session.clear()
    return redirect('/')    

def login(request):
    print(f'Login User Request method:{request.method}')
    if request.method == "GET":
        return redirect('/')

    errors = User.objects.login_validation(request.POST)

    if errors:
        messages.error(request, 'Invalid Email/Password')
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')    
    else:
        print(request.POST['email_add'], request.POST['pwd_one'])
        auth_user = User.objects.authenticate(request.POST['email_add'], request.POST['pwd_one'])
        if not auth_user:
            messages.error(request, 'Email/Password combination invalid')
            return redirect('/')    
        else:
            request.session['user_id'] = auth_user.id
            request.session['user_first_name'] = auth_user.first_name
            # return redirect('/books')
            return redirect('/recipes')

def newRecipe(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'recipe_user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'newRecipe.html', context)

def recipes(request):         # Show the recipes page
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'all_recipes': Recipe.objects.all().order_by('title'),
        'recipe_user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'recipes.html', context)

def addRecipe(request):

    print('addRecipe')

    errors = Recipe.objects.new_validation(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/newRecipe')    
    else:
        user = User.objects.get(id=request.session['user_id'])
        recipe = Recipe.objects.create(
            title = request.POST['new_recipe_title'],
            description = request.POST['new_recipe_description'],
            # description = request.POST['new_recipe_description'],
            serving = request.POST['new_recipe_serving'],
            posted_by = User.objects.get(id=request.session['user_id']),
        )
        # user added to favorites for the recipe
        user.liked_recipes.add(recipe)

        context = {
            "recipe": Recipe.objects.get(id=recipe.id),
            'recipe_user': User.objects.get(id=request.session['user_id']),
        }

        return render(request, 'receipeDetails.html', context)

def updateRecipe(request, recipe_id):

    print('updateRecipe')

    errors = Recipe.objects.update_validation(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
    else:
        user = User.objects.get(id=request.session['user_id'])
        updated_recipe = Recipe.objects.get(id=recipe_id)

        updated_recipe.description = request.POST['new_recipe_description']
        updated_recipe.serving = request.POST['new_recipe_serving']
        updated_recipe.save()

    recipe = Recipe.objects.get(id=recipe_id)

    context = {
        "recipe": Recipe.objects.get(id=recipe_id),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'receipeDetails.html', context)

def editRecipe(request, recipe_id):

    print('editRecipe')

    recipe = Recipe.objects.get(id=recipe_id)

    context = {
        "recipe": Recipe.objects.get(id=recipe_id),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),

        # 'favorite_users': Book.objects.first().users_who_like.all()
    }

    return render(request, 'receipeDetails.html', context)

def addIngredient(request):

    print('addIngredient')

    if request.method == "GET":
        return redirect('/')

    errors = Ingredient.objects.basic_validation(request.POST)
    recipe = Recipe.objects.get(id=request.POST['recipe_id'])

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        user = User.objects.get(id=request.session['user_id'])
        ingredient = Ingredient.objects.create(
            content = request.POST['new_ingredient_content'],
            posted_by = User.objects.get(id=request.session['user_id']),
        )
        recipe = Recipe.objects.get(id=request.POST['recipe_id'])
        ingredient.recipes.add(recipe)

    context = {
        "recipe": Recipe.objects.get(id=request.POST['recipe_id']),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'receipeDetails.html', context)

def addStep(request):

    print('addStep')

    if request.method == "GET":
        return redirect('/')

    errors = Step.objects.basic_validation(request.POST)
    recipe = Recipe.objects.get(id=request.POST['recipe_id'])

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        user = User.objects.get(id=request.session['user_id'])
        step = Step.objects.create(
            content = request.POST['new_step_content'],
            posted_by = User.objects.get(id=request.session['user_id']),
        )

        recipe = Recipe.objects.get(id=request.POST['recipe_id'])
        step.recipes.add(recipe)

    context = {
        "recipe": Recipe.objects.get(id=request.POST['recipe_id']),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'receipeDetails.html', context)

def removeIngredient(request, recipe_id, ingredient_id):

    print('removeIngredient')

    ingredient = Ingredient.objects.get(id=ingredient_id)
    recipe = Recipe.objects.get(id=recipe_id)
    ingredient.recipes.remove(recipe)
    ingredient.delete()

    context = {
        "recipe": Recipe.objects.get(id= recipe_id),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'receipeDetails.html', context)


def removeStep(request, recipe_id, step_id):

    print('removeStep')

    step = Step.objects.get(id=step_id)
    recipe = Recipe.objects.get(id=recipe_id)
    step.recipes.remove(recipe)
    step.delete()

    context = {
        "recipe": Recipe.objects.get(id= recipe_id),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'receipeDetails.html', context)


def viewRecipe(request, recipe_id):         # Show the recipe page
    if 'user_id' not in request.session:
        return redirect('/')

    print('viewStep')

    recipe = Recipe.objects.get(id=recipe_id)

    context = {
        "recipe": Recipe.objects.get(id= recipe_id),
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'recipe_ingredients': recipe.ingredients.all(),
        'recipe_steps': recipe.steps.all(),
    }

    return render(request, 'recipe.html', context)

def like(request, recipe_id):

    user = User.objects.get(id=request.session["user_id"])
    recipe = Recipe.objects.get(id=recipe_id)
    # user added to likes for the recipe
    user.liked_recipes.add(recipe)

    return redirect('/recipes')

def unlike(request, recipe_id):

    user = User.objects.get(id=request.session["user_id"])
    recipe = Recipe.objects.get(id=recipe_id)
    # user removes likes for the recipe    
    user.liked_recipes.remove(recipe)

    return redirect('/recipes')

def deleteRecipe(request, recipe_id):

    deleted_recipe = Recipe.objects.get(id=recipe_id)
    deleted_recipe.delete()

    return redirect('/recipes')    

def addFavorite(request, recipe_id):

    user = User.objects.get(id=request.session["user_id"])
    recipe = Recipe.objects.get(id=recipe_id)
    # user added to favorites for the recipe
    user.favorite_recipes.add(recipe)

    return redirect('/recipes')

def removeFavorite(request, recipe_id):

    user = User.objects.get(id=request.session["user_id"])
    recipe = Recipe.objects.get(id=recipe_id)
    # user remove from favorites for the recipe
    user.favorite_recipes.remove(recipe)

    return redirect('/recipes')

def favoriteRecipes(request):                           # Show User favorite recipes page
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'recipe_user': User.objects.get(id=request.session['user_id']),
        'user_recipes': Recipe.objects.filter(users_favorite=request.session['user_id']).order_by('title'),
    }

    return render(request, 'favorites.html', context)