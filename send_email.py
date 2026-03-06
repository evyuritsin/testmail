#!/usr/bin/env python3
"""
Скрипт для отправки писем на email
Поддерживает отправку через SMTP с аутентификацией
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import argparse
from typing import Optional, List


class EmailSender:
    """Класс для отправки электронных писем"""
    
    def __init__(self, smtp_server: str, smtp_port: int, 
                 username: str, password: str, use_tls: bool = True):
        """
        Инициализация отправителя
        
        Args:
            smtp_server: SMTP сервер (например, smtp.gmail.com)
            smtp_port: Порт SMTP сервера (587 для TLS, 465 для SSL)
            username: Имя пользователя/email отправителя
            password: Пароль или app-пароль
            use_tls: Использовать TLS (True) или SSL (False)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        
    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   body: str, 
                   body_type: str = "plain",
                   from_email: Optional[str] = None,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   attachments: Optional[List[str]] = None) -> bool:
        """
        Отправка письма
        
        Args:
            to_email: Email получателя
            subject: Тема письма
            body: Текст письма
            body_type: Тип текста ("plain" или "html")
            from_email: Email отправителя (если None, используется username)
            cc: Список email для копии
            bcc: Список email для скрытой копии
            attachments: Список путей к файлам для вложения
            
        Returns:
            True если отправка успешна, False в противном случае
        """
        try:
            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = from_email or self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Добавляем получателей CC и BCC
            all_recipients = [to_email]
            
            if cc:
                msg['Cc'] = ', '.join(cc)
                all_recipients.extend(cc)
                
            if bcc:
                all_recipients.extend(bcc)
            
            # Добавляем текст письма
            msg.attach(MIMEText(body, body_type))
            
            # Добавляем вложения
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        self._add_attachment(msg, attachment_path)
                    else:
                        print(f"Предупреждение: файл {attachment_path} не найден")
            
            # Подключаемся к SMTP серверу
            if self.use_tls:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.username, self.password)
                    server.send_message(msg, from_addr=msg['From'], to_addrs=all_recipients)
            else:
                # Используем SSL
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg, from_addr=msg['From'], to_addrs=all_recipients)
            
            print(f"Письмо успешно отправлено на {to_email}")
            return True
            
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, filepath: str):
        """Добавляет вложение к сообщению"""
        filename = os.path.basename(filepath)
        
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )
        msg.attach(part)


def send_simple_email(smtp_server: str, smtp_port: int, 
                      username: str, password: str,
                      to_email: str, subject: str, body: str,
                      use_tls: bool = True) -> bool:
    """
    Простая функция для отправки письма без вложений
    
    Args:
        smtp_server: SMTP сервер
        smtp_port: Порт SMTP сервера
        username: Имя пользователя/email отправителя
        password: Пароль
        to_email: Email получателя
        subject: Тема письма
        body: Текст письма
        use_tls: Использовать TLS
        
    Returns:
        True если отправка успешна
    """
    sender = EmailSender(smtp_server, smtp_port, username, password, use_tls)
    return sender.send_email(to_email, subject, body)


def main():
    """Основная функция для работы из командной строки"""
    parser = argparse.ArgumentParser(description='Отправка писем по email')
    parser.add_argument('--config', help='Файл конфигурации (JSON)')
    parser.add_argument('--to', required=True, help='Email получателя')
    parser.add_argument('--subject', required=True, help='Тема письма')
    parser.add_argument('--body', help='Текст письма (можно указать в файле с --body-file)')
    parser.add_argument('--body-file', help='Файл с текстом письма')
    parser.add_argument('--html', action='store_true', help='Использовать HTML формат')
    parser.add_argument('--attachment', action='append', help='Файл для вложения (можно указать несколько раз)')
    parser.add_argument('--cc', help='Email для копии (через запятую)')
    parser.add_argument('--bcc', help='Email для скрытой копии (через запятую)')
    
    # Параметры SMTP (можно указать в конфиге или через аргументы)
    parser.add_argument('--smtp-server', default='smtp.gmail.com', help='SMTP сервер (по умолчанию: smtp.gmail.com)')
    parser.add_argument('--smtp-port', type=int, default=587, help='SMTP порт (по умолчанию: 587)')
    parser.add_argument('--username', help='Имя пользователя/email отправителя')
    parser.add_argument('--password', help='Пароль или app-пароль')
    parser.add_argument('--no-tls', action='store_true', help='Не использовать TLS (использовать SSL)')
    
    args = parser.parse_args()
    
    # Читаем тело письма
    body = args.body
    if args.body_file:
        try:
            with open(args.body_file, 'r', encoding='utf-8') as f:
                body = f.read()
        except Exception as e:
            print(f"Ошибка при чтении файла {args.body_file}: {e}")
            return
    
    if not body:
        print("Ошибка: необходимо указать текст письма через --body или --body-file")
        return
    
    # Проверяем обязательные параметры
    if not args.username or not args.password:
        print("Ошибка: необходимо указать --username и --password")
        return
    
    # Парсим CC и BCC
    cc = args.cc.split(',') if args.cc else None
    bcc = args.bcc.split(',') if args.bcc else None
    
    # Создаем отправитель
    sender = EmailSender(
        smtp_server=args.smtp_server,
        smtp_port=args.smtp_port,
        username=args.username,
        password=args.password,
        use_tls=not args.no_tls
    )
    
    # Отправляем письмо
    success = sender.send_email(
        to_email=args.to,
        subject=args.subject,
        body=body,
        body_type="html" if args.html else "plain",
        cc=cc,
        bcc=bcc,
        attachments=args.attachment
    )
    
    if not success:
        exit(1)


if __name__ == "__main__":
    main()


# Примеры использования:
"""
# Пример 1: Простая отправка через Gmail
python send_email.py \
    --username "ваш.email@gmail.com" \
    --password "ваш-пароль-или-app-пароль" \
    --to "получатель@example.com" \
    --subject "Тестовое письмо" \
    --body "Привет! Это тестовое письмо."

# Пример 2: Отправка с HTML и вложениями
python send_email.py \
    --username "ваш.email@gmail.com" \
    --password "ваш-пароль" \
    --to "получатель@example.com" \
    --subject "Отчет" \
    --body-file "report.html" \
    --html \
    --attachment "report.pdf" \
    --attachment "data.csv"

# Пример 3: Отправка с копиями
python send_email.py \
    --username "ваш.email@gmail.com" \
    --password "ваш-пароль" \
    --to "основной@example.com" \
    --cc "копия1@example.com,копия2@example.com" \
    --bcc "скрытая@example.com" \
    --subject "Важное сообщение" \
    --body "Текст важного сообщения"

# Пример 4: Использование другого SMTP сервера (Yandex)
python send_email.py \
    --smtp-server smtp.yandex.ru \
    --smtp-port 465 \
    --no-tls \
    --username "ваш.login@yandex.ru" \
    --password "ваш-пароль" \
    --to "получатель@example.com" \
    --subject "Письмо с Yandex" \
    --body "Текст письма"
"""