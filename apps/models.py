from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMINISTRATION', 'Administration'),
        ('DEPARTMENT_HEAD', 'Department Head'),
        ('STORE_EXECUTIVE', 'Store Executive'),
        ('NORMAL_USER', 'Normal User'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    plain_text_password = models.CharField(max_length=128, blank=True)
    full_name = models.CharField(max_length=100,default='')
    department = models.CharField(max_length=100,default='')
    designation = models.CharField(max_length=100,default='')
    join_date = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10,default='Unknown')
    phone_number = models.CharField(max_length=20,default='')
    primary_email = models.EmailField(blank=True, null=True)
    secondary_email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)

    def set_password(self, raw_password):
        self.plain_text_password = raw_password
        super().set_password(raw_password)

    def __str__(self):
        return self.user_type

class Requisition(models.Model):
    user_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    requisition_date = models.DateField(default=datetime.today())
    requisition_no = models.AutoField(primary_key=True)
    remark = models.TextField(blank=True)
    role_choices=(
        ('Department Head','Department Head'),
        ('Store Executive','Store Executive'),
         ('Administration','Administration'),
    )
    approval_role = models.CharField(max_length=100, choices=role_choices, default='Department Head')


    APPROVAL_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='PENDING')



    def __str__(self):
        return str(self.requisition_no)

class Report(models.Model):
    requisition_no = models.ForeignKey(Requisition, on_delete=models.CASCADE, to_field='requisition_no')
    item_details = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    requisition_qty = models.IntegerField()
    requisition_date = models.DateField()

    def __str__(self):
        return self.item_details

class Workorder(models.Model):
    workorder_no = models.AutoField(primary_key=True)
    requisition = models.CharField(max_length=100)
    approval_status = models.CharField(max_length=100)
    date = models.DateField()
    

class Issue(models.Model):
    user_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    issue_no = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    trans_date=models.DateField(default=datetime.today())
    quantity = models.IntegerField()
    status=models.CharField(max_length=100,default='Initialise')
    remark = models.TextField()
    def __str__(self):
        return self.user_name


class StoreBalance(models.Model):
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField()
    remark = models.TextField()

class Purchase(models.Model):
    purchase_no = models.AutoField(primary_key=True)
    requisition = models.IntegerField()
    workorder = models.IntegerField()
    attach_file = models.FileField(upload_to='purchases/')

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField()
    department = models.CharField(max_length=100)
    material_name = models.CharField(max_length=100)
    transaction_date = models.DateField()
    quantity = models.IntegerField()

class ProductList(models.Model):
    material_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    def __str__(self):
        return self.material_name

from django.db import models

class Approval(models.Model):
    username=models.CharField(max_length=100,default="")
    APPROVAL_ROLES = (
        ('Department Head', 'Department Head'),
        ('Store Executive', 'Store Executive'),
        ('Administration', 'Administration'),
    )

    requisition_no = models.CharField(max_length=100)
    approval_role = models.CharField(max_length=50, choices=APPROVAL_ROLES)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    # Other fields...

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remark=models.CharField(max_length=100,default="")

    def __str__(self):
        return self.requisition_no

class DepartmentList(models.Model):
    department_name=models.CharField(max_length=100)
    def __str__(self):
        return self.department_name