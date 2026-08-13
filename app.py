from flask import Flask, render_template, request, session
from repository.database import  get_connection, init_schema

connection = get_connection()
init_schema(connection)

app = Flask(__name__)

connection.close()