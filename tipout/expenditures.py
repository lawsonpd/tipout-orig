from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.utils.timezone import now
from django.core.cache import cache
from django.views.decorators.cache import cache_control
from string import strip

from tipout.models import Employee, Expenditure, EnterExpenditureForm, EditExpenditureForm
from tipout.budget_utils import update_budgets
from custom_auth.models import TipoutUser

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def enter_expenditure(request):
    '''
    If POST, admit and process form. Otherwise, show blank form.
    '''
    if request.method == 'POST':
        form = EnterExpenditureForm(request.POST)
        if form.is_valid():
            # process form data
            u = TipoutUser.objects.get(email=request.user)
            emp = Employee.objects.get(user=u)
            exp_data = form.cleaned_data

            expends = cache.get('expends')
            if not expends:
                expends = Expenditure.objects.filter(owner=emp)
                cache.set('expends', expends)

            dupe = expends.filter(
                       date=exp_data['date']
                   ).filter(
                       note=exp_data['note'].lower()
                   )
            if dupe:
                return render(request,
                              'enter_expenditure.html',
                              {'form': EnterExpenditureForm(initial={'date': exp_data['date']}),
                               'error_message': 'An expenditure for today with that note already exists.'}
                              )
            else:
                e = Expenditure(owner=emp, cost=exp_data['cost'], date=exp_data['date'], note=exp_data['note'])
                e.save()

                expends = Expenditure.objects.filter(owner=emp)
                cache.set('expends', expends)

                if e.date < now().date():
                    update_budgets(emp, e.date)

                return redirect('/budget/')
    else:
        return render(request,
                      'enter_expenditure.html',
                      {'form': EnterExpenditureForm(initial={'date': now().date()})}
                      )

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET'])
def expenditures(request):
    '''
    Default expenditures page show TODAY'S expenditures.
    '''
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    today_expends = cache.get('today_expends')
    if not today_expends:
        today_expends = Expenditure.objects.filter(owner=emp, date=now().date())
        cache.set('today_expends', today_expends)

    return render(request, 'expenditures.html', {'exps': today_expends})

# @login_required(login_url='/login/')
# @require_http_methods(['POST'])
# def delete_expenditure(request, *args):
#     exp = args[0].replace('-', ' ')
#
#     if request.method == 'POST':
#         u = TipoutUser.objects.get(email=request.user)
#         emp = Employee.objects.get(user=u)
#
#         es = Expenditure.objects.filter(owner=emp).filter(date=now().date())
#         for exp in es:
#             if strip(exp.get_absolute_url(), '/') == args[0]:
#                 e = exp
#         e.delete()
#         return redirect('/expenditures/')

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['POST'])
def delete_expenditure(request, exp, *args):
    if request.method == 'POST':
        u = TipoutUser.objects.get(email=request.user)
        emp = Employee.objects.get(user=u)

        expends = cache.get('expends')
        if not expends:
            expends = Expenditure.objects.filter(owner=emp)
            cache.set('expends', expends)

        exp_to_delete = expends.get(pk=exp)
        # for exp in es:
        #     if strip(exp.get_absolute_url(), '/') == args[0]:
        #         e = exp
        exp_to_delete.delete()

        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

        if exp_to_delete.date < now().date():
            update_budgets(emp, exp_to_delete.date)

        return redirect('/expenditures')

# To edit an expenditure, you'll have to use pk to identify it, since the note and amount could change.
# This would effectively be deleting an expenditure and creating a new one, which might be enough anyway.
#
@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def edit_expenditure(request, exp, *args):
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    exp_to_edit = expends.get(pk=exp)

    if request.method == 'POST':
        form = EditExpenditureForm(request.POST)
        if form.is_valid():
            exp_data = form.cleaned_data

            exp_to_edit.cost = exp_data['cost']
            exp_to_edit.note = exp_data['note']
            exp_to_edit.date = exp_data['date']
            exp_to_edit.save()

            expends = Expenditure.objects.filter(owner=emp)
            cache.set('expends', expends)

            if exp_to_edit.date < now().date():
                update_budgets(emp, exp_to_edit.date)

            return redirect('/expenditures/')
    else:
        form = EditExpenditureForm(initial={'note': exp_to_edit.note,
                                            'cost': exp_to_edit.cost,
                                            'date': exp_to_edit.date
                                           }
                                  )
        return render(request, 'edit_expenditure.html', {'form': form, 'exp': exp_to_edit})

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET'])
def expenditures_archive(request, *args):
    '''
    Shows a list of years
    '''
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    all_years = [e.date.year for e in expends]
    years = set(all_years)
    return render(request, 'expenditures_archive.html', {'years': years})

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET'])
def expenditures_year_archive(request, year, *args):
    '''
    Shows a list of months
    '''
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    # all_months = [e.month_name for e in Expenditure.objects.filter(owner=u)
    #                            if e.date.year == year]
    # months = set(all_months)
    dates = expends.filter(date__year=year).dates('date', 'month')
    months = [date.month for date in dates]
    return render(request, 'expenditures_archive.html', {'year': year,
                                                         'months': months})

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET'])
def expenditures_month_archive(request, year, month, *args):
    '''
    Shows a list of days
    '''
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    dates = expends.filter(date__year=year,
                           date__month=month).dates('date', 'day')
    days = [date.day for date in dates]
    return render(request, 'expenditures_archive.html', {'year': year,
                                                         'month': month,
                                                         'days': days})

@cache_control(private=True)
@login_required(login_url='/login/')
def expenditures_day_archive(request, year, month, day, *args):
    '''
    Shows a list of expenditures
    '''
    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    day_expends = expends.filter(date__year=year,
                                 date__month=month,
                                 date__day=day)
    # expends_notes = [date.note for exp in expends]
    return render(request, 'expenditures_archive.html', {'year': year,
                                                         'month': month,
                                                         'day': day,
                                                         'exps': day_expends})

@cache_control(private=True)
@login_required(login_url='/login/')
def expenditure_detail(request, year, month, day, exp, *args):
    '''
    Shows details about a particular expenditure
    '''
    exp_note = exp.replace('-', ' ')

    u = TipoutUser.objects.get(email=request.user)
    emp = Employee.objects.get(user=u)

    expends = cache.get('expends')
    if not expends:
        expends = Expenditure.objects.filter(owner=emp)
        cache.set('expends', expends)

    exp = expends.get(date__year=year,
                      date__month=month,
                      date__day=day,
                      note=exp_note)
    return render(request, 'expenditures_archive.html', {'year': year,
                                                         'month': month,
                                                         'day': day,
                                                         'exp': exp})
