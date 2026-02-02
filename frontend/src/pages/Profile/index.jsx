
import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Tabs, List, Tag, Button, Avatar, Statistic, Empty, Spin, message, Modal, Form, Input, Select, Switch, Typography, Space } from 'antd';
import {
    UserOutlined,
    HistoryOutlined,
    StarOutlined,
    SettingOutlined,
    HeartOutlined,
    DeleteOutlined,
    EyeOutlined,
    EditOutlined,
    LockOutlined
} from '@ant-design/icons';
import api from '../../services/api';
import HistoryDetailModal from './HistoryDetailModal';
import HistoryCard from './components/HistoryCard';
import './index.css';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;

const ProfilePage = () => {
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');

    // User Data
    const [profile, setProfile] = useState(null);
    const [stats, setStats] = useState(null);
    const [settings, setSettings] = useState(null);

    // History Data
    const [baziList, setBaziList] = useState([]);
    const [ziweiList, setZiweiList] = useState([]);
    const [divinations, setDivinations] = useState([]);
    const [psychologyTests, setPsychologyTests] = useState([]);
    const [fusions, setFusions] = useState([]);
    const [favorites, setFavorites] = useState([]);

    // Modals
    const [editModalVisible, setEditModalVisible] = useState(false);
    const [passwordModalVisible, setPasswordModalVisible] = useState(false);

    // Detail Modal State
    const [detailModalVisible, setDetailModalVisible] = useState(false);
    const [selectedRecord, setSelectedRecord] = useState(null);
    const [selectedRecordType, setSelectedRecordType] = useState('');

    const [form] = Form.useForm();
    const [passwordForm] = Form.useForm();
    const [settingsForm] = Form.useForm();

    // Load initial data
    useEffect(() => {
        loadUserData();
    }, []);

    const loadUserData = async () => {
        setLoading(true);
        try {
            const [profileRes, statsRes, settingsRes] = await Promise.all([
                api.get('/api/user/profile'),
                api.get('/api/user/stats'),
                api.get('/api/user/settings')
            ]);

            setProfile(profileRes.data.data);
            setStats(statsRes.data.data);
            setSettings(settingsRes.data.data);

            // Set initial form values
            settingsForm.setFieldsValue(settingsRes.data.data);
        } catch (err) {
            console.error('Failed to load user data', err);
            message.error('加载用户数据失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    const loadHistory = async (type) => {
        try {
            let res;
            switch (type) {
                case 'bazi':
                    res = await api.get('/api/user/history/analyses', { params: { analysis_type: 'bazi' } });
                    setBaziList(res.data.data);
                    break;
                case 'ziwei':
                    res = await api.get('/api/user/history/analyses', { params: { analysis_type: 'ziwei' } });
                    setZiweiList(res.data.data);
                    break;
                case 'divinations':
                    res = await api.get('/api/user/history/divinations');
                    setDivinations(res.data.data);
                    break;
                case 'psychology':
                    res = await api.get('/api/user/history/psychology');
                    setPsychologyTests(res.data.data);
                    break;
                case 'fusions':
                    res = await api.get('/api/user/history/fusions');
                    setFusions(res.data.data);
                    break;
                case 'favorites':
                    res = await api.get('/api/user/favorites');
                    setFavorites(res.data.data);
                    break;
            }
        } catch (err) {
            console.error('加载历史记录失败', err);
            message.error('加载历史记录失败');
        }
    };

    const handleTabChange = (key) => {
        setActiveTab(key);
        if (['bazi', 'ziwei', 'divinations', 'psychology', 'fusions', 'favorites'].includes(key)) {
            loadHistory(key);
        }
    };

    const handleDelete = async (apiType, id, refreshType) => {
        try {
            await api.delete(`/api/user/history/${apiType}/${id}`);
            message.success('删除成功');
            loadHistory(refreshType || apiType);
            // Refresh stats if needed
            const statsRes = await api.get('/api/user/stats');
            setStats(statsRes.data.data);
        } catch (err) {
            message.error('删除失败');
        }
    };

    // View Detail
    const handleViewDetail = (item, type) => {
        setSelectedRecord(item);
        setSelectedRecordType(type);
        setDetailModalVisible(true);
    };

    // Update Profile
    const handleUpdateProfile = async (values) => {
        try {
            const res = await api.put('/api/user/profile', values);
            if (res.data.success) {
                message.success('资料更新成功');
                setEditModalVisible(false);
                loadUserData(); // Reload all data
            }
        } catch (err) {
            message.error('更新失败');
        }
    };

    // Change Password
    const handleChangePassword = async (values) => {
        try {
            const res = await api.post('/api/auth/change-password', values);
            if (res.data.success) {
                message.success('密码修改成功');
                setPasswordModalVisible(false);
                passwordForm.resetFields();
            }
        } catch (err) {
            message.error(err.response?.data?.detail || '密码修改失败');
        }
    };

    // Update Settings
    const handleUpdateSettings = async (values) => {
        try {
            const res = await api.put('/api/user/settings', values);
            if (res.data.success) {
                message.success('设置更新成功');
                setSettings(values);
            }
        } catch (err) {
            message.error('设置更新失败');
        }
    };

    const renderOverview = () => (
        <div className="overview-section">
            <Card className="profile-card">
                <div className="profile-header">
                    <Avatar
                        size={80}
                        icon={<UserOutlined />}
                        src={profile?.avatar}
                        style={{ backgroundColor: '#722ed1' }}
                    />
                    <div className="profile-info">
                        <Title level={3} style={{ marginBottom: 4 }}>{profile?.nickname || '用户'}</Title>
                        <Space className="profile-meta">
                            <Text type="secondary">{profile?.phone || profile?.email}</Text>
                            {profile?.gender && <Tag color={profile.gender === '男' ? 'blue' : 'magenta'}>{profile.gender}</Tag>}
                            {profile?.is_vip && <Tag color="gold">VIP会员</Tag>}
                        </Space>
                        <div style={{ marginTop: 8 }}>
                            <Text type="secondary" style={{ fontSize: 12 }}>注册时间: {new Date(profile?.created_at).toLocaleDateString()}</Text>
                        </div>
                    </div>
                    <Button icon={<EditOutlined />} onClick={() => {
                        form.setFieldsValue(profile);
                        setEditModalVisible(true);
                    }}>
                        编辑资料
                    </Button>
                </div>
            </Card>

            <Row gutter={[16, 16]} className="stats-row">
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('bazi')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="八字" value={stats?.bazi_analyses || 0} prefix={<CompassOutlined />} />
                    </Card>
                </Col>
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('ziwei')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="紫微" value={stats?.ziwei_analyses || 0} prefix={<StarOutlined />} />
                    </Card>
                </Col>
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('divinations')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="占卜" value={stats?.divinations || 0} prefix={<ExperimentOutlined />} />
                    </Card>
                </Col>
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('psychology')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="测试" value={stats?.psychology_tests || 0} prefix={<UserOutlined />} />
                    </Card>
                </Col>
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('fusions')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="融合" value={stats?.fusion_analyses || 0} prefix={<StarOutlined />} />
                    </Card>
                </Col>
                <Col xs={12} sm={8} md={4}>
                    <Card
                        className="stat-card"
                        hoverable
                        onClick={() => handleTabChange('favorites')}
                        style={{ cursor: 'pointer' }}
                    >
                        <Statistic title="收藏" value={stats?.favorites || 0} prefix={<HeartOutlined />} valueStyle={{ color: '#cf1322' }} />
                    </Card>
                </Col>
            </Row>
        </div>
    );

    const renderHistoryList = (data, listType) => {
        if (!data || data.length === 0) {
            return <Empty description="暂无记录" image={Empty.PRESENTED_IMAGE_SIMPLE} />;
        }

        return (
            <Row gutter={[16, 16]}>
                {data.map((item) => (
                    <Col xs={24} sm={24} md={12} lg={12} xl={8} key={item.id}>
                        <HistoryCard
                            record={item}
                            type={listType === 'bazi' || listType === 'ziwei' ? 'analyses' : listType} // Pass 'analyses' for HistoryCard internal logic if it expects it
                            onClick={(item) => handleViewDetail(item, listType)}
                            onDelete={(id) => {
                                const apiType = ['bazi', 'ziwei'].includes(listType) ? 'analyses' : listType;
                                handleDelete(apiType, id, listType);
                            }}
                        />
                    </Col>
                ))}
            </Row>
        );
    };

    const renderSettings = () => (
        <Card className="settings-card" title="应用设置">
            <Form
                form={settingsForm}
                layout="vertical"
                onFinish={handleUpdateSettings}
            >
                <Form.Item label="主题" name="theme">
                    <Select>
                        <Select.Option value="dark">深色模式</Select.Option>
                        <Select.Option value="light">浅色模式</Select.Option>
                    </Select>
                </Form.Item>
                <Form.Item label="语言" name="language">
                    <Select>
                        <Select.Option value="zh-CN">简体中文</Select.Option>
                        <Select.Option value="en-US">English</Select.Option>
                    </Select>
                </Form.Item>
                <Form.Item label="接收通知" name="notification_enabled" valuePropName="checked">
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" />
                </Form.Item>
                <Form.Item style={{ marginTop: 24 }}>
                    <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                        保存设置
                    </Button>
                    <Button
                        icon={<LockOutlined />}
                        style={{ marginLeft: 16 }}
                        onClick={() => setPasswordModalVisible(true)}
                    >
                        修改密码
                    </Button>
                </Form.Item>
            </Form>
        </Card>
    );

    // Need to import icons used in renderOverview & renderSettings if not imported
    const CompassOutlined = StarOutlined; // Fallback/Alias if not imported
    const ExperimentOutlined = UserOutlined; // Fallback/Alias
    const SaveOutlined = EditOutlined; // Fallback/Alias

    if (loading) {
        return (
            <div className="loading-container">
                <Spin size="large" tip="加载数据中..." />
            </div>
        );
    }

    return (
        <div className="profile-page">
            <Title level={2} className="page-title">
                <UserOutlined /> 个人中心
            </Title>

            <Tabs activeKey={activeTab} onChange={handleTabChange} className="profile-tabs" type="card">
                <TabPane tab={<span><UserOutlined />概览</span>} key="overview">
                    {renderOverview()}
                </TabPane>

                <TabPane tab={<span><HistoryOutlined />八字命理</span>} key="bazi">
                    {renderHistoryList(baziList, 'bazi')}
                </TabPane>

                <TabPane tab={<span><StarOutlined />紫微斗数</span>} key="ziwei">
                    {renderHistoryList(ziweiList, 'ziwei')}
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

            {/* Edit Profile Modal */}
            <Modal
                title="编辑资料"
                open={editModalVisible}
                onCancel={() => setEditModalVisible(false)}
                footer={null}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleUpdateProfile}
                >
                    <Form.Item label="头像链接" name="avatar" help="请输入网络图片地址，或后续支持上传">
                        <Input prefix={<UserOutlined />} placeholder="https://..." />
                    </Form.Item>
                    <Form.Item label="昵称" name="nickname" rules={[{ required: true, message: '请输入昵称' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="性别" name="gender">
                        <Select>
                            <Select.Option value="男">男</Select.Option>
                            <Select.Option value="女">女</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" block>保存</Button>
                    </Form.Item>
                </Form>
            </Modal>

            {/* Change Password Modal */}
            <Modal
                title="修改密码"
                open={passwordModalVisible}
                onCancel={() => setPasswordModalVisible(false)}
                footer={null}
            >
                <Form
                    form={passwordForm}
                    layout="vertical"
                    onFinish={handleChangePassword}
                >
                    <Form.Item
                        label="旧密码"
                        name="old_password"
                        rules={[{ required: true, message: '请输入旧密码' }]}
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item
                        label="新密码"
                        name="new_password"
                        rules={[{ required: true, message: '请输入新密码' }, { min: 6, message: '密码至少6位' }]}
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item
                        label="确认新密码"
                        name="confirm_password"
                        dependencies={['new_password']}
                        rules={[
                            { required: true, message: '请确认新密码' },
                            ({ getFieldValue }) => ({
                                validator(_, value) {
                                    if (!value || getFieldValue('new_password') === value) {
                                        return Promise.resolve();
                                    }
                                    return Promise.reject(new Error('两次输入的密码不一致'));
                                },
                            }),
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" block>修改密码</Button>
                    </Form.Item>
                </Form>
            </Modal>

            {/* History Detail Modal */}
            <HistoryDetailModal
                visible={detailModalVisible}
                onClose={() => setDetailModalVisible(false)}
                record={selectedRecord}
                type={selectedRecordType}
            />
        </div>
    );
};

export default ProfilePage;
