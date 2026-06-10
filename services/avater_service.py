import httpx

from core.config import SUPABASE_URL, SUPABASE_KEY
from utils.helpers import build_avatar_filename

async def upload_avater_to_supabase(file_bytes: bytes, content_type: str, user_id: str):
    filename = build_avatar_filename(user_id)
    
    url = f"{SUPABASE_URL}/storage/v1/object/bks_avaters/{filename}"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": content_type,
        "x-upsert": "true"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(url, content=file_bytes, headers=headers)

        if res.status_code not in [200, 201]:
            raise Exception(res.text)
        
    return filename

def get_avater_url(path: str | None):
    if not path:
        return None

    return (
        f"{SUPABASE_URL}/storage/v1/object/bks_avaters/{path}"
    )