class Material:
	"""Class for material model"""

	def __init__(self, obj=False):
		""" Initialisation of material model """
		self.id = ""
		self.name = ""
		self.buy_price = 0
		self.type_id = 0
		self.supplier_id = 0

		if obj:
			self.__dict__ = obj
		