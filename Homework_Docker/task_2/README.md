# **Задание: Создайте контейнер для REST API сервера любого вашего проекта из курса по Django**

1. Собрать образ

docker build ./ --tag stockproducts:0.0.1

2. Запустить контейнер

docker run --name my_stockproducts -d -p 8000:8000 stockproducts:0.0.1

