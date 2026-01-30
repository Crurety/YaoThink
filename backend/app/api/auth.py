"""
玄心理命 - 认证API路由
支持三种方式：手机号+验证码、手机号+密码、邮箱+密码
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    SendSmsCodeRequest, 
    PhoneSmsLoginRequest, PhonePasswordLoginRequest, EmailPasswordLoginRequest,
    PhoneRegisterRequest, EmailRegisterRequest, SetPasswordRequest,
    UserResponse, AuthService, get_current_user, TokenData
)
from app.core.database import get_db
from app.core.cache import CacheService

router = APIRouter()


# ========== 验证码 ==========

@router.post("/send-code", summary="发送验证码")
async def send_sms_code(request: SendSmsCodeRequest, db: AsyncSession = Depends(get_db)):
    """发送短信验证码到手机"""
    cache = CacheService()
    auth_service = AuthService(db, cache)
    result = await auth_service.send_sms_code(request.phone)
    return {"success": True, "data": result}


# ========== 登录 ==========

@router.post("/login/phone-sms", summary="手机号+验证码登录")
async def login_by_phone_sms(request: PhoneSmsLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    手机号+验证码登录
    - 如果手机号未注册，自动创建账号
    """
    cache = CacheService()
    auth_service = AuthService(db, cache)
    result = await auth_service.login_by_phone_sms(request.phone, request.code)
    return {"success": True, "data": result}


@router.post("/login/phone-password", summary="手机号+密码登录")
async def login_by_phone_password(request: PhonePasswordLoginRequest, db: AsyncSession = Depends(get_db)):
    """手机号+密码登录"""
    auth_service = AuthService(db)
    result = await auth_service.login_by_phone_password(request.phone, request.password)
    return {"success": True, "data": result}


@router.post("/login/email-password", summary="邮箱+密码登录")
async def login_by_email_password(request: EmailPasswordLoginRequest, db: AsyncSession = Depends(get_db)):
    """邮箱+密码登录"""
    auth_service = AuthService(db)
    result = await auth_service.login_by_email_password(request.email, request.password)
    return {"success": True, "data": result}


# ========== 注册 ==========

@router.post("/register/phone", summary="手机号注册")
async def register_by_phone(request: PhoneRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    手机号注册（带密码）
    - 需要先获取验证码
    """
    cache = CacheService()
    auth_service = AuthService(db, cache)
    result = await auth_service.register_by_phone(
        request.phone, request.code, request.password, request.nickname
    )
    return {"success": True, "data": result}


@router.post("/register/email", summary="邮箱注册")
async def register_by_email(request: EmailRegisterRequest, db: AsyncSession = Depends(get_db)):
    """邮箱注册"""
    auth_service = AuthService(db)
    result = await auth_service.register_by_email(
        request.email, request.password, request.nickname
    )
    return {"success": True, "data": result}


# ========== 密码管理 ==========

@router.post("/set-password", summary="设置/重置密码")
async def set_password(request: SetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """通过验证码设置或重置密码"""
    cache = CacheService()
    auth_service = AuthService(db, cache)
    result = await auth_service.set_password(
        phone=request.phone,
        email=request.email,
        code=request.code,
        new_password=request.new_password
    )
    return {"success": True, "data": result}


# ========== 用户信息 ==========

@router.get("/me", summary="获取当前用户信息")
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前登录用户信息"""
    from sqlalchemy import select
    from app.core.database import User
    
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    
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
            "is_vip": user.is_vip,
            "has_password": bool(user.hashed_password),
            "created_at": user.created_at
        }
    }


@router.put("/me", summary="更新用户信息")
async def update_user_info(
    nickname: str = None,
    avatar: str = None,
    gender: str = None,
    email: str = None,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    from sqlalchemy import select
    from app.core.database import User
    
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if nickname:
        user.nickname = nickname
    if avatar:
        user.avatar = avatar
    if gender:
        user.gender = gender
    if email and not user.email:
        # 检查邮箱是否已被使用
        existing = await db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="邮箱已被使用")
        user.email = email
    
    await db.commit()
    await db.refresh(user)
    
    return {
        "success": True,
        "data": {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "is_vip": user.is_vip,
            "has_password": bool(user.hashed_password),
            "created_at": user.created_at
        }
    }
