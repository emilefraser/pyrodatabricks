dbutils.widgets.multiselect(
  name='days_multiselect',
  defaultValue='Tuesday',
  choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'],
  label='Days of the Week'
)

print(dbutils.widgets.get("days_multiselect"))

# Tuesday