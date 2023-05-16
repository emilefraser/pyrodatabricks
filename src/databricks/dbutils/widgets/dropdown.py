dbutils.widgets.dropdown(
  name='toys_dropdown',
  defaultValue='basketball',
  choices=['alphabet blocks', 'basketball', 'cape', 'doll'],
  label='Toys'
)

print(dbutils.widgets.get("toys_dropdown"))

# basketball