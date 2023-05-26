from fastapi import APIRouter

from uuid import uuid4

items_router = APIRouter(prefix="/items", tags=['Items'])


@items_router.get('/{id}', name='Select items for id')
async def select_item(id: int = id):
    return {'id': id}
