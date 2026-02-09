import React, { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Button, Dropdown, Avatar, message, ConfigProvider, theme } from 'antd'
import {
    HomeOutlined,
    CompassOutlined,
    StarOutlined,
    BookOutlined,
    UserOutlined,
    ExperimentOutlined,
    LogoutOutlined,
    LoginOutlined,
    SunOutlined,
    MoonOutlined
} from '@ant-design/icons'

import Home from './pages/Home'
import BaZi from './pages/BaZi'
import ZiWei from './pages/ZiWei'
import YiJing from './pages/YiJing'
import Psychology from './pages/Psychology'
import Fusion from './pages/Fusion'
import Profile from './pages/Profile'
import AuthModal from './components/AuthModal'
import PrivateRoute from './components/PrivateRoute'
import { useUserStore, ThemeProvider, useTheme } from './stores'

const { Header, Content, Footer } = Layout

const menuItems = [
    { key: '/', icon: <HomeOutlined />, label: '首页' },
    { key: '/bazi', icon: <CompassOutlined />, label: '八字命理' },
    { key: '/ziwei', icon: <StarOutlined />, label: '紫微斗数' },
    { key: '/yijing', icon: <BookOutlined />, label: '易经占卜' },
    { key: '/psychology', icon: <ExperimentOutlined />, label: '心理测评' },
    { key: '/fusion', icon: <StarOutlined />, label: '融合分析' },
]

// 主应用内容（需要在 ThemeProvider 内部）
function AppContent() {
    const navigate = useNavigate()
    const location = useLocation()
    const [authModalVisible, setAuthModalVisible] = useState(false)
    const { user, isAuthenticated, logout } = useUserStore()
    const { theme: currentTheme, toggleTheme, isDark } = useTheme()

    const handleAuthRequired = () => {
        setAuthModalVisible(true)
        message.warning('请先登录后再使用此功能')
    }

    const handleLogout = () => {
        logout()
        message.success('已退出登录')
        navigate('/')
    }

    const userMenu = {
        items: [
            {
                key: 'profile',
                icon: <UserOutlined />,
                label: '个人中心',
                onClick: () => navigate('/profile')
            },
            {
                key: 'logout',
                icon: <LogoutOutlined />,
                label: '退出登录',
                onClick: handleLogout
            }
        ]
    }

    return (
        <ConfigProvider
            theme={{
                algorithm: isDark ? theme.darkAlgorithm : theme.defaultAlgorithm,
                token: {
                    colorPrimary: isDark ? '#8b5cf6' : '#b45309',
                    colorBgContainer: isDark ? '#1e293b' : '#fffef9',
                    colorBgElevated: isDark ? '#1e293b' : '#ffffff',
                    borderRadius: 12,
                    colorText: isDark ? undefined : '#4b5563', // 日间模式文本改为深灰 (Gray 600)
                    colorTextHeading: isDark ? undefined : '#1f2937', // 日间模式标题改为更深的灰 (Gray 800)
                }
            }}
        >
            <Layout className="app-layout">
                <Header className="app-header">
                    <div className="logo" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
                        <span className="logo-icon">☯</span>
                        <span className="logo-text">玄心理命</span>
                    </div>
                    <Menu
                        theme={isDark ? 'dark' : 'light'}
                        mode="horizontal"
                        selectedKeys={[location.pathname]}
                        items={menuItems}
                        onClick={({ key }) => navigate(key)}
                        className="header-menu"
                    />
                    <div className="header-auth">
                        {/* 主题切换按钮 */}
                        <button
                            className="theme-toggle"
                            onClick={toggleTheme}
                            title={isDark ? '切换到日间模式' : '切换到夜间模式'}
                        >
                            {isDark ? <SunOutlined style={{ color: '#fbbf24' }} /> : <MoonOutlined style={{ color: '#6366f1' }} />}
                        </button>

                        {isAuthenticated ? (
                            <Dropdown menu={userMenu} placement="bottomRight">
                                <span className="user-dropdown-link" style={{ cursor: 'pointer', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: 8 }}>
                                    <Avatar
                                        src={user?.avatar}
                                        icon={<UserOutlined />}
                                        style={{ backgroundColor: 'var(--accent-gold)' }}
                                    />
                                    <span className="user-name">{user?.nickname || user?.phone || '用户'}</span>
                                </span>
                            </Dropdown>
                        ) : (
                            <Button
                                type="primary"
                                icon={<LoginOutlined />}
                                onClick={() => setAuthModalVisible(true)}
                            >
                                登录/注册
                            </Button>
                        )}
                    </div>
                </Header>

                <Content className="app-content">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/bazi" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <BaZi />
                            </PrivateRoute>
                        } />
                        <Route path="/ziwei" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <ZiWei />
                            </PrivateRoute>
                        } />
                        <Route path="/yijing" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <YiJing />
                            </PrivateRoute>
                        } />
                        <Route path="/psychology" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <Psychology />
                            </PrivateRoute>
                        } />
                        <Route path="/fusion" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <Fusion />
                            </PrivateRoute>
                        } />
                        <Route path="/profile" element={
                            <PrivateRoute onAuthRequired={handleAuthRequired}>
                                <Profile />
                            </PrivateRoute>
                        } />
                    </Routes>
                </Content>

                <Footer className="app-footer">
                    玄心理命 ©2024 - 东方玄学与西方心理学融合
                </Footer>

                <AuthModal
                    visible={authModalVisible}
                    onClose={() => setAuthModalVisible(false)}
                />
            </Layout>
        </ConfigProvider>
    )
}

// 根组件（包裹 ThemeProvider）
function App() {
    return (
        <ThemeProvider>
            <AppContent />
        </ThemeProvider>
    )
}

export default App


