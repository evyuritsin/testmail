#!/usr/bin/env python3
"""
Примеры использования скрипта отправки писем
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_email import EmailSender, send_simple_email


def example_simple_gmail():
    """Пример простой отправки через Gmail"""
    print("Пример 1: Простая отправка через Gmail")
    
    # Настройки для Gmail
    # ВАЖНО: для Gmail нужно использовать app-пароль, если включена двухфакторная аутентификация
    # Или разрешить "ненадежные приложения" в настройках аккаунта Google
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "ваш.email@gmail.com"  # Замените на ваш email
    password = "ваш-app-пароль"       # Замените на ваш пароль или app-пароль
    
    to_email = "получатель@example.com"  # Замените на email получателя
    subject = "Тестовое письмо из Python"
    body = """
    Привет!
    
    Это тестовое письмо, отправленное с помощью Python скрипта.
    
    С уважением,
    Python скрипт
    """
    
    # Отправляем письмо
    success = send_simple_email(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password,
        to_email=to_email,
        subject=subject,
        body=body
    )
    
    if success:
        print("✓ Письмо успешно отправлено!")
    else:
        print("✗ Ошибка при отправке письма")


def example_with_attachments():
    """Пример отправки с вложениями"""
    print("\nПример 2: Отправка с вложениями")
    
    # Создаем тестовые файлы для вложения
    test_files = ["test1.txt", "test2.txt"]
    
    for filename in test_files:
        with open(filename, "w") as f:
            f.write(f"Это содержимое файла {filename}\nСоздано для теста отправки писем.")
    
    # Настройки (замените на свои)
    sender = EmailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="ваш.email@gmail.com",  # Замените
        password="ваш-пароль",           # Замените
        use_tls=True
    )
    
    # Отправляем письмо с вложениями
    success = sender.send_email(
        to_email="получатель@example.com",  # Замените
        subject="Письмо с вложениями",
        body="Привет! В этом письме есть вложения.",
        attachments=test_files
    )
    
    # Удаляем тестовые файлы
    for filename in test_files:
        if os.path.exists(filename):
            os.remove(filename)
    
    if success:
        print("✓ Письмо с вложениями успешно отправлено!")
    else:
        print("✗ Ошибка при отправке письма с вложениями")


def example_html_email():
    """Пример отправки HTML письма"""
    print("\nПример 3: Отправка HTML письма")
    
    sender = EmailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="ваш.email@gmail.com",  # Замените
        password="ваш-пароль",           # Замените
        use_tls=True
    )
    
    html_body = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background-color: #4CAF50; color: white; padding: 20px; }
            .content { padding: 20px; }
            .footer { background-color: #f1f1f1; padding: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Приветствие!</h1>
        </div>
        <div class="content">
            <p>Это <strong>HTML письмо</strong>, отправленное с помощью Python.</p>
            <p>Вы можете использовать HTML для красивого оформления писем.</p>
            <ul>
                <li>Пункт 1</li>
                <li>Пункт 2</li>
                <li>Пункт 3</li>
            </ul>
        </div>
        <div class="footer">
            <p>© 2024 Python Email Sender</p>
        </div>
    </body>
    </html>
    """
    
    success = sender.send_email(
        to_email="получатель@example.com",  # Замените
        subject="HTML письмо",
        body=html_body,
        body_type="html"
    )
    
    if success:
        print("✓ HTML письмо успешно отправлено!")
    else:
        print("✗ Ошибка при отправке HTML письма")


def example_yandex_mail():
    """Пример отправки через Yandex Mail"""
    print("\nПример 4: Отправка через Yandex Mail")
    
    # Yandex использует SSL на порту 465
    sender = EmailSender(
        smtp_server="smtp.yandex.ru",
        smtp_port=465,
        username="ваш.login@yandex.ru",  # Замените
        password="ваш-пароль",           # Замените
        use_tls=False  # Yandex использует SSL, не TLS
    )
    
    success = sender.send_email(
        to_email="получатель@example.com",  # Замените
        subject="Письмо с Yandex",
        body="Это письмо отправлено через SMTP сервер Yandex."
    )
    
    if success:
        print("✓ Письмо через Yandex успешно отправлено!")
    else:
        print("✗ Ошибка при отправке письма через Yandex")


def main():
    """Запуск всех примеров"""
    print("=" * 60)
    print("Примеры использования скрипта отправки писем")
    print("=" * 60)
    print("\nПРИМЕЧАНИЕ: Для работы примеров нужно:")
    print("1. Заменить email и пароль в коде на свои")
    print("2. Для Gmail: использовать app-пароль если включена 2FA")
    print("3. Убедиться, что SMTP доступен для вашего почтового сервиса")
    print("=" * 60)
    
    # Запускаем примеры (закомментированы, так как требуют реальных учетных данных)
    print("\nПримеры кода готовы к использованию.")
    print("Раскомментируйте нужные функции в коде и укажите свои учетные данные.")
    
    # Раскомментируйте нужные примеры:
    # example_simple_gmail()
    # example_with_attachments()
    # example_html_email()
    # example_yandex_mail()
    
    print("\n" + "=" * 60)
    print("Также вы можете использовать скрипт из командной строки:")
    print("\nБазовое использование:")
    print('python send_email.py --username "ваш@email.com" --password "пароль" \\')
    print('  --to "получатель@example.com" --subject "Тема" --body "Текст письма"')
    
    print("\nС HTML и вложениями:")
    print('python send_email.py --username "ваш@email.com" --password "пароль" \\')
    print('  --to "получатель@example.com" --subject "Отчет" \\')
    print('  --body-file "report.html" --html --attachment "file1.pdf" --attachment "file2.csv"')


if __name__ == "__main__":
    main()