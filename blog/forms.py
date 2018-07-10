from django import forms

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, authenticate
from .models import USERNAME_REGEX
from django.core.validators import RegexValidator
from django.db.models import Q
from .models import MyUser
from django.forms import ModelForm

from .models import Post
User = get_user_model()
from django import forms


from .models import Post

class PostModelForm(forms.ModelForm):
    # title = forms.CharField(
    #         max_length=120, 
    #         label='Some field', 
    #         help_text='some help text', 
    #         error_messages={
    #             "required": "The title field is required."
    #         }
    #     )
    class Meta:
        model = Post
        fields = ["title", "content",]
        labels = {
            "title": "Title ",
        }
        # help_text = {
        #     "title": "this is title labe",
        #     #"slug": "This is slug"
        # }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            
            # 'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog content'})
        }
        error_messages = {
            # "title": {
            #     "max_length": "This title is too long.",
            #     "required": "The title field is required."
            # },
            #  "slug": {
            #     "max_length": "This title is too long.",
            #     "required": "The slug field is required.",
            #     #"unique": "The slug field must be unique."
            # },
        }

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        #self.fields["title"].widget = forms.Textarea()
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Blog content'})

        self.fields["title"].error_messages = {
                "max_length": "This title is too long.",
               #"required": "The title field is required."
            }
        # self.fields["slug"].error_messages = {
        #         "max_length": "This title is too long.",
        #         "required": "The slug field is required.",
        #         "unique": "The slug field must be unique."
        #     }

        for field in self.fields.values():
            field.error_messages = {
                'required': "{fieldname} is required".format(fieldname=field.label),
            }


SOME_CHOICES = [
        ('db-value', 'Display Value'),
        ('db-value2', 'Display Value2'),
        ('db-value3', 'Display Value3'),
    ]

# INTS_CHOICES = [tuple([x,x]) for x in range(0, 102)]

# YEARS = [x for x in range(1980, 2031)]

# class TestForm(forms.Form):
#     date_field = forms.DateField(initial="2010-11-20", widget=forms.SelectDateWidget(years=YEARS))
#     some_text = forms.CharField(label='Text', widget=forms.Textarea(attrs={"rows": 4, "cols": 10}))
#     choices = forms.CharField(label='Text', widget=forms.Select(choices=SOME_CHOICES))
#     boolean = forms.BooleanField()
#     integer = forms.IntegerField(initial=101, widget=forms.Select(choices=INTS_CHOICES))
#     email = forms.EmailField(min_length=10)

#     def __init__(self, user=None, *args, **kwargs):
#         super(TestForm, self).__init__(*args, **kwargs)
#         #print(user)
#         if user:
#             self.fields["some_text"].initial = user.username

#     def clean_integer(self, *args, **kwargs):
#         integer = self.cleaned_data.get("integer")
#         if integer < 10:
#             raise forms.ValidationError("The integer must be greater than 10")
#         return integer

#     def clean_some_text(self, *args, **kwargs):
#         some_text = self.cleaned_data.get("some_text")
#         if len(some_text) < 5:
#             raise forms.ValidationError("Ensure the text is greater than 5 characters")
#         return some_text

# class UserBlogsForm(forms.ModelForm):
#   class Meta:
#       model = UserBlogs
#       fields = [
#           'title',
#           'content'
#       ]


class UserLoginForm(forms.Form):
    query =forms.CharField(label='Username / Email', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username or Email'}))
    # , validators=[RegexValidator(
    #                                       regex = USERNAME_REGEX,
    #                                       message= 'Username must be Alphanumeric or must contain any of the following:". @ + -"',
    #                                       code = 'invalid username'
                                            
    #                                   )]
    password=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))


    def clean(self, *args, **kwargs):
        query=self.cleaned_data.get("query")
        password=self.cleaned_data.get("password")

        # the_user = authenticate(username=username_a, password=password_a)
        # if not the_user:
        #   raise forms.ValidationError("invalid credentials")

        #user_qs1 = User.objects.filter(username__iexact=query)
        #user_qs2 = User.objects.filter(email__iexact=query)
        #user_qs_final = (user_qs1 | user_qs2).distinct()

        user_qs_final = User.objects.filter(
                Q(username__iexact=query)|
                Q(email__iexact=query)

            ).distinct()
        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError("invalid credentials")

    #   user_obj = User.objects.filter(username=query).first()
        user_obj = user_qs_final.first()
        # if not user_obj:
        #   raise forms.ValidationError("invalid credentials")
        # else:
        if not user_obj.check_password(password):
            
            raise forms.ValidationError("invalid password")
        #if not user_obj.is_active:
        #       raise forms.ValidationError("inactive user. please verify your email address")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)



    # def clean_username(self):
    #   username=self.cleaned_data.get("username")
    #   user_qs = User.objects.filter(username=username)
    #   user_exists = user_qs.exists()
    #   if not user_exists and user_qs !=1:
    #       raise forms.ValidationError("invalid credentials")
    #   return username


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(min_length=6,label='Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email' )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email'})
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
       # user.is_active = False
        #create a new user hash for activating email

        if commit:
            user.save()
        return user

    

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
