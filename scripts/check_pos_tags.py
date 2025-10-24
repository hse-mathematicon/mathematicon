import sqlite3

def check_pos_tags():
    conn = sqlite3.connect("data/mathematicon.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT tag, name_ru, name_en FROM pos_tags")
    tags = cursor.fetchall()
    
    print("Теги в базе данных:")
    for tag in tags:
        print(f"{tag[0]}: {tag[1]} ({tag[2]})")
    
    print(f"\nВсего тегов: {len(tags)}")
    conn.close()

if __name__ == "__main__":
    check_pos_tags()