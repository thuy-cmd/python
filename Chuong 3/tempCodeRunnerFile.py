# B1. Kết nối CSDL
import sqlite3

conn = sqlite3.connect('example.db')

# B2. Tạo con trỏ
cursor = conn.cursor()

# B3. Tạo bảng
cursor.execute("""
CREATE TABLE IF NOT EXISTS sinhvien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hoten TEXT,
    namsinh INTEGER,
    lop TEXT
)
""")

# B4. Thêm dữ liệu
# cursor.execute("INSERT INTO sinhvien (hoten, namsinh, lop) VALUES (?, ?, ?)", ('Nguyen Van A', 2000, 'CTK42'))
# cursor.execute("INSERT INTO sinhvien (hoten, namsinh, lop) VALUES (?, ?, ?)", ('Tran Thi B', 2001, 'CTK43'))
# cursor.execute("INSERT INTO sinhvien (hoten, namsinh, lop) VALUES (?, ?, ?)", ('Le Van C', 2000, 'CTK42'))

# B5. Lưu thay đổi
conn.commit()

# B6. Truy vấn dữ liệu
cursor.execute("SELECT * FROM sinhvien")

rows = cursor.fetchall()
for row in rows:
    print(row)

# B7. Đóng kết nối
conn.close()
