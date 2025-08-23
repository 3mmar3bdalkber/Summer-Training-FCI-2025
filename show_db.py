import sqlite3

DB_NAME = "store.db"   # أو database.db حسب اسم الملف عندك

def show_all_tables_and_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # جلب أسماء الجداول
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    print("📌 الجداول الموجودة:")
    for (table,) in tables:
        print(f"\n===== جدول {table} =====")

        # جلب الأعمدة
        c.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in c.fetchall()]
        print("الأعمدة:", columns)

        # جلب البيانات
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    show_all_tables_and_data()
