from django.db.models.sql.datastructures import Join
from django.db.models.fields.related import ForeignObject
from django.db.models.options import Options

from practice_app.models import Customer
from practice_app.models import CustomerInfo
from practice_app.models import CustomerHistory

join_field = ForeignObject(
    to=Customer,
    on_delete=lambda: x,
    from_fields=[None],
    to_fields=[None],
    rel=None,
    related_name=None
)

join_field.opts = Options(CustomerInfo._mata)
join_field.opts.model = CustomerInfo
join_field.get_joining_columns = lambda: (("customer_id", "customer_id"))

join = Join(
    table_name=Customer._meta.db_table,
    parent_alias=CustomerInfo._meta.db_table,
    table_alias='CI',
    join_type="INNER",
    join_field=join_field,
    nullable=False
)

q = CustomerInfo.objects.values()
q = q.extra(select={'customer': 'customer.name'})
q.query.join(join)
obj = list(q)


