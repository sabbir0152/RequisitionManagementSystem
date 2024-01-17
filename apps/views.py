from django.shortcuts import render, redirect
from .forms import RequisitionForm, IssueForm, StoreBalanceForm, PurchaseForm, TransactionForm, ProductListForm
from .models import Requisition,  Issue, StoreBalance, Purchase, Transaction, ProductList,Workorder
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Requisition
from .models import Requisition, Report,DepartmentList,CustomUser
from .forms import ReportForm
import easygui

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = form.cleaned_data.get('user_type')
            #user1 = CustomUser.objects.get(username=username)
            user = authenticate(request, username=username, password=password,user_type=user_type)
          
            if user is not None:
                login(request, user)
                # Additional logic based on user_type
                if user_type == 'DEPARTMENT_HEAD':
                    return redirect('department_head')
                elif user_type == 'NORMAL_USER':
                    return redirect('home_page')
                elif user_type == 'STORE_EXECUTIVE':
                    return redirect('store_executive')
                elif user_type == 'ADMINISTRATION':
                    return redirect('administrations')
        else:
            easygui.msgbox('Your Credentials are incorrect. Please Give Correct Username or password or usertype.', 'Fail')
    else:
        form = CustomLoginForm(request)
    return render(request, 'login.html', {'form': form})
 # Redirect to the home page or any other desired URL

  



from django.urls import reverse
def home_page(request):
    username = request.user.username
    issues = Issue.objects.filter(user_name=username,status='Approved')
    create_requisition_url = reverse('create_requisition')
    requisition_list_url = reverse('requisition_list',args=[username])
    workorder_list_url = reverse('workorder_list')
    store_balance_url=reverse('store_balance_list')
    return render(request, 'homepage.html', {
        'username': username,
        'create_requisition_url': create_requisition_url,
        'requisition_list_url': requisition_list_url,
        'workorder_list_url': workorder_list_url,
        'issues': issues,
        'store_balance_url':store_balance_url,
    })
def accept_issue(request, issue_id):
    issue = Issue.objects.get(issue_no=issue_id)
    issue.status = 'Accepted'
    issue.notification_status = True
    issue.save()
    issues2 = Issue.objects.filter(status="Accepted") 
    for i in issues2:
            sb= StoreBalance.objects.filter(product_name=i.product_name)
            for j in sb:
                j.quantity=j.quantity-i.quantity
                j.save()

    return redirect('home_page')
    # ... handle the necessary operations after accepting the issue ...


def reject_issue(request, issue_id):
    issue = Issue.objects.get(issue_no=issue_id)
    issue.status = 'Rejected'
    issue.notification_status = True
    issue.save()
    return redirect('home_page')
    # ... handle the necessary operations after rejecting the issue ...

def create_requisition(request):
    deparment_list=DepartmentList.objects.all()
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            requisition = form.save(commit=False)
            requisition.approval_status = 'PENDING'
            requisition.save()
            easygui.msgbox('Successfully Create Requisition', 'Success')
            return redirect('create_requisition')
        else:
            print(form.errors)
    else:
        form = RequisitionForm()
    return render(request, 'create_requisition.html', {'form': form,'department_list':deparment_list})


def report_view(request, requisition_no):
    product_list = ProductList.objects.all()
    
    report = Report.objects.filter(requisition_no=requisition_no)
    dh = Approval.objects.filter(requisition_no=requisition_no ,approval_role='Department Head')
    se = Approval.objects.filter(requisition_no=requisition_no ,approval_role='Store Executive')
    adm = Approval.objects.filter(requisition_no=requisition_no ,approval_role='Administration')
    req=Requisition.objects.get(requisition_no=requisition_no)
    return render(request, 'report.html', {'requisition_no': requisition_no,'product_list': product_list,'adm':adm,"req":req,'report':report,'dh':dh,'se':se})


def add_report(request, requisition_no):
    requisition = Requisition.objects.get(requisition_no=requisition_no)
    product_list = ProductList.objects.all()
   
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.requisition_no = requisition
            report.requisition_date = requisition.requisition_date
            report.save()
            return redirect('report', requisition_no=requisition_no)
        else:
            print(form.errors)
    else:
        form = ReportForm()
    
    return render(request, 'report.html', {'form': form, 'requisition': requisition, 'product_list': product_list, 'requisition_no': requisition_no})





from django.shortcuts import render, redirect
from .models import Approval
from .forms import ApprovalForm
from django.core.exceptions import ObjectDoesNotExist

def update_status(requisition_id):
    try:
        requisition = Requisition.objects.get(requisition_no=requisition_id)
    except Requisition.DoesNotExist:
        # Handle the case where the Requisition object does not exist
        return

    approvals = Approval.objects.filter(requisition_no=requisition_id)
    if approvals:
        for approval in approvals:
            requisition.approval_status = approval.status
            requisition.approval_role = approval.approval_role
            requisition.remark = approval.remark

        requisition.save()  # Save the updated fields after the loop
    else:
        # Handle the case where no approvals are found
        pass



    


def department_head(request):
    username=request.user.username
    requisitions = Requisition.objects.filter(approval_status="PENDING")
    
    form = ApprovalForm()
    return render(request, 'department_head.html', {'requisitions': requisitions, 'form': form,'username':username})


def update_approval_status(request):
    
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if request.method == 'POST':
            requisition_id = request.POST.get('requisition_no')
            requisition = Requisition.objects.get(requisition_no=requisition_id)
            status = request.POST.get('status') 
            remark=request.POST.get('remark')
            approval_role=request.POST.get('approval_role') 
            requisition.approval_status=status.upper()
            requisition.approval_role=approval_role
            requisition.remark=remark
            requisition.save()
        if form.is_valid():
            requisition_id = request.POST.get('requisition_no')
            approval = form.save(commit=False)
            approval.requisition_no= requisition_id
            approval.save()
            #update_status(requisition_id)
            return redirect('department_head')
        else:
            print(form.errors)
    else:
        form = ApprovalForm()

    requisitions = Requisition.objects.all()
    
    return render(request, 'department_head.html', {'requisitions': requisitions, 'form': form})
def store_executive(request):
    username = request.user.get_username()
    requisitions1 = Requisition.objects.filter(approval_status="APPROVED",approval_role="Store Executive")
    if len(requisitions1)==0:
        requisitions = Requisition.objects.filter(approval_status="APPROVED",approval_role="Department Head")
    else:
        requisitions=[]
    form = ApprovalForm()
    return render(request, 'store_executive.html', {'requisitions': requisitions, 'form': form,'username':username})


def update_approval_status2(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if request.method == 'POST':
            requisition_id = request.POST.get('requisition_no')
            requisition = Requisition.objects.get(requisition_no=requisition_id)
            status = request.POST.get('status') 
            remark=request.POST.get('remark')
            approval_role=request.POST.get('approval_role') 
            requisition.approval_status=status.upper()
            requisition.approval_role=approval_role
            requisition.remark=remark
            requisition.save()
        if form.is_valid():
            requisition_id = request.POST.get('requisition_no')
            approval = form.save(commit=False)
            approval.requisition_no= requisition_id
            approval.save()
            #update_status(requisition_id)
            return redirect('store_executive')
        else:
            print(form.errors)
    else:
        form = ApprovalForm()

    requisitions = Requisition.objects.all()
    
    return render(request, 'store_executive.html', {'requisitions': requisitions, 'form': form})

def administrations(request):
    username=request.user.username
    requisitions = Requisition.objects.filter(approval_status="APPROVED",approval_role="Store Executive")
    form = ApprovalForm()
    return render(request, 'administrations.html', {'requisitions': requisitions, 'form': form,'username':username})
def workorder(requisition_id):
    approvals = Approval.objects.filter(requisition_no=requisition_id,approval_role='Administration')
    requisition = Requisition.objects.get(requisition_no=requisition_id)
    
    for approval in approvals:
        if approval.status == 'Approved':
            workorder = Workorder.objects.create(
                requisition=requisition.requisition_no,
                approval_status=requisition.approval_status,
                date=requisition.requisition_date
            )
            workorder.save()

from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm

def update_profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
        else:
            print(form.errors)
            errors = form.errors
            return render(request, 'update_profile.html', {'form': form, 'errors': errors})
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'update_profile.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages

def update_credentials(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            easygui.msgbox('Your password has been changed successfully. Please log in again.', 'Success')
           
            return redirect('login_view')  # Redirect to the login page
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'update_credentials.html', {'form': form})



def profile_details(request):
    user = request.user
    return render(request, 'profile_details.html', {'user': user})




def update_approval_status3(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if request.method == 'POST':
            requisition_id = request.POST.get('requisition_no')
            requisition = Requisition.objects.get(requisition_no=requisition_id)
            status = request.POST.get('status') 
            remark=request.POST.get('remark')
            approval_role=request.POST.get('approval_role') 
            requisition.approval_status=status.upper()
            requisition.approval_role=approval_role
            requisition.remark=remark
            requisition.save()
        if form.is_valid():
            requisition_id = request.POST.get('requisition_no')
            approval = form.save(commit=False)
            approval.requisition_no= requisition_id
            approval.save()
            #update_status(requisition_id)
            workorder(requisition_id)
            return redirect('administrations')
        else:
            print(form.errors)
    else:
        form = ApprovalForm()

    requisitions = Requisition.objects.all()
    
    return render(request, 'administrations.html', {'requisitions': requisitions, 'form': form})









def workorder_list(request):
    workorders = Workorder.objects.all()
    requisition_no = request.GET.get('requisition_no')
    
   
    if requisition_no:
        workorders = Workorder.objects.filter(requisition=requisition_no)
    else:
        workorders = Workorder.objects.all()
    return render(request, 'workorder_list.html', {'workorders': workorders})




def create_issue(request):
    department_list = DepartmentList.objects.all()
    product_list = ProductList.objects.values_list('material_name', flat=True)  # Fetch only the material names

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            easygui.msgbox('Successfully Create Issue', 'Success')
            return redirect('create_issue')
        else:
            print(form.errors)
    else:
        form = IssueForm()

    return render(request, 'create_issue.html', {'form': form, 'department_list': department_list, 'product_list': product_list})

def notifications(request):
    st=Issue.objects.filter(status='Initialize')
    print(st)
    return render(request, 'notification.html', {'st': st})

def update_issue_status(request):
     if request.method == 'POST':
        issue_no = request.POST['issue_no']
        print("Issue No:", issue_no)
        status = request.POST.get('status')
        print("Status:", status)

        # Update the status field of the Issue object with the provided issue_no
        issue = Issue.objects.get(issue_no=issue_no)
        issue.status = status
        issue.save()
        
        return redirect('notifications')

    # Handle GET requests if needed



# def create_store_balance(request):
#     product_list = ProductList.objects.all()
#     if request.method == 'POST':
#         form = StoreBalanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('create_store_balance')
#     else:
#         form = StoreBalanceForm()
#     return render(request, 'create_store_balance.html', {'form': form,'product_list':product_list})


from django.shortcuts import render, redirect
from .forms import StoreBalanceForm
from .models import ProductList, StoreBalance

def create_store_balance(request):
    product_list = ProductList.objects.all()
    if request.method == 'POST':
        form = StoreBalanceForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            brand = form.cleaned_data['brand']
            quantity = form.cleaned_data['quantity']
            remark = form.cleaned_data['remark']
            
            store_balances = StoreBalance.objects.filter(product_name=product_name, brand=brand)
            
            if store_balances.exists():
                # If multiple StoreBalance objects exist, update the quantity of the first one
                store_balance = store_balances.first()
                store_balance.quantity += quantity
                store_balance.save()
            else:
                store_balance = StoreBalance(product_name=product_name, brand=brand, quantity=quantity, remark=remark)
                store_balance.save()
            
            return redirect('create_store_balance')
    else:
        form = StoreBalanceForm()
    return render(request, 'create_store_balance.html', {'form': form, 'product_list': product_list})



def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_purchase')
    else:
        form = PurchaseForm()
    return render(request, 'create_purchase.html', {'form': form})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})

def create_product_list(request):
    if request.method == 'POST':
        form = ProductListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list_list')
    else:
        form = ProductListForm()
    return render(request, 'create_product_list.html', {'form': form})

def requisition_list(request,username):
    
    requisition_number = request.GET.get('requisition_number')

    if requisition_number:
        requisitions = Requisition.objects.filter(requisition_no=requisition_number,user_name=username)
    else:
        requisitions = Requisition.objects.filter(user_name=username)
    return render(request, 'requisition_list.html', {'requisitions': requisitions})


def issue_list(request):
    username_filter = request.GET.get('username')
    if username_filter:
        issues = Issue.objects.filter(user_name=username_filter)
    else:
        issues = Issue.objects.filter(status="Accepted")
    
    return render(request, 'issue_list.html', {'issues': issues})

def store_balance_list(request):
    store_balances = StoreBalance.objects.all()
    return render(request, 'store_balance_list.html', {'store_balances': store_balances})

def purchase_list(request):
    requisition_no = request.GET.get('requisition')
    purchases = Purchase.objects.all()

    if requisition_no:
        purchases = purchases.filter(requisition=requisition_no)

    context = {
        'purchases': purchases
    }
    return render(request, 'purchase_list.html', context)

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})

def product_list_list(request):
    product_lists = ProductList.objects.all()
    return render(request, 'product_list_list.html', {'product_lists': product_lists})
