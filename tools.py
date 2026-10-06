from langchain_core.tools import tool


FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6},
    ],
}
def _fmt_vnd(n: int) -> str:
    return f"{n:,.0f}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str)-> str:
    """Tìm kiếm chuyến bay giữa hai thành phố. Trả về danh sách chuyến bay sắp xếp theo giá tăng dần."""
    try:
        o = origin.strip()
        d = destination.strip()

        key = (o, d)
        reversed_key = (d, o)

        if key in FLIGHTS_DB:
            flights = FLIGHTS_DB[key]
        elif reversed_key in FLIGHTS_DB:
            flights = FLIGHTS_DB[reversed_key]
        else:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}. Các tuyến hỗ trợ: {list(FLIGHTS_DB.keys())}"


        sorted_flights = sorted(flights, key=lambda f: f["price"])  
        lines = [f"Tìm thấy {len(sorted_flights)} chuyến bay {origin} → {destination}:"]
        for f in sorted_flights:
            lines.append(f"- {f['airline']}: {f['departure']} -> {f['arrival']}, Giá: {f['price']} VND")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi tra cứu chuyến bay: {e}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm khách sạn tại một thành phố với giá/đêm tối đa. Trả về danh sách sắp xếp theo rating giảm dần."""
    try:
        city = city.strip()
        if city not in HOTELS_DB:
            return f"Không có dữ liệu khách sạn cho {city}. Hỗ trợ: {list(HOTELS_DB.keys())}"

        filtered = [h for h in HOTELS_DB[city] if h["price_per_night"] <= max_price_per_night]
        if not filtered:
            return f"Không có khách sạn tại {city} dưới {_fmt_vnd(max_price_per_night)}/đêm."

        filtered.sort(key=lambda h: h["rating"], reverse=True)
        lines = [f"Tìm thấy {len(filtered)} khách sạn tại {city} (≤ {_fmt_vnd(max_price_per_night)}/đêm):"]
        for i, h in enumerate(filtered, 1):
            lines.append(
                f"{i}. {h['name']} ({h['stars']}★, {h['rating']}/5) - {h['area']} - {_fmt_vnd(h['price_per_night'])}/đêm"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi tra cứu khách sạn: {e}"

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính tổng chi phí và phần ngân sách còn lại.
    expenses là chuỗi dạng 'tên1:số1, tên2:số2', ví dụ: 'vé máy bay:1100000, khách sạn 2 đêm:1600000'.
    """
    try:
        if total_budget <= 0:
            return f"Ngân sách không hợp lệ: {total_budget}. Vui lòng cung cấp số dương."
        items = []
        total_spent = 0
        for part in expenses.split(","):
            if ":" not in part:
                continue
            name, value = part.split(":", 1)
            amount = int("".join(c for c in value if c.isdigit()))
            items.append((name.strip(), amount))
            total_spent += amount

        remaining = total_budget - total_spent
        lines = [f"Ngân sách: {_fmt_vnd(total_budget)}"]
        for name, amt in items:
            lines.append(f"- {name}: {_fmt_vnd(amt)}")
        lines.append(f"Tổng chi: {_fmt_vnd(total_spent)}")
        lines.append(f"Còn lại: {_fmt_vnd(remaining)}")
        if remaining < 0:
            lines.append(" VƯỢT NGÂN SÁCH!")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi tính ngân sách: {e}"
    