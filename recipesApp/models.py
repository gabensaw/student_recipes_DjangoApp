from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator, MaxLengthValidator, \
    FileExtensionValidator
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


# Here are models Recipe, Ingredient, Nutrient mapped to the database (django convert models to DB tables)

class Recipe(models.Model):
    skillsChoice = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Difficult', 'Difficult')
    )

    categoryChoice = (
        ('Picnic', 'Picnic'),
        ('Party', 'Party'),
        ('Dinner', 'Dinner'),
        ('Dessert', 'Dessert'),
        ('Drink', 'Drink'),
        ('Other', 'Other')
    )
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Anonymous')
    recipeName = models.CharField('Recipe name', max_length=150)
    image = models.ImageField(
        default='default.jpg',
        upload_to='recipes_pics',
        max_length=250,
        validators=[
            FileExtensionValidator(
                ['jpg','png','webp','tiff','gif','jpeg','bmp','ico','tif','svgz','svg','pjp','xbm','jfif','pjpeg','avif'],
                message="Specify a valid file type"
            )
        ]
    )
    cost = models.DecimalField(
        'Total cost (£)',
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), message='The cost may not be less than 0.01 £'),
            MaxValueValidator(Decimal('100.01'), message='The cost may not be greater than 100 £')
            ]
    )
    portion = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(20, message='To many portions'),
                    MinValueValidator(1, message='Portion must be more than 0')
        ]
    )
    description = models.TextField(
        max_length=120,
        validators=[MinLengthValidator(5, message='Please provide longer description')]
    )
    instruction = models.TextField(
        max_length=5000,
        validators=[MinLengthValidator(10, message='Please provide longer instruction')]
    )
    cookingTime = models.PositiveSmallIntegerField(
        'Cooking time (mins)',
        validators=[MaxValueValidator(1440, message='The cooking time is too long')]
    )
    skillsLevel = models.CharField('skills level', max_length=30, choices=skillsChoice, default=('Easy', 'Easy'))
    recipeCategory = models.CharField(
        'Recipe category',
        default=('Other', 'Other'),
        max_length=30,
        choices=categoryChoice
    )
    dateAdded = models.DateTimeField('Date added', default=timezone.now)

    # method returning new object name
    def __str__(self):
        return self.recipeName

    # a method for cropping and transforming an image and storing the reduced version in a database
    def save(self, **kwargs):
        super().save(**kwargs)

        img = Image.open(self.image.path)
        #resize the image
        if img.height > 1500 or img.width > 1200:
            outputSize = (img.height* 0.8, img.width*0.8)
            img.thumbnail(outputSize)
            img.save(self.image.path)
        return self.id

    # reverse will return the full url path as a string by specific recipe id
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    recipeName = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(3, message='Please provide longer ingredient description')
        ]
    )

    # method returning new object name
    def __str__(self):
        return 'Author: %s, Recipe: %s - %s' % (self.recipeName.author, self.recipeName, self.ingredient)


class Nutrient(models.Model):
    recipeName = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    calories = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(10000, message='To many calories')
        ]
    )
    fat = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('-0.01'), message='Fat must not be less than 0'),
            MaxValueValidator(1000, message='Too much fat')
        ]
    )
    carbohydrate = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('-0.01'), message='Carbohydrate must not be less than 0'),
            MaxValueValidator(1000, message='Too much carbohydrate')
        ]
    )
    fibre = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('-0.01'), message='Fibre must not be less than 0'),
            MaxValueValidator(500, message='Too much fibre')
        ]
    )
    protein = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('-0.01'), message='Protein must not be less than 0'),
            MaxValueValidator(1000, message='Too much protein')
        ]
    )
    salt = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('-0.01'), message='Salt must not be less than 0'),
            MaxValueValidator(500, message='Too much salt')
        ]
    )

    # method returning new object name
    def __str__(self):
        return 'Author: %s, Recipe: %s' % (self.recipeName.author, self.recipeName)
