import socket
import sys
import threading
import time
import pygame

# ==========================================
# 1. НАСТРОЙКИ СЕТИ И ПОДКЛЮЧЕНИЯ
# ==========================================
IP_ADDRESS = 'tunnel.lhrtunnel.link'
PORT = 80

# ==========================================
# 2. ГРАФИКА И ИНТЕРФЕЙС (Pygame)
# ==========================================
def run_gui():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Danigram")
    font = pygame.font.SysFont("Arial", 18)

    messages = ["[Система]: Приложение Danigram запущено."]
    input_text = ""
    MY_NAME = "Данила"
    
    # Создаем интернет-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ЗАЩИТА ОТ ВЫЛЕТОВ: если сервер в облаке спит, приложение НЕ упадет
    client_socket.settimeout(3.0) 
    
    try:
        client_socket.connect((IP_ADDRESS, PORT))
        messages.append("[Система]: Подключение установлено!")
        client_socket.settimeout(None) # Возвращаем в обычный режим
    except Exception as e:
        messages.append("[Система]: Ошибка сети. Облачный сервер выключен!")
        print(f"Лог сетевой ошибки: {e}")

    def receive_messages():
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if msg:
                    messages.append(msg)
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()
    clock = pygame.time.Clock()
    pygame.key.start_text_input()

    running = True
    while running:
        screen.fill((240, 240, 240)) # Серый фон чата
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.stop_text_input()
                running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Нажали Enter на клавиатуре
                    msg_to_send = input_text.strip()
                    if msg_to_send:
                        try:
                            # Сообщения отправляются с вашим ником
                            full_msg = f"{MY_NAME}: {msg_to_send}"
                            client_socket.send(full_msg.encode('utf-8'))
                            input_text = ""
                        except:
                            messages.append("[Система]: Ошибка отправки.")
                elif event.key == pygame.K_BACKSPACE:  # Стирание текста
                    input_text = input_text[:-1]
            
            elif event.type == pygame.TEXTINPUT:  # Перехват букв с клавиатуры Android
                input_text += event.text

        # Ваша идеальная отрисовка сообщений в одну строчку
        y_offset = 20
        for text in messages[-20:]:
            цвет = (255, 59, 48) if "@" in text else (30, 30, 30)
            screen.blit(font.render(text, True, цвет), (20, y_offset))
            y_offset += 25

        # Рисуем красивое поле ввода
        pygame.draw.rect(screen, (255, 255, 255), (10, 540, 380, 40), border_radius=5)
        pygame.draw.rect(screen, (0, 122, 255), (10, 540, 380, 40), width=2, border_radius=5)
        
        # Отображаем текущий вводимый текст
        input_surf = font.render(input_text, True, (30, 30, 30))
        screen.blit(input_surf, (20, 550))

        pygame.display.flip()
        clock.tick(30)

# ==========================================
# 3. ЗАПУСК ВСЕЙ СИСТЕМЫ
# ==========================================
if __name__ == "__main__":
    run_gui()
.