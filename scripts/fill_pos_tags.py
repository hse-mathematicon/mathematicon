import sqlite3
from pathlib import Path

def fill_pos_tags():
    """Заполняем таблицу pos_tags тегами из документации"""
    
    # Теги из вашей картинки
    pos_tags_data = [
        # (tag, info_url, name_ru, name_en, examples)
        ("ADJ", "https://universaldependencies.org/u/pos/ADJ.html", "прилагательное", "adjective", "типовой, высокий, максимальный"),
        ("ADP", "https://universaldependencies.org/u/pos/ADP.html", "адпозиция", "adposition", "в, на, плюс, минус"),
        ("ADV", "https://universaldependencies.org/u/pos/ADV.html", "наречие", "adverb", "легко, очень, вверх"),
        ("AUX", "https://universaldependencies.org/u/pos/AUX.html", "вспомогательный глагол", "auxiliary", "быть, есть, бы"),
        ("CCONJ", "https://universaldependencies.org/u/pos/CCONJ.html", "сочинительный союз", "coordinating conjunction", "но, и, или"),
        ("DET", "https://universaldependencies.org/u/pos/DET.html", "детерминатив", "determiner", "этот, моя, такая"),
        ("INTJ", "https://universaldependencies.org/u/pos/INTJ.html", "междометие", "interjection", "None"),
        ("NOUN", "https://universaldependencies.org/u/pos/NOUN.html", "существительное", "noun", "мыслитель, знаменатель, вопрос"),
        ("NUM", "https://universaldependencies.org/u/pos/NUM.html", "числительное", "numeral", "три, шесть, один"),
        ("PART", "https://universaldependencies.org/u/pos/PART.html", "частица", "particle", "вот, же, ну"),
        ("PRON", "https://universaldependencies.org/u/pos/PRON.html", "местоимение", "pronoun", "я, вы, который"),
        ("PROPN", "https://universaldependencies.org/u/pos/PROPN.html", "имя собственное", "proper noun", "Коши, Ньютон"),
        ("PTCP", "https://universaldependencies.org/u/pos/VERB.html", "причастие", "participle", "стремищийся, изображённый"),
        ("PUNCT", "https://universaldependencies.org/u/pos/PUNCT.html", "пунктуация", "punctuation", ". ?"),
        ("SCONJ", "https://universaldependencies.org/u/pos/SCONJ.html", "подчинительный союз", "subordinating conjunction", "если, как, что"),
        ("VERB", "https://universaldependencies.org/u/pos/VERB.html", "глагол", "verb", "разобрать, вынести, умножить"),
        ("X", "https://universaldependencies.org/u/pos/X.html", "неопределенный", "other", "эн, бэ, цэ")
    ]
    
    # Путь к базе данных
    db_path = Path("data/mathematicon.db")
    
    if not db_path.exists():
        print("База данных не найдена!")
        return
    
    # Подключаемся к базе
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Вставляем данные
        for tag_data in pos_tags_data:
            cursor.execute("""
                INSERT OR IGNORE INTO pos_tags (tag, info_url, name_ru, name_en, examples)
                VALUES (?, ?, ?, ?, ?)
            """, tag_data)
        
        conn.commit()
        print(f"Успешно добавлено {len(pos_tags_data)} тегов")
        
        # Проверяем что добавилось
        cursor.execute("SELECT COUNT(*) FROM pos_tags")
        count = cursor.fetchone()[0]
        print(f"Всего тегов в базе: {count}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fill_pos_tags()