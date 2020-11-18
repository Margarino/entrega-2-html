from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rapey'
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'mysecretkey'

#CRUD Restaurant
@app.route('/')
def index_restaurant():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Restaurant')
    datos = cursor.fetchall()
    return render_template('sesion-restaurant.html', restaurantes = datos)

@app.route('/agregar_restaurant', methods=['POST'])
def agregar_restaurant():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Id_restaurant= request.form['Id_restaurant']
        Id_comida = request.form['Id_comida']
        Nro_region = request.form['Nro_region']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Restaurant (Nombre ,Id_restaurant, Id_comida, Nro_region) VALUES (%s,%s,%s,%s)',
        (Nombre,Id_restaurant, Id_comida, Nro_region))
        mysql.connection.commit()
        flash('Restaurant agregado correctamente')
        return redirect(url_for('index_restaurant'))

@app.route('/edit_restaurant/<string:Id_restaurant>')
def get_restaurant(Id_restaurant):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Restaurant WHERE Id_restaurant = %s', (Id_restaurant))
    dato = cursor.fetchall()
    return render_template('edit-restaurant.html', restaurantes = dato[0])

@app.route('/update/<string:Id_restaurant>', methods = ['POST'])
def update_restaurant(Id_restaurant):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Id_restaurant = request.form['Id_restaurant']
        Id_comida = request.form['Id_comida']
        Nro_region = request.form['Nro_region']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Restaurant SET Nombre = %s, Id_restaurant = %s, Id_comida = %s, Nro_region = %s WHERE Id_restaurant = %s",(Nombre, Id_restaurant, Id_comida, Nro_region, Id_restaurant))
        mysql.connection.commit()
        flash('Restaurant actualizado correctamente')
        return redirect(url_for('index_restaurant'))

@app.route('/delete_restaurant/<string:Id_restaurant>')
def delete_restaurant(Id_restaurant):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM Restaurant WHERE Id_restaurant = %s;', (Id_restaurant))
    mysql.connection.commit()
    flash('Restaurant eliminado correctamente')
    return redirect(url_for('index_restaurant'))
#END CRUD restaurant

if __name__ == '__main__':
    app.run(port=3003,debug=True)