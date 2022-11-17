# https://es.stackoverflow.com/questions/429737/como-comprobar-si-ya-existe-un-archivo-con-el-mismo-nombre-y-si-es-asi-agregarl
from flask import Flask, flash, request, redirect, url_for, render_template, session
import os # The OS module in Python provides functions for creating and removing a directory (folder),
from os.path import join, dirname, realpath, abspath
from os import path as osPath
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
        session['usuario'] = ""
        session['contraseña'] = ""
        session['mail'] = ""
        session["nombre"] = ""
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
                return redirect('/home')
        else:
            flash('Usuario o contraseña incorrectos')
            return render_template("login.html", login = True)

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        return redirect('/register')

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
        #conn.execute(x)
        conn.commit()
        conn.close()
        return redirect('/')
    elif request.method == "GET":
        return redirect('/register')

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "GET":
        if session['usuario'] != "":
            conn = sqlite3.connect('Publicaciones.db')
            q = f"""SELECT * FROM publicaciones
                    ORDER BY id DESC"""
            x = conn.execute(q)
            listaPublicaciones = x.fetchall()
            
            
            conn2 = sqlite3.connect('SocialMedia.db')
            q2 = f"""SELECT fotoPerfil from Usuarios
                    WHERE username = '{session['usuario']}'"""
            x2 = conn2.execute(q2)
            imgPerfil = x2.fetchall()
            fotoDePerfil = imgPerfil[0][0]

            
            q4 = f"""SELECT * from Usuarios"""
            x4 = conn2.execute(q4)
            listaCompleta = x4.fetchall()
            return render_template("base.html", fotoDePerfil = fotoDePerfil, listaPublicaciones = listaPublicaciones, listaCompleta = listaCompleta, user = session['usuario'])
        elif session['usuario'] == "":
            session['usuario'] = ""
            return render_template("base.html", user = session['usuario'])
        
    elif request.method == "POST":
        return redirect('/home')

@app.route('/filtrarPor', methods=['POST','GET'])
def filtrarPor():
    if request.method == "POST":
        prenda = request.form['prendaFiltrar']
        color = request.form['colorFiltrar']

        print(prenda)
        print(color)

        if prenda == "null":
            if color != "null" and color != "multicolor":
                conn = sqlite3.connect('Publicaciones.db')
                q = f"""SELECT * FROM publicaciones
                        WHERE colorRemera LIKE '{color}'
                        OR colorAbrigo LIKE '{color}'
                        OR colorPantalon LIKE '{color}' 
                        ORDER BY id DESC"""
                x = conn.execute(q)
                listaPublicaciones = x.fetchall()
                print(listaPublicaciones)
            elif color == "null":
                return redirect('/home')
            elif color == "multicolor":
                return redirect('/home')
        elif prenda != "null":
            if color == "multicolor":
                nomPrenda = "nombre" + prenda
                conn = sqlite3.connect('Publicaciones.db')
                q = f"""SELECT * FROM publicaciones
                        WHERE {nomPrenda} NOT LIKE ''
                        ORDER BY id DESC"""
                x = conn.execute(q)
                listaPublicaciones = x.fetchall()
                print(listaPublicaciones)
            elif color != "multicolor" or color != "null":
                nomPrenda = "nombre" + prenda
                conn = sqlite3.connect('Publicaciones.db')
                q = f"""SELECT * FROM publicaciones
                        WHERE {nomPrenda} NOT LIKE ''
                        ORDER BY id DESC"""
                x = conn.execute(q)
                listaPublicaciones = x.fetchall()
                print(listaPublicaciones)
        

        conn2 = sqlite3.connect('SocialMedia.db')
        q2 = f"""SELECT fotoPerfil from Usuarios
                WHERE username = '{session['usuario']}'"""
        x2 = conn2.execute(q2)
        imgPerfil = x2.fetchall()
        fotoDePerfil = imgPerfil[0][0]

        
        q4 = f"""SELECT * from Usuarios"""
        x4 = conn2.execute(q4)
        listaCompleta = x4.fetchall()

        return render_template("base.html", fotoDePerfil = fotoDePerfil, listaPublicaciones = listaPublicaciones, listaCompleta = listaCompleta, user = session['usuario'])
    elif request.method == "GET":
        return redirect('/home')

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == "GET":
        if session['usuario'] != "":
            conn2 = sqlite3.connect('SocialMedia.db')
            q2 = f"""SELECT fotoPerfil from Usuarios
                    WHERE username = '{session['usuario']}'"""
            x2 = conn2.execute(q2)
            
            imgPerfil = x2.fetchall()
            print(imgPerfil[0][0])
            fotoDePerfil = imgPerfil[0][0]

            return render_template("profile.html", fotoDePerfil = fotoDePerfil)
        elif session['usuario'] == "":
            return redirect('/')
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

        foto1 = foto.filename.replace("(", "")
        foto2 = foto1.replace(")", "")
        foto3 = foto2.replace(" ", "_")
        print(foto3)
        imgPerfil = "/static/img/perfil/" + foto3
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
        colorRemera    = request.form["colorRemera"]
        print(colorRemera)
        colorAbrigo    = request.form["colorAbrigo"]
        print(colorAbrigo) 
        colorPantalon  = request.form["colorPantalon"]
        print(colorPantalon)
        colorSneaker   = request.form["colorSneaker"]
        print(colorSneaker)
        
        
        if imagen.filename == '':
            return redirect('/home')
        else:
            filename = secure_filename(imagen.filename)
            if osPath.exists(osPath.join(app.config['UPLOAD_FOLDER_Publicacion'], filename)) == True:
                numb = 1
                print("hola")
                # Separa el nombre del archivo de su extensión colocando el numero en el medio (al final del nombre)
                newName = "{0}_{2}{1}".format(*osPath.splitext(filename) + (numb,))
                print(newName)
                # Si existe un archivo con ese nombre incrementa el numero
                while osPath.exists(osPath.join(app.config['UPLOAD_FOLDER_Publicacion'], newName)):
                    if osPath.exists(osPath.join(app.config['UPLOAD_FOLDER_Publicacion'], newName)):
                        numb += 1
                        print("Esta sumando")
                        newName = "{0}_{2}{1}".format(*osPath.splitext(filename) + (numb,))
                        file_path = os.path.join(app.config['UPLOAD_FOLDER_Publicacion'], newName)
                        #imagen.save(file_path)
                        print(newName)
                        img = "./static/" + path2 + '/' + newName + ""   
            else:
                print("hola")
                filename = secure_filename(imagen.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER_Publicacion'], filename)
                imagen.save(file_path)
                foto1 = imagen.filename.replace("(", "")
                foto2 = foto1.replace(")", "")
                foto3 = foto2.replace(" ", "_")
                img = "./static/" + path2 + '/' + foto3 + ""
        
        precioTotal = 0
        
        if precioSneaker != "":
            pass
        else:
            precioSneaker = 0
        
        if precioRemera != "":
            pass
        else:
            precioRemera = 0
        
        if precioAbrigo != "":
            pass
        else:
            precioAbrigo = 0
            
        if precioPantalon != "":
            pass7
        else:
            precioPantalon = 0
        
        precioTotal = int(precioAbrigo) + int(precioPantalon) + int(precioRemera) + int(precioSneaker)

        conn = sqlite3.connect('Publicaciones.db')
        q = f"""INSERT INTO publicaciones
                (usuario, rutaImagen,nombreRemera , precioRemera,nombreAbrigo , precioAbrigo, nombrePantalon,
                precioPantalon ,nombreSneaker ,precioSneaker, colorRemera, colorAbrigo, colorPantalon, colorSneaker, precioTotal)
                VALUES('{session["usuario"]}', '{img}', '{modeloRemera}', '{precioRemera}', '{modeloAbrigo}', '{precioAbrigo}', 
                '{modeloPantalon}', '{precioPantalon}', '{modeloSneaker}', '{precioSneaker}', '{colorRemera}', '{colorAbrigo}', 
                '{colorPantalon}', '{colorSneaker}', '{precioTotal}')"""
        conn.execute(q)
        conn.commit()
        conn.close()
        
        return redirect('/home')
    elif request.method == "GET":
        return redirect('/home')

@app.route('/mensajes', methods=['POST', 'GET'])
def mensajes():
    if request.method == "GET":
        if session['usuario'] != "":
            conn2 = sqlite3.connect('SocialMedia.db')
            q2 = f"""SELECT fotoPerfil from Usuarios
                    WHERE username = '{session['usuario']}'"""
            x2 = conn2.execute(q2)
            imgPerfil = x2.fetchall()
            fotoDePerfil = imgPerfil[0][0]

            return render_template('mensajes.html', fotoDePerfil = fotoDePerfil)
        elif session['usuario'] == "":
            return redirect('/')
    elif request.method == "POST":
        return redirect('/mensajes')

@app.route('/buscarNombre', methods=['POST', 'GET'])
def buscarUsuario():
    if request.method == "POST":
        search_term = request.form
        search = search_term["value"]
        
        conn = sqlite3.connect('SocialMedia.db')
        conn2 = sqlite3.connect('Publicaciones.db')

        q3 = f"""SELECT * FROM publicaciones
                WHERE usuario LIKE '%{search}%'
                ORDER BY id DESC"""
        x3 = conn2.execute(q3)
        listaPublicaciones = x3.fetchall()
        print(listaPublicaciones)

        q4 = f"""SELECT * from Usuarios"""
        x4 = conn.execute(q4)
        listaCompleta = x4.fetchall()

        q5 = f"""SELECT fotoPerfil from Usuarios
                WHERE username = '{session['usuario']}'"""
        x5 = conn.execute(q5)
        
        imgPerfil = x5.fetchall()
        fotoDePerfil = imgPerfil[0][0]

        return render_template("base.html", fotoDePerfil = fotoDePerfil, listaPublicaciones = listaPublicaciones, listaCompleta = listaCompleta, user = session['usuario'])
    elif request.method == "GET":
        return redirect('/home')
    # Falta hacer que cambie el HTML, sino hacer otra página para el buscar #

@app.route('/admin', methods=['POST', 'GET'])
def moderador():
    if request.method == "GET":
        if session['usuario'] == "elmascapodelproyecto":
            
            conn = sqlite3.connect('SocialMedia.db')
            q = f"""SELECT username FROM Usuarios"""
            listaUsuarios = conn.execute(q).fetchall()

            return render_template('moderador.html', listaUsuarios = listaUsuarios)
        else:
            return redirect('/home')
    elif request.method == "POST":
        return redirect('/home')

@app.route('/eliminarUsuario', methods=['POST', 'GET'])
def eliminarUsuario():
    if request.method == 'POST':
        usuarioBan = request.form["userBan"]
        print(usuarioBan)

        conn = sqlite3.connect('SocialMedia.db')
        conn2 = sqlite3.connect('Publicaciones.db')

        q = f"""DELETE FROM Usuarios
                WHERE username = '{usuarioBan}'"""
        
        q2 = f"""DELETE FROM publicaciones
                WHERE usuario = '{usuarioBan}'"""

        conn.execute(q)
        conn2.execute(q2)
        conn.commit()
        conn.close()
        conn2.commit()
        conn2.close()

        return redirect('/admin')
    elif request.method == 'GET':
        return redirect('/')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
        session['usuario'] = ""
        session['contraseña'] = ""
        session['mail'] = ""
        session["nombre"] = ""
        return redirect('/')

@app.route('/<username>', methods=['POST', 'GET'])
def mostrarUsuario(username):
    if request.method == "GET":
        conn = sqlite3.connect('Publicaciones.db')
        q = f"""SELECT rutaImagen FROM publicaciones
                WHERE usuario = '{username}'
                ORDER BY id DESC"""
        x = conn.execute(q)
        listaPublicacionesDelUser = x.fetchall()


        conn2 = sqlite3.connect('SocialMedia.db')
        q2 = f"""SELECT fotoPerfil from Usuarios
                WHERE username = '{session['usuario']}'"""
        x2 = conn2.execute(q2)
        
        imgPerfil = x2.fetchall()
        fotoDePerfil = imgPerfil[0][0]

        return render_template("profile.html", listaPublicacionesDelUser = listaPublicacionesDelUser, fotoDePerfil = fotoDePerfil)
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