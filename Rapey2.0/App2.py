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

#CRUD Repartidores
@app.route('/')
def index_Repartidor():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM repartidor')
    datos = cursor.fetchall()
    return render_template('sesion-repartidor.html', repartidor = datos)

@app.route('/agregar_repartidor', methods = ['POST'])
def agregar_repartidor():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        rut = request.form['Rut']
        region = request.form['Region']
        telefono = request.form['Telefono']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO repartidor (Nombre_repartidor, Rut_repartidor, Nro_region, telefono) VALUES (%s, %s, %s, %s)',
        (nombre,rut,region,telefono))
        mysql.connection.commit()
        flash('Repartidor agregado correctamente')
        return redirect(url_for('index_Repartidor'))

@app.route('/edit_repartidor/<string:rut>')
def get_repartidor(rut):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM repartidor WHERE Rut_repartidor = %s',(rut))
    dato = cursor.fetchall()
    return render_template('edit-repartidor.html', repartidor = dato[0])

@app.route('/update/<string:rut>', methods= ['POST'])
def update_repartidor(rut):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        rut1 = request.form['Rut']
        region = request.form['Region']
        fono = request.form['Telefono']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE repartidor
            SET Nombre_repartidor= %s,
                Rut_repartidor= %s,
                Nro_region= %s,
                telefono= %s
            WHERE rut_repartidor = %s
        """,(nombre,rut1,region,fono, rut))
        mysql.connection.commit()
        flash('Repartidor actualizado correctamente')
    return redirect(url_for('index_Repartidor'))

@app.route('/delete_repartidor/<string:rut>')
def delete_cliente(rut):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM repartidor WHERE Rut_repartidor = {0}'.format(rut))
    mysql.connection.commit()
    flash('Repartidor eliminado corretcamente')
    return redirect(url_for('index_Repartidor'))

if __name__ == '__main__':
    app.run(port=3001,debug=True)