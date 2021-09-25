from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.asteroid
import codeitsuisse.routes.options_optimization
import codeitsuisse.routes.fixed_race
# import the file that we have just created
