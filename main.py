import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from groq_ai import *
from TTS import *
import base64

# Функция для автоматического воспроизведения аудио в Streamlit
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()

    # Конвертируем аудиофайл в base64
    b64 = base64.b64encode(data).decode()

    # Создаём HTML-код для автоматического воспроизведения аудио
    md = f"""
    <audio controls autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    # Встраиваем аудио в Streamlit
    st.markdown(md, unsafe_allow_html=True)

# Основная функция для запуска Streamlit приложения
def main():
    st.title("Разговорный ассистент с AI")
    st.write("Нажмите на кнопку ниже, чтобы начать запись.")

    # Инициализируем кнопку
    stt_button = Button(label="Говорить", width=100)
   

    # Обрабатываем события нажатия кнопки с помощью JavaScript
    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'ru-RU';  // Устанавливаем язык на русский

        recognition.onresult = function(e) {
            var value = '';
            for (var i = e.resultIndex; i < e.results.length; i++) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }

            if (value !== '') {
                document.dispatchEvent(new CustomEvent("GET_TEXT", { detail: value }));
            }
        };

        recognition.start();
    """))

    # Используем события Bokeh для прослушивания голосового ввода
    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0
    )

    # Обрабатываем результаты событий
    if result:
        if "GET_TEXT" in result:
            user_input = result["GET_TEXT"]
            response = generate_response(user_input)  # Генерируем ответ с помощью AI-модели
            file = TTS(response)  # Конвертируем текстовый ответ в речь
            autoplay_audio(file)  # Проигрываем сгенерированный аудиофайл

# Запускаем основную функцию при выполнении этого скрипта
if __name__ == '__main__':
    main()
