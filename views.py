from flask import Flask, render_template, redirect, url_for, request, make_response
from itsdangerous import Signer

app = Flask(__name__)

@app.route("/")         #Adresin nerede olduğunu belirtir burası anasayfa
def definition():
    signer = Signer("secret key")                   #cookie koruma
    signed_name = request.cookies.get('name')
    try:
        name = signer.unsign(signed_name).decode()
        print('name' ,name)
    except BadSignature:
        print("bad signature")

    response = make_response("<html><body><h1>İlk Flask Denemesi</h1></body></html>")
    response.set_cookie('name',signed_name)
    return response

@app.route("/hello")    #burası hello sayfası
def Hello():
    return render_template("hello.html")    #html dosyasını getirir

@app.route("/helloAdmin")
def HelloAdmin():
    return render_template("helloAdmin.html")

@app.route("/helloUser/<name>")        # ./<name> kısmı parametre olarak gider yani değişkendir
def HelloUser(name):                   # fonksiyona parametre olarak gönderdik ki değişkene atansın
    if name.lower() == "admin":
        return redirect(url_for("HelloAdmin"))
    return render_template("helloUser.html " , username=name )  #değişkeni html dosyasına gönderme

@app.route("/add/<int:number1>/<int:number2>")
def Add(number1, number2):
    calculationResult = number1 + number2
    return render_template("add.html", number1 = number1 , number2 = number2, result = calculationResult)

@app.route("/login" , methods=['POST' , 'GET'])
def Login():
    if request.method == 'POST':

        username = request.form["username"]
        return redirect(url_for("HelloUser",name=username))

    else:
        return render_template("login.html")

@app.route("/student")
def Student():
    return render_template("student.html ")

@app.route("/result", methods=['POST'])
def Result():
    ContextData = {
    'name' : request.form.get("name"),
    'matematik' : request.form.get("matematik"),
    'fizik' : request.form.get("fizik"),
    'kimya' : request.form.get("kimya")
    }
    return render_template("studentResult.html" , **ContextData)