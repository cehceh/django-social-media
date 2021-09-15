from django.db.models import TextField

class SpecialTextField(TextField):

	def formField(self, **kwargs):
		kwargs['strip'] = False
		return Super(SpecialTextField, self).formField(**kwargs)