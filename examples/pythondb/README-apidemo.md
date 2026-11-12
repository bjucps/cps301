# Products API (SQLite)

[products_api.py](products_api.py) is a small web API, built with Flask, that lets you
**C**reate, **R**ead, **U**pdate, and **D**elete rows in the `product` table of
[products.sqlite3](products.sqlite3).

| Method   | URL              | What it does           |
|----------|------------------|------------------------|
| `GET`    | `/products`      | List all products      |
| `GET`    | `/products/<id>` | Get one product        |
| `POST`   | `/products`      | Add a product          |
| `PUT`    | `/products/<id>` | Change a product       |
| `DELETE` | `/products/<id>` | Remove a product       |

## 1. Install the prerequisites

You need **Python 3.9 or newer** and the **Flask** library. SQLite support is already built into Python, so there is
nothing else to install for the database.

Check your Python version:

```
python --version
```

Install Flask:

```
pip install flask
```

On macOS/Linux you may need to type `python3` and `pip3` instead of `python` and `pip`.

You also need **curl** to test the API. It comes with Windows 10/11, macOS, and most Linux systems. Check with:

```
curl --version
```

## 2. Launch the server

Open a terminal, go to the folder that contains `products_api.py` and `products.sqlite3`, and run:

```
python products_api.py
```

You should see output ending with something like:

```
 * Running on http://127.0.0.1:5000
```

The server is now running. **Leave this terminal open**; the server stops if you close it or press `Ctrl+C`.

## 3. Test it with curl

Open a **second** terminal window for the curl commands. The examples below use product id `3`; use an id that exists
in your database (the first command shows you what is there).

Note: The commands given here work with the Windows command prompt (not Powershell). If you are in Powershell,
type `cmd` and press Enter to get to the Windows command prompt.

### Read 

List all products:

```
curl http://127.0.0.1:5000/products
```

Get one product:

```
curl http://127.0.0.1:5000/products/1
```

Ask for a product that doesn't exist (you should get an error message):

```
curl -i http://127.0.0.1:5000/products/999
```

(`-i` also prints the HTTP status line, such as `404 NOT FOUND`.)

### Create, Update, Delete

Create and update send JSON, and **how you type the quotes depends on your terminal**. Pick the section that matches
yours.

#### Windows Command Prompt (cmd)

Wrap the JSON in double quotes and put a backslash before each double quote inside it.

```
curl -X POST http://127.0.0.1:5000/products --json "{\"description\":\"Widget\",\"price\":2.50}"
```

```
curl -X PUT http://127.0.0.1:5000/products/3 --json "{\"description\":\"Big Widget\",\"price\":3.00}"
```
```
curl -X PATCH http://127.0.0.1:5000/products/3 --json "{\"price\":4.50}"
```

```
curl -i -X DELETE http://127.0.0.1:5000/products/3
```

#### macOS, Linux, or Git Bash

Wrap the JSON in single quotes. No backslashes needed.

```
curl -X POST http://127.0.0.1:5000/products --json '{"description":"Widget","price":2.50}'
```

```
curl -X PUT http://127.0.0.1:5000/products/3 --json '{"description":"Big Widget","price":3.00}'
```

```
curl -i -X DELETE http://127.0.0.1:5000/products/3
```

### What you should see

| Request                                   | Result                                      |
|-------------------------------------------|---------------------------------------------|
| `POST` with valid JSON                    | `201 CREATED` and the new product           |
| `PUT` or `PATCH` on an existing product              | `200 OK` and the updated product            |
| `DELETE` on an existing product           | `204 NO CONTENT` (empty body)               |
| `GET`, `PUT`, or `DELETE` with a bad id   | `404 NOT FOUND` and `{"error": "Product not found"}` |
| `POST` or `PUT` with missing/invalid data | `400 BAD REQUEST` and an error message      |

Try breaking things on purpose, such as leaving out `price` or using a negative price, to see the error messages.

## Troubleshooting

- **`Cannot connect` / `Failed to connect`**: the server isn't running. Start it (step 2) and keep that terminal open.
- **`{"error": "Request body must be a JSON object"}` when the JSON looks right**: the quotes were changed by your
  terminal. Use the quoting style for your terminal from step 3. In PowerShell this error happens if you forget the
  backslashes.
- **`ModuleNotFoundError: No module named 'flask'`**: run `pip install flask`, and make sure `pip` belongs to the same
  Python you run the program with.
- **`Address already in use`**: another program is using port 5000. Close the other copy of the server, or stop
  whatever is using the port.
- **Changes to the database are permanent.** POST, PUT, and DELETE modify `products.sqlite3`. To start fresh, restore
  the file from your original copy (or `git restore products.sqlite3` if you use git).
