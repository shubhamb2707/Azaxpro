from django import forms
from .models import User

CHOICES =( 
    ("student", "student"), 
    ("teacher", "teacher"),
)


class UserForm(forms.Form):
	username = forms.CharField(
		required = True,
		label = 'Username',
		max_length = 32
	)
	
	email = forms.CharField(
		required = True,
		label = 'Email',
		max_length = 32,
		widget = forms.EmailInput()
	)
	
	password = forms.CharField(
		required = True,
		label = 'Password',
		max_length = 32,
		widget = forms.PasswordInput()
	)
	
	first_name = forms.CharField(
		required = True,
		label = 'First_name',
		max_length = 32
	)
	
	last_name = forms.CharField(
		required = True,
		label = 'Last_name',
		max_length = 32
	)
	
	UserField = forms.ChoiceField(
		label= "UserField",
		choices = CHOICES,
		widget = forms.Select()
		)
    


	# class Meta:
	# 	model = User
	# 	fields = ["username","first_name","last_name","password","email","UserField"]
	
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)