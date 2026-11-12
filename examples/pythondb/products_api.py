# A simple CRUD web API for the product table in products.sqlite3.
#
# To use this app:
#   pip install flask
#   python products_api.py
#
# The product table in products.sqlite3 looks like this:
#
#   CREATE TABLE product (
#       id INTEGER NOT NULL PRIMARY KEY,
#       description VARCHAR(80) NOT NULL,
#       price FLOAT NOT NULL
#   );
#
# CRUD = Create, Read, Update, Delete. Each one has its own URL + HTTP method:
#
#   GET    /products        Read: list all products
#   GET    /products/<id>   Read: get one product
#   POST   /products        Create: add a product
#   PUT    /products/<id>   Update: change a product
#   PATCH  /products/<id>   Update: change a product
#   DELETE /products/<id>   Delete: remove a product
#
# For POST and PUT, send JSON like:  {"description": "Widget", "price": 2.50}

import sqlite3
from typing import Any, Optional

from flask import Flask, jsonify, request


# The database file is in the same folder as this program
DB_PATH = "products.sqlite3"

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Database helper functions
# These do NOT open, commit, or close connections. The endpoint that calls
# them is in charge of that, so several SQL statements can succeed or fail
# together. (INSERT, UPDATE, and DELETE statements are run directly in the
# endpoints that need them.)
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """Open and return a new connection to the database."""
    return sqlite3.connect(DB_PATH)


def select_products(con: sqlite3.Connection, sql: str, params: list) -> list:
    """Run a SELECT statement on the product table and return a list of products.

    The SELECT must list the columns in this order: id, description, price.
    Each product is a dictionary, like {'id': 1, 'description': 'Oranges', 'price': 3.3},
    which is easy to convert to JSON.
    """
    cursor = con.cursor()
    cursor.execute(sql, params)

    # SQLite gives us each row as a tuple, like (1, 'Oranges', 3.3).
    # Turn each tuple into a dictionary.
    products = []
    for row in cursor.fetchall():
        product = {"id": row[0], "description": row[1], "price": row[2]}
        products.append(product)
    return products


def find_product(con: sqlite3.Connection, product_id: int) -> Optional[dict]:
    """Return the product with this id as a dictionary, or None if not found."""
    rows = select_products(con, "SELECT id, description, price FROM product WHERE id = ?",
                       [product_id])
    if len(rows) == 0:
        return None
    return rows[0]


# ---------------------------------------------------------------------------
# Input checking
# ---------------------------------------------------------------------------

def check_product_data(data: Any) -> Optional[str]:
    """Check the JSON sent by the client.

    Returns an error message (a string) if something is wrong,
    or None if the data is fine.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"
    if "description" not in data or "price" not in data:
        return "description and price are required"
    if not isinstance(data["description"], str) or data["description"] == "":
        return "description must be a non-empty string"
    if len(data["description"]) > 80:
        return "description must be at most 80 characters"
    if not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return "price must be a number that is not negative"
    return None


# ---------------------------------------------------------------------------
# Routes (one function for each CRUD operation)
# ---------------------------------------------------------------------------

@app.route("/products", methods=["GET"])
def list_products():
    # This endpoint only reads data, so there is nothing to commit or roll back.
    con = get_connection()
    try:
        products = select_products(con, "SELECT id, description, price FROM product ORDER BY id", [])
        return jsonify(products)
    finally:
        con.close()  # always runs, even after a return or an error


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    # This endpoint only reads data, so there is nothing to commit or roll back.
    con = get_connection()
    try:
        product = find_product(con, product_id)
        if product is None:
            return jsonify(error="Product not found"), 404
        return jsonify(product)
    finally:
        con.close()


@app.route("/products", methods=["POST"])
def create_product():
    # Check the data first. There's no need to open a connection if it's bad.
    data: Any = request.get_json(silent=True)  # None if the body isn't valid JSON
    message = check_product_data(data)
    if message is not None:
        return jsonify(error=message), 400

    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO product (description, price) VALUES (?, ?)",
                       [data["description"], data["price"]])
        new_id = cursor.lastrowid or 0  # the id the database gave the new product
        product = find_product(con, new_id)
        con.commit()  # the new product is saved only now
        return jsonify(product), 201  # 201 means "Created"
    finally:
        con.close()


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int):
    data: Any = request.get_json(silent=True)
    message = check_product_data(data)
    if message is not None:
        return jsonify(error=message), 400

    con = get_connection()
    try:
        if find_product(con, product_id) is None:
            return jsonify(error="Product not found"), 404

        cursor = con.cursor()
        cursor.execute("UPDATE product SET description = ?, price = ? WHERE id = ?",
                       [data["description"], data["price"], product_id])
        product = find_product(con, product_id)
        con.commit()
        return jsonify(product)
    finally:
        con.close()

@app.route("/products/<int:product_id>", methods=["PATCH"])
def patch_product(product_id: int):
    data: Any = request.get_json(silent=True)

    con = get_connection()
    try:
        if find_product(con, product_id) is None:
            return jsonify(error="Product not found"), 404

        cursor = con.cursor()
        
        if "description" in data:
            cursor.execute("UPDATE product SET description = ? WHERE id = ?",
                        [data["description"], product_id])

        if "price" in data:
            cursor.execute("UPDATE product SET price = ? WHERE id = ?",
                        [data["price"], product_id])

        product = find_product(con, product_id)
        con.commit()
        return jsonify(product)
    finally:
        con.close()


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    con = get_connection()
    try:
        if find_product(con, product_id) is None:
            con.rollback()  # nothing to save
            return jsonify(error="Product not found"), 404

        cursor = con.cursor()
        cursor.execute("DELETE FROM product WHERE id = ?", [product_id])
        con.commit()
        return "", 204  # 204 means "No Content" (success, nothing to send back)
    finally:
        con.close()


# Start the web server when this file is run directly
if __name__ == "__main__":
    app.run(debug=True)
