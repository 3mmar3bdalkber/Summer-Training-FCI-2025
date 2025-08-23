from database import get_db_connection

def delete_all_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("تم حذف كل الحسابات بنجاح.")

if __name__ == "__main__":
    delete_all_users()
