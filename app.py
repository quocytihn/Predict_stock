from flask import Flask, jsonify, request, render_template
from model import predict_stock


app = Flask(__name__)

# API để dự đoán
@app.route("/api/predict", methods=["POST"])
def predict():
    """
    API nhận mã cổ phiếu và trả về ngày, giá thực tế, giá dự đoán.
    """
    try:
        # Nhận mã cổ phiếu từ JSON request
        request_data = request.get_json()
        stock_code = request_data.get("stock_code")
        
        if not stock_code:
            return jsonify({"error": "Mã cổ phiếu không được để trống"}), 400

        # Huấn luyện mô hình và dự đoán
        dates, actual_prices, predictions = predict_stock(stock_code)
        # Tạo output JSON với format theo yêu cầu
        result = []
        for date, actual, pred in zip(dates, actual_prices, predictions):
            result.append({
                "date": date,
                "actual_price": actual,
                "predicted_price": pred
            })

        return jsonify({
            "stock_code": stock_code,
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Trang HTML hiển thị biểu đồ đường giá cổ phiếu  
@app.route("/chart/<stock_code>")
def chart(stock_code):
    """
    Trang HTML hiển thị biểu đồ đường giá cổ phiếu.
    """
    try:
        # Lấy dữ liệu từ API
        dates, actual_prices, predictions = predict_stock(stock_code)
        
        # Loại bỏ giá trị 'N/A'
        clean_dates = []
        clean_actual_prices = []
        clean_predictions = []
        for date, actual, pred in zip(dates, actual_prices, predictions):
            if actual != "N/A":
                clean_dates.append(date)
                clean_actual_prices.append(actual)
            clean_predictions.append(pred)
        
        # Render HTML template
        return render_template(
            "chart.html",
            stock_code=stock_code,
            dates=clean_dates,
            actual_prices=clean_actual_prices,
            predicted_prices=clean_predictions,
        )
    except Exception as e:
        return f"Lỗi: {str(e)}", 500

# Route đơn giản để kiểm tra API
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
