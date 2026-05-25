import uvicorn
from fastapi import FastAPI
app = FastAPI(title='CONFIG Node')
@app.get('/health')
def h(): return {'status':'healthy'}
if __name__ == '__main__': uvicorn.run(app, host='0.0.0.0', port=8000)
