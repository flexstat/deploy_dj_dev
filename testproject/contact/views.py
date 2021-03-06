from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length = 100)
    sender = forms.EmailField()
    message = forms.CharField()
    copy = forms.BooleanField(required = False)



from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		#Если форма заполнена корректно, сохраняем все введённые пользователем значения
		if form.is_valid():
			subject = form.cleaned_data['subject']
			sender = form.cleaned_data['sender']
			message = form.cleaned_data['message']
			copy = form.cleaned_data['copy']
			recipients = ['bigcaches@ya.ru']
			#Если пользователь захотел получить копию себе, добавляем его в список получателей
			if copy:
				recipients.append(sender)
			try:
				send_mail(subject, message, 'bigcaches@ya.ru', recipients)
			except BadHeaderError: #Защита от уязвимости
				return HttpResponse('block некорректный заголовок')
			#Переходим на другую страницу, если сообщение отправлено
			return render(request, 'landing/landing.html')
	else:
		#Заполняем форму
		form = ContactForm()
	#Отправляем форму на страницу
	return render(request, 'contact/contact.html', {'form': form})





#def contact(request):
 #   return render(request, 'contact/contact.html', locals()) 
