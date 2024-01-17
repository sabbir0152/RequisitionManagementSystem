from django import forms
from .models import Requisition ,Issue, StoreBalance, Purchase, Transaction, ProductList,DepartmentList
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Report

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class UpdateCredentialsForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter your current password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter a new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm the new password'

    class Meta:
        model = User
        fields = []


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'department', 'designation', 'join_date', 'dob', 'blood_group', 'phone_number', 'primary_email', 'secondary_email', 'photo']



class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        exclude = ['approval_role', 'approval_status']
        fields = '__all__'
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['item_details', 'brand_name', 'unit', 'requisition_qty', 'requisition_date']



class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'

class StoreBalanceForm(forms.ModelForm):
    class Meta:
        model = StoreBalance
        fields = '__all__'

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class ProductListForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = '__all__'
from django import forms
from .models import Approval


class ApprovalForm(forms.ModelForm):
   

    class Meta:
        model = Approval
        fields = ['username','requisition_no', 'approval_role', 'status', 'remark']
from django import forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=[('ADMINISTRATION', 'Administration'),
        ('DEPARTMENT_HEAD', 'Department Head'),
        ('STORE_EXECUTIVE', 'Store Executive'),
        ('NORMAL_USER', 'Normal User'),])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['user_type'].widget.attrs.update({'placeholder': 'User Type'})

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        # Additional validation or processing logic for user_type if needed
        return cleaned_data
class DeparmentListForm(forms.ModelForm):
    class Meta:
        model = DepartmentList
        fields = '__all__'
