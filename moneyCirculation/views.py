from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Reports
from users.models import Wallet
from datetime import datetime

'''
Function Lists:
0. wallet_update :
1. category_get :
2. request_get :
3. request_create :
4. request_update :
5. request_delete :
6. statistic :
'''


def wallet_update(owner, change):
    '''Update wallet every time report added, updated and deleted'''
    wallet = Wallet.objects.get(owner=owner)
    wallet.total += change
    wallet.save()
    return


def category_get(request):
    '''GET method for category'''
    query = request.GET.get('q', '')
    picked_category = Category.objects.filter(name__contains=query)

    result = {
        'data': [cat.serialize for cat in picked_category],
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})


def reports_get(request):
    '''GET method for reports'''
    max_obj = int(request.GET.get('max', '25'))
    query = request.GET.get('q', '')
    username = request.GET.get('u', 'anonymous')
    page = int(request.GET.get('page', '1'))
    page -= 1
    start = 0 + (max_obj*page)
    end = max_obj + (max_obj*page)

    # get query
    picked_reports = Reports.objects.filter(owner__username=username, category__name__contains=query).order_by('-transactionDate', '-id')[start:end]
    obj_count = Reports.objects.filter(owner__username=username, category__name__contains=query).count()

    page_count = obj_count // max_obj

    result = {
        'data': [rep.serialize for rep in picked_reports],
        'pages': page_count + 1,
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})


def reports_create(request):
    '''POST method for reports'''
    # if request is GET, return nothing
    if request.method == "GET":
        result = {
            'data': [],
            'status': 0,
            'info': 'request cannot be processed'
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    # check if category already exists, if not create new one
    try:
        category = Category.objects.get(name=request.POST.get('category').lower())
    except Exception:
        category = None

    if not category:
        new_category = Category(name=request.POST.get('category').lower())
        new_category.save()
        category = new_category

    # make new report
    # get user first
    username = request.POST.get('u', 'anonymous')
    owner = User.objects.get(username=username)

    # abort report addition if anonymous reports already exceeding 1500 objects
    if username == "anonymous" and Reports.objects.filter(owner=owner).count() > 1500:
        result = {
            'data': [],
            'status': 0,
            'info': 'Already Exceeding Maximum amount for Anonymous'
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    amount = int(request.POST.get('amount'))
    isExpense = True if request.POST.get('isExpense') == 'true' else False
    transactionDate = datetime.strptime(request.POST.get('transactionDate'), '%d %m %Y').date()

    new_report = Reports(
            amount=amount,
            isExpense=isExpense,
            transactionDate=transactionDate,
            owner=owner,
            category=category)
    new_report.save()

    # updating wallet
    change = (-1)**new_report.isExpense * new_report.amount
    wallet_update(owner=owner, change=change)

    print("Adding New Report")

    result = {
        'data': new_report.serialize,
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})


def reports_update(request):
    '''UPDATE/PUT method for reports'''
    # if request is GET, return nothing
    if request.method == "GET":
        # check if the id is exists
        try:
            report_id = int(request.GET.get("id"))
            picked_report = Reports.objects.get(id=report_id)
        except Exception as e:
            result = {
                'data': [],
                'status': 0,
                'info': f"{e}"
            }
            return JsonResponse(result, json_dumps_params={'indent': 2})

        # return the data only if the owner of the report is the same as request.user
        if picked_report.owner == request.user or picked_report.owner.username == 'anonymous':
            result = {
                'data': picked_report.serialize,
                'status': 1,
                'info': 'success getting data'
            }
        else:
            result = {
                'data': [],
                'status': 0,
                'info': "not allowed to view data"
            }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    # try getting the report first, if not exist return nothing
    try:
        report_id = int(request.POST.get("id"))
        picked_report = Reports.objects.get(id=report_id)
    except Exception as e:
        result = {
            'data': [],
            'status': 0,
            'info': f"{e}"
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    # change the table row according to the sent data
    if 'category' in request.POST:
        # check if category exists, else make new one
        try:
            category = Category.objects.get(name=request.POST.get('category').lower())
        except Exception:
            category = None

        if not category:
            new_category = Category(name=request.POST.get('category').lower())
            new_category.save()
            category = new_category
        picked_report.category = category

    if 'transactionDate' in request.POST:
        picked_report.transactionDate = datetime.strptime(request.POST.get('transactionDate'), '%d %m %Y').date()

    if 'amount' in request.POST:
        old_amount = picked_report.amount
        new_amount = int(request.POST.get('amount'))
        picked_report.amount = new_amount

        # updating wallet
        wallet_update(owner=picked_report.owner, change=new_amount-old_amount)

    if 'isExpense' in request.POST:
        picked_report.isExpense = True if request.POST.get('isExpense') == 'true' else False

    picked_report.save()

    print(f"Updating Report {picked_report.id}")

    # updating wallet
    change = (-1)**picked_report.isExpense * picked_report.amount
    wallet_update(owner=picked_report.owner, change=change)

    result = {
        'data': picked_report.serialize,
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})


def reports_delete(request):
    '''DELETE method for reports'''
    # if request is GET, return nothing
    if request.method == "GET":
        result = {
            'data': [],
            'status': 0,
            'info': "request cannot be processed"
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    # try to get the report first, if not exist return nothing
    try:
        report_id = int(request.POST.get("id"))
        picked_report = Reports.objects.get(id=report_id)
    except Exception as e:
        result = {
            'data': [],
            'status': 0,
            'info': f"{e}"
        }
        return JsonResponse(result, json_dumps_params={'indent': 2})

    # updating wallet first
    change = -(-1)**picked_report.isExpense * picked_report.amount
    wallet_update(owner=picked_report.owner, change=change)

    # deleting report
    picked_report.delete()

    print("Deleting New Report")

    result = {
        'data': [],
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})


def statistic(request):
    '''GET method for statistic data'''
    # get default month-year
    today = timezone.now().date()
    month = request.GET.get('month', today.month)
    year = request.GET.get('year', today.year)
    print(f"year : {year}, month : {month}")

    # get users data
    username = request.GET.get('u', 'anonymous')
    picked_reports = Reports.objects.filter(transactionDate__month=month, transactionDate__year=year, owner__username=username)

    summary = {}
    for report in picked_reports:
        if report.category.name not in summary:
            summary[report.category.name] = (-1)**report.isExpense * report.amount
        else:
            summary[report.category.name] += (-1)**report.isExpense * report.amount

    result = {
        'data': summary,
        'query': {
            'month': month,
            'year': year
        },
        'status': 1,
        'info': 'success'
    }
    return JsonResponse(result, json_dumps_params={'indent': 2})
