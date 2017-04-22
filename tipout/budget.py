from django.utils.timezone import now
from tipout.models import Paycheck
from decimal import Decimal

def avg_daily_tips_earned_initial(init_avg_daily_tips, tips_so_far, signup_date):
    '''
    This calculates what a user makes on average from tips *on the days they work*,
    so we're dividing by 21.3 assuming 21.3 work days per month.
    '''
    days_so_far = (now().date() - signup_date).days
    return (init_avg_daily_tips * Decimal((30 - days_so_far) * .71) + sum(tips_so_far)) / Decimal(21.3)

def avg_daily_tips_earned(tips):
    '''
    List -> Int
    '''
    # calculate tips for last 30 days
    if tips:
        return sum(tips) / 21.3
    else:
        return 0

def tips_available_per_day_initial(init_avg_daily_tips, tips_so_far, signup_date):
    '''
    This is what we want to use to calculate how much a user has *available* each day
    from their tips as part of their budget.
    We divide by 30 instead of 21.3 because we're not interested in how much they *make*
    on average each day they work, but instead how much they *have* daily based on
    the total amount earned.
    '''
    days_so_far = (now().date() - signup_date).days
    return (init_avg_daily_tips * Decimal((30 - days_so_far) * .71) + sum(tips_so_far)) / Decimal(30)

def tips_available_per_day(tips):
    '''
    This is what we want to use to calculate how much a user has *available* each day
    from their tips as part of their budget.
    We divide by 30 instead of 21.3 because we're not interested in how much they *make*
    on average each day they work, but instead how much they *have* daily based on
    the total amount earned.
    '''
    return sum(tips) / 30

def daily_avg_from_paycheck(paycheck_amts):
    # assuming paychecks are bi-weekly (2/mo)
    # return (sum(paycheck_amts) / len(paycheck_amts)) / 15
    # no need to do this ^
    # simply add up the paychecks from the last 30 days
    return sum(paycheck_amts) / 30

def avg_hourly_wage(tips, paychecks, num_days):
    # will need to call avg_daily_tips and daily_avg_from_paycheck
    #
    # hours from paychecks and hours from tips should be equal
    '''
    total_hours should really be hours in past num_days days
    '''
    total_hours = sum([ tip.hours_worked for tip in tips ])

    return ((avg_daily_tips(tips) + daily_avg_from_paycheck(paychecks)) * num_days) / total_hours

def pretty_dollar_amount(amount):
  '''
  This only works if amount is multiple of 100 (e.g. '500')
  '''
  return '$' + '{0:.2f}'.format(amount)
