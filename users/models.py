from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Reminders(models.Model):
    '''
    model for reminders
    it holds data for reminders for an activity, time and status whether done or postponed
    '''
    reminder_choice = [('Snooze',"snooze"), ('Done', 'done')]
    set = models.BooleanField(default=False)    # indicator to show that a reminder is set
    activity = models.CharField(max_length=200) # activity that need reminder
    time = models.DateTimeField()   # reminder time
    status = models.CharField(choices=reminder_choice, max_length=6)  # reminder status


# new 16th June
class PopularExercises(models.Model):
    '''
    This stores videos on popular exercise
    '''

    title = models.CharField(max_length=200)    # holds the video title
    file = models.FileField(upload_to='videos/', null=True)     # holds the  url for the video


# new 16th june
class QuickTips(models.Model):
    '''
    This stores the details of quick tips
    '''

    category = models.CharField(max_length=200)     # holds tips category like: fitness, health , nutrients...
    title = models.CharField(max_length=200)    # holds the title of the tip e.g 6 reasons why you should meditate daily
    content = models.TextField()    # holds the tips content / details


class FitnessActivityTracker(models.Model):
    '''
    This model tracks the fitness activity
    '''
    duration = models.IntegerField()  # planned duration (no of days/weeks/month of the particular activity
    start_date = models.DateField()  # start date of the activity
    end_date = models.DateField()  # planned end date of the activity
    on_track = models.BooleanField()  # on track status of the activity


class FitnessActivity(models.Model):
    '''
    This model hold each activity a user can perform,
    description of the activity and
    tracker for the activity
    '''
    name = models.CharField(max_length=200)     # name of the fitness activity
    description = models.TextField()    # description of the fitness activity
    fitness_activity_tracker = models.ForeignKey(FitnessActivityTracker, on_delete=models.CASCADE)      # activity tracker

    def __str__(self):
        return self.name


class SnacksAm(models.Model):
    '''
    This stores the list of available snacks with their calories
    '''
    name = models.CharField(max_length=200)  # the name of the snacks / combination
    calories = models.IntegerField()  # the calories of the snacks

    def __str__(self):
        return self.name


class SnacksPm(models.Model):
    '''
    This stores the list of available snacks with their calories
    '''
    name = models.CharField(max_length=200)  # the name of the snacks / combination
    calories = models.IntegerField()  # the calories of the snacks

    def __str__(self):
        return self.name


class MealBreakfast(models.Model):
    '''
    This stores the list of available meals with their calories
    '''
    name = models.CharField(max_length=200)  # stores the name of the meal (Fufu + Equsi + ....
    calories = models.IntegerField()  # stores the calories of the meal

    def __str__(self):
        return self.name


class MealLunch(models.Model):
    '''
    This stores the list of available meals with their calories
    '''
    name = models.CharField(max_length=200)  # stores the name of the meal (Fufu + Equsi + ....
    calories = models.IntegerField()  # stores the calories of the meal

    def __str__(self):
        return self.name


class MealDinner(models.Model):
    '''
    This stores the list of available meals with their calories
    '''
    name = models.CharField(max_length=200)  # stores the name of the meal (Fufu + Equsi + ....
    calories = models.IntegerField()  # stores the calories of the meal

    def __str__(self):
        return self.name


class DayMealPlan(models.Model):
    '''
    This holds data for meal plan for a single day
    '''
    day = models.CharField(max_length=100)  # holds data for which day (day1, day2...

    breakfast = models.ForeignKey(MealBreakfast, on_delete=models.CASCADE)  # holds data for expected breakfast meal

    lunch = models.ForeignKey(MealLunch, on_delete=models.CASCADE)  # holds data for expected lunch meal

    dinner = models.ForeignKey(MealDinner, on_delete=models.CASCADE)  # holds data for expected dinner meal

    am_snacks = models.ForeignKey(SnacksAm, on_delete=models.CASCADE)  # hols data for morning snacks

    pm_snacks = models.ForeignKey(SnacksPm, on_delete=models.CASCADE)  # holds data for afternoon snacks


class MealPlan(models.Model):
    name = models.CharField(max_length=200)  # holds the name for the meal plan. there are different meal plan
    start_date = models.DateTimeField()  # holds the meal plan start date.
    plan = models.ManyToManyField(DayMealPlan)  # holds as many plan as possible for the user


class CustomAccountManager(BaseUserManager):
    '''
    MANAGER FOR OUR CUSTOM USER
    controls what happens when new users/superusers are created.
    '''
    # creates super user with mandatory field specified.
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        # print(f"[x][]{other_fields}")
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)

        # quick validation. a superuser must be admin, superuser and a staff
        if other_fields.get('is_staff') is not True:
            raise ValueError("A superuser must be assinged 'is_staff'=True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("A superuser must be assinged 'is_superuser'=True")

        if other_fields.get('is_admin') is not True:
            raise ValueError("A superuser must be assigned to 'is_superuser'=True")
        # print(f"[][x]{other_fields}")

        # create user (superuser) with the information provided.
        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        # validation: since email will be required for log in. it must be provided.
        if not email:
            raise ValueError(_('You must provide email address'))

        # normalize the email
        email = self.normalize_email(email)
        # create a user model variable and apply information
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        # set the password with the provided password
        user.set_password(password)
        # save the user to database
        user.save()
        # return user created.
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    '''
    This create a custom user model that inherits / replace default django user model.
    specifying " AUTH_USER_MODEL = 'users.NewUser'  " in the settings causes django to use this model instead of default User
    '''
    sex_choice = [('male', 'M'), ('female', 'F')]

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)

    birthday = models.DateField(null=True)  # users birthday
    height = models.IntegerField(null=True)  # user's height
    weight = models.IntegerField(null=True)  # user's weight
    sex = models.CharField(max_length=6, choices=sex_choice)  # user's sex
    reminders = models.ManyToManyField(Reminders)  # holds every reminders set by user
    fitness_activities = models.ManyToManyField(FitnessActivity)  # holds all activities enrolled by the user
    meal_plan = models.ManyToManyField(MealPlan)

    is_staff = models.BooleanField(default=False)  # if user is a staff
    is_active = models.BooleanField(default=False)  # if user is active: possibly activated when email of user is confirmed
    is_admin = models.BooleanField(default=False)  # if user is admin: this might be a duplicate of is_superuser

    objects = CustomAccountManager()    # tells django that we are using custom account manager

    USERNAME_FIELD = 'email'  # this change the default which is username to email
    REQUIRED_FIELDS = ['user_name','first_name']    # required field when creating users/superusers.

    # option for setting username as the default.
    # USERNAME_FIELD = 'user_name'  # this change the default which is username to email
    # REQUIRED_FIELDS = ['email','first_name']

    def __str__(self):
        return self.user_name
