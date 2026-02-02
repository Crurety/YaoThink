"""
玄心理命 - 用户服务层
用户管理、历史记录、收藏等功能
"""

from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .database import (
    User, BirthInfo, AnalysisRecord, DivinationRecord, 
    PsychologyTest, FusionRecord, Favorite, UserSettings, ExportHistory
)


class UserService:
    """用户服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ==================== 用户管理 ====================
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_user_profile(
        self, 
        user_id: int, 
        **kwargs
    ) -> Optional[User]:
        """更新用户资料"""
        allowed_fields = ['nickname', 'avatar', 'gender', 'birthday']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            await self.db.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            await self.db.commit()
        
        return await self.get_user_by_id(user_id)
    
    async def get_user_stats(self, user_id: int) -> Dict:
        """获取用户统计数据"""
        # 各类型记录数
        bazi_count = await self.db.execute(
            select(func.count()).select_from(AnalysisRecord).where(
                AnalysisRecord.user_id == user_id,
                AnalysisRecord.analysis_type == 'bazi'
            )
        )
        
        ziwei_count = await self.db.execute(
            select(func.count()).select_from(AnalysisRecord).where(
                AnalysisRecord.user_id == user_id,
                AnalysisRecord.analysis_type == 'ziwei'
            )
        )
        
        divination_count = await self.db.execute(
            select(func.count()).select_from(DivinationRecord).where(
                DivinationRecord.user_id == user_id
            )
        )
        
        psychology_count = await self.db.execute(
            select(func.count()).select_from(PsychologyTest).where(
                PsychologyTest.user_id == user_id
            )
        )
        
        fusion_count = await self.db.execute(
            select(func.count()).select_from(FusionRecord).where(
                FusionRecord.user_id == user_id
            )
        )
        
        favorite_count = await self.db.execute(
            select(func.count()).select_from(Favorite).where(
                Favorite.user_id == user_id
            )
        )
        
        return {
            "bazi_analyses": bazi_count.scalar() or 0,
            "ziwei_analyses": ziwei_count.scalar() or 0,
            "divinations": divination_count.scalar() or 0,
            "psychology_tests": psychology_count.scalar() or 0,
            "fusion_analyses": fusion_count.scalar() or 0,
            "favorites": favorite_count.scalar() or 0
        }


class HistoryService:
    """历史记录服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ==================== 命理分析记录 ====================
    
    async def save_analysis(
        self,
        user_id: int,
        analysis_type: str,
        birth_info_id: int,
        result_data: Dict
    ) -> AnalysisRecord:
        """保存分析记录"""
        record = AnalysisRecord(
            user_id=user_id,
            birth_info_id=birth_info_id,
            analysis_type=analysis_type,
            result_data=result_data
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_user_analyses(
        self,
        user_id: int,
        analysis_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[AnalysisRecord]:
        """获取用户分析历史"""
        query = select(AnalysisRecord).where(
            AnalysisRecord.user_id == user_id
        )
        
        if analysis_type:
            query = query.where(AnalysisRecord.analysis_type == analysis_type)
        
        query = query.order_by(AnalysisRecord.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_analysis_by_id(
        self, 
        record_id: int,
        user_id: int
    ) -> Optional[AnalysisRecord]:
        """获取特定分析记录"""
        result = await self.db.execute(
            select(AnalysisRecord).where(
                AnalysisRecord.id == record_id,
                AnalysisRecord.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def delete_analysis(self, record_id: int, user_id: int) -> bool:
        """删除分析记录"""
        result = await self.db.execute(
            delete(AnalysisRecord).where(
                AnalysisRecord.id == record_id,
                AnalysisRecord.user_id == user_id
            )
        )
        await self.db.commit()
        return result.rowcount > 0
    
    # ==================== 占卜记录 ====================
    
    async def save_divination(
        self,
        user_id: int,
        method: str,
        question: str,
        result_data: Dict
    ) -> DivinationRecord:
        """保存占卜记录"""
        record = DivinationRecord(
            user_id=user_id,
            method=method,
            question=question,
            result_data=result_data
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_user_divinations(
        self,
        user_id: int,
        method: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[DivinationRecord]:
        """获取用户占卜历史"""
        query = select(DivinationRecord).where(
            DivinationRecord.user_id == user_id
        )
        
        if method:
            query = query.where(DivinationRecord.method == method)
        
        query = query.order_by(DivinationRecord.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_divination_by_id(
        self,
        record_id: int,
        user_id: int
    ) -> Optional[DivinationRecord]:
        """获取特定占卜记录"""
        result = await self.db.execute(
            select(DivinationRecord).where(
                DivinationRecord.id == record_id,
                DivinationRecord.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_divination_by_id(
        self,
        record_id: int,
        user_id: int
    ) -> Optional[DivinationRecord]:
        """获取特定占卜记录"""
        result = await self.db.execute(
            select(DivinationRecord).where(
                DivinationRecord.id == record_id,
                DivinationRecord.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    # ==================== 心理测试记录 ====================
    
    async def save_psychology_test(
        self,
        user_id: int,
        test_type: str,
        answers: List[Dict],
        result_data: Dict
    ) -> PsychologyTest:
        """保存心理测试记录"""
        record = PsychologyTest(
            user_id=user_id,
            test_type=test_type,
            answers=answers,
            result_data=result_data
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_user_psychology_tests(
        self,
        user_id: int,
        test_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[PsychologyTest]:
        """获取用户心理测试历史"""
        query = select(PsychologyTest).where(
            PsychologyTest.user_id == user_id
        )
        
        if test_type:
            query = query.where(PsychologyTest.test_type == test_type)
        
        query = query.order_by(PsychologyTest.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_psychology_test_by_id(
        self,
        record_id: int,
        user_id: int
    ) -> Optional[PsychologyTest]:
        """获取特定心理测试记录"""
        result = await self.db.execute(
            select(PsychologyTest).where(
                PsychologyTest.id == record_id,
                PsychologyTest.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_latest_psychology_results(self, user_id: int) -> Dict:
        """获取用户最新的各类心理测试结果"""
        results = {}
        
        for test_type in ['mbti', 'big5', 'archetype', 'enneagram']:
            query = select(PsychologyTest).where(
                PsychologyTest.user_id == user_id,
                PsychologyTest.test_type == test_type
            ).order_by(PsychologyTest.created_at.desc()).limit(1)
            
            result = await self.db.execute(query)
            record = result.scalar_one_or_none()
            
            if record:
                results[test_type] = record.result_data
        
        return results
    
    # ==================== 融合分析记录 ====================
    
    async def save_fusion(
        self,
        user_id: int,
        title: str,
        fusion_result: Dict,
        report_markdown: str,
        confidence: float,
        bazi_record_id: Optional[int] = None,
        ziwei_record_id: Optional[int] = None,
        psychology_test_ids: Optional[List[int]] = None
    ) -> FusionRecord:
        """保存融合分析记录"""
        record = FusionRecord(
            user_id=user_id,
            title=title,
            bazi_record_id=bazi_record_id,
            ziwei_record_id=ziwei_record_id,
            psychology_test_ids=psychology_test_ids,
            fusion_result=fusion_result,
            report_markdown=report_markdown,
            confidence=confidence
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_user_fusions(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> List[FusionRecord]:
        """获取用户融合分析历史"""
        query = select(FusionRecord).where(
            FusionRecord.user_id == user_id
        ).order_by(FusionRecord.created_at.desc())
        
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_fusion_by_id(
        self,
        record_id: int,
        user_id: int
    ) -> Optional[FusionRecord]:
        """获取特定融合分析记录"""
        result = await self.db.execute(
            select(FusionRecord).where(
                FusionRecord.id == record_id,
                FusionRecord.user_id == user_id
            )
        )
        return result.scalar_one_or_none()


class FavoriteService:
    """收藏服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_favorite(
        self,
        user_id: int,
        item_type: str,
        item_id: int,
        note: Optional[str] = None
    ) -> Favorite:
        """添加收藏"""
        # 检查是否已收藏
        existing = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.item_type == item_type,
                Favorite.item_id == item_id
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("已收藏")
        
        favorite = Favorite(
            user_id=user_id,
            item_type=item_type,
            item_id=item_id,
            note=note
        )
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite
    
    async def remove_favorite(
        self,
        user_id: int,
        item_type: str,
        item_id: int
    ) -> bool:
        """取消收藏"""
        result = await self.db.execute(
            delete(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.item_type == item_type,
                Favorite.item_id == item_id
            )
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def get_user_favorites(
        self,
        user_id: int,
        item_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Favorite]:
        """获取用户收藏列表"""
        query = select(Favorite).where(Favorite.user_id == user_id)
        
        if item_type:
            query = query.where(Favorite.item_type == item_type)
        
        query = query.order_by(Favorite.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def is_favorited(
        self,
        user_id: int,
        item_type: str,
        item_id: int
    ) -> bool:
        """检查是否已收藏"""
        result = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.item_type == item_type,
                Favorite.item_id == item_id
            )
        )
        return result.scalar_one_or_none() is not None


class SettingsService:
    """用户设置服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_or_create_settings(self, user_id: int) -> UserSettings:
        """获取或创建用户设置"""
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            settings = UserSettings(user_id=user_id)
            self.db.add(settings)
            await self.db.commit()
            await self.db.refresh(settings)
        
        return settings
    
    async def update_settings(
        self,
        user_id: int,
        **kwargs
    ) -> UserSettings:
        """更新用户设置"""
        allowed_fields = ['theme', 'language', 'timezone', 'notification_enabled', 'preferences']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if update_data:
            await self.db.execute(
                update(UserSettings).where(
                    UserSettings.user_id == user_id
                ).values(**update_data)
            )
            await self.db.commit()
        
        return await self.get_or_create_settings(user_id)
