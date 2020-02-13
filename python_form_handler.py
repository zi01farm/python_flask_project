import cgi

form = cgi.FieldStorage()
value = form.getvalue("foodName")

print(value)