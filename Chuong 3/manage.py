import sqlite3
import os

def createTable(conn, create_table_sql):
    """ Tạo một bảng từ câu lệnh create_table_sql
    (Đã sửa lại để nhận connection làm tham số)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        print(f"Tạo thành công bảng hoặc bảng đã tồn tại.")
    except sqlite3.Error as e:
        print(e)

def insertData(conn, data):
    """ Thêm dữ liệu vào bảng, data là một danh sách các lệnh INSERT """
    try:
        cursor = conn.cursor()
        for item in data:
            cursor.execute(item)
        conn.commit()
        print(f"Đã thực thi thành công {len(data)} lệnh.")
    except sqlite3.Error as e:
        print(f"Có lỗi xảy ra: {e}")
        conn.rollback()

# def main():
#     database_file = "thu_vien.db"

#     # Xóa file database cũ nếu tồn tại để chạy lại từ đầu
#     if os.path.exists(database_file):
#         os.remove(database_file)
#         print(f"Đã xóa database cũ: {database_file}")

#     # Tạo kết nối mới
#     connect = sqlite3.connect(database_file)
#     print(f"Đã tạo và kết nối tới {database_file}")

#     # --- Định nghĩa các câu lệnh SQL ---

#     danh_muc_sach_sql = """ CREATE TABLE IF NOT EXISTS danhmucsach (
#                                         MaSach INTEGER PRIMARY KEY AUTOINCREMENT,
#                                         TenSach TEXT NOT NULL,
#                                         TacGia TEXT,
#                                         NamXuatBan INTEGER,
#                                         TheLoai TEXT,
#                                         SoLuong INTEGER NOT NULL DEFAULT 1
#                                     ); """

#     doc_gia_sql = """CREATE TABLE IF NOT EXISTS docgia (
#                                     MaDocGia INTEGER PRIMARY KEY AUTOINCREMENT,
#                                     HoTen TEXT NOT NULL,
#                                     NgaySinh TEXT,
#                                     DiaChi TEXT,
#                                     SoDienThoai TEXT UNIQUE
#                                 );"""

#     phieu_muon_sql = """CREATE TABLE IF NOT EXISTS phieumuon (
#                                     SoPhieuMuon INTEGER PRIMARY KEY AUTOINCREMENT,
#                                     MaDocGia INTEGER NOT NULL,
#                                     NgayMuon TEXT NOT NULL,
#                                     FOREIGN KEY (MaDocGia) REFERENCES docgia (MaDocGia)
#                                 );"""

#     chi_tiet_phieu_muon_sql = """CREATE TABLE IF NOT EXISTS chitietphieumuon (
#                                             SoPhieuMuon INTEGER NOT NULL,
#                                             MaSach INTEGER NOT NULL,
#                                             NgayTraDuKien TEXT,
#                                             NgayTraThucTe TEXT,
#                                             TrangThai TEXT NOT NULL,
#                                             PRIMARY KEY (SoPhieuMuon, MaSach),
#                                             FOREIGN KEY (SoPhieuMuon) REFERENCES phieumuon (SoPhieuMuon),
#                                             FOREIGN KEY (MaSach) REFERENCES danhmucsach (MaSach)
#                                         );"""

#     # --- Dữ liệu mẫu ---
#     docgia_data = [
#         ('Nguyễn Văn An', '1995-05-20', 'Hà Nội', '0912345678'),
#         ('Trần Thị Bình', '2001-11-12', 'TP. Hồ Chí Minh', '0987654321'),
#         ('Lê Minh Cường', '1998-02-01', 'Đà Nẵng', '0905112233')
#     ]
#     sach_data = [
#         ('Lão Hạc', 'Nam Cao', 1943, 'Truyện ngắn', 10),
#         ('Số Đỏ', 'Vũ Trọng Phụng', 1936, 'Tiểu thuyết', 5),
#         ('Lập trình Python', 'Nhiều tác giả', 2022, 'Sách kỹ thuật', 15),
#         ('Nhà Giả Kim', 'Paulo Coelho', 1988, 'Tiểu thuyết', 20),
#         ('Đắc Nhân Tâm', 'Dale Carnegie', 1936, 'Sách kỹ năng', 30)
#     ]
#     phieumuon_data = [(1, '2025-10-01'), (2, '2025-10-05'), (1, '2025-10-10')]
#     chitietphieumuon_data = [
#         (1, 1, '2025-10-08', '2025-10-07', 'Đã trả'), (1, 3, '2025-10-08', None, 'Chưa trả'),
#         (2, 4, '2025-10-12', None, 'Chưa trả'), (3, 5, '2025-10-17', None, 'Chưa trả')
#     ]

#     # --- Chuyển đổi dữ liệu sang chuỗi lệnh SQL ---
#     docgia_sql_strings = [f"INSERT INTO docgia(HoTen, NgaySinh, DiaChi, SoDienThoai) VALUES('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}');" for i in docgia_data]
#     sach_sql_strings = [f"INSERT INTO danhmucsach(TenSach, TacGia, NamXuatBan, TheLoai, SoLuong) VALUES('{i[0]}', '{i[1]}', {i[2]}, '{i[3]}', {i[4]});" for i in sach_data]
#     phieumuon_sql_strings = [f"INSERT INTO phieumuon(MaDocGia, NgayMuon) VALUES({i[0]}, '{i[1]}');" for i in phieumuon_data]
#     chitietphieumuon_sql_strings = [f"INSERT INTO chitietphieumuon(SoPhieuMuon, MaSach, NgayTraDuKien, NgayTraThucTe, TrangThai) VALUES({i[0]}, {i[1]}, '{i[2]}', {'NULL' if i[3] is None else f"'{i[3]}'" }, '{i[4]}');" for i in chitietphieumuon_data]

#     # --- Thực thi ---

#     # 1. Tạo các bảng
#     print("\n--- BƯỚC 1: TẠO BẢNG ---")
#     createTable(connect, doc_gia_sql)
#     createTable(connect, danh_muc_sach_sql)
#     createTable(connect, phieu_muon_sql)
#     createTable(connect, chi_tiet_phieu_muon_sql)

#     # 2. Thêm dữ liệu theo đúng thứ tự (phụ thuộc khóa ngoại)
#     print("\n--- BƯỚC 2: THÊM DỮ LIỆU ---")
#     print("Thêm độc giả...")
#     insertData(connect, docgia_sql_strings)

#     print("Thêm sách...")
#     insertData(connect, sach_sql_strings)

#     print("Thêm phiếu mượn...")
#     insertData(connect, phieumuon_sql_strings)

#     print("Thêm chi tiết phiếu mượn...")
#     insertData(connect, chitietphieumuon_sql_strings)

#     # Đóng kết nối
#     connect.close()
#     print("\nHoàn tất! Đã đóng kết nối tới database.")


# if __name__ == '__main__':
#     main()

database_file = "thu_vien.db"
connect = sqlite3.connect(database_file)

cursor = connect.cursor()

cursor.execute("SELECT * FROM danhmucsach")

rows = cursor.fetchall()
for row in rows:
    print(row)

connect.close()
