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

#CRUD Region
@app.route('/')
def index_region():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM region')
    datos = cursor.fetchall()
    return render_template('sesion-region.html', regiones = datos)

@app.route('/agregar_region', methods=['POST'])
def agregar_region():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Id_region = request.form['Id_region']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Region (Nombre, Id_region) VALUES (%s,%s)',
        (Nombre,Id_region,))
        mysql.connection.commit()
        flash('Region agregada correctamente')
        return redirect(url_for('index_region'))

@app.route('/edit_region/<string:Id_region>')
def get_region(Id_region):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Region WHERE Id_region = %s', (Id_region))
    dato = cursor.fetchall()
    return render_template('edit-region.html', regiones = dato[0])

@app.route('/update/<string:Id_region>', methods = ['POST'])
def update_region(Id_region):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Id_region = request.form['Id_region']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Region SET Nombre = %s, Id_region = %s, WHERE Id_region = %s; ",(Nombre, Id_region, Id_region))
        mysql.connection.commit()
        flash('Region actualizada correctamente')
        return redirect(url_for('index_region'))

@app.route('/delete_region/<string:Id_region>')
def delete_region(Id_region):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM Region WHERE Id_region = %s', (Id_region))
    mysql.connection.commit()
    flash('Region eliminada correctamente')
    return redirect(url_for('index_region'))
#END CRUD Region

if __name__ == '__main__':
    app.run(port=3002,debug=True)