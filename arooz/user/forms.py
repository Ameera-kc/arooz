from django import forms
from django.forms.widgets import TextInput, EmailInput, Textarea
from user.models import Login


# class LoginRegister(forms.ModelForm):
#     class Meta:
#         model = Login
#         fields = ('customer_name', 'phone_number', 'email', 'address')
#         widgets= {
#             'customer_name':TextInput(attrs={'class':'form-control','name':'customer_name','placeholder':'Full Name','required':'required','autocomplete':'off',}),
#             'password':TextInput(attrs={'class':'form-control','name':'customer_name','placeholder':'Full Name','required':'required','autocomplete':'off',}),
#             'phone_number':TextInput(attrs={'class':'form-control','name':'phone_number','placeholder':'Phone Number','required':'required','autocomplete':'off',}),
#             'email': EmailInput(attrs={'class':'form-control','name':'email','placeholder':'Email','required':'required','autocomplete':'off',}),
#             'address':Textarea(attrs={'class':'form-control','name':'address','placeholder':'Full Address','required':'required','autocomplete':'off',}),
#        }
   


