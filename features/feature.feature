Feature: Парсинг ru.investing.com
Scenario: Открытие сайта ru.investing.com
  Given Запущен драйвер chromedriver
  Then Переходим по адресу 'https://ru.investing.com/'
  Then Переходим в меню 'Акции'
  Then Переходим в меню 'Россия'
  Then Проверяем заголовок по имени 'Россия - акции'
  Then Получаем таблицу с котировками с сайта
