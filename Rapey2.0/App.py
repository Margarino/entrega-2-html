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

#CRUD Cliente
@app.route('/')
def index_cliente():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cliente')
    datos = cursor.fetchall()
    return render_template('sesion-cliente.html', clientes = datos)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        rut = request.form['Rut']
        edad = request.form['Edad']
        direccion = request.form['Direccion']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO cliente (Nombre_cliente,Rut_cliente, Edad, Direccion) VALUES (%s,%s,%s,%s)',
        (nombre,rut, edad, direccion))
        mysql.connection.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('index_cliente'))

@app.route('/edit_cliente/<string:rut>')
def get_cliente(rut):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cliente WHERE Rut_cliente = %s', (rut))
    dato = cursor.fetchall()
    return render_template('edit-clientes.html', clientes = dato[0])

@app.route('/update/<string:rut>', methods = ['POST'])
def update_cliente(rut):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        rut1 = request.form['Rut']
        edad = request.form['Edad']
        direccion = request.form['Direccion']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE cliente
            SET Nombre_cliente = %s,
                Rut_cliente = %s,
                Edad = %s,
                Direccion = %s
            WHERE rut_cliente = %s
        """,(nombre,rut1, edad,direccion, rut))
        mysql.connection.commit()
        flash('Cliente actualizado correctamente')
        return redirect(url_for('index_cliente'))

@app.route('/delete_cliente/<string:rut>')
def delete_cliente(rut):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM cliente WHERE Rut_cliente = {0}'.format(rut))
    mysql.connection.commit()
    flash('Cliente eliminado correctamente')
    return redirect(url_for('index_cliente'))
#END CRUD Cliente

if __name__ == '__main__':
    app.run(port=3000,debug=True)