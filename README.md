# SIPNET Balance для Home Assistant

Интеграция получает баланс SIPNET и публикует его как сенсор Home Assistant.

## Возможности

- настройка SIP UID и пароля через Config Flow;
- периодический опрос баланса;
- ручное обновление через `sipnet_balance.refresh`;
- диагностическое состояние доступности;
- локальные иконка и логотип.

## Установка

Через HACS добавьте `bezuglyy/sipnet_balance` как Integration. Вручную скопируйте `custom_components/sipnet_balance` в `/config/custom_components/` и перезапустите HA.

## Архитектура и безопасность

`config_flow.py` создаёт запись, `sensor.py` выполняет запрос баланса, `__init__.py` регистрирует сервис обновления. Пароль сохраняется в Config Entry и не должен публиковаться в issue, логе или README.

## Лицензия

MIT.
