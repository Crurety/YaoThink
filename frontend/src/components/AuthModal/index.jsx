import React, { useState, useEffect } from 'react'
import { Modal, Form, Input, Button, Tabs, message, Divider, theme } from 'antd'
import { MobileOutlined, SafetyOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { useUserStore } from '../../stores'
import api from '../../services/api'

const { useToken } = theme

function AuthModal({ visible, onClose }) {
    const { token } = useToken()
    const [activeTab, setActiveTab] = useState('phone-sms')
    const [mode, setMode] = useState('login')  // login / register
    const [loading, setLoading] = useState(false)
    const [sendingCode, setSendingCode] = useState(false)
    const [countdown, setCountdown] = useState(0)
    const [form] = Form.useForm()
    const { login } = useUserStore()

    // 倒计时
    useEffect(() => {
        let timer
        if (countdown > 0) {
            timer = setTimeout(() => setCountdown(countdown - 1), 1000)
        }
        return () => clearTimeout(timer)
    }, [countdown])

    // 切换标签时重置表单
    useEffect(() => {
        form.resetFields()
    }, [activeTab, mode])

    // 发送验证码
    const handleSendCode = async () => {
        try {
            const phone = form.getFieldValue('phone')
            if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
                message.error('请输入正确的手机号')
                return
            }

            setSendingCode(true)
            const response = await api.post('/api/auth/send-code', { phone })

            if (response.data.success) {
                message.success('验证码已发送')
                setCountdown(60)
                if (response.data.data.debug_code) {
                    form.setFieldValue('code', response.data.data.debug_code)
                }
            }
        } catch (error) {
            message.error(error.response?.data?.detail || '发送失败')
        } finally {
            setSendingCode(false)
        }
    }

    // 处理登录/注册
    const handleSubmit = async (values) => {
        console.log('[Auth] Submit values:', values)
        const hideLoading = message.loading('正在处理请求...', 0)
        setLoading(true)
        try {
            let endpoint = ''
            let payload = {}

            if (mode === 'login') {
                switch (activeTab) {
                    case 'phone-sms':
                        endpoint = '/api/auth/login/phone-sms'
                        payload = { phone: values.phone, code: values.code }
                        break
                    case 'phone-password':
                        endpoint = '/api/auth/login/phone-password'
                        payload = { phone: values.phone, password: values.password }
                        break
                    case 'email-password':
                        endpoint = '/api/auth/login/email-password'
                        payload = { email: values.email, password: values.password }
                        break
                }
            } else {
                switch (activeTab) {
                    case 'phone-sms':
                        endpoint = '/api/auth/register/phone'
                        payload = {
                            phone: values.phone,
                            code: values.code,
                            password: values.password,
                            nickname: values.nickname
                        }
                        break
                    case 'email-password':
                        endpoint = '/api/auth/register/email'
                        payload = {
                            email: values.email,
                            password: values.password,
                            nickname: values.nickname
                        }
                        break
                }
            }

            console.log('[Auth] Sending request to:', endpoint)
            const response = await api.post(endpoint, payload)
            console.log('[Auth] Response:', response)

            if (response.data.success) {
                const { user, token, is_new_user } = response.data.data
                // 兼容性处理：token可能是对象也可能是字符串
                const tokenStr = token.access_token || token

                console.log('[Auth] Login success, token:', tokenStr)
                login(user, tokenStr)

                message.success(is_new_user ? '注册成功！' : '登录成功！')
                onClose()
                form.resetFields()
            } else {
                console.error('[Auth] Failed success flag:', response.data)
                message.error('请求虽成功但返回失败状态')
            }
        } catch (error) {
            console.error('[Auth] Error:', error)
            const errorMsg = error.response?.data?.detail || error.message || '操作失败'
            message.error(`登录失败: ${errorMsg}`)
        } finally {
            hideLoading()
            setLoading(false)
        }
    }

    // --- Style Injection for Autofill ---
    // Using a very dark color for autofill background to match dark theme. 
    // The transition delay is the primary fix, the shadow is fallback.
    const autofillStyles = `
        .dark-autofill input:-webkit-autofill,
        .dark-autofill input:-webkit-autofill:hover, 
        .dark-autofill input:-webkit-autofill:focus, 
        .dark-autofill input:-webkit-autofill:active {
            -webkit-box-shadow: 0 0 0 1000px #2a2a2a inset !important;
            -webkit-text-fill-color: ${token.colorText} !important;
            transition: background-color 5000s ease-in-out 0s;
        }
        
        /* Remove double borders/focus outlines if any */
        .custom-auth-input .ant-input-affix-wrapper {
             background: transparent !important;
             border: none !important;
             box-shadow: none !important;
        }
        
        /* The container itself */
        .custom-input-container {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            padding: 4px 11px;
        }
        
        .custom-input-container:hover {
            border-color: ${token.colorPrimary}80;
        }

        .custom-input-container:focus-within {
            border-color: ${token.colorPrimary};
            box-shadow: 0 0 0 2px ${token.colorPrimary}20;
        }
        
        .custom-input-container input {
            background: transparent !important;
        }
    `

    const iconStyle = { color: token.colorTextSecondary, fontSize: 18, marginRight: 8 }

    // Wrapper component to handle the container style cleanly
    const CustomInput = ({ prefix, ...props }) => {
        return (
            <div className="custom-input-container dark-autofill">
                {prefix && React.cloneElement(prefix, { style: iconStyle })}
                <Input
                    {...props}
                    bordered={false}
                    style={{ padding: '8px 0', background: 'transparent' }} // reset internal styles
                />
            </div>
        )
    }

    const CustomPassword = ({ prefix, ...props }) => {
        return (
            <div className="custom-input-container dark-autofill">
                {prefix && React.cloneElement(prefix, { style: iconStyle })}
                <Input.Password
                    {...props}
                    bordered={false}
                    style={{ padding: '8px 0', background: 'transparent' }}
                />
            </div>
        )
    }

    // 手机号+验证码表单
    const PhoneSmsForm = () => (
        <>
            <Form.Item
                name="phone"
                rules={[
                    { required: true, message: '请输入手机号' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
                ]}
            >
                <CustomInput
                    prefix={<MobileOutlined />}
                    placeholder="请输入手机号"
                    maxLength={11}
                />
            </Form.Item>

            <Form.Item
                name="code"
                rules={[
                    { required: true, message: '请输入验证码' },
                    { len: 6, message: '请输入6位验证码' }
                ]}
            >
                <div style={{ display: 'flex', gap: 12, alignItems: 'stretch' }}>
                    <Form.Item noStyle name="code">
                        <div style={{ flex: 1 }}>
                            <CustomInput
                                prefix={<SafetyOutlined />}
                                placeholder="请输入验证码"
                                maxLength={6}
                            />
                        </div>
                    </Form.Item>
                    <Button
                        size="large"
                        onClick={handleSendCode}
                        loading={sendingCode}
                        disabled={countdown > 0}
                        style={{
                            width: 120,
                            borderRadius: 8,
                            height: 'auto',
                            background: 'rgba(255, 255, 255, 0.04)',
                            border: '1px solid rgba(255, 255, 255, 0.15)',
                            color: token.colorPrimary
                        }}
                    >
                        {countdown > 0 ? `${countdown}s` : '获取验证码'}
                    </Button>
                </div>
            </Form.Item>

            {mode === 'register' && (
                <>
                    <Form.Item
                        name="password"
                        rules={[
                            { required: true, message: '请设置密码' },
                            { min: 6, message: '密码至少6位' }
                        ]}
                    >
                        <CustomPassword
                            prefix={<LockOutlined />}
                            placeholder="设置密码（便于下次登录）"
                        />
                    </Form.Item>
                    <Form.Item name="nickname">
                        <CustomInput placeholder="昵称（可选）" />
                    </Form.Item>
                </>
            )}
        </>
    )

    // 手机号+密码表单
    const PhonePasswordForm = () => (
        <>
            <Form.Item
                name="phone"
                rules={[
                    { required: true, message: '请输入手机号' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
                ]}
            >
                <CustomInput
                    prefix={<MobileOutlined />}
                    placeholder="请输入手机号"
                    maxLength={11}
                />
            </Form.Item>
            <Form.Item
                name="password"
                rules={[
                    { required: true, message: '请输入密码' },
                    { min: 6, message: '密码至少6位' }
                ]}
            >
                <CustomPassword
                    prefix={<LockOutlined />}
                    placeholder="请输入密码"
                />
            </Form.Item>
        </>
    )

    // 邮箱+密码表单
    const EmailPasswordForm = () => (
        <>
            <Form.Item
                name="email"
                rules={[
                    { required: true, message: '请输入邮箱' },
                    { type: 'email', message: '请输入正确的邮箱格式' }
                ]}
            >
                <CustomInput
                    prefix={<MailOutlined />}
                    placeholder="请输入邮箱"
                />
            </Form.Item>
            <Form.Item
                name="password"
                rules={[
                    { required: true, message: '请输入密码' },
                    { min: 6, message: '密码至少6位' }
                ]}
            >
                <CustomPassword
                    prefix={<LockOutlined />}
                    placeholder="请输入密码"
                />
            </Form.Item>
            {mode === 'register' && (
                <Form.Item name="nickname">
                    <CustomInput placeholder="昵称（可选）" />
                </Form.Item>
            )}
        </>
    )

    const tabItems = [
        { key: 'phone-sms', label: mode === 'login' ? '验证码登录' : '手机号注册', children: <PhoneSmsForm /> },
        // 注册模式下不支持单纯的"手机+密码"（必须验证码），所以隐藏
        ...(mode === 'login' ? [{ key: 'phone-password', label: '密码登录', children: <PhonePasswordForm /> }] : []),
        { key: 'email-password', label: mode === 'login' ? '邮箱登录' : '邮箱注册', children: <EmailPasswordForm /> }
    ]

    // 如果当前在"密码登录"标签页切换到注册模式，自动切回"手机注册"
    useEffect(() => {
        if (mode === 'register' && activeTab === 'phone-password') {
            setActiveTab('phone-sms')
        }
    }, [mode])

    return (
        <Modal
            title={null}
            open={visible}
            onCancel={onClose}
            footer={null}
            width={400}
            centered
            destroyOnClose
            maskStyle={{ backdropFilter: 'blur(5px)' }}
            bodyStyle={{ padding: '32px 24px' }}
        >
            <style>{autofillStyles}</style>
            <div style={{ textAlign: 'center', marginBottom: 32 }}>
                <div style={{ fontSize: 48, marginBottom: 8 }}>☯</div>
                <div style={{ fontSize: 24, fontWeight: 'bold', background: 'linear-gradient(45deg, #FFD700, #FFA500)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    玄心理命
                </div>
                <div style={{ fontSize: 14, color: token.colorTextSecondary, marginTop: 8 }}>
                    {mode === 'login' ? '欢迎回来' : '开启您的命理之旅'}
                </div>
            </div>

            <Form
                form={form}
                onFinish={handleSubmit}
                onFinishFailed={(errorInfo) => {
                    console.error('[Auth] Validation failed:', errorInfo)
                    message.error('请检查填写的信息')
                }}
                layout="vertical"
                requiredMark={false}
            >
                <Tabs
                    activeKey={activeTab}
                    onChange={setActiveTab}
                    items={tabItems}
                    centered
                    size="large"
                    destroyInactiveTabPane={true}
                    tabBarStyle={{ marginBottom: 24 }}
                />

                <Form.Item style={{ marginBottom: 16, marginTop: 8 }}>
                    <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        block
                        size="large"
                        style={{ height: 44, borderRadius: 8, fontSize: 16 }}
                        onClick={() => console.log('[Auth] Login button clicked')}
                    >
                        {mode === 'login' ? '立即登录' : '立即注册'}
                    </Button>
                </Form.Item>
            </Form>

            <Divider style={{ margin: '16px 0', borderColor: 'rgba(255,255,255,0.1)' }}>
                <span style={{ color: token.colorTextSecondary, fontSize: 12 }}>
                    {mode === 'login' ? '还没有账号？' : '已有账号？'}
                </span>
            </Divider>

            <Button
                type="text"
                block
                style={{ color: token.colorPrimary }}
                onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
            >
                {mode === 'login' ? '免费注册账号' : '返回登录'}
            </Button>
        </Modal>
    )
}

export default AuthModal
