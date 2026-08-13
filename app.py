from repository.database import  get_connection, init_schema

connection = get_connection()
init_schema(connection)

connection.close()