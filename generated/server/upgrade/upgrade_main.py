import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI(title='OTA Upgrade Node', version='1.5.0')
class UpgradePayload(BaseModel):
    component: str = Field(..., min_length=3, max_length=50)
    force_update: bool = False
@app.get('/health')
def upgrade_health(): return {'status': 'healthy'}
@app.post('/api/v1/upgrade/apply')
def apply_upgrade(payload: UpgradePayload):
    if payload.component == 'core-kernel' and not payload.force_update: raise HTTPException(400)
    return {'status': 'upgraded', 'component': payload.component}
if __name__ == '__main__': uvicorn.run(app, host='0.0.0.0', port=8060)
