"""
玄心理命 - 用户个人中心API
历史记录、收藏、设置管理
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..core.database import get_db, async_session
from ..core.user_service import UserService, HistoryService, FavoriteService, SettingsService
from ..core.auth import get_current_user  # 假设已有

router = APIRouter(prefix="/user", tags=["用户中心"])


# ==================== 请求/响应模型 ====================

class UserProfileUpdate(BaseModel):
    """用户资料更新"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None


class FavoriteRequest(BaseModel):
    """收藏请求"""
    item_type: str = Field(..., description="类型: bazi/ziwei/yijing/psychology/fusion")
    item_id: int
    note: Optional[str] = None


class SettingsUpdate(BaseModel):
    """设置更新"""
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    notification_enabled: Optional[bool] = None
    preferences: Optional[Dict] = None


class PaginationParams(BaseModel):
    """分页参数"""
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)


# ==================== 用户资料 ====================

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """获取当前用户资料"""
    async with async_session() as db:
        service = UserService(db)
        user = await service.get_user_by_id(current_user["id"])
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return {
            "success": True,
            "data": {
                "id": user.id,
                "phone": user.phone,
                "email": user.email,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "gender": user.gender,
                "birthday": user.birthday.isoformat() if user.birthday else None,
                "is_vip": user.is_vip,
                "vip_expire_date": user.vip_expire_date.isoformat() if user.vip_expire_date else None,
                "created_at": user.created_at.isoformat()
            }
        }


@router.put("/profile")
async def update_user_profile(
    data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新用户资料"""
    async with async_session() as db:
        service = UserService(db)
        
        update_data = data.dict(exclude_unset=True, exclude_none=True)
        user = await service.update_user_profile(current_user["id"], **update_data)
        
        return {
            "success": True,
            "message": "资料更新成功"
        }


@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """获取用户统计数据"""
    async with async_session() as db:
        service = UserService(db)
        stats = await service.get_user_stats(current_user["id"])
        
        return {
            "success": True,
            "data": stats
        }


# ==================== 历史记录 ====================

@router.get("/history/analyses")
async def get_analysis_history(
    analysis_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """获取命理分析历史"""
    async with async_session() as db:
        service = HistoryService(db)
        records = await service.get_user_analyses(
            current_user["id"], 
            analysis_type=analysis_type,
            limit=limit, 
            offset=offset
        )
        
        return {
            "success": True,
            "data": [
                {
                    "id": r.id,
                    "type": r.analysis_type,
                    "birth_info_id": r.birth_info_id,
                    "result_summary": r.result_data.get("summary", "") if r.result_data else "",
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
        }


@router.get("/history/analyses/{record_id}")
async def get_analysis_detail(
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """获取分析记录详情"""
    async with async_session() as db:
        service = HistoryService(db)
        record = await service.get_analysis_by_id(record_id, current_user["id"])
        
        if not record:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        return {
            "success": True,
            "data": {
                "id": record.id,
                "type": record.analysis_type,
                "birth_info_id": record.birth_info_id,
                "result_data": record.result_data,
                "created_at": record.created_at.isoformat()
            }
        }


@router.delete("/history/analyses/{record_id}")
async def delete_analysis(
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """删除分析记录"""
    async with async_session() as db:
        service = HistoryService(db)
        success = await service.delete_analysis(record_id, current_user["id"])
        
        if not success:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        return {"success": True, "message": "删除成功"}


@router.get("/history/divinations")
async def get_divination_history(
    method: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """获取占卜历史"""
    async with async_session() as db:
        service = HistoryService(db)
        records = await service.get_user_divinations(
            current_user["id"],
            method=method,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "data": [
                {
                    "id": r.id,
                    "method": r.method,
                    "question": r.question,
                    "hexagram": r.result_data.get("hexagram_name", "") if r.result_data else "",
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
        }


@router.get("/history/psychology")
async def get_psychology_history(
    test_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """获取心理测试历史"""
    async with async_session() as db:
        service = HistoryService(db)
        records = await service.get_user_psychology_tests(
            current_user["id"],
            test_type=test_type,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "data": [
                {
                    "id": r.id,
                    "test_type": r.test_type,
                    "result_summary": _get_psychology_summary(r.test_type, r.result_data),
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
        }


@router.get("/history/psychology/latest")
async def get_latest_psychology_results(
    current_user: dict = Depends(get_current_user)
):
    """获取最新的各类心理测试结果"""
    async with async_session() as db:
        service = HistoryService(db)
        results = await service.get_latest_psychology_results(current_user["id"])
        
        return {
            "success": True,
            "data": results
        }


@router.get("/history/fusions")
async def get_fusion_history(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """获取融合分析历史"""
    async with async_session() as db:
        service = HistoryService(db)
        records = await service.get_user_fusions(
            current_user["id"],
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "data": [
                {
                    "id": r.id,
                    "title": r.title,
                    "confidence": r.confidence,
                    "created_at": r.created_at.isoformat()
                }
                for r in records
            ]
        }


# ==================== 收藏管理 ====================

@router.post("/favorites")
async def add_favorite(
    data: FavoriteRequest,
    current_user: dict = Depends(get_current_user)
):
    """添加收藏"""
    async with async_session() as db:
        service = FavoriteService(db)
        
        try:
            favorite = await service.add_favorite(
                current_user["id"],
                data.item_type,
                data.item_id,
                data.note
            )
            return {
                "success": True,
                "message": "收藏成功",
                "data": {"id": favorite.id}
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/favorites")
async def remove_favorite(
    item_type: str,
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """取消收藏"""
    async with async_session() as db:
        service = FavoriteService(db)
        success = await service.remove_favorite(
            current_user["id"],
            item_type,
            item_id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="收藏不存在")
        
        return {"success": True, "message": "已取消收藏"}


@router.get("/favorites")
async def get_favorites(
    item_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """获取收藏列表"""
    async with async_session() as db:
        service = FavoriteService(db)
        favorites = await service.get_user_favorites(
            current_user["id"],
            item_type=item_type,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "data": [
                {
                    "id": f.id,
                    "item_type": f.item_type,
                    "item_id": f.item_id,
                    "note": f.note,
                    "created_at": f.created_at.isoformat()
                }
                for f in favorites
            ]
        }


@router.get("/favorites/check")
async def check_favorite(
    item_type: str,
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """检查是否已收藏"""
    async with async_session() as db:
        service = FavoriteService(db)
        is_favorited = await service.is_favorited(
            current_user["id"],
            item_type,
            item_id
        )
        
        return {"success": True, "is_favorited": is_favorited}


# ==================== 用户设置 ====================

@router.get("/settings")
async def get_settings(current_user: dict = Depends(get_current_user)):
    """获取用户设置"""
    async with async_session() as db:
        service = SettingsService(db)
        settings = await service.get_or_create_settings(current_user["id"])
        
        return {
            "success": True,
            "data": {
                "theme": settings.theme,
                "language": settings.language,
                "timezone": settings.timezone,
                "notification_enabled": settings.notification_enabled,
                "preferences": settings.preferences
            }
        }


@router.put("/settings")
async def update_settings(
    data: SettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新用户设置"""
    async with async_session() as db:
        service = SettingsService(db)
        
        update_data = data.dict(exclude_unset=True, exclude_none=True)
        settings = await service.update_settings(current_user["id"], **update_data)
        
        return {
            "success": True,
            "message": "设置更新成功"
        }


# ==================== 辅助函数 ====================

def _get_psychology_summary(test_type: str, result_data: Optional[Dict]) -> str:
    """获取心理测试结果摘要"""
    if not result_data:
        return ""
    
    if test_type == "mbti":
        return result_data.get("type_code", "")
    elif test_type == "big5":
        scores = result_data.get("scores", {})
        return f"O:{scores.get('O', 0)} C:{scores.get('C', 0)} E:{scores.get('E', 0)}"
    elif test_type == "archetype":
        return result_data.get("primary", {}).get("name", "")
    elif test_type == "enneagram":
        return f"{result_data.get('primary_type', '')}号"
    
    return ""
