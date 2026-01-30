import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
    HomeOutlined,
    CompassOutlined,
    StarOutlined,
    BookOutlined,
    UserOutlined,
    ExperimentOutlined
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

import Home from './pages/Home'
import BaZi from './pages/BaZi'
import ZiWei from './pages/ZiWei'
import YiJing from './pages/YiJing'
import Psychology from './pages/Psychology'
import Fusion from './pages/Fusion'
import Profile from './pages/Profile'

const { Header, Content, Footer } = Layout

const menuItems = [
    { key: '/', icon: <HomeOutlined />, label: '首页' },
    { key: '/bazi', icon: <CompassOutlined />, label: '八字命理' },
    { key: '/ziwei', icon: <StarOutlined />, label: '紫微斗数' },
    { key: '/yijing', icon: <BookOutlined />, label: '易经占卜' },
    { key: '/psychology', icon: <ExperimentOutlined />, label: '心理测评' },
    { key: '/fusion', icon: <StarOutlined />, label: '融合分析' },
    { key: '/profile', icon: <UserOutlined />, label: '个人中心' }
]

function App() {
    const navigate = useNavigate()
    const location = useLocation()

    return (
        <Layout className="app-layout">
            <Header className="app-header">
                <div className="logo">
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
            </Header>

            <Content className="app-content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/bazi" element={<BaZi />} />
                    <Route path="/ziwei" element={<ZiWei />} />
                    <Route path="/yijing" element={<YiJing />} />
                    <Route path="/psychology" element={<Psychology />} />
                    <Route path="/fusion" element={<Fusion />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </Content>

            <Footer className="app-footer">
                玄心理命 ©2024 - 东方玄学与西方心理学融合
            </Footer>
        </Layout>
    )
}

export default App
