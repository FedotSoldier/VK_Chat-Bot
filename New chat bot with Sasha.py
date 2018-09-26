import vk_api
import time
import json

token = 'ea8d297a72d3e516eab6f27152e1204cb4cdca86f5518622d7d49981363fd45e98fd0f2b0215954d854a0'
# Сменить токен. У меня старый телефон и не могу указать ключ доступа для новой беседы.
vk=vk_api.VkApi(token=token)
vk._auth_token() # vk.auth() не работает

print(  # Получаем информацию о чате.
		vk.method('messages.getConversations')
		)

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
# Я уже устал, а мне еще литру нам делать с другими дз. Так что я заливаю на GitHub и хватит на сегодня
