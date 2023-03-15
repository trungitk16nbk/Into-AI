Đồ án 1: Các thuật toán tìm kiếm
Môn: Nhập môn Trí tuệ nhân tạo

Các thành viên của nhóm:
	20120023 - Bùi Quốc Trung
	20120101 - Dũ Quốc Huy
	20120448 - Nguyễn Kông Đại

Các file và thư mục đi kèm:
	run.sh: chứa câu lệnh giúp chạy toàn bộ các thuật toán cho tất cả các bản đồ
	report.pdf: file báo cáo của nhóm
	source: chứa các file mà nguồn chương trình
	input: chứa các folder con (level_1, level_2, level_3, advance), trong đó là các file input<x>.txt (x là thứ tự file), chứa thông tin các bản đồ.

Khi chạy xong chương trình: sẽ tự động tạo thư mục output (ngang cấp với folder input) chia làm nhiều level -> input > thuật toán khác nhau. Chứa trong đó là tập tin cho thấy đường đi ngắn nhất có thể tìm thấy (NO nếu không tìm ra) và file đồ họa (.mp4)

Chương trình sử dụng thư viện pygame và vidmaker để tạo ra các file đồ họa, cần install 2 thư viện này để sử dụng.

Chú thích màu:
	Màu vàng: là điểm chặn, bức tường
	Màu đỏ: điểm Start (khi chạy đường đi thì đường màu đỏ chính là đường đi)
	Màu xanh nước biển: điểm đích
	Màu xanh lá: điểm bonus/ điểm đón
	Màu xám: các điểm được duyệt của thuật toán
	Màu xanh highlight: điểm bonus/ điểm đón mà được ăn trên đường đi của thuật toán

Cảm ơn đã đọc <3