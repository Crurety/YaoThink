import React, { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Button, Dropdown, Avatar, message } from 'antd'
import {
    HomeOutlined,
    CompassOutlined,
    StarOutlined,
    BookOutlined,
    UserOutlined,
    ExperimentOutlined,
    LogoutOutlined,
    LoginOutlined
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
import { useUserStore } from './stores'

const { Header, Content, Footer } = Layout

const menuItems = [
    { key: '/', icon: <HomeOutlined />, label: '首页' },
    { key: '/bazi', icon: <CompassOutlined />, label: '八字命理' },
    { key: '/ziwei', icon: <StarOutlined />, label: '紫微斗数' },
    { key: '/yijing', icon: <BookOutlined />, label: '易经占卜' },
    { key: '/psychology', icon: <ExperimentOutlined />, label: '心理测评' },
    { key: '/fusion', icon: <StarOutlined />, label: '融合分析' },
]

function App() {
    const navigate = useNavigate()
    const location = useLocation()
    const [authModalVisible, setAuthModalVisible] = useState(false)
    const { user, isAuthenticated, logout } = useUserStore()

    // 未登录时自动弹出登录框（访问受保护页面）
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
        <Layout className="app-layout">
            <Header className="app-header">
                <div className="logo" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
                    <span className="logo-icon">☯</span>
                    <span className="logo-text">玄心理命</span>
                </div>
                <Menu
                    theme="dark"
                    mode="horizontal"
                    selectedKeys={[location.pathname]}
                    items={menuItems}
                    onClick={({ key }) => navigate(key)}
                    className="header-menu"
                />
                <div className="header-auth">
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
    )
}

export default App

