import os
import json
import re
import asyncio
from translator_pkg.mod_gtrans4 import TransLate as tr4, LangDetect as ld4, CodeLang as cl4
from translator_pkg.mod_deep import TransLate as trd, LangDetect as ldd, CodeLang as cld


def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s.strip()]


async def main():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        input_file = config["input_file"]
        target_lang = config["target_lang"]
        module_name = config["module"]
        output_mode = config["output"]
        sentence_count = config["sentence_count"]

        if not os.path.exists(input_file):
            print("Помилка: файл не знайдено")
            return

        file_size = os.path.getsize(input_file)

        with open(input_file, "r", encoding="utf-8") as f:
            full_text = f.read()

        char_count = len(full_text)
        all_sentences = split_sentences(full_text)
        total_sentences = len(all_sentences)

        sample_text = " ".join(all_sentences[:sentence_count])

        if module_name == "mod_gtrans4":
            translate_func = tr4
            detect_func = ld4
            code_func = cl4
        elif module_name == "mod_deep":
            translate_func = trd
            detect_func = ldd
            code_func = cld
        else:
            print("Помилка: невідомий модуль у config.json")
            return

        lang_info = await detect_func(full_text, "lang")

        print(f"Назва файлу: {input_file}")
        print(f"Розмір файлу: {file_size} байт")
        print(f"Кількість символів: {char_count}")
        print(f"Кількість речень: {total_sentences}")
        print(f"Мова тексту: {lang_info}")

        translated_text = await translate_func(sample_text, "auto", target_lang)

        lang_name = code_func(target_lang)

        if output_mode == "screen":
            print(f"Мова перекладу: {lang_name}")
            print(f"Модуль перекладу: {module_name}")
            print("Перекладений текст:")
            print(translated_text)

        elif output_mode == "file":
            base_name, ext = os.path.splitext(input_file)
            output_file = f"{base_name}_{target_lang}{ext}"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(translated_text)

            print("Ok")
        else:
            print("Помилка: output має бути 'screen' або 'file'")

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    asyncio.run(main())