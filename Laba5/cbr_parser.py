import requests
from bs4 import BeautifulSoup
import urllib3
from config import CBR_DAILY_URL

# Отключаем предупреждения об отсутствии SSL-сертификата.
# Это необходимо, так как для доступа к cbr.ru могут понадобиться корневые сертификаты РФ
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_currency_rate(currency_code: str) -> str:
    """
    Получает текущий курс указанной валюты с официального сайта ЦБ РФ.
    
    :param currency_code: Буквенный код валюты (например, 'USD', 'EUR', 'CNY').
    :return: Строка с информацией о курсе или сообщение об ошибке.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Отправляем GET-запрос к странице с ежедневными курсами валют
        # Использование verify=False обходит ошибки SSL-сертификата (свойственно государственным сайтам)
        response = requests.get(CBR_DAILY_URL, headers=headers, verify=False)
        response.raise_for_status() # Проверяем, что запрос завершился успешно (статус 200)
        
        # Разбираем HTML-код страницы
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # На сайте ЦБ таблица с валютами обычно имеет класс 'data'
        table = soup.find('table', class_='data')
        if not table:
            return "Ошибка: Не удалось найти таблицу с курсами валют на сайте."
        
        # Ищем все строки таблицы, пропуская первую строку с заголовками
        rows = table.find_all('tr')[1:]
        
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 5:
                # Столбцы таблицы на сайте ЦБ:
                # 0: Цифр. код
                # 1: Букв. код
                # 2: Единиц
                # 3: Валюта
                # 4: Курс
                current_code = columns[1].text.strip()
                
                if current_code == currency_code.upper():
                    nominal = columns[2].text.strip()
                    name = columns[3].text.strip()
                    rate = columns[4].text.strip()
                    
                    return f"За {nominal} {name} дают {rate} рублей."
        
        return f"Валюта с кодом {currency_code} не найдена в таблице ЦБ."
        
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при подключении к сайту ЦБ: {e}"
    except Exception as e:
        return f"Внутренняя ошибка парсера: {e}"
