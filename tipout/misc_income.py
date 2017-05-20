from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now, timedelta
from django.core.cache import cache
from django.views.decorators.cache import cache_control

from tipout.models import OtherFunds, EnterOtherFundsForm, Employee, Balance

from custom_auth.models import TipoutUser

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def enter_other_funds(request):
	u = TipoutUser.objects.get(email=request.user)
	emp = Employee.objects.get(user=u)

	if request.method == 'POST':
		form = EnterOtherFundsForm(request.POST)
		if form.is_valid():
			other_funds_data = form.cleaned_data

			new_other_funds = OtherFunds.objects.create(owner=emp,
														amount=other_funds_data['amount'],
														date_earned=other_funds_data['date_earned'],
														note=other_funds_data['note']
			)

			balance = Balance.objects.get(owner=emp)
			balance.amount += new_other_funds.amount
			balance.save()

			return redirect('/other-funds/')
		else:
			return render(request, "There was an error.")

	else:
		form = EnterOtherFundsForm()
		return render(request, 'enter_other_funds.html', {'form': form})

@cache_control(private=True)
@login_required(login_url='/login/')
@require_http_methods(['GET'])
def other_funds(request):
	u = TipoutUser.objects.get(email=request.user)
	emp = Employee.objects.get(user=u)

	emp_other_funds = OtherFunds.objects.filter(owner=emp)

	return render(request, 'other_funds.html', {'other_funds': emp_other_funds})

