import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Tabs, List, Tag, Button, Avatar, Statistic, Empty, Spin, message, Modal, Form, Input, Select, Switch, Typography } from 'antd';
import {
    UserOutlined,
    HistoryOutlined,
    StarOutlined,
    SettingOutlined,
    HeartOutlined,
    DeleteOutlined,
    EyeOutlined,
    EditOutlined
} from '@ant-design/icons';
import axios from 'axios';
import './index.css';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;

const ProfilePage = () => {
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');

    // 用户数据
    const [profile, setProfile] = useState(null);
    const [stats, setStats] = useState(null);
    const [settings, setSettings] = useState(null);

    // 历史记录
    const [analyses, setAnalyses] = useState([]);
    const [divinations, setDivinations] = useState([]);
    const [psychologyTests, setPsychologyTests] = useState([]);
    const [fusions, setFusions] = useState([]);
    const [favorites, setFavorites] = useState([]);

    // 弹窗
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [settingsModalVisible, setSettingsModalVisible] = useState(false);

    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

    // 加载用户数据
    useEffect(() => {
        loadUserData();
    }, []);

    const loadUserData = async () => {
        setLoading(true);
        try {
            // 并行加载数据
            const [profileRes, statsRes, settingsRes] = await Promise.all([
                axios.get(`${API_BASE}/api/user/profile`),
                axios.get(`${API_BASE}/api/user/stats`),
                axios.get(`${API_BASE}/api/user/settings`)
            ]);

            setProfile(profileRes.data.data);
            setStats(statsRes.data.data);
            setSettings(settingsRes.data.data);
        } catch (err) {
            console.error('加载用户数据失败', err);
            // 使用模拟数据
            setProfile({
                id: 1,
                nickname: '玄学爱好者',
                avatar: null,
                phone: '138****8888',
                email: null,
                is_vip: false,
                created_at: new Date().toISOString()
            });
            setStats({
                bazi_analyses: 5,
                ziwei_analyses: 3,
                divinations: 12,
                psychology_tests: 4,
                fusion_analyses: 2,
                favorites: 8
            });
            setSettings({
                theme: 'dark',
                language: 'zh-CN',
                timezone: 'Asia/Shanghai',
                notification_enabled: true
            });
        } finally {
            setLoading(false);
        }
    };

    // 加载历史记录
    const loadHistory = async (type) => {
        try {
            let res;
            switch (type) {
                case 'analyses':
                    res = await axios.get(`${API_BASE}/api/user/history/analyses`);
                    setAnalyses(res.data.data);
                    break;
                case 'divinations':
                    res = await axios.get(`${API_BASE}/api/user/history/divinations`);
                    setDivinations(res.data.data);
                    break;
                case 'psychology':
                    res = await axios.get(`${API_BASE}/api/user/history/psychology`);
                    setPsychologyTests(res.data.data);
                    break;
                case 'fusions':
                    res = await axios.get(`${API_BASE}/api/user/history/fusions`);
                    setFusions(res.data.data);
                    break;
                case 'favorites':
                    res = await axios.get(`${API_BASE}/api/user/favorites`);
                    setFavorites(res.data.data);
                    break;
            }
        } catch (err) {
            console.error('加载历史失败', err);
        }
    };

    // Tab切换时加载对应数据
    const handleTabChange = (key) => {
        setActiveTab(key);
        if (key === 'analyses') loadHistory('analyses');
        else if (key === 'divinations') loadHistory('divinations');
        else if (key === 'psychology') loadHistory('psychology');
        else if (key === 'fusions') loadHistory('fusions');
        else if (key === 'favorites') loadHistory('favorites');
    };

    // 删除历史记录
    const handleDelete = async (type, id) => {
        try {
            await axios.delete(`${API_BASE}/api/user/history/${type}/${id}`);
            message.success('删除成功');
            loadHistory(type);
        } catch (err) {
            message.error('删除失败');
        }
    };

    // 渲染概览
    const renderOverview = () => (
        <div className="overview-section">
            <Card className="profile-card">
                <div className="profile-header">
                    <Avatar size={80} icon={<UserOutlined />} src={profile?.avatar} />
                    <div className="profile-info">
                        <Title level={3}>{profile?.nickname || '用户'}</Title>
                        <Text type="secondary">{profile?.phone || profile?.email}</Text>
                        {profile?.is_vip && <Tag color="gold">VIP会员</Tag>}
                    </div>
                    <Button icon={<EditOutlined />} onClick={() => setEditModalVisible(true)}>
                        编辑资料
                    </Button>
                </div>
            </Card>

            <Row gutter={[16, 16]} className="stats-row">
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="八字分析" value={stats?.bazi_analyses || 0} />
                    </Card>
                </Col>
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="紫微分析" value={stats?.ziwei_analyses || 0} />
                    </Card>
                </Col>
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="易经占卜" value={stats?.divinations || 0} />
                    </Card>
                </Col>
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="心理测试" value={stats?.psychology_tests || 0} />
                    </Card>
                </Col>
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="融合分析" value={stats?.fusion_analyses || 0} />
                    </Card>
                </Col>
                <Col span={4}>
                    <Card className="stat-card">
                        <Statistic title="我的收藏" value={stats?.favorites || 0} prefix={<HeartOutlined />} />
                    </Card>
                </Col>
            </Row>
        </div>
    );

    // 渲染历史列表
    const renderHistoryList = (data, type) => (
        <List
            className="history-list"
            dataSource={data}
            locale={{ emptyText: <Empty description="暂无记录" /> }}
            renderItem={(item) => (
                <List.Item
                    actions={[
                        <Button icon={<EyeOutlined />} type="link">查看</Button>,
                        <Button icon={<DeleteOutlined />} type="link" danger onClick={() => handleDelete(type, item.id)}>删除</Button>
                    ]}
                >
                    <List.Item.Meta
                        title={item.title || item.result_summary || item.question || `${item.type || item.test_type}分析`}
                        description={new Date(item.created_at).toLocaleString()}
                    />
                    {item.hexagram && <Tag color="blue">{item.hexagram}</Tag>}
                    {item.method && <Tag color="purple">{item.method}</Tag>}
                    {item.test_type && <Tag color="green">{item.test_type.toUpperCase()}</Tag>}
                    {item.confidence && <Tag color="orange">{`${item.confidence}%`}</Tag>}
                </List.Item>
            )}
        />
    );

    // 渲染设置
    const renderSettings = () => (
        <Card className="settings-card">
            <Form layout="vertical" initialValues={settings}>
                <Form.Item label="主题" name="theme">
                    <Select>
                        <Select.Option value="dark">深色</Select.Option>
                        <Select.Option value="light">浅色</Select.Option>
                    </Select>
                </Form.Item>
                <Form.Item label="语言" name="language">
                    <Select>
                        <Select.Option value="zh-CN">简体中文</Select.Option>
                        <Select.Option value="en-US">English</Select.Option>
                    </Select>
                </Form.Item>
                <Form.Item label="时区" name="timezone">
                    <Select>
                        <Select.Option value="Asia/Shanghai">东八区 (北京)</Select.Option>
                        <Select.Option value="Asia/Tokyo">东九区 (东京)</Select.Option>
                        <Select.Option value="America/New_York">西五区 (纽约)</Select.Option>
                    </Select>
                </Form.Item>
                <Form.Item label="接收通知" name="notification_enabled" valuePropName="checked">
                    <Switch />
                </Form.Item>
                <Button type="primary">保存设置</Button>
            </Form>
        </Card>
    );

    if (loading) {
        return (
            <div className="loading-container">
                <Spin size="large" tip="加载中..." />
            </div>
        );
    }

    return (
        <div className="profile-page">
            <Title level={2} className="page-title">
                <UserOutlined /> 个人中心
            </Title>

            <Tabs activeKey={activeTab} onChange={handleTabChange} className="profile-tabs">
                <TabPane tab={<span><UserOutlined />概览</span>} key="overview">
                    {renderOverview()}
                </TabPane>

                <TabPane tab={<span><HistoryOutlined />命理分析</span>} key="analyses">
                    {renderHistoryList(analyses, 'analyses')}
                </TabPane>

                <TabPane tab={<span><StarOutlined />易经占卜</span>} key="divinations">
                    {renderHistoryList(divinations, 'divinations')}
                </TabPane>

                <TabPane tab={<span><UserOutlined />心理测试</span>} key="psychology">
                    {renderHistoryList(psychologyTests, 'psychology')}
                </TabPane>

                <TabPane tab={<span><StarOutlined />融合分析</span>} key="fusions">
                    {renderHistoryList(fusions, 'fusions')}
                </TabPane>

                <TabPane tab={<span><HeartOutlined />我的收藏</span>} key="favorites">
                    {renderHistoryList(favorites, 'favorites')}
                </TabPane>

                <TabPane tab={<span><SettingOutlined />设置</span>} key="settings">
                    {renderSettings()}
                </TabPane>
            </Tabs>

            {/* 编辑资料弹窗 */}
            <Modal
                title="编辑资料"
                open={editModalVisible}
                onCancel={() => setEditModalVisible(false)}
                footer={null}
            >
                <Form layout="vertical" initialValues={profile}>
                    <Form.Item label="昵称" name="nickname">
                        <Input />
                    </Form.Item>
                    <Form.Item label="性别" name="gender">
                        <Select>
                            <Select.Option value="男">男</Select.Option>
                            <Select.Option value="女">女</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" block>保存</Button>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default ProfilePage;
