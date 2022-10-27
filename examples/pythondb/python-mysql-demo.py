
# Requires the mysql.connector Python library
# To use this app:
#   pip install mysql-connector-python
# 
# For docs, see: https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html
# See PEP-249 for the API standard: https://www.python.org/dev/peps/pep-0249/

# This example uses the simpledb database located in 
# class/sampledb/simpledb_mysql.sql

from mysql.connector import connect

con = connect(user='root', password='passw0rd', database='simpledb', host='localhost')

cursor = con.cursor()

# Make INSERT/DELETE/UPDATE take effect immediately without a separate commit command
con.autocommit = True

# Execute an INSERT/DELETE/UPDATE statement
cursor.execute("""
    update Product 
    set Quantity = Quantity + 1
    where ProdName = 'Fifi'
""")
print("Updated {} rows.".format(cursor.rowcount))

cursor.execute("""
    select ProdId, ProdName
    from product
    """)

result = cursor.fetchall()              # Retrieve list of rows from database

print('\nProduct table:')
for row in result:
    (prodId, prodName) = row      # Extract prodId and prodName from row tuple
    print(f"{prodId}: {prodName}")
