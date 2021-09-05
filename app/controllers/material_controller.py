from app import app
from flask import request
from app.models.material import Material
from app.controllers.mysql_controller import SQLBuilder
import json

# Field to select goes here
field_to_select = [
	'material.id as id',
	'material.name as name',
	'buy_price',
	'type_id',
	'material_type.name as material_type_name',
	'supplier_id',
	'supplier.name as supplier_name' 
]

""" Error in API """
DATA_NOT_FOUND = {
	'code' : "DATA_NOT_FOUND",
	'msg' : "Sorry, we cannot find this material data"
}

UPDATE_SUCCESS = {
	'code' : "Data is Inserted/Updated Successfully",
	'msg' : "Action is completed successfully"
}

DELETE_SUCCESS = {
	'code' : "Deleted Successfully",
	'msg' : "Action is completed successfully"
}

# Controller Functions
def get_material(id=False):
	""" Function for getting all material data or specific material data by id """
	sql = SQLBuilder()
	sql = sql.select(field_to_select, "material")
	sql = sql.inner_join("material_type").on("material.type_id = material_type.id")
	sql = sql.inner_join("supplier").on("material.supplier_id = supplier.id")
	
	if id: # Filter to getting data by id
		sql.where("material.id = " + str(id))
		sql = sql.execute()
		if len(sql) > 0:
			material = Material(sql[0])
			return material
		return DATA_NOT_FOUND
	return sql.execute()

def get_material_by_type(id):
	sql = SQLBuilder()
	sql = sql.select(field_to_select, "material")
	sql = sql.inner_join("material_type").on("material.type_id = material_type.id")
	sql = sql.inner_join("supplier").on("material.supplier_id = supplier.id")
	sql = sql.where("type_id = '" + str(id) + "' OR material_type.name = '" + str(id) + "'")
	return sql.execute()

def update_material():
	data = request.get_json()
	material = Material(data)
	sql = SQLBuilder()
	sql = sql.insert("material").set(material.__dict__).on_duplicate_key("id").update(material.__dict__)
	sql = sql.execute()
	return UPDATE_SUCCESS

@app.route('/material', methods = ['GET'])
def material_index():
	return json.dumps(get_material())

@app.route('/material/id/<id>', methods=['GET','POST','DELETE'])
def material_by_id(id):

	if request.method == 'GET':
		return json.dumps(get_material())

	elif request.method == 'POST':
		return json.dumps(update_material())

	elif request.method == 'DELETE':
		sql = SQLBuilder()
		sql.delete("material").where('id = ' + str(id))
		sql.execute()
		return DELETE_SUCCESS

@app.route('/material/type/<id>', methods=['GET'])
def material_filter(id):
	return json.dumps(get_material_by_type(id))