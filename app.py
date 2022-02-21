from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
from werkzeug.utils import secure_filename
import urllib.request
import os
from datetime import datetime
import cv2
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pi'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# USER
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password'].encode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE Email=%s",(Email,))
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            if bcrypt.hashpw(Password, user[3].encode('utf-8')) == user[3].encode('utf-8'):
                session['Id_User'] = user[0]
                session['Nom'] = user[1]
                session['Email'] = user[2]
                session['Type'] = user[4]
                print(user[4])
                if session['Type']==1:
                    return render_template("homeAdmin.html")
                else:
                    return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")
@app.route('/facturation')
def fact():
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    Id_User = session['Id_User']
    cur.execute("SELECT * FROM price_pub INNER JOIN pub ON price_pub.Id_Pub = pub.Id_Pub WHERE pub.Id_User=%s", (Id_User,))
    data = cur.fetchall()
    cur1.execute("SELECT SUM(price_pub.total) FROM price_pub INNER JOIN pub ON price_pub.Id_Pub = pub.Id_Pub WHERE pub.Id_User=%s", (Id_User,))
    data1 = cur1.fetchall()
    i= len( str(data1[0]) ) - 2
    cur2.execute("SELECT * FROM user WHERE Id_User=%s", (Id_User,))
    data2 = cur2.fetchall()
    print(str(data1[0])[2:i])
    cur.close()
    return render_template("facturation.html", prices=data ,somme = str(data1[0])[2:i], users= data2)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        flash("Your Account Has Been Created Successfully")
        Nom = request.form['Nom']
        Email = request.form['Email']
        Password = request.form['Password'].encode('utf-8')
        hash_password = bcrypt.hashpw(Password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (Nom, Email, Password, Type) VALUES (%s,%s,%s,%s)",(Nom,Email,hash_password,0))
        mysql.connection.commit()
        session['Nom'] = request.form['Nom']
        session['Email'] = request.form['Email']
        return redirect(url_for('home'))


# PUB & RECLAMATION 
@app.route('/pubs')
def IndexPub():
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    Id_User = session['Id_User']
    cur.execute("SELECT * FROM pub WHERE Id_User=%s",(Id_User,))
    data = cur.fetchall()
    cur.close()
    cur1.execute("SELECT reclamation.Reponse AS Rep, pub.Id_Pub AS pub FROM reclamation INNER JOIN pub ON reclamation.Id_Pub = pub.Id_Pub WHERE pub.Id_User=%s", (Id_User,))
    data1 = cur1.fetchall()
    print(data1)
    cur1.close()
    return render_template('pub.html', pubs=data, recls=data1)


app.config["PUB_UPLOADS"] = 'C:/Users/Nour/Desktop/Builboard_Display/static'
ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg', 'gif' ,'jfif'])
ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'avi','mov']) 
  
def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE
def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        duree = 10  
        frequence = request.form['frequence']
        dateDebut1 = request.form['dateDebut']
        dateFin1 = request.form['dateFin']
        dateDebut = datetime.strptime(dateDebut1, '%Y-%m-%d')
        dateFin= datetime.strptime(dateFin1, '%Y-%m-%d')
        dateRecl = datetime.now()
        file = request.files['fileImage']
        if file and allowed_file_image(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PUB_UPLOADS'], filename))
            typeFile = "image"
            duree = request.form['duree']
        if file and allowed_file_video(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PUB_UPLOADS'], filename))
            typeFile = "video"
            cap = cv2.VideoCapture("C:/Users/Nour/Desktop/Builboard_Display/static/"+file.filename)
            fps = cap.get(cv2.CAP_PROP_FPS)      
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duree = frame_count/fps
            cap.release()
        prix = (float(duree)/60)*(int(frequence)*2500)
        daypub = dateFin - dateDebut
        
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        Id_User = session['Id_User']
        cur.execute("INSERT INTO pub (Duree, Frequence, Date_Debut, Date_Fin, Prix, Statut, File_Pub, Id_User,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
        (duree, frequence, dateDebut, dateFin, prix, 0, file.filename, Id_User, typeFile))
        idPub = cur.lastrowid
        somme = daypub * prix
        cur2.execute("INSERT INTO price_pub (Days,Price,Total,Id_Pub,Pub_Name) VALUES (%s,%s,%s,%s,%s)", (daypub,prix,somme,idPub,file.filename))
        cur1.execute("INSERT INTO reclamation (Reponse, Date_Recl, Id_Pub) VALUES (%s,%s,%s)", 
        ("Your claim is pending.", dateRecl, idPub))
        mysql.connection.commit()
        return redirect(url_for('IndexPub'))
    

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Pub Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur3 = mysql.connection.cursor()
    cur1.execute("SELECT File_Pub FROM pub WHERE Id_Pub=%s", (id_data,))
    data = cur1.fetchall()
    i= len( str(data[0]) ) - 3
    os.remove("C:/Users/Nour/Desktop/Builboard_Display/static/"+str(data[0])[2:i])
    cur1.close()
    cur2.execute("DELETE FROM reclamation WHERE Id_Pub=%s", (id_data,))
    cur2.execute("DELETE FROM price_pub WHERE Id_Pub=%s", (id_data,))
    cur.execute("DELETE FROM pub WHERE Id_Pub=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('IndexPub'))


@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['idImage']
        duree = request.form['duree']
        frequence = request.form['frequence']
        dateDebut1 = request.form['dateDebut']
        dateFin1 = request.form['dateFin']
        dateDebut = datetime.strptime(dateDebut1, '%Y-%m-%d')
        dateFin= datetime.strptime(dateFin1, '%Y-%m-%d')
        file = request.files['fileImage']
        if file and allowed_file_image(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PUB_UPLOADS'], filename))
            typeFile = "image"
            duree = request.form['duree']
        if file and allowed_file_video(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PUB_UPLOADS'], filename))
            typeFile = "video"
            cap = cv2.VideoCapture("C:/Users/Nour/Desktop/Builboard_Display/static/"+file.filename)
            fps = cap.get(cv2.CAP_PROP_FPS)      
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duree = frame_count/fps
            cap.release()
        cur = mysql.connection.cursor()
        Id_User = session['Id_User']
        prix = (float(duree)/60)*(int(frequence)*2500)
        cur.execute("UPDATE pub SET Duree=%s, Frequence=%s, Date_Debut=%s, Date_Fin=%s, Prix=%s, Statut=%s, File_Pub=%s WHERE Id_Pub=%s", 
               (duree, frequence, dateDebut, dateFin, prix, 0,file.filename ,id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('IndexPub'))


# MSG
@app.route('/msgs')
def IndexMsg():
    cur = mysql.connection.cursor()
    Id_User = session['Id_User']
    cur.execute("SELECT * FROM message WHERE Id_User=%s",(Id_User,))
    data = cur.fetchall()
    cur.close()
    return render_template('msg.html', msgs=data )


@app.route('/insertMsg', methods = ['POST'])
def insertMsg():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        msg = request.form['textMsg']
        local_dt = datetime.now()
        cur = mysql.connection.cursor()
        Id_User = session['Id_User']
        cur.execute("INSERT INTO message (Text_Msg, Statut, Date_Msg, Id_User) VALUES (%s,%s,%s,%s)", (msg,0,local_dt,Id_User))
        mysql.connection.commit()
        return redirect(url_for('IndexMsg'))


@app.route('/deleteMsg/<string:id_data>', methods = ['GET'])
def deleteMsg(id_data):
    flash("Pub Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM message WHERE Id_Msg=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('IndexMsg'))


# PUB & MSG ADMIN 
@app.route('/pubsAdmin')
def IndexPubAdmin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pub")
    data = cur.fetchall()
    cur.close()
    return render_template('pubAdmin.html', pubs=data)


@app.route('/deleteAdmin/<string:id_data>', methods = ['GET'])
def deleteAdmin(id_data):
    flash("Pub Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur1.execute("SELECT File_Pub FROM pub WHERE Id_Pub=%s", (id_data,))
    data = cur1.fetchall()
    i= len( str(data[0]) ) - 3
    os.remove("C:/Users/Nour/Desktop/Builboard_Display/static/"+str(data[0])[2:i])
    cur1.close()
    cur2.execute("DELETE FROM reclamation WHERE Id_Pub=%s", (id_data,))
    cur.execute("DELETE FROM pub WHERE Id_Pub=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('IndexPubAdmin'))


@app.route('/accept',methods=['POST'])
def accept():
    id_data = request.form['idImage']
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    cur.execute("UPDATE pub SET Statut=%s WHERE Id_Pub=%s", (1 ,id_data))
    cur1.execute("UPDATE reclamation SET Reponse=%s WHERE Id_Pub=%s", 
    (" Your claim has been accepted .", id_data))
    flash("Pub Accepted ")
    mysql.connection.commit()
    return redirect(url_for('IndexPubAdmin'))


@app.route('/msgsAdmin')
def IndexMsgAdmin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM message")
    data = cur.fetchall()
    cur.close()
    return render_template('msgAdmin.html', msgs=data )


@app.route('/deleteMsgAdmin/<string:id_data>', methods = ['GET'])
def deleteMsgAdmin(id_data):
    flash("Message Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM message WHERE Id_Msg=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('IndexMsgAdmin'))

@app.route('/acceptMsg',methods=['POST'])
def acceptMsg():
    id_data = request.form['idMsg']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE message SET Statut=%s WHERE Id_Msg=%s", (1 ,id_data))
    flash("Message Accepted ")
    mysql.connection.commit()
    return redirect(url_for('IndexMsgAdmin'))



if __name__ == '__main__':
    app.secret_key = "x62lgUrZLOzNiPJnlseUEw"
    app.run(debug=True)