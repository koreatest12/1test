import uvicorn
from fastapi import FastAPI

app = FastAPI(title='Enterprise AI Gateway Server', version='1.2.0')

@app.get('/health')
def gateway_health():
    return {'status': 'healthy', 'service': 'api_gateway_core', 'runtime': 'Node24-compatible'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
