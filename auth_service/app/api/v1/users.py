from fastapi import APIRouter
from app.db.session import sessionDep
from app.service.user_service import delete_user_by_id,get_user_by_userid

router=APIRouter(prefix="/users")

@router.post("/delete")
async def deleteUser(session:sessionDep,id:int):
    await delete_user_by_id(session,id)


