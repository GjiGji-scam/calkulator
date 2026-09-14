"""
🧮 ИИ-Калькулятор
Простые примеры считает локально, сложные — через ИИ (Groq).
"""

import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "Ты — математический калькулятор. Решай примеры точно. "
    "Отвечай кратко: сначала ответ, потом одна строка с решением."
)

BANNER = """
╔══════════════════════════════════════════╗
║        🧮  ИИ-Калькулятор  v1.0          ║
╚══════════════════════════════════════════╝
Примеры:
  • 2 + 2 * 10
  • сколько будет корень из 144?
  • реши уравнение 2x + 5 = 17
Введи 'exit' для выхода.
"""

EXIT_WORDS = {"exit", "quit", "выход", "q"}
_ALLOWED = re.compile(r"^[\d\s+\-*/().,]+$")


def local_calc(expression):
    if not expression or not _ALLOWED.fullmatch(expression):
        return None
    try:
        return eval(expression.replace(",", "."), {"__builtins__": {}}, {})
    except Exception:
        return None


def ask_ai(client, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def main():
    print(BANNER)

    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key) if api_key else None

    if not client:
        print("⚠️  GROQ_API_KEY не найден — работает только локальный режим.\n")

    while True:
        try:
            user_input = input("Ты: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока! 👋")
            break

        if not user_input:
            continue
        if user_input.lower() in EXIT_WORDS:
            print("Пока! 👋")
            break

        result = local_calc(user_input)
        if result is not None:
            print(f"🤖 Калькулятор: {result}\n")
            continue

        if not client:
            print("⚠️  Нужен ИИ, но ключ не задан.\n")
            continue

        try:
            print(f"🤖 ИИ: {ask_ai(client, user_input)}\n")
        except Exception as e:
            print(f"⚠️  Ошибка ИИ: {e}\n")


if __name__ == "__main__":
    main()