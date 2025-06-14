from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, predict_routes, info_routes, allergy_routes, document_routes
from config.database import engine
from models import user_model, prediction_model, disease_model, document_model

# Create database tables if they don't exist
user_model.Base.metadata.create_all(bind=engine)
prediction_model.Base.metadata.create_all(bind=engine)
disease_model.Base.metadata.create_all(bind=engine)
document_model.Base.metadata.create_all(bind=engine)

# IMPORTANT: Populate diseases on startup if database is empty
try:
    from services.disease_service import populate_sample_diseases
    populate_sample_diseases()
    print("✅ Disease database initialization completed")
except Exception as e:
    print(f"⚠️ Warning: Could not populate diseases: {e}")

app = FastAPI(title="IPHC Backend API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["User"])  # Fixed: Changed from "/user" to "/users"
app.include_router(predict_routes.router, prefix="/predict", tags=["Predict"])
app.include_router(info_routes.router, prefix="/info", tags=["Info"])
app.include_router(allergy_routes.router, prefix="/allergies", tags=["Allergies"])
app.include_router(document_routes.router, prefix="/documents", tags=["Documents"])

# Add the disease info route directly to app root for /api/disease/ endpoint
@app.get("/api/disease/{disease_name}")
async def get_disease_details_root(disease_name: str):
    try:
        from services.disease_service import get_disease_by_name
        import urllib.parse

        decoded_name = urllib.parse.unquote(disease_name)
        disease_info = get_disease_by_name(decoded_name)
        if disease_info:
            return {"success": True, "disease": disease_info}
        else:
            # fallback (should rarely happen)
            return {
                "success": True,
                "disease": {
                    "name": decoded_name,
                    "overview": f"{decoded_name} is a medical condition that requires proper medical evaluation. Please consult with a healthcare professional for accurate diagnosis and treatment recommendations.",
                    "causes": "Various factors may contribute to this condition. A healthcare provider can help identify specific causes in your case.",
                    "symptoms": "Symptoms can vary between individuals. Please discuss your specific symptoms with a medical professional.",
                    "treatments": "Treatment options should be discussed with a qualified healthcare provider who can assess your individual situation.",
                    "prevention": "Prevention strategies may be available. Consult with a healthcare professional for personalized advice.",
                    "when_to_see_doctor": "Consult a healthcare provider for proper evaluation and treatment recommendations.",
                    "how_common": "Frequency information varies. Please consult a healthcare professional for more details."
                }
            }
    except Exception as e:
        print(f"DEBUG: Exception in disease info endpoint: {e}")
        return {
            "success": True,
            "disease": {
                "name": str(disease_name),
                "overview": "Medical condition information. Please consult with a healthcare professional for more information.",
                "causes": "Please consult a healthcare professional.",
                "symptoms": "Please consult a healthcare professional.",
                "treatments": "Please consult a healthcare professional.",
                "prevention": "Please consult a healthcare professional.",
                "when_to_see_doctor": "Please consult a healthcare professional.",
                "how_common": "Please consult a healthcare professional."
            }
        }

@app.get("/")
def read_root():
    return {
        "message": "🚀 IPHC Backend API is running!",
        "version": "1.0.0",
        "endpoints": {
            "user": "/user",
            "predict": "/predict",
            "info": "/info",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "IPHC Backend API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)