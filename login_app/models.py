from django.db import models
from datetime import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class StepManager(models.Manager):
    def basic_validation(self, form):

        errors = {}

        # add keys and values to errors dictionary for Quote Basic Validation
        if len(form['new_step_content']) < 3:
            errors['new_step_content'] = 'Step must be greater than 2 characters'

        return errors


# Recipe custom manager.

class IngredientManager(models.Manager):
    def basic_validation(self, form):

        errors = {}

        # add keys and values to errors dictionary for Quote Basic Validation
        if len(form['new_ingredient_content']) < 3:
            errors['new_ingredient_content'] = 'Ingredient must be greater than 2 characters'

        return errors


# Recipe custom manager.

class RecipeManager(models.Manager):
    def new_validation(self, form):

        errors = {}

        print('new_recipe_serving')
        print(form['new_recipe_serving'])

        # add keys and values to errors dictionary for Quote Basic Validation
        if len(form['new_recipe_title']) < 3:
            errors['new_recipe_title'] = 'Recipe title must be greater than 2 characters'
        if len(form['new_recipe_title']) > 24:
            errors['new_recipe_title'] = 'Recipe title must be less than 25 characters'
        if len(form['new_recipe_description']) < 6:
            errors['new_recipe_description'] = 'Recipe description must be greater than 5 characters'
        if len(form['new_recipe_description']) > 255:
            errors['new_recipe_description'] = 'Recipe description must be less than 255 characters'
        if form['new_recipe_serving'] == '':
            errors['new_recipe_serving'] = 'Serving required'

        return errors

    def update_validation(self, form):

        errors = {}

        # add keys and values to errors dictionary for Quote Basic Validation
        if len(form['new_recipe_description']) < 6:
            errors['new_recipe_description'] = 'Recipe description must be greater than 10 characters'
        if len(form['new_recipe_description']) > 255:
            errors['new_recipe_description'] = 'Recipe description must be less than 255 characters'

        return errors


# User custom manager.

class UserManager(models.Manager):
    def register_validation(self, form):

        errors = {}

        # add keys and values to errors dictionary for each invalid field
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'
        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email_add']):    # test whether a field matches the pattern            
            errors['email_add'] = ("Invalid email address!")

        if len(form['pwd_one']) < 8:
            errors['pwd_one'] = 'Password must be at least 8 characters'

        if form['pwd_one'] != form['pwd_two']:
            errors['pwd_one'] = 'Passwords do not match'

        if (len(form['birthday_dt']) < 1):
            errors['birthday_dt'] = 'Birthday missing'
        else:
            today = datetime.today()
            birthday = datetime.strptime(form['birthday_dt'], '%Y-%m-%d')
            print('Today:', today)        
            print('Birthday:', birthday)
            age = today.year - birthday.year - ((today.month, today.day) <
                (birthday.month, birthday.day))
            print('Age:', age)

            if datetime.strptime(form['birthday_dt'], '%Y-%m-%d') > datetime.now():
                errors['birthday_dt'] = 'Birthday cannot be in the future'

            if age < 13:
                errors['age'] = 'User cannot be under 13 years old'

        # Email check with Filter (return list if multiple, single object if one, or empty list )
        emails = User.objects.filter(email=form['email_add'])
        if len(emails) > 0:
            errors['email_add'] = 'Email address exists'

        return errors

    def login_validation(self, form):

        errors = {}
        if len(form['email_add']) < 1:
            errors['email_add'] = 'Missing email'

        if len(form['pwd_one']) < 1:
            errors['pwd_one'] = 'Missing password'

        return errors

    def register(self, form):
        print('User register method')
        pw = bcrypt.hashpw(form['pwd_one'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email_add'],
            birthday = form['birthday_dt'],
            password = pw,
        )

    def authenticate(self, email, password):
        user = self.filter(email=email)
        if user:
            if bcrypt.checkpw(password.encode(), user[0].password.encode()):
                print('Passwords Match!')
                return user[0]
            else:
                print('Passwords does not Match!')
        return False

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()       #Custom User manager


class Step(models.Model):
    content =models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='steps_posted',on_delete=models.CASCADE)     # User who posted the Step
    objects = StepManager()       # Step manager

class Ingredient(models.Model):
    content =models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='ingredients_posted',on_delete=models.CASCADE)     # User who posted the Ingredient
    objects = IngredientManager()       # Ingredient manager


class Recipe(models.Model):
    title =models.CharField(max_length=255) 
    description = models.CharField(max_length=255)
    serving = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='recipes_posted',on_delete=models.CASCADE)     # User who posted Recipe
    users_who_like = models.ManyToManyField(User, related_name='liked_recipes')                     # Users who liked Recipe
    users_favorite = models.ManyToManyField(User, related_name='favorite_recipes')                  # Users who favorite Recipe
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')                        # Ingredients for Recipe
    steps = models.ManyToManyField(Step, related_name='recipes')                                    # Steps for Recipe
    objects = RecipeManager()           # Recipe manager

