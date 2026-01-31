"""
登录流程测试脚本
"""
import httpx
import asyncio
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

async def test_login_flow():
    async with httpx.AsyncClient() as client:
        print("=" * 50)
        print("玄心理命 - 登录流程测试")
        print("=" * 50)
        
        # 1. 测试发送验证码
        print("\n[1] 发送验证码...")
        phone = "13800138001"
        try:
            response = await client.post(
                f"{BASE_URL}/api/auth/send-code",
                json={"phone": phone}
            )
            print(f"    状态码: {response.status_code}")
            data = response.json()
            print(f"    响应: {data}")
            
            if response.status_code == 200 and data.get("success"):
                code = data["data"].get("debug_code")
                print(f"    验证码: {code}")
            else:
                print(f"    错误: {data}")
                return
        except Exception as e:
            print(f"    异常: {e}")
            return
        
        # 2. 测试手机号+验证码登录
        print("\n[2] 手机号+验证码登录...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/auth/login/phone-sms",
                json={"phone": phone, "code": code}
            )
            print(f"    状态码: {response.status_code}")
            data = response.json()
            
            if response.status_code == 200 and data.get("success"):
                user = data["data"]["user"]
                token = data["data"]["token"]["access_token"]
                is_new = data["data"]["is_new_user"]
                print(f"    ✅ 登录成功!")
                print(f"    用户ID: {user['id']}")
                print(f"    昵称: {user['nickname']}")
                print(f"    新用户: {is_new}")
                print(f"    Token: {token[:30]}...")
            else:
                print(f"    ❌ 登录失败: {data}")
                return
        except Exception as e:
            print(f"    异常: {e}")
            return
        
        # 3. 测试获取当前用户信息
        print("\n[3] 获取当前用户信息...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"    状态码: {response.status_code}")
            data = response.json()
            
            if response.status_code == 200 and data.get("success"):
                user = data["data"]
                print(f"    ✅ 获取成功!")
                print(f"    用户信息: {user}")
            else:
                print(f"    ❌ 获取失败: {data}")
        except Exception as e:
            print(f"    异常: {e}")
        
        # 4. 测试邮箱注册
        print("\n[4] 邮箱注册测试...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/auth/register/email",
                json={
                    "email": "test@example.com",
                    "password": "123456",
                    "nickname": "测试用户"
                }
            )
            print(f"    状态码: {response.status_code}")
            data = response.json()
            
            if response.status_code == 200 and data.get("success"):
                print(f"    ✅ 注册成功!")
                print(f"    用户: {data['data']['user']['nickname']}")
            else:
                print(f"    结果: {data}")
        except Exception as e:
            print(f"    异常: {e}")
        
        # 5. 测试邮箱登录
        print("\n[5] 邮箱登录测试...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/auth/login/email-password",
                json={
                    "email": "test@example.com",
                    "password": "123456"
                }
            )
            print(f"    状态码: {response.status_code}")
            data = response.json()
            
            if response.status_code == 200 and data.get("success"):
                print(f"    ✅ 邮箱登录成功!")
            else:
                print(f"    结果: {data}")
        except Exception as e:
            print(f"    异常: {e}")
        
        print("\n" + "=" * 50)
        print("测试完成!")
        print("=" * 50)

if __name__ == "__main__":
    # 重定向输出到文件
    with open("test_result.txt", "w", encoding="utf-8") as f:
        import contextlib
        with contextlib.redirect_stdout(f):
            asyncio.run(test_login_flow())
    print("Results written to test_result.txt")
