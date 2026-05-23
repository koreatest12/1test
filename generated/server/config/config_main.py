import uvicorn
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title='Enterprise Configuration Management Node', version='1.3.0')

# CodeQL 대비: 형상관리 메타데이터 주입 및 크로스 사이트 스크립팅 방어
class CommitPayload(BaseModel):
    repo_name: str = Field(..., pattern=r'^[a-zA-Z0-9_\-]{3,50}$')
    commit_message: str = Field(..., min_length=1, max_length=200)
    changes_count: int = Field(..., ge=1, le=5000)

@app.get('/api/v1/config/health')
def config_health():
    return {'status': 'healthy', 'node': 'config_management_v1'}

@app.post('/api/v1/config/commit')
def record_commit(payload: CommitPayload):
    # 위험 문자열 스캔 (디렉토리 취약점 및 XSS 시도 1차 필터)
    if '..' in payload.commit_message or '<script>' in payload.commit_message:
        raise HTTPException(status_code=400, detail='Path Traversal or XSS payload detected.')
    
    return {
        'status': 'committed',
        'repository': payload.repo_name,
        'changes_applied': payload.changes_count
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8100)
