from services.info_service import get_disease_info, get_multiple_disease_info

def get_info(disease_name):
    try:
        result = get_disease_info(disease_name)
        if "message" in result and "not found" in result["message"].lower():
            return {
                "success": False,
                "message": result["message"],
                "data": None
            }
        return {
            "success": True,
            "message": f"Info for '{disease_name}' retrieved successfully",
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to retrieve info: {str(e)}",
            "data": None
        }

def get_batch_info(disease_list):
    try:
        result = get_multiple_disease_info(disease_list)
        return {
            "success": True,
            "message": "Batch info retrieved successfully",
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Batch info failed: {str(e)}",
            "data": None
        }
