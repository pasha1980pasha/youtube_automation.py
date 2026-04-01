
import webbrowser
import psutil
import time
import pyautogui
import cv2
import os
import logging
import subprocess  # Добавляем модуль для работы с командной строкой

# Настройка логирования
logging.basicConfig(
    filename="debug.log",  # Файл для сохранения логов
    level=logging.DEBUG,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def open_youtube():
    logging.info("Пытаемся открыть YouTube...")
    webbrowser.open("https://www.youtube.com")

def is_browser_opened(browser_name):
    for process in psutil.process_iter(['pid', 'name']):
        if browser_name.lower() in process.info['name'].lower():
            return True
    return False

def record_video():
    output_folder = r"C:\Users\Администратор\Desktop\скрин шоты"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_video_filename = os.path.join(output_folder, "recorded_video.mp4")
    frame_width = 640
    frame_height = 480
    fps = 30
    record_duration = 5

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        logging.error("Ошибка: Камера не доступна.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_filename, fourcc, fps, (frame_width, frame_height))

    logging.info("Камера доступна. Начинаем запись видео...")
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Ошибка: Не удалось получить кадр.")
            break

        out.write(frame)
        cv2.imshow("Recording...", frame)

        if time.time() - start_time >= record_duration:
            logging.info("Запись завершена.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.info(f"Видео сохранено в файл: {output_video_filename}")

    # Открываем папку и выделяем файл
    try:
        subprocess.run(f'explorer /select,"{output_video_filename}"', shell=True)
        logging.info("Папка с видео открыта, файл выделен.")
    except Exception as e:
        logging.error(f"Ошибка при открытии папки: {e}")

def main():
    try:
        open_youtube()
        time.sleep(5)
        
        browser_name = "chrome"
        if is_browser_opened(browser_name):
            logging.info(f"Браузер {browser_name} успешно открыт!")
        else:
            logging.warning(f"Браузер {browser_name} не открылся.")
        
        time.sleep(5)
        
        try:
            # Первый клик
            pyautogui.click(x=2376, y=116)
            logging.info("Клик выполнен по координатам (2376, 116).")
            time.sleep(2)

            # Второй клик
            pyautogui.click(x=2381, y=155)
            logging.info("Клик выполнен по координатам (2381, 155).")
            time.sleep(2)

            # Запись видео
            record_video()

            # Третий клик (новый клик)
            pyautogui.click(x=1908, y=644)
            logging.info("Клик выполнен по координатам (1908, 644).")
            time.sleep(2)

        except Exception as e:
            logging.error(f"Ошибка при выполнении клика: {e}")

    except Exception as e:
        logging.error(f"Ошибка в основной программе: {e}")

if __name__ == "__main__":
    main()
    input("Нажмите Enter для выхода...")  # Ожидание ввода перед закрытием
