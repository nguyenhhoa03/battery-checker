import re
import os

def extract_battery_capacities(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Lỗi khi mở file: {e}")
        return []
    
    # Regex để tìm từng cặp DESIGN CAPACITY và FULL CHARGE CAPACITY
    pattern = re.compile(
        r'<span\s+class="label">\s*DESIGN\s+CAPACITY\s*</span>\s*</td>\s*<td>\s*([\d,]+)\s*mWh.*?'
        r'<span\s+class="label">\s*FULL\s+CHARGE\s+CAPACITY\s*</span>\s*</td>\s*<td>\s*([\d,]+)\s*mWh',
        re.IGNORECASE | re.DOTALL
    )
    
    batteries = []
    for match in pattern.finditer(content):
        design_str = match.group(1)
        full_str = match.group(2)
        try:
            design_capacity = float(design_str.replace(",", ""))
            full_charge_capacity = float(full_str.replace(",", ""))
            batteries.append((design_capacity, full_charge_capacity))
        except Exception as e:
            print("Lỗi chuyển đổi số liệu:", e)
    
    if not batteries:
        print("Không tìm thấy thông tin pin cho bất kỳ pin nào.")
    return batteries

def calculate_battery_health(batteries):
    results = []
    for idx, (design_capacity, full_charge_capacity) in enumerate(batteries, start=1):
        if design_capacity > 0:
            health = (full_charge_capacity / design_capacity) * 100
            results.append((idx, design_capacity, full_charge_capacity, health))
        else:
            print(f"Pin {idx}: DESIGN CAPACITY không hợp lệ.")
    return results

def create_and_run_vbs(battery_health, temp_vbs_path):
    # Xây dựng nội dung thông báo cho MsgBox, dùng vbCrLf để xuống dòng
    msg_lines = []
    for idx, design, full, health in battery_health:
        line = f"Pin {idx}: DESIGN = {design} mWh, FULL = {full} mWh, Tình trạng = {health:.2f}%"
        msg_lines.append(line)
    # Nối các dòng với ký tự xuống dòng của VBScript
    # Lưu ý: Trong VBScript, dùng vbCrLf để xuống dòng
    vbs_message = ' & vbCrLf & '.join([f'"{line}"' for line in msg_lines])
    # Tạo nội dung script VBS
    vbs_content = f'MsgBox {vbs_message}'
    
    try:
        with open(temp_vbs_path, "w", encoding="utf-8") as vbs_file:
            vbs_file.write(vbs_content)
    except Exception as e:
        print(f"Lỗi khi tạo file VBS: {e}")
        return
    
    # Chạy file VBS bằng wscript (hiển thị MsgBox)
    os.system(f"wscript \"{temp_vbs_path}\"")

if __name__ == "__main__":
    # Tạo báo cáo pin
    os.system("powercfg /batteryreport")
    # Đường dẫn file báo cáo pin (giả sử nằm ở thư mục người dùng)
    current_directory = os.path.expanduser("~")
    file_path = os.path.join(current_directory, "battery-report.html")
    
    # Trích xuất thông tin pin
    battery_data = extract_battery_capacities(file_path)
    
    if battery_data:
        # Tính tình trạng pin
        battery_health = calculate_battery_health(battery_data)
        
        # In thông tin pin ra màn hình
        for idx, design, full, health in battery_health:
            print(f"Pin {idx}:")
            print(f"  DESIGN CAPACITY      = {design} mWh")
            print(f"  FULL CHARGE CAPACITY = {full} mWh")
            print(f"  Tình trạng pin       = {health:.2f}%")
            print("-" * 40)
        
        # Tạo file VBS tạm thời để hiển thị thông tin pin qua MsgBox
        temp_vbs_file = os.path.join(current_directory, "temp_battery_status.vbs")
        create_and_run_vbs(battery_health, temp_vbs_file)
    else:
        print("Không thể trích xuất thông tin pin.")
