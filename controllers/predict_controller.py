from services.predict_service import predict_result, get_predictions_by_user, delete_prediction_by_id

def handle_predict(data: dict):
    try:
        result = predict_result(data)
        return {
            "success": True,
            "message": "Prediction successful",
            "data": {
                "predict_id": result["predict_id"],
                "input": result["input"],
                "results": result["top_results"]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Prediction failed: {str(e)}",
            "data": None
        }

def handle_get_predictions(user_id: int):
    try:
        predictions = get_predictions_by_user(user_id)
        return {
            "success": True,
            "message": f"Menemukan {len(predictions)} prediksi",
            "data": predictions
        }
    except ValueError as e:
        return {"success": False, "message": str(e), "data": None}
    except Exception as e:
        return {"success": False, "message": f"Gagal mengambil data: {str(e)}", "data": None}

def handle_delete_prediction(predict_id: int):
    try:
        delete_prediction_by_id(predict_id)
        return {"success": True, "message": "Prediksi berhasil dihapus", "data": None}
    except ValueError as e:
        return {"success": False, "message": str(e), "data": None}
    except Exception as e:
        return {"success": False, "message": f"Gagal menghapus prediksi: {str(e)}", "data": None}