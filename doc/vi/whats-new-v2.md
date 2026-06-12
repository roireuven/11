# Có gì mới trong v2.3 / v2.4

Hướng dẫn này tóm tắt các tính năng chính được thêm vào trong **ổn định v2.3** và **ổn định v2.4** của HotelRestaurantMini-MartQuản lý.

**Trang web sống ổn định:**

| Phiên bản | URL |
|----------|------|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Phát triển** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Giao diện đầy đủ bằng 21 ngôn ngữ

Giao diện người dùng ứng dụng web có sẵn bằng **21 ngôn ngữ**: tiếng Anh, tiếng Tây Ban Nha, tiếng Pháp, tiếng Đức, tiếng Nhật, tiếng Hàn, tiếng Ả Rập, tiếng Hindi, tiếng Thái, tiếng Việt, tiếng Indonesia, tiếng Thổ Nhĩ Kỳ, tiếng Nga, tiếng Ý, tiếng Hà Lan, tiếng Ba Lan, tiếng Do Thái, tiếng Lào, tiếng Bồ Đào Nha (Brazil), tiếng Trung (Giản thể) và tiếng Trung (Phồn thể).

### Nơi thay đổi ngôn ngữ

| Màn hình | Như thế nào |
|--------|------|
| **Đăng nhập / thiết lập** | Ngôn ngữ thả xuống trong tiêu đề (trước khi đăng nhập) |
| **Sau khi đăng nhập** | Bộ chọn ngôn ngữ thanh trên cùng hoặc **Bản địa hóa** trong menu |
| **Cài đặt** | Phần ngôn ngữ ứng dụng |

Tùy chọn được lưu trong bộ nhớ trình duyệt (`hotel_mgr_uiLocale`).

### RTL (từ phải sang trái)

**Tiếng Ả Rập** và **Tiếng Do Thái** bật bố cục RTL cho toàn bộ ứng dụng. Các biểu mẫu phương thức sử dụng tính năng căn chỉnh được cải tiến để nhãn và thông tin đầu vào đọc chính xác bằng cả ngôn ngữ LTR và RTL.

---

## Thiết lập lần đầu (đã dịch)

Trình hướng dẫn thiết lập được bản địa hóa hoàn toàn:

- Tên doanh nghiệp/khách sạn
- Văn bản tiêu đề hệ thống
- Các trường tên người dùng, email và mật khẩu của quản trị viên
- Tất cả các nút và thông báo xác nhận

Sau khi thiết lập, tên khách sạn sẽ được lưu trữ và hiển thị trong tiêu đề ứng dụng đã định cấu hình.

---

## Thao tác nhanh trên bảng điều khiển (lưới PMS)

**Trang tổng quan** hiển thị một lưới các nút **++** màu xanh lam cho các tác vụ phổ biến:

| Nút | Mở |
|--------|--------|
| Thêm Phòng | Mẫu phòng mới |
| Thêm đặt chỗ | Hình thức đặt phòng mới |
| Thêm khách | Mẫu khách mới |
| Thêm nhiệm vụ | Phiếu bảo trì mới |
| Thêm dịch vụ | Yêu cầu dịch vụ mới |
| Thêm hóa đơn | Mẫu hóa đơn mới |
| Thêm hàng | Mặt hàng tồn kho mới |
| Thêm Thực đơn | Mục menu mới |
| Thêm mặt hàng trong cửa hàng | Cửa hàng mới / mặt hàng mini-mart |
| Thêm người dùng | Tài khoản nhân viên mới |

**Lưu ý:** *Thêm dịch vụ dọn dẹp* và *Thêm giao dịch* đã bị xóa khỏi lưới này (v2.4). Sử dụng thanh bên cho **Dọn phòng** và **Giao dịch** khi cần.

---

## Các dạng thức được dịch

Hộp thoại thêm và chỉnh sửa được bản địa hóa bằng tất cả 21 ngôn ngữ, bao gồm:

- **Bảo trì** — vé mới (phòng, mức độ ưu tiên, vấn đề, ghi chú)
- **Hóa đơn** — thêm / chỉnh sửa (khách, phòng, ngày, số tiền, trạng thái thanh toán)
- **Hàng tồn kho** — thêm / chỉnh sửa mặt hàng (tên, mã vạch, danh mục, số lượng, tính khả dụng của POS)
- **Mục menu** — thêm / chỉnh sửa (tên, biểu tượng, giá, danh mục, hình ảnh, liên kết chứng khoán)
- **Mặt hàng trong cửa hàng** — thêm / chỉnh sửa (tên, giá, danh mục, biểu tượng kệ, mã vạch, kho)- **Tài khoản người dùng** — thêm / chỉnh sửa (tên, email, mật khẩu, vai trò)

Nhãn tải lên hình ảnh (“từ thiết bị”, “hoặc URL hình ảnh”) tuân theo ngôn ngữ hiện hoạt.

---

## Đặt phòng → Khách mới

Khi tạo **đặt phòng**, nếu khách chưa có trong thư mục:

1. Nhấn vào **+ Khách mới** (hoặc tương đương) trên mẫu đặt phòng.
2. Điền vào ô **New Guest** (tên, hộ chiếu, quốc tịch, ngày sinh, phương thức thanh toán, liên hệ, ghi chú).
3. Nhấn **Thêm khách và quay lại** — bạn quay lại đặt phòng với khách mới đã chọn.

Bộ chọn quốc tịch (danh sách tìm kiếm) cũng được dịch.

---

## Tài liệu

- Hướng dẫn **Có gì mới** này có sẵn ở tất cả 21 ngôn ngữ tài liệu.
- Mở tài liệu từ ứng dụng: **thanh trên cùng → Tài liệu**, **☰ Trợ giúp → Tài liệu** hoặc **điều hướng dưới cùng → Tài liệu**.
- URL độc lập: `/doc/?lang={code}#/whats-new-v2`

---

## Dành cho quản trị viên

| Nhiệm vụ | Ở đâu |
|------|--------|
| Đào tạo nhân viên về chuyển đổi ngôn ngữ | [Localization](localization.md) |
| Cấu hình thuộc tính sau khi nâng cấp | [Settings & configuration](settings-and-configuration.md) |
| Triển khai các bản cập nhật | [Deployment](deployment.md) — `npm run deploy:stable` xuất bản lên v2.3 và v2.4 |

---

## Hướng dẫn liên quan

- [Localization](localization.md) — ngôn ngữ, RTL, tệp ngôn ngữ
- [First-time setup](first-time-setup.md) — cấu hình ban đầu
- [Navigation & UI](navigation-and-ui.md) — bảng điều khiển, thanh bên, điều hướng di động
- [Hotel operations](hotel-operations.md) — đặt chỗ và khách
- [Deployment](deployment.md) — phát triển so với ổn định v2.3 / v2.4