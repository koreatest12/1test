import uvicorn
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(title='Isolated Enterprise Security Node', version='1.2.0')

class QueryModel(BaseModel):
    rule_id: str
    @field_validator('rule_id')
    @classmethod
    def validate_rule(cls, v):
        if not re.match(r'^SEC-[0-9]+$', v) or not (3 <= len(v) <= 50):
            raise ValueError('Invalid rule format')
        return v

@app.get('/api/v1/security/status')
def security_node_status():
    return {'status': 'healthy'}

@app.post('/api/v1/security/inspect')
def inspect_rule(query: QueryModel):
    mock_db = {'SEC-101': 'Injection Defense Triggered', 'SEC-102': 'Broken Auth Patched'}
    result = mock_db.get(query.rule_id)
    if not result:
        raise HTTPException(status_code=404, detail='Security rule not found.')
    return {'rule_id': query.rule_id, 'audit_result': result}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
