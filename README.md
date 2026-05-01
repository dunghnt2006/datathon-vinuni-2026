# DATATHON 2026 - The Gridbreaker

**Team Name:** 3 con cá

**Team Members / Contributors:**
* Trần Yến Linh 
* Đinh Phương Hồng Ngọc
* Hồ Nguyễn Thuỳ Dung 
## Cấu trúc thư mục

```
├── data/                        # Dữ liệu cuộc thi
│   ├── products.csv
│   ├── customers.csv 
│   ├── promotions.csv
│   ├── geography.csv          
│   ├── orders.csv
│   ├── order_items.csv
│   ├── payments.csv
│   ├── shipments.csv
│   ├── returns.csv
│   ├── reviews.csv
│   ├── sales.csv
│   ├── inventory.csv
│   ├── web_traffic.csv
│   ├── baseline.ipynb
│   └── sample_submission.csv
│
├── MCQs.ipynb                   # Phần 1: Câu hỏi Trắc nghiệm
├── master.py                    # Script tạo bảng master tổng hợp (Phần 2)
├── master_data.xlsx             # Phân tích doanh thu & margin theo segment/promo (Phần 2)
├── inventory.xlsx               # Phân tích tồn kho theo category (Phần 2)
├── sales_forecasting.ipynb      # Phần 3: Mô hình Dự báo Doanh thu
├── submission.csv               # File kết quả dự báo nộp lên Kaggle
└── README.md
```

---

## Mô tả các file

### `MCQs.ipynb` — Phần 1: Câu hỏi Trắc nghiệm
Notebook này chứa toàn bộ code phân tích dữ liệu để trả lời 10 câu hỏi trắc nghiệm

### `master.py` + `master_data.xlsx` + `inventory.xlsx` — Phần 2: Trực quan hoá & Phân tích
 
- **`master.py`**: join các bảng dữ liệu thô và tính các cột `real_revenue`, `gross_profit`, `margin_pct`, xuất ra `master_data.csv`
- **`master_data.xlsx`**: phân tích doanh thu và biên lợi nhuận theo segment và khuyến mãi
- **`inventory.xlsx`**: phân tích tồn kho và sell-through rate theo category

### `sales_forecasting.ipynb` — Phần 3: Mô hình Dự báo Doanh thu
 
Notebook triển khai pipeline dự báo đồng thời `Revenue` và `COGS` cho giai đoạn `01/01/2023 – 01/07/2024` bằng **LightGBM**, bao gồm:
- **Feature engineering**: đặc trưng từ promotions, web_traffic, inventory, orders, returns, reviews (lag 1 ngày để tránh leakage); lag 1/7/14/30 ngày và rolling mean/std cho Revenue & COGS; calendar features có cờ mùa vụ Việt Nam (Tết, sale cuối năm, mid-year)
- **Huấn luyện**: hai mô hình độc lập cho Revenue và COGS, train đến 2020, validation 2021–2022, early stopping 100 rounds
- **Recursive prediction**: dự báo tuần tự từng ngày, cập nhật lag/rolling từ kết quả đã predict
- **Giải thích mô hình**: SHAP summary plot cho cả hai mô hình
- **Xuất kết quả**: lưu `submission.csv`

---

## Hướng dẫn chạy lại kết quả

### 1. Yêu cầu môi trường

```bash
pip install pandas numpy scikit-learn matplotlib seaborn shap lightgbm
```

### 2. Chuẩn bị dữ liệu

Đặt tất cả file CSV vào thư mục `data/` theo đúng cấu trúc ở trên.

### 3. Chạy notebook

---

## Kết quả mô hình trên tập validation

| Mục tiêu | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| **Revenue** | 81,934.79 | 120,892.50 | 0.9947 |
| **COGS** | 181,941.34 | 283,309.61 | 0.9618 |
