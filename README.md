# Python Email Sender

Скрипт для отправки писем на email через SMTP протокол.

## Возможности

- Отправка простых текстовых писем
- Отправка HTML писем
- Вложения файлов
- Копии (CC) и скрытые копии (BCC)
- Поддержка TLS/SSL
- Работа с различными почтовыми сервисами (Gmail, Yandex, Mail.ru и др.)
- Командная строка и программный интерфейс

## Требования

- Python 3.6+
- Стандартные библиотеки Python (не требует установки дополнительных пакетов)

## Установка

1. Скопируйте файлы в нужную директорию:
   ```bash
   git clone <репозиторий>
   cd python-email-sender
   ```

2. Убедитесь, что у вас есть Python 3:
   ```bash
   python3 --version
   ```

## Настройка почтового сервиса

### Gmail
1. Войдите в свой аккаунт Google
2. Если включена двухфакторная аутентификация:
   - Перейдите в [Управление аккаунтом Google](https://myaccount.google.com/)
   - Безопасность → Вход в Google → Пароли приложений
   - Создайте пароль для приложения (выберите "Другое" и введите название)
   - Используйте этот пароль в скрипте
3. Если двухфакторная аутентификация отключена:
   - Разрешите "ненадежные приложения" в [настройках безопасности](https://myaccount.google.com/security)

### Yandex Mail
1. Включите IMAP в настройках почты
2. Используйте пароль от почты
3. SMTP сервер: `smtp.yandex.ru`, порт: 465 (SSL)

### Mail.ru
1. Включите IMAP в настройках почты
2. Используйте пароль от почты
3. SMTP сервер: `smtp.mail.ru`, порт: 465 (SSL)

## Использование

### Командная строка

#### Базовое использование:
```bash
python send_email.py \
  --username "ваш.email@gmail.com" \
  --password "ваш-пароль" \
  --to "получатель@example.com" \
  --subject "Тема письма" \
  --body "Текст письма"
```

#### С HTML и вложениями:
```bash
python send_email.py \
  --username "ваш.email@gmail.com" \
  --password "ваш-пароль" \
  --to "получатель@example.com" \
  --subject "Отчет" \
  --body-file "report.html" \
  --html \
  --attachment "file1.pdf" \
  --attachment "file2.csv" \
  --cc "копия1@example.com,копия2@example.com" \
  --bcc "скрытая@example.com"
```

#### Чтение тела письма из файла:
```bash
python send_email.py \
  --username "ваш.email@gmail.com" \
  --password "ваш-пароль" \
  --to "получатель@example.com" \
  --subject "Письмо из файла" \
  --body-file "message.txt"
```

#### Использование другого SMTP сервера (Yandex):
```bash
python send_email.py \
  --smtp-server smtp.yandex.ru \
  --smtp-port 465 \
  --no-tls \
  --username "ваш.login@yandex.ru" \
  --password "ваш-пароль" \
  --to "получатель@example.com" \
  --subject "Письмо с Yandex" \
  --body "Текст письма"
```

### Программный интерфейс (API)

#### Простая отправка:
```python
from send_email import send_simple_email

success = send_simple_email(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="ваш.email@gmail.com",
    password="ваш-пароль",
    to_email="получатель@example.com",
    subject="Тема письма",
    body="Текст письма"
)
```

#### Расширенная отправка с вложениями:
```python
from send_email import EmailSender

# Создаем отправитель
sender = EmailSender(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="ваш.email@gmail.com",
    password="ваш-пароль",
    use_tls=True
)

# Отправляем письмо
success = sender.send_email(
    to_email="получатель@example.com",
    subject="Письмо с вложениями",
    body="Текст письма",
    body_type="html",  # или "plain"
    cc=["копия1@example.com", "копия2@example.com"],
    bcc=["скрытая@example.com"],
    attachments=["file1.pdf", "file2.txt"]
)
```

## Примеры

Смотрите файл `example_usage.py` для подробных примеров использования:

```bash
python example_usage.py
```

## Параметры командной строки

```
--to EMAIL              Email получателя (обязательно)
--subject TEXT          Тема письма (обязательно)
--body TEXT             Текст письма
--body-file FILE        Файл с текстом письма
--html                  Использовать HTML формат
--attachment FILE       Файл для вложения (можно указать несколько раз)
--cc EMAILS             Email для копии (через запятую)
--bcc EMAILS            Email для скрытой копии (через запятую)
--smtp-server SERVER    SMTP сервер (по умолчанию: smtp.gmail.com)
--smtp-port PORT        SMTP порт (по умолчанию: 587)
--username USER         Имя пользователя/email отправителя
--password PASS         Пароль или app-пароль
--no-tls                Не использовать TLS (использовать SSL)
--config FILE           Файл конфигурации (JSON)
```

## Конфигурационный файл

Вы можете создать файл конфигурации `config.json`:

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "ваш.email@gmail.com",
  "password": "ваш-пароль",
  "use_tls": true,
  "default_from": "ваш.email@gmail.com"
}
```

И использовать его:
```bash
python send_email.py --config config.json --to ... --subject ... --body ...
```

## Безопасность

1. **Не храните пароли в коде** - используйте переменные окружения или файлы конфигурации
2. **Используйте app-пароли** для сервисов с двухфакторной аутентификацией
3. **Удаляйте чувствительную информацию** из истории Git
4. **Используйте TLS/SSL** для шифрования соединения

### Использование переменных окружения:
```bash
export EMAIL_USER="ваш.email@gmail.com"
export EMAIL_PASS="ваш-пароль"

python send_email.py \
  --username "$EMAIL_USER" \
  --password "$EMAIL_PASS" \
  --to "получатель@example.com" \
  --subject "Тема" \
  --body "Текст"
```

## Устранение неполадок

### Ошибка аутентификации
- Проверьте правильность логина и пароля
- Для Gmail: используйте app-пароль если включена 2FA
- Убедитесь, что разрешены "ненадежные приложения"

### Ошибка соединения
- Проверьте настройки брандмауэра
- Убедитесь, что SMTP порт открыт
- Проверьте правильность SMTP сервера и порта

### Письмо не доставляется
- Проверьте папку "Спам" у получателя
- Убедитесь, что email получателя правильный
- Проверьте логи SMTP сервера (если доступны)

## Лицензия

MIT

## Автор

Скрипт создан для удобной отправки писем из Python приложений.