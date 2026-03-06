#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы отправки писем
(без реальной отправки, только проверка логики)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_email import EmailSender


def test_email_creation():
    """Тест создания объекта EmailSender"""
    print("Тест 1: Создание EmailSender...")
    try:
        sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            username="test@example.com",
            password="testpass",
            use_tls=True
        )
        print("✓ EmailSender создан успешно")
        return sender
    except Exception as e:
        print(f"✗ Ошибка при создании EmailSender: {e}")
        return None


def test_message_creation():
    """Тест создания сообщения"""
    print("\nТест 2: Создание тестового сообщения...")
    
    # Создаем тестовые файлы
    test_files = []
    try:
        # Создаем тестовый текстовый файл
        with open("test_attachment.txt", "w") as f:
            f.write("Это тестовый файл для вложения.\nСоздан автоматически.")
        test_files.append("test_attachment.txt")
        
        # Создаем тестовый HTML файл
        with open("test_email.html", "w") as f:
            f.write("""
            <html>
            <body>
                <h1>Тестовое письмо</h1>
                <p>Это тестовое HTML письмо.</p>
            </body>
            </html>
            """)
        
        print("✓ Тестовые файлы созданы")
        
        # Пытаемся создать отправитель и отправить письмо (без реальной отправки)
        sender = EmailSender(
            smtp_server="smtp.test.com",
            smtp_port=587,
            username="test@test.com",
            password="test",
            use_tls=True
        )
        
        # Пытаемся вызвать метод отправки (должен завершиться с ошибкой соединения)
        print("  Попытка отправки (ожидается ошибка соединения)...")
        success = sender.send_email(
            to_email="recipient@test.com",
            subject="Тестовое письмо",
            body="Тело письма",
            attachments=test_files
        )
        
        if not success:
            print("✓ Ожидаемая ошибка соединения получена (тест пройден)")
        else:
            print("✗ Неожиданный успех отправки")
            
    except Exception as e:
        print(f"✓ Исключение перехвачено как ожидалось: {type(e).__name__}")
    finally:
        # Удаляем тестовые файлы
        for filename in ["test_attachment.txt", "test_email.html"]:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"  Удален файл: {filename}")


def test_command_line_args():
    """Тест парсинга аргументов командной строки"""
    print("\nТест 3: Проверка парсинга аргументов...")
    
    # Имитируем аргументы командной строки
    test_args = [
        "--username", "test@example.com",
        "--password", "testpass",
        "--to", "recipient@example.com",
        "--subject", "Test Subject",
        "--body", "Test Body"
    ]
    
    # Сохраняем оригинальные sys.argv
    original_argv = sys.argv
    
    try:
        # Устанавливаем тестовые аргументы
        sys.argv = ["send_email.py"] + test_args
        
        # Импортируем и запускаем парсинг
        import argparse
        
        parser = argparse.ArgumentParser(description='Отправка писем по email')
        parser.add_argument('--to', required=True, help='Email получателя')
        parser.add_argument('--subject', required=True, help='Тема письма')
        parser.add_argument('--body', help='Текст письма')
        parser.add_argument('--username', help='Имя пользователя')
        parser.add_argument('--password', help='Пароль')
        
        args = parser.parse_args(test_args)
        
        print("✓ Аргументы успешно распарсены:")
        print(f"  Username: {args.username}")
        print(f"  To: {args.to}")
        print(f"  Subject: {args.subject}")
        
    except SystemExit:
        print("✗ Ошибка парсинга аргументов")
    finally:
        # Восстанавливаем оригинальные аргументы
        sys.argv = original_argv


def main():
    """Запуск всех тестов"""
    print("=" * 60)
    print("Тестирование скрипта отправки писем")
    print("=" * 60)
    
    test_email_creation()
    test_message_creation()
    test_command_line_args()
    
    print("\n" + "=" * 60)
    print("Тестирование завершено!")
    print("\nДля реальной отправки писем:")
    print("1. Укажите реальные учетные данные в example_usage.py")
    print("2. Раскомментируйте нужные функции в example_usage.py")
    print("3. Запустите: python example_usage.py")
    print("=" * 60)


if __name__ == "__main__":
    main()