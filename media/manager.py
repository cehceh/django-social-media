from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

	use_in_migrations = True

	def _create_user(self, email,password, **extra_fields):
			
		email = self.normalize_email(email)
		print(email)
		user = self.model(email=email, **extra_fields)
		if password:

			user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):

         return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):

		user = self.create_user(
			email = self.normalize_email(email),
			password=password)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True

		user.save(using=self._db)
		return user