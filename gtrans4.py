import asyncio
from translator_pkg import NAME, AUTHOR
from translator_pkg.mod_gtrans4 import TransLate, LangDetect, CodeLang, LanguageList


async def main():
    print(f"Пакет: {NAME}")
    print(f"Автор: {AUTHOR}")

    print("1. Переклад тексту:")
    print(await TransLate("Добрий день", "uk", "en"))

    print("2. Визначення мови:")
    print(await LangDetect("Добрий день", "all"))

    print("3. Код мови Estonian:")
    print(CodeLang("estonian"))

    print("4. Назва мови et:")
    print(CodeLang("et"))

    print("5. Таблиця мов:")
    print(await LanguageList("screen", "Добрий день"))


if __name__ == "__main__":
    asyncio.run(main())