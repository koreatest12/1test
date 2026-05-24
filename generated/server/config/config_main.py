import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title='Enterprise Config Node', version='1.3.0')

class CommitPayload(BaseModel):
    repo_name: str = Field(..., pattern=r'^[a-zA-Z0-9_\-]{3,50}$')
    commit_message: str = Field(..., min_length=1, max_length=200)
    changes_count: int = Field(..., ge=1, le=5000)

@app.get('/health')
def config_health():
    return {'status': 'healthy'}

@app.post('/api/v1/config/commit')
def record_commit(payload: CommitPayload):
    if '..' in payload.commit_message or '<script>' in payload.commit_message:
        raise HTTPException(status_code=400, detail='Invalid payload')
    return {'status': 'committed', 'repository': payload.repo_name}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8070)
