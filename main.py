import uvicorn
import os

if __name__ == "__main__":
    # Use environment variables for configuration if available, otherwise default
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting Telecom Churn Agent on {host}:{port}")
    uvicorn.run("src.api:app", host=host, port=port, reload=True)
