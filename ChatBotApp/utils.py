import nltk
from nltk.tokenize import word_tokenize
import json
import os

from ChatBotApp.models import Message

# Xác định đường dẫn đến file JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'du_lieu_du_lich.json')

# Đọc dữ liệu từ file JSON khi module được load
try:
    with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
        du_lieu_du_lich = json.load(f)
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file dữ liệu tại {DATA_FILE_PATH}")
    du_lieu_du_lich = {"dia_diem_du_lich": {}}  # Khởi tạo một dictionary rỗng để tránh lỗi


def get_bot_response(user_input):
    user_input_lower = user_input.lower()
    tokens = word_tokenize(user_input_lower)
    print(f"User input (lower): '{user_input_lower}'")
    print(f"Tokens: {tokens}")

    if not tokens:
        print("Input trống.")
        return "Bạn nói gì vậy?"

    if any(word in tokens for word in ["xin", "chào", "hello", "hi"]):
        print("Tìm thấy lời chào.")
        return "Xin chào! Tôi có thể giúp gì cho bạn về du lịch."

    bot_response = None

    for dia_diem, thong_tin in du_lieu_du_lich.get("dia_diem_du_lich", {}).items():
        print(f"Đang kiểm tra địa điểm: '{dia_diem}'")
        if dia_diem in user_input_lower:
            print(f"Tìm thấy địa điểm '{dia_diem}' trong input.")

            # Kiểm tra cụm từ "thời điểm"
            if "thời điểm" in user_input_lower or any(word in tokens for word in ["mùa", "đi khi nào", "lúc nào", "thích hợp"]):
                print("Tìm thấy từ khóa hoặc cụm từ thời điểm.")
                thoi_diem_ly_tuong = thong_tin.get("thoi_diem_ly_tuong")
                print(f"Giá trị của thoi_diem_ly_tuong cho '{dia_diem}': {thoi_diem_ly_tuong}")
                if thoi_diem_ly_tuong:
                    bot_response = f"Thời điểm lý tưởng để đi {dia_diem.capitalize()} là: {', '.join(thoi_diem_ly_tuong)}."
                else:
                    bot_response = f"Tôi không có thông tin cụ thể về thời điểm lý tưởng để đi {dia_diem.capitalize()}."
                print(f"Bot response (thời điểm): '{bot_response}'")
                break

            # Kiểm tra cụm từ "địa điểm nổi tiếng"
            elif "địa điểm nổi tiếng" in user_input_lower or any(word in tokens for word in ["nổi tiếng", "tham quan", "khám phá", "điểm đến"]):
                print("Tìm thấy từ khóa hoặc cụm từ địa điểm nổi tiếng.")
                dia_diem_noi_tieng = thong_tin.get("dia_diem_noi_tieng")
                print(f"Giá trị của dia_diem_noi_tieng cho '{dia_diem}': {dia_diem_noi_tieng}")
                if dia_diem_noi_tieng:
                    bot_response = f"Một số địa điểm nổi tiếng ở {dia_diem.capitalize()} là: {', '.join(dia_diem_noi_tieng)}."
                else:
                    bot_response = f"Tôi không có thông tin về các địa điểm nổi tiếng ở {dia_diem.capitalize()}."
                print(f"Bot response (địa điểm nổi tiếng): '{bot_response}'")
                break

            # Kiểm tra cụm từ "chi phí"
            elif "chi phí" in user_input_lower or "giá cả" in user_input_lower or any(word in tokens for word in ["khoảng bao nhiêu", "tốn khoảng", "giá"]):
                print("Tìm thấy từ khóa hoặc cụm từ chi phí.")
                chi_phi_tham_khao = thong_tin.get("chi_phi_tham_khao")
                print(f"Giá trị của chi_phi_tham_khao cho '{dia_diem}': {chi_phi_tham_khao}")
                if chi_phi_tham_khao:
                    bot_response = f"Chi phí tham khảo cho một ngày ở {dia_diem.capitalize()} khoảng {chi_phi_tham_khao}."
                else:
                    bot_response = f"Tôi không có thông tin cụ thể về chi phí tham khảo ở {dia_diem.capitalize()}."
                print(f"Bot response (chi phí): '{bot_response}'")
                break

            elif "hoạt động" in user_input_lower or "làm gì" in user_input_lower or "vui chơi" in user_input_lower or any(
                    word in tokens for word in
                    ["hoạt", "động", "làm", "gì", "vui", "chơi", "các hoạt động", "những hoạt động", "hoạt động nào"]):
                print("Tìm thấy từ khóa hoặc cụm từ hoạt động.")
                hoat_dong_pho_bien = thong_tin.get("hoat_dong_pho_bien")
                print(f"Giá trị của hoat_dong_pho_bien cho '{dia_diem}': {hoat_dong_pho_bien}")
                if hoat_dong_pho_bien:
                    bot_response = f"Một số hoạt động phổ biến ở {dia_diem.capitalize()} là: {', '.join(hoat_dong_pho_bien)}."
                else:
                    bot_response = f"Tôi không có thông tin về các hoạt động phổ biến ở {dia_diem.capitalize()}."
                print(f"Bot response (hoạt động): '{bot_response}'")
                break

            elif any(word in tokens for word in ["khách", "sạn", "nhà nghỉ", "homestay", "ở", "ngủ", "phòng"]):
                print("Tìm thấy từ khóa khách sạn.")
                luu_tru = thong_tin.get("luu_tru_tham_khao", [])
                print(f"Giá trị của luu_tru cho '{dia_diem}': {luu_tru}")
                if luu_tru:
                    response = f"Các lựa chọn lưu trú tham khảo ở {dia_diem.capitalize()}:\n"
                    for item in luu_tru:
                        response += f"- Loại: {item.get('loai', 'Không rõ')}, Tên: {item.get('ten', 'Không rõ')}, Giá: {item.get('gia_tham_khao', 'Không rõ')}\n"
                    if any(word in tokens for word in ["giá rẻ", "rẻ"]):
                        khach_san_gia_re = [item for item in luu_tru if "rẻ" in item.get('gia_tham_khao', '').lower()]
                        print(f"Khách sạn giá rẻ tiềm năng: {khach_san_gia_re}")
                        if khach_san_gia_re:
                            bot_response = f"Các lựa chọn lưu trú giá rẻ tham khảo ở {dia_diem.capitalize()}:\n" + "\n".join([f"- Loại: {item.get('loai', 'Không rõ')}, Tên: {item.get('ten', 'Không rõ')}, Giá: {item.get('gia_tham_khao', 'Không rõ')}" for item in khach_san_gia_re])
                        else:
                            bot_response = f"Hiện tại không có thông tin về khách sạn giá rẻ ở {dia_diem.capitalize()}."
                    else:
                        bot_response = response
                else:
                    bot_response = f"Hiện tại không có thông tin về lưu trú ở {dia_diem.capitalize()}."
                print(f"Bot response (khách sạn): '{bot_response}'")
                break

            elif any(word in tokens for word in ["đặc sản", "ăn gì", "món ăn"]):
                print("Tìm thấy từ khóa đặc sản.")
                nha_hang_dac_san = thong_tin.get("nha_hang_dac_san")
                print(f"Giá trị của nha_hang_dac_san cho '{dia_diem}': {nha_hang_dac_san}")
                if nha_hang_dac_san:
                    response = f"Một số món đặc sản và địa điểm gợi ý ở {dia_diem.capitalize()}:\n"
                    for item in nha_hang_dac_san:
                        response += f"- {item.get('ten', 'Không rõ')}: {item.get('mon_dac_san', 'Không rõ')}\n"
                    bot_response = response
                else:
                    bot_response = f"Tôi không có thông tin về đặc sản ở {dia_diem.capitalize()}."
                print(f"Bot response (đặc sản): '{bot_response}'")
                break




            elif any(word in tokens for word in ["giới thiệu", "thông tin cơ bản", "về"]):
                print("Tìm thấy từ khóa giới thiệu.")
                gioi_thieu = thong_tin.get("gioi_thieu")
                dia_diem_noi_tieng = thong_tin.get("dia_diem_noi_tieng", [])
                print(f"Giá trị của gioi_thieu cho '{dia_diem}': {gioi_thieu}")
                print(f"Giá trị của dia_diem_noi_tieng cho '{dia_diem}': {dia_diem_noi_tieng}")
                bot_response = f"Thông tin về {dia_diem.capitalize()}: {gioi_thieu}. Một số địa điểm nổi tiếng ở đây là: {', '.join(dia_diem_noi_tieng)}."
                print(f"Bot response (giới thiệu): '{bot_response}'")
                break


            elif any(word in tokens for word in ["di chuyển", "đi lại", "phương tiện"]):
                print("Tìm thấy từ khóa di chuyển.")
                # Bạn có thể thêm thông tin về phương tiện di chuyển vào file JSON nếu cần
                bot_response = f"Về phương tiện di chuyển ở {dia_diem.capitalize()}, bạn có thể tham khảo thêm thông tin trên các trang web du lịch hoặc hỏi người dân địa phương."
                print(f"Bot response (di chuyển): '{bot_response}'")
                break

            else:
                print("Không tìm thấy từ khóa cụ thể, trả về thông tin chung.")
                bot_response = f"Thông tin về {dia_diem.capitalize()}: {thong_tin.get('gioi_thieu', 'Không có thông tin.')}. Một số địa điểm nổi tiếng ở đây là: {', '.join(thong_tin.get('dia_diem_noi_tieng', []) )}."
                print(f"Bot response (chung): '{bot_response}'")
                break

    if bot_response:
        print(f"Trả về bot response: '{bot_response}'")
        return bot_response

    elif any(word in tokens for word in ["đi", "đến", "thăm", "khám", "du", "lịch", "ở đâu", "nơi nào", "địa điểm"]):
        print("Câu hỏi chung về địa điểm.")
        return "Bạn muốn khám phá địa điểm nào?"
    elif any(word in tokens for word in ["khách", "sạn", "nhà nghỉ", "homestay", "ở", "ngủ", "phòng"]):
        print("Câu hỏi chung về lưu trú.")
        return "Bạn đang tìm kiếm khách sạn ở đâu và khi nào?"
    elif any(word in tokens for word in ["chuyến", "bay", "vé", "máy", "tàu", "xe", "đi", "đến", "lúc", "giờ"]):
        print("Câu hỏi chung về phương tiện di chuyển.")
        return "Bạn muốn đi đâu, khi nào và bằng phương tiện gì?"
    elif any(word in tokens for word in ["cảm", "ơn", "thank", "thanks"]):
        print("Lời cảm ơn.")
        return "Rất vui được hỗ trợ bạn!"
    else:
        print("Không hiểu câu hỏi.")
        return "Tôi xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi về địa điểm, khách sạn, chuyến bay, v.v."


def process_user_message(conversation, user_message):
    Message.objects.create(conversation=conversation, sender='user', text=user_message)
    bot_response_text = get_bot_response(user_message)
    print(f"Giá trị của bot_response_text (từ process_user_message): '{bot_response_text}'")
    bot_message = Message.objects.create(conversation=conversation, sender='bot', text=bot_response_text)
    return bot_message
