# Технические требования #

Сервис:
- реализует спецификацию API, описанную в файле <code>openapi.yaml</code>, и корректно отвечает на запросы проверяющей системы
- сервис должен быть развернут в контейнере на адресе `0.0.0.0:80`
- сервис должен обеспечивать персистентность данных (должен сохранять состояние данных при перезапуске)
- сервис должен обладать возможностью автоматического перезапуска при рестарте системы
- после запуска сервиса время ответа сервиса на все методы API не должно превышать 1 секунду
- время полного старта сервиса не должно превышать 1 минуту
- импорт и удаление данных не превосходит 1000 элементов в 1 минуту
- RPS (Request per second) получения истории, недавних изменений и информации об элементе суммарно не превосходит 100 запросов в секунду

# Как развернуть №

(очень просто - вручную)

- Склонировать репозиторий 
- Скопировать файл enrollment.service в systemd
- Пнуть Димона: systemctl daemon-reload

# Запуск #

- Запустить сервис: docker-compose up -d (Из директории с проектом)
- Применить миграции (Если необходимо): docker exec {контейнер} enrollment-db upgrade head
