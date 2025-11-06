import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db_config = {
    'host': "localhost",
    'user': "root",
    'password': "########",
    'database': "libreria_db"
}

@app.route('/')
def index():
    connector = mysql.connector.connect(**db_config)
    cursor = connector.cursor(dictionary=True)
    
    cursor.execute("SELECT ID, nombre, precio, stock FROM libros")
    libros = cursor.fetchall()
    
    return render_template('index.html', lista_libros=libros)


@app.route('/agregar')
def agregar_libro_form():
    return render_template('agregar.html')


@app.route('/guardar_libro', methods=['POST'])
def guardar_libro():
    nombre = request.form['nombre']
    precio = request.form['precio']
    stock = request.form['stock']
    
    connector = mysql.connector.connect(**db_config)
    cursor = connector.cursor()
        
    #consulta SQL
    query = "INSERT INTO libros (nombre, precio, stock) VALUES (%s, %s, %s)"
    data = (nombre, precio, stock)
    
    cursor.execute(query, data)
    connector.commit()
    print(f"Libro agregado: {nombre}")

    return redirect('/')


@app.route('/eliminar/<int:id>')
def eliminar(id):
    connector = mysql.connector.connect(**db_config)
    cursor = connector.cursor()
    
    cursor.execute("DELETE FROM libros WHERE id=%s", (id,))
    connector.commit()
    
    return redirect('/')


@app.route('/editar/<int:id>')
def editar(id):
    connector = mysql.connector.connect(**db_config)
    cursor = connector.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros WHERE ID=%s", (id,))
    libro = cursor.fetchone()
    cursor.close()
    
    return render_template('editar.html', libro=libro)


@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    stock = request.form.get('stock')

    connector = mysql.connector.connect(**db_config)
    cursor = connector.cursor()
    
    query = "UPDATE libros SET nombre=%s, precio=%s, stock=%s WHERE ID=%s"
    data = (nombre, precio, stock, id)
    
    cursor.execute(query, data)
    connector.commit()
    
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)