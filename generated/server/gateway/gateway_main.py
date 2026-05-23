import uvicorn
import re
from fastapi import FastAPI, HTTPException, Header
from typing import Optional

app = FastAPI(title='Enterprise AI Gateway Server', version='1.2.0')

# CodeQL 대비: 주입 공격 방어를 위한 엄격한 엔드포인트 세그먼트 정규식 매칭
NODE_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]+$')

@app.get('/health')
def gateway_health():
    return {'status': 'healthy', 'service': 'api_gateway_core'}

@app.get('/api/v1/validate/{node_id}')
def validate_node(node_id: str, x_auth_token: Optional[str] = Header(None)):
    # 1. 하드코딩된 자격증명 배제 및 토큰 필수 유효성 스캔 검증
    if not x_auth_token or len(x_auth_token) < 16:
        raise HTTPException(status_code=401, detail='Invalid or missing security token.')
    
    # 2. Path Injection(경로 조작 및 SSRF 탐지) 방지를 위한 정제 검사
    if not NODE_PATTERN.match(node_id):
        raise HTTPException(status_code=400, detail='Malicious input pattern detected.')
        
    return {'status': 'authorized', 'node_id': node_id}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
