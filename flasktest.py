from flask import Flask, request, redirect, url_for  
    
app = Flask(__name__)  
   
@app.route('/')  
def index():  
    return redirect(url_for('username'), code=302)    # URL跳转，默认代码是302，可以省略  
   
@app.route('/username', methods=['GET', 'POST'])  
def username():  
    HTML = '''<!DOCTYPE HTML> 
<html> 
<head> 
    <meta charset="utf-8"/> 
    <title>Flask POST方法演示</title>
</head> 
<body> 
{} 
<form action="" method="POST"> 
    <p>username</p>
    <input type="text" name="username" value="" /> 
    <p>password</p>
    <input type="text" name="password" value="" />
    <input type="submit" name="enter" value="enter" /> 
</form> 
   
</body> 
</html>'''
    if request.method == 'GET':  
        return HTML.format('')  
    elif request.method == 'POST':  
        if request.form['username']:  
            name = request.form['username']  
            pwd = request.form["password"]
            fp = open('txt.txt','a')  
            fp.write('username:'+name+'\n')  
            fp.write('password:'+pwd+'\n')
            fp.close()  
            if name=='admin' and pwd=='password':
                return HTML.format('<p>Welcome <strong>{}</strong>!</p>'.format(name))
                # return HTML.format('<p>Your name is <strong>{}</strong></p>'.format(name))  
            else:
                return HTML.format('<p>Username or password error!</p>')
        else:  
            return redirect(url_for('username'))  
    
if __name__ == '__main__':  
    app.run()  