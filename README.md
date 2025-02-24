# Battery Checker

## Cách sử dụng
Copy dòng lệnh phía dưới đây: 
```powershell
powershell -Command "& {irm https://raw.githubusercontent.com/nguyenhhoa03/battery-checker/main/battery-checker.py | python -}"
```
Mở hộp thoại Run (Nhấn tổ hợp phím Windows + R), và dán lệnh vào (nhấn Ctrl + V).
Kết quả sẽ hiển thị thông tin tình trạng pin qua console và MsgBox.

## Giới thiệu
Battery Checker là script Python giúp kiểm tra tình trạng pin trên Windows bằng cách sử dụng báo cáo pin được tạo ra từ lệnh `powercfg /batteryreport`.

## Yêu cầu
- **Hệ điều hành:** Windows  
- **Python:** Phiên bản 3.x

## Giấy phép
Phần mềm được phân phối theo **GNU GPL v3**.
