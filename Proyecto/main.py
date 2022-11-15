from flask import Flask, flash, request, redirect, url_for, render_template, session
import os # The OS module in Python provides functions for creating and removing a directory (folder),
from os.path import join, dirname, realpath, abspath
# fetching its contents, changing and identifying the current directory, etc.

import sqlite3

from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
UPLOAD_FOLDER_FotoPerfil = './Proyecto/static/img/perfil'
UPLOAD_FOLDER_Publicacion = './Proyecto/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
pathFotoPerfil = './Proyecto/static/img'
path2 = 'img'

app = Flask(__name__)
app.config['UPLOAD_FOLDER_FotoPerfil'] = UPLOAD_FOLDER_FotoPerfil
app.config['UPLOAD_FOLDER_Publicacion'] = UPLOAD_FOLDER_Publicacion
app.secret_key = "asdasdazsdawefdfascacs"
#socketio = SocketIO(app)

#if __name__ == '__main__':
#    socketio.run(app)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == "GET":
        return render_template("login.html", login = False)
    elif request.method == "POST":
        return redirect('/')

@app.route('/usuarioIngresado', methods=['GET', 'POST'])
def checkearUsuario():
    if request.method == "GET":
        return redirect('/')
    elif request.method == "POST":
        session['contraseña'] = request.form["user-password"]
        session['usuario'] = request.form["username"]
        conn = sqlite3.connect('SocialMedia.db')
        q = f"""
                SELECT contraseña, username FROM Usuarios 
                WHERE contraseña = '{session['contraseña']}'
                and username = '{session['usuario']}'
                """
        resu = conn.execute(q)
        
        if resu.fetchone():
            if session['usuario'] == "elmascapodelproyecto":
                return redirect('/admin')
            else:
                return redirect('/home')
        else:
            flash('Usuario o contraseña incorrectos')
            return render_template("login.html", login = True)


@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        return redirect('/')

@app.route('/añadirUsuario', methods=['POST', 'GET'])
def agregarUsuario():
    if request.method == "POST":
        session['usuario'] = request.form["username"]
        session['contraseña'] = request.form["user-password"]
        session['mail'] = request.form['e-mail']
        session["nombre"] = request.form['name']
        session['mail'] = session['mail'].replace("@", ".")

        # Checkeamos que el usuario no este usado
        conn = sqlite3.connect('SocialMedia.db')
        q = f"""SELECT username FROM Usuarios"""
        x = conn.execute(q)
        listaUsuarios = x.fetchall()
        print(listaUsuarios)
        print(len(listaUsuarios))

        for i in range(len(listaUsuarios)):
            if session['usuario'] == listaUsuarios[i][0]:
                flash('Nombre de usuario ya ingresado')
                return render_template("register.html", login = True)
        
        # Checkeamos que el mail no este usado 
        q2 = f"""SELECT mail FROM Usuarios"""
        x2 = conn.execute(q2)
        listaMails = x2.fetchall()
        print(listaMails)
        print(len(listaMails))

        for i in range(len(listaMails)):
            if session['mail'] == listaMails[i][0]:
                flash('Email ya regsitrado, pruebe con otro')
                return render_template("register.html", login = True)
        
        # Inserto los datos en la tabla de Usuarios
        q = f"""INSERT INTO Usuarios(nombre, contraseña, mail, username, fotoPerfil) 
                VALUES('{session["nombre"]}', '{session['contraseña']}', '{session['mail']}', '{session['usuario']}', '/static/img/sin-foto-perfil.jpeg')"""
        conn.execute(q)

        #x = f"""CREATE TABLE IF NOT EXISTS {session['usuario']} 
        #    (publicacion TEXT);"""
        conn.execute(x)
        conn.commit()
        conn.close()
        return redirect('/')
    elif request.method == "GET":
        return redirect('/register')

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "GET":
        conn = sqlite3.connect('Publicaciones.db')
        q = f"""SELECT * FROM publicaciones
                ORDER BY id DESC"""
        x = conn.execute(q)
        listaPublicaciones = x.fetchall()
        
        print(listaPublicaciones)
        print(len(listaPublicaciones))
        
        conn2 = sqlite3.connect('SocialMedia.db')
        q2 = f"""SELECT fotoPerfil from Usuarios
                WHERE username = '{session['usuario']}'"""
        x2 = conn2.execute(q2)
        
        imgPerfil = x2.fetchall()
        print(imgPerfil[0][0])
        fotoDePerfil = imgPerfil[0][0]

        
        q4 = f"""SELECT * from Usuarios"""
        x4 = conn2.execute(q4)
        listaCompleta = x4.fetchall()
        print(listaCompleta)
        print(listaCompleta[0][3])
        
        
        return render_template("base.html", fotoDePerfil = fotoDePerfil, listaPublicaciones = listaPublicaciones, listaCompleta = listaCompleta)
    elif request.method == "POST":
        return redirect('/home')

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == "GET":
        conn2 = sqlite3.connect('SocialMedia.db')
        q2 = f"""SELECT fotoPerfil from Usuarios
                WHERE username = '{session['usuario']}'"""
        x2 = conn2.execute(q2)
        
        imgPerfil = x2.fetchall()
        print(imgPerfil[0][0])
        fotoDePerfil = imgPerfil[0][0]

        return render_template("profile.html", fotoDePerfil = fotoDePerfil)
    elif request.method == "POST":
        return redirect('/profile')

@app.route('/subirFotoPerfil', methods= ['POST', 'GET'])
def nuevaFoto():
    if request.method == 'POST':
        foto = request.files["profile-photo"]
            
        if foto.filename == '':
            flash('No selected file')
            return redirect('/home')
        else:
            print("hola")
            filename = secure_filename(foto.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_FotoPerfil'], filename)
            foto.save(file_path)
    
        imgPerfil = "/static/img/perfil/" + foto.filename
        print(imgPerfil)

        conn = sqlite3.connect('SocialMedia.db')
        q = f"""UPDATE Usuarios
                SET fotoPerfil  = '{imgPerfil}'
                WHERE username = '{session['usuario']}'"""
        conn.execute(q)
        conn.commit()
        conn.close()
        
        return redirect('/profile')
    elif request.method == "GET":
        return redirect('/profile')


@app.route('/subirImagen', methods=['POST', 'GET'])
def nuevaImagen():
    if request.method == "POST":
        imagen         = request.files["imagen"]        
        modeloRemera   = request.form["modeloRemera"]
        precioRemera   = request.form["precioRemera"]
        modeloAbrigo   = request.form["modeloAbrigo"]
        precioAbrigo   = request.form["precioAbrigo"]
        modeloPantalon = request.form["modeloPantalon"]
        precioPantalon = request.form["precioPantalon"]
        modeloSneaker  = request.form["modeloSneaker"]
        precioSneaker  = request.form["precioSneaker"]

        if imagen.filename == '':
            flash('No selected file')
            return redirect('/home')
        else:
            print("hola")
            filename = secure_filename(imagen.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_Publicacion'], filename)
            imagen.save(file_path)
            img = "./static/" + path2 + '/publicacion' + filename + ""
        
        print(file_path)
        print(filename)
        print(img)

        conn = sqlite3.connect('Publicaciones.db')
        q = f"""INSERT INTO publicaciones
                (usuario, rutaImagen,nombreRemera , precioRemera,nombreAbrigo , precioAbrigo, nombrePantalon,
                precioPantalon ,nombreSneaker ,precioSneaker)
                VALUES('{session["usuario"]}', '{img}', '{modeloRemera}', '{precioRemera}', '{modeloAbrigo}', '{precioAbrigo}', 
                '{modeloPantalon}', '{precioPantalon}', '{modeloSneaker}', '{precioSneaker}')"""
        conn.execute(q)
        conn.commit()
        conn.close()
        
        return redirect('/home')
    elif request.method == "GET":
        return redirect('/home')

@app.route('/mensajes', methods=['POST', 'GET'])
def mensajes():
    if request.method == "GET":
        return render_template('mensajes.html')
    elif request.method == "POST":
        return redirect('/mensajes')

@app.route('/buscarNombre', methods=['POST'])
def buscarUsuario():
    pass
    #pasar todos los usuarios con la linea "WHERE (usuario de la base de datos) LIKE "%valorInput%"


@app.route('/admin', methods=['POST', 'GET'])
def moderador():
    if request.method == "GET":
        if session['usuario'] == "elmascapodelproyecto":
            return render_template('moderador.html')
        else:
            return redirect('/')
    elif request.method == "POST":
        return redirect('/')


#@socketio.on('connect')
#def test_connect():
#    print('Client connected')
 
#@socketio.on('disconnect')
#def test_disconnect():
#    print('Client disconnected')

#@socketio.on('join')
#def on_join(data):
#    username = session.get("username")
#    room = data['room']
#    session['room'] = data['room']
#    join_room(room)
#    print(username + ' has entered the room.')
#    send(username + ' has entered the room.', to=room)

#@socketio.on('recibirMsg')
#def handle_message(json):
#    json = str(session['username']) + ": " + str(json)
#    emit('enviarMsg', str(json), to=session['room'])

#@socketio.on('leave')
#def on_leave(data):
#    username = session.get("username")
#    room = data["room"]
#    leave_room(room)
#    send(username + ' has left the room.', to=room)

#if __name__ == '__main__':
#    socketio.run(app, host='0.0.0.0')

app.run(host='0.0.0.0', port=81)