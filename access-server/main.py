import uvicorn
from app.main import main
app = main()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8090)