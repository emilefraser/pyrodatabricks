dbutils.widgets.combobox(
  name='fruits_combobox',
  defaultValue='banana',
  choices=['apple', 'banana', 'coconut', 'dragon fruit'],
  label='Fruits'
)

print(dbutils.widgets.get("fruits_combobox"))

# banana