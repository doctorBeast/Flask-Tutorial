# Problems while going through admin login.
# admin gets logged in but don't know how does the company loging takes place
# I think there is some problem with login_manager.login_view in __init__.py
# I will have to check how to create two login views possible.
# Also adminindex.html is unnecessary.

from my_app import app 

if __name__ == '__main__':
	app.run(host = '127.0.0.1' , port =5000 ,debug = True)