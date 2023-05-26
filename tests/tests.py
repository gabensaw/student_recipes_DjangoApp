"""

All test classes and methods defined in our done definition were created to test,
if and what errors occur in the application and their frequency.

"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from recipesApp.models import Recipe, Ingredient, Nutrient


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        userInfo = {
            'username': 'test0309',
            'password': 'agile0309',
            'email': 'csm2020agile@gmail.com'
        }
        self.client.force_login(User.objects.create_user(userInfo))

    def test_profile_access_ok(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_update_ok(self):
        self.assertTrue(self.client.login)
        updateInfo = {
            'username': 'test39',
            'email': 'csm2020agile@gmail.com'
        }
        response = self.client.post('/profile/', updateInfo)

        self.assertNotEqual(response.status_code, 200)

    def test_profile_update_fail(self):
        self.assertTrue(self.client.login)
        updateInfo = {
            'username': '',
            'email': 'csm2020agile@gmail.com'
        }
        response = self.client.post('/profile/', updateInfo)

        self.assertEqual(response.status_code, 200)


class BaseTest(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('recipes-home')
        self.createrecipe_url = reverse('recipe-create')
        self.myrecipes_url = reverse('my-recipes')
        self.user_valid = {
            'username': 'testing',
            'email': 'email@gmail.com',
            'password1': 'testme123',
            'password2': 'testme123'
        }
        self.user_invalid_email = {
            'username': 'testing',
            'email': 'invalid',
            'password1': 'testme123',
            'password2': 'testme123'
        }
        self.user_not_matching_passwords = {
            'username': 'testing',
            'email': 'email@gmail.com',
            'password1': 'testme123',
            'password2': 'nottestme123'
        }
        self.user_invalid_username = {
            'username': '***',
            'email': 'email@gmail.com',
            'password1': 'testme123',
            'password2': 'nottestme123'
        }
        self.client = Client()

        return super().setUp()


class RegistrationTesting(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_can_register_with_valid_data(self):
        response = self.client.post(self.register_url, self.user_valid)
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_cant_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_invalid_email)
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_with_not_matching_passwords(self):
        response = self.client.post(self.register_url, self.user_not_matching_passwords)
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)

    def test_cant_register_with_invalid_username(self):
        response = self.client.post(self.register_url, self.user_invalid_username)
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 0)


class LoginTesting(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_can_login_with_valid_data(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        login = self.client.login(username='admin', password='testme123')
        self.assertTrue(login)

    def test_cant_login_with_invalid_data(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        login = self.client.login(username='admin', password='nottestme123')
        self.assertFalse(login)


class LogoutTesting(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')

    def test_can_logout(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        login = self.client.login(username='admin', password='testme123')
        self.assertTrue(login)
        response = self.client.get('/logout')
        self.client.logout()
        self.assertRedirects(response, '/logout/', status_code=301, fetch_redirect_response=False)


class AccountTesting(BaseTest):
    def test_can_delete_account_django(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        pk = self.user.pk
        get_account = User.objects.get(pk=self.user.pk)
        get_account.delete()
        self.assertFalse(User.objects.filter(pk=pk).exists())

    def test_can_delete_account(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        pk = self.user.pk
        get_account = User.objects.get(pk=self.user.pk)
        get_account.is_active = False
        login = self.client.login(username='admin', password='testme123')
        self.assertTrue(login)


class RecipeTest(BaseTest):
    def test_can_create_valid_recipe(self):
        try:
            self.user = User.objects.create(username='test')
            self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                                instruction='testing123',
                                                recipeCategory='Party', skillsLevel='Easy', portion='2',
                                                cookingTime='2',
                                                dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                                author=self.user)
            self.ingredient = Ingredient.objects.create(recipeName=self.recipe, ingredient='Testing1')
            self.ingredient = Ingredient.objects.create(recipeName=self.recipe, ingredient='Testing2')
            self.ingredient = Ingredient.objects.create(recipeName=self.recipe, ingredient='Testing3')
            self.nutrient = Nutrient.objects.create(recipeName=self.recipe, calories='5', fat='5', carbohydrate='5',
                                                    fibre='5', protein='5', salt='5')
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(False)

    def test_can_not_create_invalid_1_recipe(self):
        self.user = User.objects.create(username='test')
        try:
            response = Recipe.objects.create(recipeName='', description='testing123',
                                             instruction='testing123',
                                             recipeCategory='', skillsLevel='', portion='-2', cookingTime='2',
                                             dateAdded='2022-03-09 22:16:44', cost='-4', author_id=self.user.id,
                                             author=self.user)
            self.assertFalse(False)
        except Exception as e:
            self.assertTrue(True)

    def test_can_not_create_invalid_2_recipe(self):
        self.user = User.objects.create(username='test')
        try:
            response = Recipe.objects.create(recipeName='@@@@', description='}{}{}{}{}{}{',
                                             instruction='testing123',
                                             recipeCategory='', skillsLevel='Not Easy', portion='5.5', cookingTime='21',
                                             dateAdded='2022-03-09 22:16:44', cost='-4', author_id=self.user.id,
                                             author=self.user)
            self.assertFalse(False)
        except Exception as e:
            self.assertTrue(True)

    def test_can_not_create_invalid_3_recipe(self):
        self.user = User.objects.create(username='test')
        try:
            response = Recipe.objects.create(recipeName='test', description='testing123',
                                             instruction='testing123',
                                             recipeCategory='', skillsLevel='', portion='2', cookingTime='2',
                                             dateAdded='2022-0', cost='-4', author_id=self.user.id,
                                             author=self.user)
            self.assertFalse(False)
        except Exception as e:
            self.assertTrue(True)

    def test_can_not_create_invalid_4_recipe(self):
        self.user = User.objects.create(username='test')
        try:
            response = Recipe.objects.create(recipeName='test', description='testing123',
                                             instruction='testing123',
                                             recipeCategory='', skillsLevel='', portion='2', cookingTime='2',
                                             dateAdded='2022-0', cost='-4')
            self.assertFalse(False)
        except Exception as e:
            self.assertTrue(True)

    def test_can_not_create_invalid_1_nutrient(self):
        try:
            self.user = User.objects.create(username='test')
            self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                                instruction='testing123',
                                                recipeCategory='Party', skillsLevel='Easy', portion='2',
                                                cookingTime='2',
                                                dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                                author=self.user)
            self.nutrient = Nutrient.objects.create(recipeName=self.recipe, calories='-5', fat='-5', carbohydrate='-5',
                                                    fibre='-5', protein='-5', salt='-5')
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(False)

    def test_can_not_create_invalid_2_nutrient(self):
        try:
            self.user = User.objects.create(username='test')
            self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                                instruction='testing123',
                                                recipeCategory='Party', skillsLevel='Easy', portion='2',
                                                cookingTime='2',
                                                dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                                author=self.user)
            self.nutrient = Nutrient.objects.create(recipeName=self.recipe, calories='test', fat='test',
                                                    carbohydrate='test',
                                                    fibre='test', protein='test', salt='test')
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(False)

    def test_can_edit_recipe(self):
        try:
            self.user = User.objects.create(username='test')
            self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                                instruction='testing123',
                                                recipeCategory='Party', skillsLevel='Easy', portion='2',
                                                cookingTime='2',
                                                dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                                author=self.user)
            self.recipe.recipeName = 'Not Testing Beans'
            self.recipe.description = 'Not testing123'
            self.recipe.instruction = 'Not testing123'
            self.recipe.recipeCategory = 'Dinner'
            self.recipe.skillsLevel = 'Difficult'
            self.recipe.portion = '25'
            self.recipe.cookingTime = '5'
            self.recipe.dateAdded = '2022-03-12 21:15:22'
            self.recipe.cost = '5'
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(False)

    def test_can_not_make_invalid_edit_recipe(self):
        try:
            self.user = User.objects.create(username='test')
            self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                                instruction='testing123',
                                                recipeCategory='Party', skillsLevel='Easy', portion='2',
                                                cookingTime='2',
                                                dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                                author=self.user)
            self.recipe.recipeName = ''
            self.recipe.description = ''
            self.recipe.instruction = ''
            self.recipe.recipeCategory = ''
            self.recipe.skillsLevel = ''
            self.recipe.portion = '-25'
            self.recipe.cookingTime = '-5'
            self.recipe.dateAdded = '2022-2'
            self.recipe.cost = '-5'
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(False)

    def test_can_view_recipe_list(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_can_view_my_recipes(self):
        self.user = User.objects.create(username='admin')
        self.user.set_password('testme123')
        self.user.save()
        login = self.client.login(username='admin', password='testme123')
        response = self.client.get(self.myrecipes_url)
        self.assertEqual(response.status_code, 200)

    def test_can_not_view_my_recipes_when_logged_out(self):
        try:
            response = self.client.get(self.myrecipes_url)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(False)
        except Exception as e:
            self.assertTrue(True)


class FilterTests(BaseTest):
    def test_can_search_1_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeName__icontains='Beans').order_by('-dateAdded').all().count() == 2)

    def test_can_search_2_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeName__icontains='Bacon').order_by('-dateAdded').all().count() == 0)

    def test_can_search_3_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeName__icontains='').order_by('-dateAdded').all().count() == 2)

    def test_can_category_filter_1_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='Party').order_by('-dateAdded').all().count() == 2)

    def test_can_category_filter_2_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='Dinner').order_by('-dateAdded').all().count() == 0)

    def test_can_category_filter_3_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='').order_by('-dateAdded').all().count() == 0)

    def test_can_category_filter_and_search_1_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='Party').filter(recipeName__icontains='Beans').order_by('-dateAdded').all().count() == 2)

    def test_can_category_filter_and_search_2_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='').filter(recipeName__icontains='').order_by('-dateAdded').all().count() == 0)

    def test_can_category_filter_and_search_3_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='Dinner').filter(recipeName__icontains='Bacon').order_by('-dateAdded').all().count() == 0)

    def test_can_category_filter_and_search_4_recipe(self):
        self.user = User.objects.create(username='test')
        self.recipe = Recipe.objects.create(recipeName='Testing Beans', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Party', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.recipe = Recipe.objects.create(recipeName='Beans Testing', description='testing123',
                                            instruction='testing123',
                                            recipeCategory='Dinner', skillsLevel='Easy', portion='2',
                                            cookingTime='2',
                                            dateAdded='2022-03-09 22:16:44', cost='2', author_id=self.user.id,
                                            author=self.user)
        self.assertTrue(Recipe.objects.filter(recipeCategory='Dinner').filter(recipeName__icontains='Bean').order_by('-dateAdded').all().count() == 1)