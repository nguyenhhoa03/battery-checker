import re
import os

def parse_battery_report(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Lỗi khi mở file: {e}")
        return

    # Tách nội dung theo từng phần pin (giả sử mỗi phần bắt đầu với từ "BATTERY" theo sau số thứ tự)
    sections = re.split(r'(?i)BATTERY\s+\d+', content)
    if len(sections) < 2:
        print("Không tìm thấy thông tin pin trong báo cáo.")
        return

    for idx, section in enumerate(sections[1:], start=1):
        # Tìm Design Capacity và Full Charge Capacity trong phần của từng pin
        design_match = re.search(r"DESIGN\s+CAPACITY\s*[:\-]?\s*([\d,]+)\s*mWh", section, re.IGNORECASE)
        full_charge_match = re.search(r"FULL\s+CHARGE\s+CAPACITY\s*[:\-]?\s*([\d,]+)\s*mWh", section, re.IGNORECASE)
        if design_match and full_charge_match:
            try:
                design_capacity = float(design_match.group(1).replace(",", ""))
                full_charge_capacity = float(full_charge_match.group(1).replace(",", ""))
                percentage = (full_charge_capacity / design_capacity) * 100
                print(f"Pin {idx}: Tình trạng pin = {percentage:.2f}%")
            except Exception as ex:
                print(f"Pin {idx}: Lỗi khi tính toán - {ex}")
        else:
            print(f"Pin {idx}: Không tìm thấy đủ thông tin.")

if __name__ == "__main__":
    os.system("powercfg /batteryreport")
    # Lấy thư mục home của người dùng một cách động (phù hợp cho nhiều máy tính)
    home_directory = os.path.expanduser("~")
    # Giả sử file báo cáo pin nằm trong thư mục home, nếu không hãy điều chỉnh lại đường dẫn phù hợp
    file_path = os.path.join(home_directory, "battery-report.html")
    parse_battery_report(file_path)

