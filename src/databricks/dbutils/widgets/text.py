dbutils.widgets.text(
  name='your_name_text',
  defaultValue='Enter your name',
  label='Your name'
)

print(dbutils.widgets.get("your_name_text"))

# Enter your name