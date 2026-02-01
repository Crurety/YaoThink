"""
玄心理命 - JWT用户认证系统
支持三种登录方式：手机号+验证码、手机号+密码、邮箱+密码
"""

from datetime import datetime, timedelta
from typing import Optional, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
import os
import random
import string


# ==================== 配置 ====================

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-玄心理命-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

SMS_CODE_EXPIRE_SECONDS = 300  # 5分钟


# ==================== 数据模型 ====================

class Token(BaseModel):
    """Token响应模型"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token载荷数据"""
    user_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[datetime] = None


# ========== 请求模型 ==========

class SendSmsCodeRequest(BaseModel):
    """发送验证码请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")


class PhoneSmsLoginRequest(BaseModel):
    """手机号+验证码登录"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., min_length=4, max_length=6)


class PhonePasswordLoginRequest(BaseModel):
    """手机号+密码登录"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    password: str = Field(..., min_length=6)


class EmailPasswordLoginRequest(BaseModel):
    """邮箱+密码登录"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class PhoneRegisterRequest(BaseModel):
    """手机号注册（设置密码）"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., min_length=4, max_length=6)
    password: str = Field(..., min_length=6)
    nickname: Optional[str] = None


class EmailRegisterRequest(BaseModel):
    """邮箱注册"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    nickname: Optional[str] = None


class SetPasswordRequest(BaseModel):
    """设置/修改密码"""
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$")
    email: Optional[EmailStr] = None
    code: str = Field(..., min_length=4, max_length=6)
    new_password: str = Field(..., min_length=6)


class ChangePasswordRequest(BaseModel):
    """修改密码（已登录）"""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    phone: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
    avatar: Optional[str]
    is_vip: bool
    has_password: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 工具函数 ====================

def generate_sms_code(length: int = 6) -> str:
    """生成短信验证码"""
    return ''.join(random.choices(string.digits, k=length))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    # bcrypt 限制密码最长72字节
    password = password[:72] if len(password.encode('utf-8')) > 72 else password
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[TokenData]:
    """解码JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            user_id=payload.get("user_id"),
            phone=payload.get("phone"),
            email=payload.get("email"),
            exp=datetime.fromtimestamp(payload.get("exp"))
        )
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """获取当前用户（依赖注入）"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = decode_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if token_data.exp and token_data.exp < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data


async def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> Optional[TokenData]:
    """获取当前用户（可选）"""
    if not token:
        return None
    try:
        return await get_current_user(token)
    except HTTPException:
        return None


# ==================== 认证服务 ====================

class AuthService:
    """认证服务"""
    
    def __init__(self, db_session, cache_service=None):
        self.db = db_session
        self.cache = cache_service
    
    def _generate_token(self, user) -> Token:
        """生成用户令牌"""
        access_token = create_access_token(
            data={
                "user_id": user.id,
                "phone": user.phone,
                "email": user.email
            }
        )
        return Token(
            access_token=access_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def _user_response(self, user) -> dict:
        """构建用户响应"""
        return {
            "id": user.id,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "is_vip": user.is_vip,
            "has_password": bool(user.hashed_password),
            "created_at": user.created_at
        }
    
    # ========== 验证码相关 ==========
    
    async def send_sms_code(self, phone: str) -> dict:
        """发送短信验证码"""
        code = generate_sms_code()
        
        if self.cache:
            await self.cache.set(f"sms_code:{phone}", code, SMS_CODE_EXPIRE_SECONDS)
        
        # TODO: 接入短信服务商
        print(f"[DEBUG] 验证码 {phone}: {code}")
        
        return {
            "message": "验证码已发送",
            "expires_in": SMS_CODE_EXPIRE_SECONDS,
            "debug_code": code if os.getenv("DEBUG", "true").lower() == "true" else None
        }
    
    async def verify_sms_code(self, phone: str, code: str) -> bool:
        """验证短信验证码"""
        # [测试用] 允许使用通用测试码跳过验证（仅用于无法发送短信的生产测试环境）
        if code == "666666":
            return True

        if self.cache:
            stored_code = await self.cache.get(f"sms_code:{phone}")
            if stored_code and stored_code == code:
                await self.cache.delete(f"sms_code:{phone}")
                return True
            return False
        # 开发环境
        return len(code) == 6 and code.isdigit()
    
    # ========== 手机号+验证码登录 ==========
    
    async def login_by_phone_sms(self, phone: str, code: str) -> dict:
        """手机号+验证码登录（自动注册）"""
        from sqlalchemy import select
        from app.core.database import User
        
        if not await self.verify_sms_code(phone, code):
            raise HTTPException(status_code=400, detail="验证码错误或已过期")
        
        result = await self.db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        
        is_new_user = False
        if not user:
            user = User(phone=phone, nickname=f"用户{phone[-4:]}", is_active=True)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            is_new_user = True
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="账户已被禁用")
        
        return {
            "user": self._user_response(user),
            "token": self._generate_token(user),
            "is_new_user": is_new_user
        }
    
    # ========== 手机号+密码登录 ==========
    
    async def login_by_phone_password(self, phone: str, password: str) -> dict:
        """手机号+密码登录"""
        from sqlalchemy import select
        from app.core.database import User
        
        result = await self.db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="手机号未注册")
        
        if not user.hashed_password:
            raise HTTPException(status_code=400, detail="请使用验证码登录或先设置密码")
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="密码错误")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="账户已被禁用")
        
        return {
            "user": self._user_response(user),
            "token": self._generate_token(user)
        }
    
    # ========== 邮箱+密码登录 ==========
    
    async def login_by_email_password(self, email: str, password: str) -> dict:
        """邮箱+密码登录"""
        from sqlalchemy import select
        from app.core.database import User
        
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="邮箱未注册")
        
        if not user.hashed_password:
            raise HTTPException(status_code=400, detail="请先设置密码")
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="密码错误")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="账户已被禁用")
        
        return {
            "user": self._user_response(user),
            "token": self._generate_token(user)
        }
    
    # ========== 注册 ==========
    
    async def register_by_phone(self, phone: str, code: str, password: str, nickname: str = None) -> dict:
        """手机号注册（带密码）"""
        from sqlalchemy import select
        from app.core.database import User
        
        if not await self.verify_sms_code(phone, code):
            raise HTTPException(status_code=400, detail="验证码错误或已过期")
        
        result = await self.db.execute(select(User).where(User.phone == phone))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="手机号已注册")
        
        user = User(
            phone=phone,
            hashed_password=get_password_hash(password),
            nickname=nickname or f"用户{phone[-4:]}",
            is_active=True
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return {
            "user": self._user_response(user),
            "token": self._generate_token(user)
        }
    
    async def register_by_email(self, email: str, password: str, nickname: str = None) -> dict:
        """邮箱注册"""
        from sqlalchemy import select
        from app.core.database import User
        
        result = await self.db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="邮箱已注册")
        
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            nickname=nickname or email.split("@")[0],
            is_active=True
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return {
            "user": self._user_response(user),
            "token": self._generate_token(user)
        }
    
    # ========== 设置密码 ==========
    
    async def set_password(self, phone: str = None, email: str = None,
                           code: str = None, new_password: str = None) -> dict:
        """设置/重置密码"""
        from sqlalchemy import select
        from app.core.database import User
        
        if phone:
            if not await self.verify_sms_code(phone, code):
                raise HTTPException(status_code=400, detail="验证码错误或已过期")
            result = await self.db.execute(select(User).where(User.phone == phone))
        elif email:
            # TODO: 邮箱验证码逻辑
            result = await self.db.execute(select(User).where(User.email == email))
        else:
            raise HTTPException(status_code=400, detail="请提供手机号或邮箱")
        
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()
        
        return {"message": "密码设置成功"}

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """修改密码"""
        from sqlalchemy import select
        from app.core.database import User
        
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
            
        if not user.hashed_password:
            raise HTTPException(status_code=400, detail="请先设置密码")
            
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="旧密码错误")
            
        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()
        
        return {"message": "密码修改成功"}
