        import uvicorn; from fastapi import FastAPI, HTTPException; from fastapi.middleware.cors import CORSMiddleware; from pydantic import BaseModel, Field
        app = FastAPI(title='Enterprise Fencing Service', version='2.0.0'); app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        class FenceRule(BaseModel): target_ip: str = Field(..., pattern=r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'); action: str = Field(..., pattern=r'^(ALLOW|DENY)$')
        @app.get('/health')
def fencing_health(): return {'status': 'healthy', 'node': 'fencing', 'port': 8050}
        if __name__ == '__main__': uvicorn.run(app, host='0.0.0.0', port=8050)
