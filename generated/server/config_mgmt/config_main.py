import uvicorn
import hashlib
import json as _json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

app = FastAPI(title='Config Management Server', version='1.2.0')

CONFIG_REGISTRY = {}

class ConfigPayload(BaseModel):
    service_name: str = Field(..., min_length=3, max_length=80)
    version: str = Field(..., pattern=r'^v[0-9]+\.[0-9]+\.[0-9]+$')
    config_data: Dict[str, Any]
    description: Optional[str] = Field(None, max_length=200)

@app.get('/health')
def config_health():
    return {'status': 'healthy', 'registered_services': len(CONFIG_REGISTRY)}

@app.post('/api/v1/config/register')
def register_config(payload: ConfigPayload):
    raw = _json.dumps(payload.config_data, sort_keys=True).encode()
    checksum = hashlib.sha256(raw).hexdigest()[:16]
    return {'status': 'registered', 'service': payload.service_name, 'version': payload.version}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8070)
