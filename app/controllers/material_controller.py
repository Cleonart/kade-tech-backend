from app import app
from app.models.material import Material
from mysql_controller import SQLBuilder
import json

@app.route('/material', methods = ['GET'])
def material_index():
	material = Material()
	return json.dumps(material.__dict__)