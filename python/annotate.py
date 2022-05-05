import datetime
from django.utils import timezone

from django.db import connection
from auctions.models import Bid, Auction
from payments.models import Transaction, Payment
from affiliate.models import AffiliateTransaction
from users.models import User
from slots.models import Ownership
from django.db.models import (Count, Sum, Value, IntegerField, F, Q)




class Report:

    def __init__(self, field_options):
        self.field_options = field_options

    def get_annotations(self, qs, result_field):
        for field in self.field_options:
            if field['result_field'] == result_field:
                qs = qs.annotate(
                    **{field['result_field']: field.get('result_func', Value(1, IntegerField()))}
                )
            else:
                qs = qs.annotate(
                    **{field['result_field']:Value(0, IntegerField())}
                )
            
        return qs

    def get_report(self, group_by=None, start_date=None, end_date=None):
        now = timezone.now().date()
        last_30_days = now - datetime.timedelta(30)
        start_date = start_date or last_30_days
        end_date = end_date or now
        group_by = group_by or 'day'
        result_fields = []
        querysets = []
        
        
        for field in self.field_options:
            result_fields.append(field['result_field'])

        fields = ['__date'] + result_fields

        for field in self.field_options:
            qs = field['model'].objects.filter(
                field.get('filters', Q()),
                **{field['date_field']+'__gte':start_date, 
                field['date_field']+'__lte':end_date}, 
            ).annotate(
                __date=F(field['date_field']),
            )
            qs = self.get_annotations(qs, field['result_field']).values(*fields)
            querysets.append(qs)

        result_fields_list = []
        for field_name in result_fields:
            result_fields_list.append(f'sum({field_name}) as {field_name}')
        sql_text = ",".join(result_fields_list)
        
    
        sql, params = querysets[0].union(*querysets[1:], all=True).query.sql_with_params()

        with connection.cursor() as cur:
            sql = f"""
            SELECT 
                DATE_TRUNC('{group_by}', "__date" AT TIME ZONE 'UTC') AS "{group_by}",
                {sql_text}
            FROM 
                ({sql})
            AS X
            GROUP BY {group_by}
            ORDER BY {group_by} DESC
            """
            cur.execute(sql, params)
            return cur.fetchall()
        

def get_daily_report(group_by, start_date, end_date):

    field_options = (
        {'model': User, 'result_field': 'users_count',
            'date_field': 'date_joined'},
        {'model': User, 'result_field': 'active_users_count', 'date_field': 'date_joined',
            'filters': Q(is_active=True)},
        {'model': Auction, 'result_field': 'start_auctions_count',
            'date_field': 'start_time'},
        {'model': Auction, 'result_field': 'won_auctions_count', 'date_field': 'start_time',
            'filters': Q(status=Auction.Status.WON)},
        {'model': Auction, 'result_field': 'lost_auctions_count', 'date_field': 'start_time',
            'filters': Q(status=Auction.Status.LOST)},
        {'model': Bid, 'result_field': 'bids_count',
            'date_field': 'created_at'},
        {'model': Bid, 'result_field': 'won_bids_count', 'date_field': 'created_at',
            'filters': Q(winner=True)},
        {'model': Transaction, 'result_field': 'sum_spending_default', 'date_field': 'created_at', 'result_func': F(
            'amount'), 'filters': Q(account_type=Transaction.AccountType.DEFAULT, amount__lt=0)},
        {'model': Transaction, 'result_field': 'sum_spending_bonus', 'date_field': 'created_at', 'result_func': F(
            'amount'), 'filters': Q(account_type=Transaction.AccountType.BONUS, amount__lt=0)},
        {'model': Payment, 'result_field': 'sum_replenish',
            'date_field': 'confirmed_at', 'result_func': F('amount')},
        {'model': AffiliateTransaction, 'result_field': 'sum_affiliate_replenish',
            'date_field': 'created_at', 'result_func': F('amount')},
        {'model': Ownership, 'result_field': 'sum_pending_slots', 'date_field': 'created_at',
            'filters': Q(status=Ownership.Status.PENDING)},
        {'model': Ownership, 'result_field': 'sum_setup_costs',
            'date_field': 'created_at', 'result_func': F('setup_costs'),
            'filters': Q(status=Ownership.Status.CONFIRMED)},
        {'model': Ownership, 'result_field': 'sum_setup_costs_pending',
            'date_field': 'created_at', 'result_func': F('setup_costs'),
            'filters': Q(status=Ownership.Status.PENDING)},
    )
    report = Report(field_options)
    daily_report = report.get_report(group_by, start_date, end_date)
    return daily_report


def get_affiliate_report(group_by, start_date, end_date, user_id):

    field_options = (
        {'model': User, 'result_field': 'invited_users_count',
            'date_field': 'date_joined', 'filters': Q(invited_by=user_id)},
        {'model': AffiliateTransaction, 'result_field': 'sum_affiliate_replenish',
            'date_field': 'created_at', 'result_func': F('amount'), 'filters': Q(user=user_id)},
        {'model': AffiliateTransaction, 'result_field': 'sum_affiliate_replenish_credited',
            'date_field': 'credited_at', 'result_func': F('amount'), 'filters': Q(user=user_id)},
        {'model': Transaction, 'result_field': 'sum_spending_default', 'date_field': 'created_at', 'result_func': F(
            'amount'), 'filters': Q(user__invited_by=user_id, account_type=Transaction.AccountType.DEFAULT, amount__lt=0)},
        {'model': Transaction, 'result_field': 'sum_spending_bonus', 'date_field': 'created_at', 'result_func': F(
            'amount'), 'filters': Q(user__invited_by=user_id, account_type=Transaction.AccountType.BONUS, amount__lt=0)},
        {'model': Payment, 'result_field': 'sum_replenish',
            'date_field': 'confirmed_at', 'result_func': F('amount'), 'filters': Q(user__invited_by=user_id)},
        {'model': Ownership, 'result_field': 'sum_setup_costs',
            'date_field': 'created_at', 'result_func': F('setup_costs'),
            'filters': Q(user__invited_by=user_id, status=Ownership.Status.CONFIRMED)},
    )
    report = Report(field_options)
    affiliate_report = report.get_report(group_by, start_date, end_date)
    return affiliate_report