import vk_api
import time, json

token = 'ea8d297a72d3e516eab6f27152e1204cb4cdca86f5518622d7d49981363fd45e98fd0f2b0215954d854a0'
# Сменить токен. У меня новый телефон и не могу получить ключ доступа для новой беседы.
vk=vk_api.VkApi(login='+79151472057', token=token)  # scope - права доступа(не знаю точно, что это)
# В поле login рекомендуется указать номер телефона, для автоматического обхода проверки безопасности
# Насколько я понял многие методы не работают без авторизации
# То есть некоторые методы недоступны без указания своего логина и пароля
vk.auth(token_only=True) # vk.auth() не работает без login
# Если авторизоваться, то вся информация пойдет о пользователе, а не о сообществе
# Чтобы получить информацию о пользователе, при возникновении ошибки no acces_token passed
# нужно передать password в vk = VkApi(... и запустить программу еще раз. Потом password можно будет убрать

print(  # Получаем информацию о чате.
		#vk.method('messages.getConversations')
		vk.method('messages.getConversations', {'group_id':168296857}),  # messages.getConversations
		# vk.method('users.get')
		)
# При использовании методов users.get или docs.get в текущей директории появляется файл vk_config.v2.json с информацией о пользователе
# 'messages.getLongPollServer' ts = 1755371275
'''
# Создаём клавиатуру в формате словаря(это списал с сайта)
keyboard = \
{ 
		"one_time": True, 
		"buttons": [ 
			[{ 
				"action": { 
					"type": "text", 
					"label": "Red" 
				}, 
				"color": "negative" 
			}, 
		 { 
				"action": { 
					"type": "text",  
					"label": "Green" 
				}, 
				"color": "positive" 
			}], 
			[{ 
				"action": { 
					"type": "text", 
					"label": "White" 
				}, 
				"color": "default" 
			}, 
		 { 
				"action": { 
					"type": "text", 
					"label": "Blue" 
				}, 
				"color": "primary" 
			}] 
		] 
	} 

my_id = vk.method('messages.getConversations')['items'][0]['last_message']['from_id']
# my_id - это id последнего сообщения в чате, поэтому сначала напиши в группу любое сообщение.
# (Или убедись, что твоё сообщение последнее)

vk.method('messages.send', 
			{'user_id':my_id, 
			'message':'Клавиатуру в студию!',
			'keyboard':str(json.dumps(keyboard)) # Делаем из нашего словаря с параметрами клавиатуры json объект
			})									 # Как это работает я понятия не имею. 
												 # Просто передаем словарь с параметрами клавиатуры в соответствующую функцию,
												 # встроенной библиотеки json и получаем результат
'''
