import datetime
import hashlib
from lunar_python import Lunar, LunarYear

def calculate_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

def get_nth_weekday_of_month(year, month, weekday, n):
    first_day = datetime.date(year, month, 1)
    days_ahead = (weekday - first_day.weekday()) % 7
    return first_day + datetime.timedelta(days=days_ahead + 7 * (n - 1))

def get_solar_from_lunar(year, month, day):
    lunar = Lunar.fromYmd(year, month, day)
    solar = lunar.getSolar()
    return datetime.date(solar.getYear(), solar.getMonth(), solar.getDay())

def get_thanh_minh_date(year):
    solar = Lunar.fromYmd(year, 2, 15).getJieQiTable()["清明"]
    return datetime.date(solar.getYear(), solar.getMonth(), solar.getDay())

def format_lunar_month_name(month):
    is_leap = month < 0
    m = abs(month)
    if m == 1:
        base = "tháng Giêng"
    elif m == 12:
        base = "tháng Chạp"
    else:
        base = f"tháng {m}"
    return f"{base} nhuận" if is_leap else base

def format_lunar_day_description(day, month):
    is_leap = month < 0
    m = abs(month)
    if m in (1, 12):
        return f"{day} {format_lunar_month_name(month)}"
    leap_str = " nhuận" if is_leap else ""
    return f"{day} tháng {m}{leap_str} Âm lịch"

def format_mung_1_meaning(month):
    header = format_lunar_day_description(1, month)
    month_name = format_lunar_month_name(month)
    meaning = (
        f"Ngày Mùng 1 {month_name} (ngày Sóc - khởi đầu một chu kỳ trăng mới trong tháng Âm lịch). "
        "Theo truyền thống văn hóa tâm linh của người Việt, ngày Mùng 1 đầu tháng mang ý nghĩa khởi đầu mới mẻ, thanh tịnh. "
        "Các gia đình thường dọn dẹp bàn thờ trang nghiêm, dâng hương, hoa tươi, trái cây cúng Phật và gia tiên, "
        "đi chùa lễ Phật hoặc ăn chay nhằm cầu mong một tháng mới bình an, may mắn, công việc hanh thông và gia đạo êm ấm."
    )
    return f"{header}\n{meaning}"

def format_ram_meaning(month):
    header = format_lunar_day_description(15, month)
    month_name = format_lunar_month_name(month)
    m = abs(month)
    is_leap = month < 0
    extra = ""
    if not is_leap:
        if m == 1:
            extra = " Đặc biệt, Rằm tháng Giêng (Tết Thượng Nguyên / Tết Nguyên Tiêu) là đêm trăng tròn đầu tiên của năm mới, được dân gian coi trọng với câu 'Lễ Phật quanh năm không bằng Rằm tháng Giêng'."
        elif m == 4:
            extra = " Đặc biệt, Rằm tháng Tư Âm lịch gắn liền với Đại lễ Phật Đản kỷ niệm ngày Đức Phật Thích Ca Mâu Ni đản sinh."
        elif m == 7:
            extra = " Đặc biệt, Rằm tháng Bảy (Tết Trung Nguyên) gắn liền với Đại lễ Vu Lan báo hiếu cha mẹ và lễ Xá tội vong nhân trong tín ngưỡng dân gian."
        elif m == 8:
            extra = " Đặc biệt, Rằm tháng Tám là đêm trăng tròn và sáng nhất mùa thu, gắn liền với Tết Trung Thu (Tết Đoàn Viên, Tết Thiếu Nhi)."
        elif m == 10:
            extra = " Đặc biệt, Rằm tháng Mười (Tết Hạ Nguyên / Tết Cơm Mới) là dịp các gia đình dâng lễ mừng lúa mới, tạ ơn trời đất và tổ tiên sau mùa thu hoạch."
        elif m == 12:
            extra = " Đây là ngày Rằm cuối cùng của năm Âm lịch, dịp các gia đình dâng hương tạ ơn thần linh, tổ tiên đã phù hộ suốt một năm qua và chuẩn bị đón Tết cổ truyền."
    meaning = (
        f"Ngày Rằm {month_name} (ngày Vọng - thời điểm mặt trăng tròn và sáng rõ nhất trong tháng Âm lịch, 'Vọng' nghĩa là nhìn xa trông rộng). "
        "Trong văn hóa truyền thống Việt Nam, ngày Rằm là dịp con cháu sửa soạn hương hoa, phẩm vật dâng cúng thần linh và gia tiên để bày tỏ lòng thành kính, "
        f"đi lễ chùa cầu quốc thái dân an, gia đạo bình an, đồng thời hướng tâm làm việc thiện và ăn chay thanh tịnh.{extra}"
    )
    return f"{header}\n{meaning}"

def escape_ics_text(text):
    return (
        text.replace("\\", "\\\\")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )

def fold_ics_line(line, max_octets=75):
    if len(line.encode("utf-8")) <= max_octets:
        return line
    lines = []
    current_chars = []
    current_bytes = 0

    i = 0
    n = len(line)
    while i < n:
        if line[i] == "\\" and i + 1 < n:
            token = line[i : i + 2]
            i += 2
        else:
            token = line[i]
            i += 1
        token_bytes = len(token.encode("utf-8"))
        if current_bytes + token_bytes > max_octets:
            lines.append("".join(current_chars))
            current_chars = [" ", token]
            current_bytes = 1 + token_bytes
        else:
            current_chars.append(token)
            current_bytes += token_bytes

    if current_chars:
        lines.append("".join(current_chars))
    return "\r\n".join(lines)

def write_ics_line(f, line):
    f.write(fold_ics_line(line) + "\r\n")

def write_event(f, start_date, duration_days, summary, description="", uid="", dtstamp="20260101T000000Z", rrule=""):
    end_date = start_date + datetime.timedelta(days=duration_days)
    write_ics_line(f, "BEGIN:VEVENT")
    write_ics_line(f, f"UID:{uid}")
    write_ics_line(f, f"DTSTAMP:{dtstamp}")
    write_ics_line(f, f"DTSTART;VALUE=DATE:{start_date.strftime('%Y%m%d')}")
    write_ics_line(f, f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}")
    if rrule:
        write_ics_line(f, f"RRULE:{rrule}")
    write_ics_line(f, f"SUMMARY:{escape_ics_text(summary)}")

    if description:
        write_ics_line(f, f"DESCRIPTION:{escape_ics_text(description)}")

    write_ics_line(f, "BEGIN:VALARM")
    write_ics_line(f, "ACTION:DISPLAY")
    write_ics_line(f, f"DESCRIPTION:{escape_ics_text(f'Nhắc nhở: {summary}')}")
    write_ics_line(f, "TRIGGER:-P1D")
    write_ics_line(f, "END:VALARM")
    write_ics_line(f, "BEGIN:VALARM")
    write_ics_line(f, "ACTION:DISPLAY")
    write_ics_line(f, f"DESCRIPTION:{escape_ics_text(f'Nhắc nhở: {summary}')}")
    write_ics_line(f, "TRIGGER:PT5H")
    write_ics_line(f, "END:VALARM")
    write_ics_line(f, "END:VEVENT")

def generate_calendar():
    output_file = "lich_vietnam_2026_2125.ics"
    dtstamp = "20260101T000000Z"
    event_seq = 0

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        write_ics_line(f, "BEGIN:VCALENDAR")
        write_ics_line(f, "VERSION:2.0")
        write_ics_line(f, "PRODID:-//Holidays//Vietnam//VI")
        write_ics_line(f, "CALSCALE:GREGORIAN")
        write_ics_line(f, "METHOD:PUBLISH")

        for year in range(2026, 2126):
            events = []

            def add_event(start_date, duration_days, summary, description="", rrule=""):
                events.append((start_date, duration_days, summary, description, rrule))

            def add_yearly_solar_event(start_date, duration_days, summary, description=""):
                if year == 2026:
                    add_event(start_date, duration_days, summary, description, rrule="FREQ=YEARLY;UNTIL=21251231")

            # 1. Lễ & Ngày kỉ niệm Việt Nam (Dương lịch)
            add_yearly_solar_event(
                datetime.date(year, 1, 1),
                1,
                "Tết Dương Lịch",
                "Nghỉ lễ toàn quốc\n"
                "Năm 153 trước Công Nguyên, La Mã là quốc gia đầu tiên chọn ngày 1 tháng 1 làm ngày đầu năm mới. "
                "Tết Dương lịch có thể coi là ngày lễ chung lớn nhất, thường có pháo hoa bắn vào lúc nửa đêm khi năm mới bắt đầu theo múi giờ. "
                "Ở phương Tây, Tết Dương lịch là dịp để mọi người quây quần, tụ họp cùng nhau đón chào năm mới. "
                "Họ có nhiều cách chào đón khác nhau nhưng đều chung một ý nghĩa là thể hiện sự biết ơn một năm đã qua và hi vọng vào một năm tiếp theo gặp nhiều may mắn, an lành.",
            )
            add_yearly_solar_event(
                datetime.date(year, 1, 6),
                1,
                "Tổng tuyển cử đầu tiên của Quốc hội Việt Nam",
                "Ngày 06/01/1946, cuộc Tổng tuyển cử đầu tiên bầu Quốc hội nước Việt Nam Dân chủ Cộng hòa đã diễn ra trên phạm vi cả nước theo nguyên tắc phổ thông, bình đẳng, trực tiếp và bỏ phiếu kín. "
                "Đây là mốc son lịch sử trọng đại mở đầu cho thời kỳ đất nước có một Quốc hội thống nhất, bản Hiến pháp tiến bộ và hệ thống chính quyền hợp hiến, hợp pháp đại diện cho ý chí và nguyện vọng của nhân dân Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 1, 9),
                1,
                "Học sinh, Sinh viên Việt Nam",
                "Ngày 09/01/1950, Đoàn Thanh niên Cứu quốc và Đoàn học sinh Sài Gòn - Chợ Lớn đã vận động hơn 2.000 học sinh, sinh viên cùng giáo viên và nhân dân biểu tình đòi đảm bảo an ninh học đường và trả tự do cho những học sinh, sinh viên bị bắt. "
                "Cuộc đấu tranh bị đàn áp đẫm máu, học sinh Trần Văn Ơn đã anh dũng hy sinh. "
                "Đại hội toàn quốc Liên đoàn Thanh niên Việt Nam lần thứ nhất (tháng 2/1950 tại Việt Bắc) đã quyết định lấy ngày 9 tháng 1 hằng năm làm Ngày truyền thống Học sinh - Sinh viên Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 2, 3),
                1,
                "thành lập Đảng Cộng sản Việt Nam",
                "Mùa xuân năm 1930 (từ ngày 3 đến ngày 7/2/1930), tại Cửu Long (Hương Cảng, Trung Quốc), lãnh tụ Nguyễn Ái Quốc đã chủ trì Hội nghị hợp nhất ba tổ chức cộng sản ở Việt Nam (Đông Dương Cộng sản Đảng, An Nam Cộng sản Đảng và Đông Dương Cộng sản Liên đoàn) thành một đảng duy nhất là Đảng Cộng sản Việt Nam. "
                "Sự kiện thành lập Đảng là bước ngoặt vĩ đại trong lịch sử cách mạng Việt Nam, chấm dứt cuộc khủng hoảng về đường lối cứu nước và giai cấp lãnh đạo, mở ra kỷ nguyên độc lập dân tộc gắn liền với chủ nghĩa xã hội.",
            )
            add_yearly_solar_event(
                datetime.date(year, 2, 14),
                1,
                "Valentine",
                "Ngày lễ Tình nhân (Valentine's Day - 14/2) có nguồn gốc từ phương Tây, gắn liền với truyền thuyết về vị linh mục tử vì đạo tên là Valentine dưới thời Hoàng đế La Mã Claudius II vì đã bí mật cử hành hôn lễ cho các đôi uyên ương. "
                "Ngày nay, 14 tháng 2 là ngày lễ tôn vinh tình yêu đôi lứa trên toàn thế giới, là dịp để những người yêu nhau trao gửi thiệp, hoa hồng, sô-cô-la cùng những lời chúc ngọt ngào, chân thành.",
            )
            add_yearly_solar_event(
                datetime.date(year, 2, 27),
                1,
                "Thầy thuốc Việt Nam",
                "Ngày 27/02/1955, Chủ tịch Hồ Chí Minh đã viết thư gửi Hội nghị cán bộ y tế toàn quốc, ân cần căn dặn đội ngũ y bác sĩ phải đoàn kết, thương yêu người bệnh như anh em ruột thịt với lời dạy sâu sắc: 'Lương y phải như từ mẫu'. "
                "Ngày 06/02/1985, Hội đồng Bộ trưởng đã quyết định lấy ngày 27 tháng 2 hằng năm làm Ngày Thầy thuốc Việt Nam nhằm tôn vinh, tri ân những người làm công tác y tế chăm sóc và bảo vệ sức khỏe nhân dân.",
            )
            add_yearly_solar_event(
                datetime.date(year, 3, 3),
                1,
                "Biên phòng toàn dân",
                "Ngày 03/03/1959, Thủ tướng Chính phủ ban hành Nghị định số 100/TTg thành lập lực lượng Công an nhân dân vũ trang (nay là Bộ đội Biên phòng). "
                "Đến năm 1989, Hội đồng Bộ trưởng quyết định lấy ngày 3 tháng 3 hằng năm là 'Ngày Biên phòng toàn dân' đồng thời là Ngày truyền thống của Bộ đội Biên phòng, nhằm phát huy sức mạnh tổng hợp của cả hệ thống chính trị và toàn dân trong sự nghiệp xây dựng, quản lý và bảo vệ chủ quyền lãnh thổ, an ninh biên giới quốc gia.",
            )
            add_yearly_solar_event(
                datetime.date(year, 3, 8),
                1,
                "Quốc tế Phụ nữ",
                "Ngày Quốc tế Phụ nữ (8/3) bắt nguồn từ phong trào đấu tranh đòi quyền sống, ngày làm việc 8 giờ, trả lương bình đẳng và quyền bầu cử của nữ công nhân ngành dệt, may tại Mỹ vào cuối thế kỷ XIX - đầu thế kỷ XX. "
                "Tại Việt Nam, ngày 8 tháng 3 còn là dịp kỷ niệm cuộc khởi nghĩa oanh liệt của Hai Bà Trưng (năm 40 sau Công nguyên) — hai vị nữ anh hùng dân tộc đầu tiên đánh đuổi giặc ngoại xâm — đồng thời tôn vinh vai trò, phẩm chất cao đẹp và những đóng góp to lớn của phụ nữ đối với gia đình và xã hội.",
            )
            add_yearly_solar_event(
                datetime.date(year, 3, 20),
                1,
                "Quốc tế Hạnh phúc",
                "Tháng 6/2012, Đại hội đồng Liên Hợp Quốc đã quyết định chọn ngày 20 tháng 3 hằng năm là Ngày Quốc tế Hạnh phúc (International Day of Happiness) theo sáng kiến của Vương quốc Bhutan. "
                "Ngày 20/3 rơi vào dịp Xuân phân khi mặt trời nằm ngang đường xích đạo, độ dài ngày và đêm bằng nhau — biểu tượng cho sự cân bằng, hài hòa của vũ trụ. "
                "Đây là dịp để nhân loại cùng hành động vì một cuộc sống ấm no, yêu thương, sẻ chia và xây dựng thế giới hòa bình, thịnh vượng.",
            )
            add_yearly_solar_event(
                datetime.date(year, 3, 26),
                1,
                "thành lập Đoàn TNCS Hồ Chí Minh",
                "Từ ngày 20 đến ngày 26/03/1931, tại Hội nghị Ban Chấp hành Trung ương Đảng lần thứ 2 do Tổng Bí thư Trần Phú chủ trì, Trung ương Đảng đã dành phần quan trọng bàn về công tác thanh niên và quyết định thành lập tổ chức Đoàn Thanh niên Cộng sản. "
                "Tháng 3/1961, Đại hội Đoàn toàn quốc lần thứ III được sự đồng ý của Bộ Chính trị và Chủ tịch Hồ Chí Minh đã quyết định lấy ngày 26 tháng 3 hằng năm làm Ngày thành lập Đoàn Thanh niên Cộng sản Hồ Chí Minh.",
            )
            add_yearly_solar_event(
                datetime.date(year, 3, 27),
                1,
                "Thể thao Việt Nam",
                "Ngày 27/03/1946, Chủ tịch Hồ Chí Minh ký Sắc lệnh số 38 thiết lập Nha Thanh niên và Thể dục thuộc Bộ Quốc gia Giáo dục, đồng thời viết bài 'Sức khỏe và thể dục' đăng trên báo Cứu Quốc kêu gọi toàn dân tập thể dục với tư tưởng 'Dân cường thì Quốc thịnh'. "
                "Ngày 29/01/1991, Hội đồng Bộ trưởng ban hành Quyết định số 25/CT lấy ngày 27 tháng 3 hằng năm làm Ngày Thể thao Việt Nam nhằm thúc đẩy phong trào rèn luyện thân thể trong toàn dân.",
            )
            add_yearly_solar_event(
                datetime.date(year, 4, 1),
                1,
                "Cá tháng Tư",
                "Ngày Cá tháng Tư (April Fools' Day - 1/4) là ngày hội nói đùa truyền thống có nguồn gốc từ Pháp vào thế kỷ XVI, khi vua Charles IX ban hành lịch mới lấy ngày 1/1 làm đầu năm thay vì đầu tháng 4 như trước. "
                "Vào ngày này, mọi người ở nhiều quốc gia thường dành cho nhau những trò đùa hóm hỉnh, vô hại nhằm mang lại tiếng cười sảng khoái và niềm vui trong cuộc sống.",
            )
            add_yearly_solar_event(
                datetime.date(year, 4, 21),
                1,
                "Sách và Văn hóa đọc Việt Nam",
                "Ngày 21 tháng 4 gắn liền với sự kiện cuốn sách 'Đường Kách mệnh' của lãnh tụ Nguyễn Ái Quốc — tác phẩm đầu tiên bằng tiếng Việt được in bởi những người thợ in cách mạng Việt Nam — được xuất bản vào tháng 4/1927. "
                "Theo Quyết định của Thủ tướng Chính phủ, ngày 21 tháng 4 hằng năm được chọn là Ngày Sách và Văn hóa đọc Việt Nam nhằm tôn vinh giá trị của sách, khẳng định vai trò của tri thức và khuyến khích phong trào đọc sách trong cộng đồng.",
            )
            add_yearly_solar_event(
                datetime.date(year, 4, 30),
                1,
                "Giải phóng miền Nam, thống nhất đất nước",
                "Nghỉ lễ toàn quốc\n"
                "Ngày 30/04/1975 là mốc son chói lọi trong lịch sử dựng nước và giữ nước của dân tộc Việt Nam. "
                "Đúng 11 giờ 30 phút trưa 30/4/1975, lá cờ cách mạng tung bay trên nóc Dinh Độc Lập, đánh dấu thắng lợi hoàn toàn của Chiến dịch Hồ Chí Minh lịch sử, giải phóng miền Nam, kết thúc 21 năm kháng chiến chống Mỹ cứu nước đầy hy sinh gian khổ và thu non sông về một mối, mở ra kỷ nguyên độc lập, thống nhất cho Tổ quốc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 5, 1),
                1,
                "Quốc tế Lao động",
                "Nghỉ lễ toàn quốc\n"
                "Ngày Quốc tế Lao động (1/5) bắt nguồn từ cuộc tổng bãi công của hàng chục vạn công nhân tại thành phố Chicago (Mỹ) vào ngày 01/05/1886 đòi thực hiện chế độ ngày làm việc 8 giờ. "
                "Năm 1889, Đại hội lần thứ nhất của Quốc tế Cộng sản II đã quyết định lấy ngày 1 tháng 5 hằng năm làm Ngày Quốc tế Lao động. "
                "Tại Việt Nam, đây là ngày hội lớn của giai cấp công nhân và nhân dân lao động, tôn vinh những cống hiến của người lao động trong công cuộc xây dựng và bảo vệ Tổ quốc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 5, 7),
                1,
                "Chiến thắng Điện Biên Phủ",
                "Chiều ngày 07/05/1954, lá cờ 'Quyết chiến Quyết thắng' của Quân đội Nhân dân Việt Nam tung bay trên nóc hầm chỉ huy của tướng Pháp De Castries, đánh dấu thắng lợi hoàn toàn của Chiến dịch Điện Biên Phủ sau 56 ngày đêm 'khoét núi, ngủ hầm, mưa dầm, cơm vắt'. "
                "Chiến thắng 'lừng lẫy năm châu, chấn động địa cầu' đã đập tan ách thống trị của thực dân Pháp, buộc Pháp phải ký Hiệp định Genève chấm dứt chiến tranh, lập lại hòa bình ở Đông Dương.",
            )
            add_yearly_solar_event(
                datetime.date(year, 5, 15),
                1,
                "thành lập Đội Thiếu niên Tiền phong Hồ Chí Minh",
                "Ngày 15/05/1941, tại thôn Nà Mạ, xã Trường Hà, huyện Hà Quảng, tỉnh Cao Bằng, Hội Nhi đồng Cứu quốc (nay là Đội Thiếu niên Tiền phong Hồ Chí Minh) được thành lập với 5 đội viên đầu tiên do anh Kim Đồng (Nông Văn Dền) làm Đội trưởng. "
                "Trải qua các thời kỳ lịch sử, tổ chức Đội luôn là cái nôi giáo dục, rèn luyện các thế hệ thiếu niên, nhi đồng Việt Nam học tập và làm theo 5 điều Bác Hồ dạy.",
            )
            add_yearly_solar_event(
                datetime.date(year, 5, 19),
                1,
                "Ngày sinh Chủ tịch Hồ Chí Minh",
                "Kỷ niệm ngày sinh của Chủ tịch Hồ Chí Minh (19/05/1890) — vị lãnh tụ thiên tài của Đảng và nhân dân ta, người thầy vĩ đại của cách mạng Việt Nam, Anh hùng giải phóng dân tộc và Danh nhân văn hóa kiệt xuất. "
                "Người đã hiến dâng trọn cuộc đời mình cho sự nghiệp giải phóng dân tộc, thống nhất đất nước và tự do, hạnh phúc của nhân dân. "
                "Ngày 19 tháng 5 hằng năm là dịp để toàn Đảng, toàn dân, toàn quân bày tỏ lòng biết ơn vô hạn đối với công lao trời biển của Bác Hồ kính yêu.",
            )
            add_yearly_solar_event(
                datetime.date(year, 6, 1),
                1,
                "Quốc tế Thiếu nhi",
                "Ngày Quốc tế Thiếu nhi (1/6) bắt nguồn từ sự kiện rạng sáng 01/06/1942 khi phát xít Đức tàn sát dã man trẻ em và phụ nữ tại làng Lidice (Tiệp Khắc). "
                "Năm 1949, Liên đoàn Phụ nữ Dân chủ Quốc tế họp tại Moskva đã quyết định lấy ngày 1 tháng 6 hằng năm làm Ngày Quốc tế Bảo vệ Thiếu nhi. "
                "Tại Việt Nam, ngày 1/6 là ngày hội tràn ngập niềm vui dành cho trẻ em, thể hiện sự quan tâm, chăm sóc và bảo vệ của gia đình cùng toàn xã hội đối với thế hệ măng non của đất nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 6, 5),
                1,
                "Bác Hồ ra đi tìm đường cứu nước",
                "Ngày 05/06/1911, từ Bến cảng Nhà Rồng (Sài Gòn), người thanh niên yêu nước Nguyễn Tất Thành (với tên gọi Văn Ba) đã lên con tàu buôn Pháp Amiral Latouche-Tréville rời Tổ quốc, bắt đầu hành trình 30 năm bôn ba qua gần 30 quốc gia trên nhiều châu lục để tìm con đường cứu nước, giải phóng dân tộc. "
                "Người đã đến với chủ nghĩa Mác - Lênin, tìm ra con đường cách mạng vô sản và đưa dân tộc Việt Nam đi tới độc lập, tự do.",
            )
            add_yearly_solar_event(
                datetime.date(year, 6, 21),
                1,
                "Báo chí Cách mạng Việt Nam",
                "Ngày 21/06/1925, tại Quảng Châu (Trung Quốc), lãnh tụ Nguyễn Ái Quốc đã sáng lập báo 'Thanh Niên' — cơ quan ngôn luận của Hội Việt Nam Cách mạng Thanh niên, đặt nền móng cho nền báo chí cách mạng Việt Nam. "
                "Tháng 2/1985, Ban Bí thư Trung ương Đảng quyết định lấy ngày 21 tháng 6 hằng năm làm Ngày Báo chí Việt Nam (từ năm 2000 gọi là Ngày Báo chí Cách mạng Việt Nam) nhằm tôn vinh những người làm báo — những chiến sĩ xung kích trên mặt trận tư tưởng, văn hóa.",
            )
            add_yearly_solar_event(
                datetime.date(year, 6, 28),
                1,
                "Gia đình Việt Nam",
                "Ngày 28/06/2000, Ban Bí thư Trung ương Đảng ban hành Chỉ thị số 55-CT/TW nhấn mạnh vai trò nền tảng của gia đình trong việc bảo vệ, chăm sóc và giáo dục thế hệ trẻ. "
                "Ngày 04/05/2001, Thủ tướng Chính phủ ban hành Quyết định số 72/2001/QĐ-TTg lấy ngày 28 tháng 6 hằng năm là Ngày Gia đình Việt Nam. "
                "Đây là dịp tôn vinh những giá trị văn hóa truyền thống tốt đẹp của gia đình Việt Nam, hướng tới xây dựng gia đình no ấm, bình đẳng, tiến bộ và hạnh phúc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 7, 27),
                1,
                "Thương binh, Liệt sĩ",
                "Tháng 6/1947, theo chỉ thị của Chủ tịch Hồ Chí Minh, hội nghị đại biểu các cơ quan, đoàn thể tại Đại Từ (Thái Nguyên) đã thống nhất chọn ngày 27 tháng 7 hằng năm làm Ngày Thương binh toàn quốc (từ năm 1955 đổi thành Ngày Thương binh - Liệt sĩ). "
                "Đây là ngày lễ mang ý nghĩa nhân văn sâu sắc, thể hiện truyền thống 'Uống nước nhớ nguồn', 'Ăn quả nhớ người trồng cây' của dân tộc Việt Nam, tưởng nhớ các anh hùng liệt sĩ và tri ân các thương binh, bệnh binh, Bà mẹ Việt Nam Anh hùng cùng các gia đình có công với nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 7, 28),
                1,
                "thành lập Công đoàn Việt Nam",
                "Ngày 28/07/1929, tại số nhà 15 phố Hàng Nón (Hà Nội), Đại hội đại biểu Tổng Công hội Đỏ Bắc Kỳ lần thứ nhất do đồng chí Nguyễn Đức Cảnh chủ trì đã quyết định thành lập Tổng Công hội Đỏ Bắc Kỳ — tiền thân của Tổng Liên đoàn Lao động Việt Nam ngày nay. "
                "Ngày 28 tháng 7 hằng năm là Ngày thành lập Công đoàn Việt Nam, đánh dấu sự lớn mạnh của phong trào công nhân và tổ chức đại diện bảo vệ quyền, lợi ích hợp pháp của người lao động.",
            )
            add_yearly_solar_event(
                datetime.date(year, 8, 10),
                1,
                "Vì nạn nhân chất độc da cam Việt Nam",
                "Ngày 10/08/1961 là ngày đầu tiên quân đội Mỹ tiến hành rải chất độc hóa học (chất độc da cam/dioxin) xuống miền Nam Việt Nam, gây ra thảm họa môi trường nghiêm trọng và nỗi đau thể xác, tinh thần di truyền qua nhiều thế hệ. "
                "Ngày 10 tháng 8 hằng năm được chọn là Ngày Vì nạn nhân chất độc da cam Việt Nam nhằm thức tỉnh lương tri nhân loại, vận động cộng đồng trong nước và quốc tế chung tay xoa dịu nỗi đau da cam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 8, 19),
                1,
                "Cách mạng tháng Tám",
                "Ngày 19/08/1945, dưới sự lãnh đạo của Đảng và Mặt trận Việt Minh, hơn 20 vạn nhân dân Hà Nội đã vùng lên khởi nghĩa giành chính quyền thắng lợi, tạo sức lan tỏa quyết định giúp Tổng khởi nghĩa Cách mạng tháng Tám thành công trên cả nước. "
                "Thắng lợi của Cách mạng tháng Tám năm 1945 đã đập tan xiềng xích nô lệ của thực dân, phát xít và lật đổ chế độ quân chủ chuyên chế hàng ngàn năm, đưa nhân dân Việt Nam từ thân phận nô lệ lên làm chủ đất nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 9, 1),
                1,
                "Quốc khánh bổ sung",
                "Nghỉ lễ toàn quốc\n"
                "Theo quy định của Bộ luật Lao động năm 2019 (có hiệu lực từ ngày 01/01/2021), người lao động trên cả nước được nghỉ lễ Quốc khánh 02 ngày (ngày 2 tháng 9 và 01 ngày liền kề trước hoặc sau) hưởng nguyên lương. "
                "Ngày nghỉ Quốc khánh bổ sung giúp người dân có kỳ nghỉ lễ trọn vẹn để sum họp gia đình và tham gia các hoạt động kỷ niệm ngày Tết Độc lập của dân tộc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 9, 2),
                1,
                "Quốc khánh",
                "Nghỉ lễ toàn quốc\n"
                "Ngày 02/09/1945, tại Quảng trường Ba Đình lịch sử (Hà Nội), Chủ tịch Hồ Chí Minh đã thay mặt Chính phủ lâm thời đọc bản Tuyên ngôn Độc lập, trịnh trọng tuyên bố trước quốc dân đồng bào và toàn thế giới sự ra đời của nước Việt Nam Dân chủ Cộng hòa (nay là nước Cộng hòa Xã hội Chủ nghĩa Việt Nam). "
                "Từ đó, ngày 2 tháng 9 hằng năm trở thành Ngày Quốc khánh — ngày Tết Độc lập thiêng liêng của toàn dân tộc Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 9, 10),
                1,
                "thành lập Mặt trận Tổ quốc Việt Nam",
                "Ngày 10/09/1955, Đại hội Mặt trận Dân tộc Thống nhất họp tại Hà Nội đã quyết định thành lập Mặt trận Tổ quốc Việt Nam và thông qua Chương trình nhằm đoàn kết rộng rãi mọi lực lượng dân tộc, dân chủ và hòa bình trong cả nước. "
                "Đây là dấu mốc lịch sử quan trọng trong quá trình phát triển của khối đại đoàn kết toàn dân tộc Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 9, 20),
                1,
                "Việt Nam gia nhập Liên Hợp Quốc",
                "Ngày 20/09/1977, tại phiên khai mạc khóa họp lần thứ 32 của Đại hội đồng Liên Hợp Quốc tại New York (Mỹ), nước Cộng hòa Xã hội Chủ nghĩa Việt Nam chính thức được kết nạp làm thành viên thứ 149 của Liên Hợp Quốc. "
                "Sự kiện này mở ra chương mới trong lịch sử đối ngoại đa phương của Việt Nam, khẳng định vị thế của một quốc gia độc lập, thống nhất, yêu chuộng hòa bình trên trường quốc tế.",
            )
            add_yearly_solar_event(
                datetime.date(year, 9, 23),
                1,
                "Nam Bộ kháng chiến",
                "Đêm 22 rạng sáng 23/09/1945, thực dân Pháp được quân Anh hỗ trợ đã nổ súng đánh chiếm trụ sở Ủy ban Nhân dân Nam Bộ tại Sài Gòn, mở đầu cuộc xâm lược Việt Nam lần thứ hai. "
                "Ngay sáng 23/9/1945, Xứ ủy và Ủy ban Nhân dân Nam Bộ đã họp tại đường Cây Mai (Chợ Lớn), ra lời kêu gọi toàn dân Nam Bộ đứng lên kháng chiến bảo vệ nền độc lập vừa giành được, xứng danh 'Thành đồng Tổ quốc' đi trước về sau.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 1),
                1,
                "Quốc tế Người cao tuổi",
                "Ngày 14/12/1990, Đại hội đồng Liên Hợp Quốc đã thông qua Nghị quyết số 45/106 lấy ngày 1 tháng 10 hằng năm làm Ngày Quốc tế Người cao tuổi (International Day of Older Persons). "
                "Tại Việt Nam, ngày 1/10 là dịp phát huy truyền thống 'Kính lão đắc thọ', 'Uống nước nhớ nguồn', tôn vinh những đóng góp quý báu của người cao tuổi và đẩy mạnh công tác chăm sóc sức khỏe, đời sống tinh thần cho các bậc cao niên.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 10),
                1,
                "Giải phóng Thủ đô",
                "Sáng ngày 10/10/1954, các đoàn quân chiến thắng của Quân đội Nhân dân Việt Nam tiến qua 5 cửa ô tiếp quản Thủ đô Hà Nội trong cờ hoa rực rỡ và niềm hân hoan của hàng chục vạn người dân sau 9 năm kháng chiến chống thực dân Pháp. "
                "Ngày Giải phóng Thủ đô là mốc son chói lọi khép lại ách thống trị của thực dân trên đất Thăng Long ngàn năm văn hiến, mở ra thời kỳ xây dựng và phát triển mới của Hà Nội.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 13),
                1,
                "Doanh nhân Việt Nam",
                "Ngày 13/10/1945, Chủ tịch Hồ Chí Minh gửi thư cho giới Công - Thương Việt Nam, khẳng định vai trò quan trọng của doanh nhân đối với sự thịnh vượng của đất nước: 'Việc nước và việc nhà bao giờ cũng đi đôi với nhau. Nền kinh tế quốc dân thịnh vượng nghĩa là các sự kinh doanh của các nhà công nghiệp, thương nghiệp thịnh vượng'. "
                "Ngày 20/09/2004, Thủ tướng Chính phủ ký Quyết định lấy ngày 13 tháng 10 hằng năm làm Ngày Doanh nhân Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 14),
                1,
                "thành lập Hội Nông dân Việt Nam",
                "Tháng 10/1930, Hội nghị Ban Chấp hành Trung ương Đảng Cộng sản Đông Dương đã thông qua Án nghị quyết về việc thành lập Tổng Nông hội Đông Dương — tiền thân của Hội Nông dân Việt Nam ngày nay. "
                "Ngày 17/01/1991, Bộ Chính trị đã quyết định lấy ngày 14 tháng 10 hằng năm làm Ngày thành lập Hội Nông dân Việt Nam nhằm ghi nhận và phát huy vai trò to lớn của giai cấp nông dân trong sự nghiệp cách mạng và phát triển nông nghiệp, nông thôn.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 15),
                1,
                "truyền thống Hội Liên hiệp Thanh niên Việt Nam",
                "Ngày 15/10/1956, tại Thủ đô Hà Nội, Đại hội đại biểu toàn quốc lần thứ I của Hội Liên hiệp Thanh niên Việt Nam được tổ chức trọng thể, vinh dự đón Chủ tịch Hồ Chí Minh đến dự và căn dặn thanh niên đoàn kết phấn đấu vì Tổ quốc. "
                "Từ đó, ngày 15 tháng 10 hằng năm được chọn là Ngày truyền thống của Hội Liên hiệp Thanh niên Việt Nam — tổ chức xã hội rộng rãi tập hợp mọi tầng lớp thanh niên Việt Nam yêu nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 20),
                1,
                "Phụ nữ Việt Nam",
                "Ngày 20/10/1930, Hội Phụ nữ phản đế Việt Nam (nay là Hội Liên hiệp Phụ nữ Việt Nam) chính thức được thành lập. "
                "Để đánh dấu sự kiện lịch sử này, Đảng Cộng sản Việt Nam đã quyết định chọn ngày 20 tháng 10 hằng năm làm Ngày Phụ nữ Việt Nam. "
                "Đây là dịp đặc biệt để toàn xã hội tôn vinh vẻ đẹp, phẩm chất 'Anh hùng, bất khuất, trung hậu, đảm đang' và gửi lời tri ân sâu sắc tới những người bà, người mẹ, người chị em phụ nữ Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 10, 31),
                1,
                "Halloween",
                "Lễ hội Halloween (All Hallows' Eve) diễn ra vào đêm 31 tháng 10 hằng năm, bắt nguồn từ lễ hội Samhain cổ xưa của người Celt ở châu Âu đánh dấu sự kết thúc của mùa thu hoạch và bước vào mùa đông. "
                "Ngày nay, Halloween đã trở thành lễ hội văn hóa vui nhộn phổ biến tại nhiều quốc gia với các hoạt động hóa trang sáng tạo, trang trí đèn bí ngô (Jack-o'-lantern) và trò chơi 'Cho kẹo hay bị ghẹo' (Trick or Treat).",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 9),
                1,
                "Pháp luật Việt Nam",
                "Ngày 09/11/1946, Quốc hội khóa I nước Việt Nam Dân chủ Cộng hòa đã thông qua bản Hiến pháp đầu tiên của nước ta — bản Hiến pháp dân chủ đầu tiên ở Đông Nam Á. "
                "Theo Luật Phổ biến, giáo dục pháp luật năm 2012, ngày 9 tháng 11 hằng năm được chọn là Ngày Pháp luật nước Cộng hòa Xã hội Chủ nghĩa Việt Nam nhằm tôn vinh Hiến pháp, pháp luật và nâng cao ý thức thượng tôn pháp luật của mọi công dân.",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 18),
                1,
                "Đại đoàn kết toàn dân tộc",
                "Ngày 18/11/1930, Ban Thường vụ Trung ương Đảng Cộng sản Đông Dương đã ban hành Chỉ thị về việc thành lập Hội Phản đế đồng minh — hình thức tổ chức đầu tiên của Mặt trận Dân tộc Thống nhất Việt Nam (nay là Mặt trận Tổ quốc Việt Nam). "
                "Hằng năm, ngày 18 tháng 11 là Ngày truyền thống của Mặt trận Tổ quốc Việt Nam và Ngày hội Đại đoàn kết toàn dân tộc được tổ chức sôi nổi tại các khu dân cư trên khắp cả nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 19),
                1,
                "Quốc tế Nam giới",
                "Ngày Quốc tế Nam giới (International Men's Day - 19/11) được Tiến sĩ Jerome Teelucksingh khởi xướng năm 1999 tại Trinidad và Tobago và được hưởng ứng tại nhiều quốc gia trên thế giới. "
                "Ngày lễ này nhằm ghi nhận và tôn vinh những đóng góp tích cực của nam giới đối với gia đình, cộng đồng và xã hội, đồng thời nâng cao nhận thức về chăm sóc sức khỏe thể chất, tinh thần cho nam giới và thúc đẩy bình đẳng giới.",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 20),
                1,
                "Nhà giáo Việt Nam",
                "Tháng 8/1957, Hội nghị Quốc tế các nhà giáo họp tại Warszawa (Ba Lan) đã thông qua bản 'Hiến chương các nhà giáo' và quyết định lấy ngày 20 tháng 11 hằng năm là Ngày Quốc tế Hiến chương các nhà giáo. "
                "Ngày 28/09/1982, Hội đồng Bộ trưởng ban hành Quyết định số 167-HĐBT chính thức lấy ngày 20 tháng 11 là Ngày Nhà giáo Việt Nam. "
                "Đây là dịp truyền thống để các thế hệ học trò và toàn xã hội bày tỏ lòng biết ơn, tri ân sâu sắc đối với các thầy cô giáo theo đạo lý 'Tôn sư trọng đạo' của dân tộc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 23),
                1,
                "Di sản Văn hóa Việt Nam",
                "Ngày 23/11/1945, Chủ tịch Hồ Chí Minh đã ký Sắc lệnh số 65/SL 'Ấn định nhiệm vụ của Đông Phương Bác cổ Học viện' — văn bản pháp lý đầu tiên của Nhà nước cách mạng về việc bảo tồn di sản văn hóa dân tộc. "
                "Ngày 24/02/2005, Thủ tướng Chính phủ ký Quyết định số 36/2005/QĐ-TTg lấy ngày 23 tháng 11 hằng năm là Ngày Di sản Văn hóa Việt Nam nhằm khơi dậy lòng tự hào dân tộc và ý thức gìn giữ, phát huy kho tàng di sản văn hóa đất nước.",
            )
            add_yearly_solar_event(
                datetime.date(year, 11, 24),
                1,
                "Văn hóa Việt Nam",
                "Nghỉ lễ toàn quốc\n"
                "Ngày 24/11/1946, Hội nghị Văn hóa toàn quốc lần thứ nhất được khai mạc trọng thể tại Nhà hát Lớn Hà Nội, nơi Chủ tịch Hồ Chí Minh đã nêu rõ sứ mệnh thiêng liêng: 'Văn hóa phải soi đường cho quốc dân đi'. "
                "Nhằm đề cao vai trò nền tảng tinh thần của văn hóa dân tộc và tạo điều kiện cho nhân dân thụ hưởng, sáng tạo các giá trị văn hóa, ngày 24 tháng 11 hằng năm được chọn là Ngày Văn hóa Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 6),
                1,
                "thành lập Hội Cựu chiến binh Việt Nam",
                "Ngày 06/12/1989, Bộ Chính trị Ban Chấp hành Trung ương Đảng Cộng sản Việt Nam (khóa VI) đã quyết định thành lập Hội Cựu chiến binh Việt Nam. "
                "Ngày 6 tháng 12 hằng năm là Ngày truyền thống của Hội Cựu chiến binh Việt Nam nhằm tôn vinh các thế hệ cựu chiến binh luôn giữ vững và phát huy phẩm chất cao đẹp 'Bộ đội Cụ Hồ', đóng góp tích cực vào sự nghiệp xây dựng và bảo vệ Tổ quốc.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 19),
                1,
                "Toàn quốc kháng chiến",
                "Đêm 19/12/1946, trước sự bội ước và hành động gây chiến trắng trợn của thực dân Pháp, Chủ tịch Hồ Chí Minh đã ra 'Lời kêu gọi Toàn quốc kháng chiến' với ý chí sắt đá: 'Chúng ta thà hy sinh tất cả, chứ nhất định không chịu mất nước, nhất định không chịu làm nô lệ'. "
                "Đúng 20 giờ ngày 19/12/1946, tiếng đại bác từ pháo đài Láng nổ vang, mở đầu cuộc kháng chiến toàn dân, toàn diện, trường kỳ chống thực dân Pháp xâm lược.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 22),
                1,
                "thành lập Quân đội Nhân dân Việt Nam",
                "Ngày 22/12/1944, tại khu rừng giữa hai tổng Hoàng Hoa Thám và Trần Hưng Đạo (huyện Nguyên Bình, tỉnh Cao Bằng), Đội Việt Nam Tuyên truyền Giải phóng quân — tiền thân của Quân đội Nhân dân Việt Nam — được thành lập theo chỉ thị của lãnh tụ Hồ Chí Minh, do đồng chí Võ Nguyên Giáp trực tiếp chỉ huy với 34 chiến sĩ. "
                "Từ năm 1989, ngày 22 tháng 12 hằng năm đồng thời là Ngày hội Quốc phòng toàn dân, tôn vinh truyền thống 'Trung với Đảng, hiếu với dân' của lực lượng vũ trang nhân dân Việt Nam.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 24),
                1,
                "Đêm Giáng Sinh",
                "Đêm Giáng Sinh (Christmas Eve - tối 24/12), còn gọi là Đêm vọng Lễ Giáng Sinh, là đêm trước ngày kỷ niệm Chúa Giê-su ra đời tại Bethlehem theo đức tin Kitô giáo. "
                "Đây là thời điểm ấm áp khi mọi người cùng trang hoàng cây thông Noel, tham dự thánh lễ nửa đêm, trao gửi những món quà ý nghĩa và quây quần bên gia đình, bạn bè trong tiếng nhạc Giáng Sinh an lành.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 25),
                1,
                "Lễ Giáng Sinh",
                "Lễ Giáng Sinh (Noel / Christmas - 25/12) là ngày lễ trọng đại kỷ niệm sự ra đời của Chúa Giê-su. "
                "Không chỉ mang ý nghĩa tôn giáo thiêng liêng đối với người theo đạo Kitô, Lễ Giáng Sinh ngày nay đã trở thành ngày hội văn hóa phổ biến trên toàn thế giới, lan tỏa thông điệp về hòa bình, lòng nhân ái, sự sẻ chia và tình yêu thương gia đình.",
            )
            add_yearly_solar_event(
                datetime.date(year, 12, 31),
                1,
                "Giao Thừa Tết Dương Lịch",
                "Ngày cuối cùng của năm theo lịch Gregory (New Year's Eve - 31/12), đánh dấu thời khắc chuẩn bị khép lại năm cũ và chuyển giao sang năm mới Dương lịch. "
                "Vào đêm 31 tháng 12, người dân khắp nơi thường quây quần bên người thân, tham gia các chương trình đếm ngược (Countdown), thưởng thức pháo hoa rực rỡ và dành cho nhau những lời chúc tốt đẹp nhất đón chào năm mới.",
            )

            easter_date = calculate_easter(year)
            add_event(
                easter_date,
                1,
                "Lễ Phục Sinh",
                "Lễ Phục Sinh (Easter) là một trong những ngày lễ quan trọng nhất của Kitô giáo, tưởng niệm sự kiện Chúa Giê-su sống lại từ cõi chết sau khi chịu đóng đinh trên thập tự giá. "
                "Lễ Phục Sinh được tính vào ngày Chủ nhật đầu tiên sau ngày trăng tròn đầu tiên tính từ điểm Xuân phân, biểu trưng cho sự tái sinh, niềm hy vọng, sự khởi đầu mới và chiến thắng của ánh sáng, sự sống.",
            )

            if year == 2026:
                mothers_day = get_nth_weekday_of_month(year, 5, 6, 2)
                add_event(
                    mothers_day,
                    1,
                    "Ngày của Mẹ",
                    "Ngày của Mẹ (Mother's Day) có nguồn gốc từ phong trào do bà Anna Marie Jarvis khởi xướng tại Mỹ vào đầu thế kỷ XX và được tổ chức phổ biến vào Chủ nhật tuần thứ hai của tháng 5 hằng năm. "
                    "Đây là dịp đặc biệt để những người con bày tỏ lòng biết ơn sâu sắc, tình yêu thương và sự kính trọng đối với sự hy sinh thầm lặng cùng công ơn sinh thành, dưỡng dục bao la của mẹ.",
                    rrule="FREQ=YEARLY;BYMONTH=5;BYDAY=2SU;UNTIL=21251231",
                )

                fathers_day = get_nth_weekday_of_month(year, 6, 6, 3)
                add_event(
                    fathers_day,
                    1,
                    "Ngày của Cha",
                    "Ngày của Cha (Father's Day) được khởi xướng bởi bà Sonora Smart Dodd tại bang Washington (Mỹ) vào năm 1910 để tri ân người cha cựu chiến binh đã một mình tần tảo nuôi dạy 6 anh chị em bà nên người, và được tổ chức vào Chủ nhật tuần thứ ba của tháng 6 hằng năm. "
                    "Đây là dịp để con cái tôn vinh vai trò trụ cột, điểm tựa vững chắc và tình yêu thương, che chở của người cha đối với gia đình.",
                    rrule="FREQ=YEARLY;BYMONTH=6;BYDAY=3SU;UNTIL=21251231",
                )

            try:
                thanh_minh_date = get_thanh_minh_date(year)
                add_event(
                    thanh_minh_date,
                    1,
                    "Tiết Thanh Minh",
                    "Tiết Thanh Minh là tiết khí thứ 5 trong 24 tiết khí của lịch phương Đông ('Thanh' là trong sáng, 'Minh' là tươi sáng, ấm áp). "
                    "Trong văn hóa truyền thống Việt Nam — như câu thơ Kiều nổi tiếng 'Thanh minh trong tiết tháng ba / Lễ là tảo mộ, hội là đạp thanh' — đây là dịp con cháu hướng về cội nguồn, đi tảo mộ, phát cỏ, đắp đất sửa sang phần mộ ông bà tổ tiên và du xuân gắn kết tình thân.",
                )

                # 2. Lễ Việt Nam (Âm lịch)
                mung_1_tet = get_solar_from_lunar(year, 1, 1)

                giao_thua = mung_1_tet - datetime.timedelta(days=1)
                ngay_29_tet = mung_1_tet - datetime.timedelta(days=2)
                ngay_28_tet = mung_1_tet - datetime.timedelta(days=3)

                add_event(
                    get_solar_from_lunar(year - 1, 12, 23),
                    1,
                    "Ngày ông Táo về trời",
                    "23 tháng Chạp\n"
                    "Theo quan niệm của dân gian, 23 ông Táo về trời, tâu với Ngọc Hoàng chuyện đời trong năm. Vì thế, người Việt làm lễ cúng ông Táo thịnh soạn, với mong muốn ông Táo sẽ tâu những điều tốt đẹp với Ngọc Hoàng.\n"
                    "- Tiễn ông Táo - Nét đẹp văn hóa dân gian:\n"
                    "Người Việt cúng cá chép để ông Táo có phương tiện về chầu trời. Ở miền Bắc người ta cúng một con cá chép còn sống thả trong chậu nước, ngụ ý 'cá hóa long' nghĩa là cá sẽ biến thành Rồng đưa ông Táo về trời. Con cá chép này sẽ được 'phóng sinh' (thả ra ao hồ hay ra sông) sau khi cúng.\n"
                    "Ở miền Trung, người ta cúng một con ngựa bằng giấy với yên, cương đầy đủ.\n"
                    "Miền Nam thì lễ vật đơn giản, cúng mũ, áo và đôi hia bằng giấy. Tùy theo từng gia cảnh, ngoài các lễ vật chính kể trên, người dân làm mâm cỗ mặn (với xôi gà, chân giò luộc, các món nấu nấm, măng…) hay lễ chay (trầu cau, hoa, quả, giấy vàng, giấy bạc…) để tiễn Táo Quân.",
                )
                add_event(
                    ngay_28_tet,
                    1,
                    "28 Tết Nguyên Đán",
                    "Những ngày giáp Tết Nguyên Đán cổ truyền của dân tộc, khi các gia đình Việt tất bật dọn dẹp, trang hoàng nhà cửa, sắm sửa hoa đào, hoa mai, quất cảnh, chuẩn bị lá dong, gạo nếp gói bánh chưng, bánh tét và bày mâm ngũ quả đón xuân.",
                )
                add_event(
                    ngay_29_tet,
                    1,
                    "29 Tết Nguyên Đán",
                    "Ngày áp Tết Nguyên Đán, thời điểm những người con xa quê trở về đoàn tụ bên gia đình, hoàn tất việc lau dọn bàn thờ gia tiên, nấu bánh chưng, bánh tét bên bếp lửa hồng và chuẩn bị đón thời khắc khép lại năm cũ.",
                )
                add_event(
                    giao_thua,
                    1,
                    "Giao Thừa",
                    "Đêm Tất Niên\n"
                    "Ngày cuối cùng của năm Âm lịch (chiều 30 Tết hoặc 29 Tết nếu tháng Chạp thiếu). Buổi chiều, các gia đình làm lễ cúng Tất niên mời ông bà tổ tiên về ăn Tết cùng con cháu và quây quần bên bữa cơm đoàn viên ấm áp cuối năm. "
                    "Đúng thời khắc chuyển giao giữa năm cũ và năm mới (đêm Giao Thừa - 'cựu giao, tân tiếp'), lễ cúng Giao Thừa ngoài trời và trong nhà được cử hành trang trọng để tiễn vị Hành khiển năm cũ, nghênh đón vị Hành khiển năm mới và cầu chúc một năm mới bình an, vạn sự cát tường.",
                )
                add_event(
                    giao_thua,
                    1,
                    "Đón ông Táo về nhà",
                    "Theo tín ngưỡng dân gian truyền thống, sau khi về trời chầu Ngọc Hoàng vào ngày 23 tháng Chạp, đến chiều 30 Tết (hoặc 29 Tết nếu tháng Chạp thiếu) trong lễ cúng Tất niên hoặc thời khắc Giao Thừa chuyển giao năm mới, các gia đình làm lễ rước ông Táo trở về ngự tại gian bếp để tiếp tục coi sóc bếp lửa, giữ gìn sự ấm no, gia đạo bình an và may mắn suốt năm mới.",
                )

                add_event(
                    mung_1_tet,
                    1,
                    "Mùng 1",
                    "Nghỉ lễ toàn quốc\n"
                    "Ngày Mùng 1 tháng Giêng Âm lịch — ngày đầu tiên của Tết Nguyên Đán, lễ hội cổ truyền lớn và thiêng liêng nhất của dân tộc Việt Nam đánh dấu sự khởi đầu của năm mới và mùa xuân mới. "
                    "Theo tục lệ 'Mùng 1 Tết Cha, Mùng 2 Tết Mẹ, Mùng 3 Tết Thầy', sáng Mùng 1 các gia đình làm lễ cúng gia tiên, thực hiện tục xông đất đầu năm, con cháu chúc thọ ông bà cha mẹ bên nội, trao nhận phong bao lì xì đỏ may mắn và đi lễ chùa cầu bình an, tài lộc.",
                )
                add_event(
                    mung_1_tet + datetime.timedelta(days=1),
                    1,
                    "Mùng 2",
                    "Nghỉ lễ toàn quốc\n"
                    "Ngày Mùng 2 tháng Giêng Âm lịch. Theo truyền thống 'Mùng 1 Tết Cha, Mùng 2 Tết Mẹ, Mùng 3 Tết Thầy', đây là ngày con cháu về thăm, chúc Tết và sum họp bên ông bà, họ hàng bên ngoại, đồng thời đi du xuân, trao gửi những lời chúc đầu năm tốt đẹp.",
                )
                add_event(
                    mung_1_tet + datetime.timedelta(days=2),
                    1,
                    "Mùng 3",
                    "Nghỉ lễ toàn quốc\n"
                    "Ngày Mùng 3 tháng Giêng Âm lịch. Theo truyền thống 'Mùng 1 Tết Cha, Mùng 2 Tết Mẹ, Mùng 3 Tết Thầy', đây là dịp học trò đến thăm hỏi, chúc Tết thầy cô giáo thể hiện đạo lý 'Tôn sư trọng đạo'. "
                    "Nhiều gia đình Việt cũng chọn ngày Mùng 3 để làm lễ cúng hóa vàng (tiễn ông bà tổ tiên sau những ngày về sum họp đón Tết cùng con cháu).",
                )
                add_event(
                    mung_1_tet + datetime.timedelta(days=3),
                    1,
                    "Mùng 4",
                    "Nghỉ lễ toàn quốc\n"
                    "Ngày Mùng 4 tháng Giêng Âm lịch. Trong kỳ nghỉ Tết Nguyên Đán, đây là ngày nhiều gia đình làm lễ hóa vàng tiễn gia tiên, đi trẩy hội mùa xuân hoặc bắt đầu khai xuân, mở hàng lấy ngày lành cho một năm mới công việc hanh thông, thuận lợi.",
                )
                add_event(
                    mung_1_tet + datetime.timedelta(days=4),
                    1,
                    "Mùng 5",
                    "Nghỉ lễ toàn quốc\n"
                    "Ngày Mùng 5 tháng Giêng Âm lịch — ngày nghỉ cuối trong dịp Tết Nguyên Đán truyền thống, đồng thời là ngày kỷ niệm Chiến thắng Ngọc Hồi - Đống Đa lịch sử (mùa xuân năm Kỷ Dậu 1789), khi Hoàng đế Quang Trung (Nguyễn Huệ) chỉ huy nghĩa quân Tây Sơn thần tốc đại phá 29 vạn quân Thanh, giải phóng kinh thành Thăng Long.",
                )

                add_event(
                    get_solar_from_lunar(year, 1, 10),
                    1,
                    "Vía Thần Tài",
                    "10 tháng Giêng\n"
                    "Theo tín ngưỡng dân gian, ngày mùng 10 tháng Giêng Âm lịch là ngày Thần Tài — vị thần cai quản tiền bạc, tài lộc — bay về trời sau thời gian xuống nhân gian. "
                    "Vào ngày này, các gia đình và đặc biệt là giới kinh doanh, buôn bán thường sắm lễ cúng Thần Tài (như bộ tam sên, cá lóc nướng, hoa tươi, trái cây...) và mua vàng cầu may với ước vọng một năm mới buôn may bán đắt, tài lộc dồi dào, sung túc.",
                )
                add_event(
                    get_solar_from_lunar(year, 1, 15),
                    1,
                    "Tết Nguyên Tiêu",
                    "15 tháng Giêng\n"
                    "Tết Nguyên Tiêu (còn gọi là Tết Thượng Nguyên hay Rằm tháng Giêng) là đêm trăng tròn đầu tiên của năm mới Âm lịch ('Nguyên' là thứ nhất, 'Tiêu' là đêm). "
                    "Với quan niệm 'Lễ Phật quanh năm không bằng Rằm tháng Giêng', người Việt thường đi chùa lễ Phật, dâng hương cúng gia tiên cầu mong quốc thái dân an, gia đạo bình an, may mắn suốt cả năm. "
                    "Tại Việt Nam, ngày Rằm tháng Giêng hằng năm còn là Ngày Thơ Việt Nam.",
                )
                add_event(
                    get_solar_from_lunar(year, 3, 3),
                    1,
                    "Tết Hàn Thực",
                    "3 tháng 3 Âm lịch\n"
                    "Tết Hàn Thực diễn ra vào ngày mùng 3 tháng 3 Âm lịch hằng năm ('Hàn thực' nghĩa là thức ăn nguội). "
                    "Khi tiếp biến vào văn hóa Việt Nam, ngày lễ này mang đậm bản sắc thuần Việt: người dân không kiêng lửa mà cùng nhau làm bánh trôi, bánh chay ('bánh trôi nước') từ bột gạo nếp thơm dẻo, nhân đường phên hoặc đậu xanh để dâng cúng Phật và ông bà tổ tiên, thể hiện tấm lòng thành kính hướng về cội nguồn.",
                )
                add_event(
                    get_solar_from_lunar(year, 3, 10),
                    1,
                    "Giỗ Tổ Hùng Vương",
                    "Nghỉ lễ toàn quốc - 10 tháng 3 Âm lịch\n"
                    "'Dù ai đi ngược về xuôi / Nhớ ngày Giỗ Tổ mùng mười tháng ba'. Ngày Giỗ Tổ Hùng Vương (Lễ hội Đền Hùng) là ngày Quốc lễ trọng đại của dân tộc Việt Nam nhằm tưởng nhớ và tri ân công lao dựng nước của các Vua Hùng — những vị vua đầu tiên đã lập nên nhà nước Văn Lang. "
                    "Tín ngưỡng thờ cúng Hùng Vương đã được UNESCO ghi danh là Di sản văn hóa phi vật thể đại diện của nhân loại, biểu trưng cho tinh thần đại đoàn kết và đạo lý 'Uống nước nhớ nguồn' của con Lạc cháu Hồng.",
                )
                add_event(
                    get_solar_from_lunar(year, 4, 15),
                    1,
                    "Lễ Phật Đản",
                    "15 tháng 4 Âm lịch\n"
                    "Đại lễ Phật Đản (Vesak) kỷ niệm ngày Đức Phật Thích Ca Mâu Ni (Thái tử Tất Đạt Đa) đản sinh tại vườn Lâm Tỳ Ni vào năm 624 trước Công nguyên. "
                    "Từ năm 1999, Liên Hợp Quốc đã công nhận Đại lễ Vesak là lễ hội văn hóa, tôn giáo quốc tế. "
                    "Vào dịp Rằm tháng Tư Âm lịch, các tự viện và Phật tử khắp nơi trang hoàng cờ hoa, tổ chức lễ tắm Phật, rước xe hoa, phóng sinh, ăn chay và làm việc thiện, lan tỏa thông điệp từ bi, trí tuệ và hòa bình.",
                )
                add_event(
                    get_solar_from_lunar(year, 5, 5),
                    1,
                    "Tết Đoan Ngọ",
                    "5 tháng 5 Âm lịch\n"
                    "Tết Đoan Ngọ diễn ra vào giờ Ngọ ngày mùng 5 tháng 5 Âm lịch, tại Việt Nam còn được gọi dân dã là 'Tết diệt sâu bọ' hoặc 'Tết nửa năm'. "
                    "Đây là thời điểm giao mùa chuyển sang nắng nóng, sâu bệnh dễ phát sinh. Theo phong tục cổ truyền, ngay từ sáng sớm các gia đình làm lễ cúng tổ tiên và thưởng thức cơm rượu nếp, bánh ú tro, các loại trái cây đầu mùa (mận, vải, xoài...) để 'diệt sâu bọ' trong cơ thể, cầu mong sức khỏe bình an và mùa màng bội thu.",
                )
                add_event(
                    get_solar_from_lunar(year, 7, 7),
                    1,
                    "Lễ Thất Tịch",
                    "7 tháng 7 Âm lịch\n"
                    "Lễ Thất Tịch (mùng 7 tháng 7 Âm lịch) gắn liền với chuyện tình cảm động của Ngưu Lang - Chức Nữ và sự tích Ông Ngâu - Bà Ngâu trong dân gian Việt Nam: mỗi năm hai người chỉ được đoàn tụ một lần vào đêm 7/7 trên cầu Ô Thước do đàn chim khách kết thành, những giọt nước mắt ngày hội ngộ và chia ly hóa thành mưa ngâu tháng Bảy. "
                    "Ngày Thất Tịch được xem là ngày lễ tình nhân phương Đông, nhiều bạn trẻ cũng có phong tục ăn chè đậu đỏ để cầu tình duyên viên mãn, may mắn.",
                )
                add_event(
                    get_solar_from_lunar(year, 7, 15),
                    1,
                    "Lễ Vu Lan",
                    "15 tháng 7 Âm lịch\n"
                    "Lễ Vu Lan báo hiếu (Rằm tháng Bảy Âm lịch) bắt nguồn từ sự tích Bồ tát Mục Kiền Liên đại hiếu cứu mẹ thoát khỏi kiếp ngạ quỷ, đồng thời trùng với lễ Xá tội vong nhân (Tết Trung Nguyên) trong tín ngưỡng dân gian. "
                    "Đây là dịp lễ lớn trong văn hóa Việt Nam để mỗi người con tưởng nhớ, tri ân công ơn sinh thành dưỡng dục của cha mẹ với nghi thức 'Bông hồng cài áo' thiêng liêng, đồng thời làm lễ cúng gia tiên, cúng chúng sinh và làm việc thiện tích phước.",
                )
                add_event(
                    get_solar_from_lunar(year, 8, 15),
                    1,
                    "Trung Thu",
                    "15 tháng 8 Âm lịch\n"
                    "Tết Trung Thu (còn gọi là Tết Đoàn Viên, Tết Trông Trăng hay Tết Thiếu Nhi) diễn ra vào đêm Rằm tháng Tám Âm lịch khi mặt trăng thu tròn đầy và sáng đẹp nhất trong năm. "
                    "Vào dịp này, các gia đình quây quần bên nhau dâng cúng tổ tiên, thưởng thức bánh nướng, bánh dẻo, uống trà ngắm trăng và tổ chức cho trẻ em rước đèn ông sao, múa lân, phá cỗ trông trăng gắn liền với sự tích Chú Cuội - Chị Hằng.",
                )
                add_event(
                    get_solar_from_lunar(year, 9, 9),
                    1,
                    "Tết Trùng Cửu",
                    "9 tháng 9 Âm lịch\n"
                    "Tết Trùng Cửu (hay Tết Trùng Dương) diễn ra vào ngày mùng 9 tháng 9 Âm lịch, bắt nguồn từ quan niệm số 9 trong Kinh Dịch là số dương cực thịnh. "
                    "Do chữ 'Cửu' (số 9) đồng âm với chữ 'Cửu' trong 'vĩnh cửu, trường thọ', ngày lễ này mang ý nghĩa chúc thọ ông bà, cha mẹ và người cao tuổi, gắn liền với nét đẹp văn hóa đăng cao (lên núi thưởng ngoạn thu cảnh) và thưởng trà, rượu hoa cúc dưỡng sinh.",
                )
                add_event(
                    get_solar_from_lunar(year, 10, 10),
                    1,
                    "Tết Trùng Thập",
                    "10 tháng 10 Âm lịch\n"
                    "Tết Trùng Thập diễn ra vào ngày mùng 10 tháng 10 Âm lịch, trong dân gian Việt Nam còn gọi là Tết Cơm Mới (Tết Thường Tân) hoặc ngày lễ truyền thống của các thầy thuốc, lương y. "
                    "Sau vụ gặt tháng Mười, người nông dân chọn những hạt lúa nếp mới thơm dẻo nhất để thổi xôi, làm bánh dâng cúng Thần Nông và tổ tiên nhằm tạ ơn trời đất đã ban cho mưa thuận gió hòa, mùa màng bội thu.",
                )
                add_event(
                    get_solar_from_lunar(year, 10, 15),
                    1,
                    "Tết Hạ Nguyên",
                    "15 tháng 10 Âm lịch\n"
                    "Tết Hạ Nguyên (Rằm tháng Mười Âm lịch) là một trong ba ngày lễ 'Tam Nguyên' lớn trong năm Âm lịch (cùng với Thượng Nguyên 15/1 và Trung Nguyên 15/7). "
                    "Trong văn hóa cổ truyền Việt Nam, Tết Hạ Nguyên gắn liền với tục tiến tân (lễ mừng lúa mới): khi vụ mùa thu hoạch đã hoàn tất, các gia đình nấu cơm gạo mới dâng cúng thần linh và ông bà tổ tiên để bày tỏ lòng biết ơn, cầu mong gia đình ấm no, sung túc.",
                )

                # 3. Ngày Mùng Một - Rằm hàng tháng (bao gồm cả tháng nhuận) rơi vào năm dương lịch `year`
                for lunar_y in (year - 1, year):
                    lunar_year_obj = LunarYear.fromYear(lunar_y)
                    for m_obj in lunar_year_obj.getMonthsInYear():
                        m = m_obj.getMonth()
                        month_name = format_lunar_month_name(m)

                        mung_1_date = get_solar_from_lunar(lunar_y, m, 1)
                        if mung_1_date.year == year and m != 1:
                            add_event(
                                mung_1_date,
                                1,
                                f"Mùng 1 {month_name}",
                                format_mung_1_meaning(m),
                            )

                        ram_date = get_solar_from_lunar(lunar_y, m, 15)
                        if ram_date.year == year:
                            add_event(
                                ram_date,
                                1,
                                f"Rằm {month_name}",
                                format_ram_meaning(m),
                            )

            except Exception as e:
                print(f"Lỗi khi xử lý âm lịch năm {year}: {e}")

            events.sort(key=lambda item: item[0])
            for start_date, duration_days, summary, description, rrule in events:
                event_seq += 1
                uid_hash = hashlib.md5(
                    f"{start_date.isoformat()}|{duration_days}|{summary}|{event_seq}".encode("utf-8")
                ).hexdigest()[:12]
                uid = f"{start_date.strftime('%Y%m%d')}-{event_seq:05d}-{uid_hash}@vietnam-holidays"
                write_event(
                    f,
                    start_date,
                    duration_days,
                    summary,
                    description,
                    uid=uid,
                    dtstamp=dtstamp,
                    rrule=rrule,
                )

        write_ics_line(f, "END:VCALENDAR")
        print(f"Đã tạo thành công tệp {output_file}")

if __name__ == "__main__":
    generate_calendar()
