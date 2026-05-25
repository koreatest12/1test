import uvicorn; from fastapi import FastAPI; from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title='MIGRATION Node', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
@app.get('/health')
def h(): return {'status':'healthy', 'service': 'migration', 'port': 8090, 'version': '2.0.0'}
if __name__ == '__main__': uvicorn.run(app, host='0.0.0.0', port=8090)
