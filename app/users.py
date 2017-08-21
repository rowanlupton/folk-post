class User():
	def __init(self, username):
		self.username = username

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	@staticmethod
	def validate_login(password_hash, password):
		return check_password_hash(password_hash, password)

