import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Button, Steps, Typography, Tag, Spin, message, Progress, Collapse, Divider, Modal, List, Empty } from 'antd';
import {
    ThunderboltOutlined,
    UserOutlined,
    StarOutlined,
    FileTextOutlined,
    SyncOutlined,
    HistoryOutlined,
    CheckOutlined
} from '@ant-design/icons';
import api from '../../services/api';
import ReactMarkdown from 'react-markdown';
import './index.css';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

// 六大类别配置
const CATEGORIES = {
    bazi: { name: '八字命理', icon: <StarOutlined />, apiType: 'analyses', queryParam: 'bazi' },
    ziwei: { name: '紫微斗数', icon: <StarOutlined />, apiType: 'analyses', queryParam: 'ziwei' },
    mbti: { name: 'MBTI测试', icon: <UserOutlined />, apiType: 'psychology', queryParam: 'mbti' },
    big5: { name: '大五人格', icon: <StarOutlined />, apiType: 'psychology', queryParam: 'big5' },
    archetype: { name: '荣格原型', icon: <ThunderboltOutlined />, apiType: 'psychology', queryParam: 'archetype' },
    enneagram: { name: '九型人格', icon: <UserOutlined />, apiType: 'psychology', queryParam: 'enneagram' }
};

// 融合分析页面
const FusionPage = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [report, setReport] = useState(null);
    const [step, setStep] = useState(0);

    // 选中的历史报告
    const [selectedRecords, setSelectedRecords] = useState({
        bazi: null,
        ziwei: null,
        mbti: null,
        big5: null,
        archetype: null,
        enneagram: null
    });

    // Modal 状态
    const [modalVisible, setModalVisible] = useState(false);
    const [modalCategory, setModalCategory] = useState(null);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [historyList, setHistoryList] = useState([]);

    // 计算已选择的报告数量
    const selectedCount = Object.values(selectedRecords).filter(v => v !== null).length;
    const canAnalyze = selectedCount >= 1; // 至少选择一项

    // 打开选择历史记录弹窗
    const openSelectModal = async (category) => {
        setModalCategory(category);
        setModalVisible(true);
        setHistoryLoading(true);
        setHistoryList([]);

        try {
            const config = CATEGORIES[category];
            let endpoint = '';
            let params = {};

            if (config.apiType === 'analyses') {
                endpoint = '/user/history/analyses';
                params = { analysis_type: config.queryParam, limit: 20 };
            } else {
                endpoint = '/user/history/psychology';
                params = { test_type: config.queryParam, limit: 20 };
            }

            const res = await api.get(endpoint, { params });
            if (res.data.success) {
                setHistoryList(res.data.data || []);
            }
        } catch (err) {
            console.error('加载历史记录失败:', err);
            message.error('加载历史记录失败');
        } finally {
            setHistoryLoading(false);
        }
    };

    // 选择一条历史记录
    const selectRecord = (record) => {
        setSelectedRecords(prev => ({
            ...prev,
            [modalCategory]: record
        }));
        setModalVisible(false);
        message.success(`已选择 ${CATEGORIES[modalCategory].name} 报告`);
    };

    // 取消选择
    const clearSelection = (category) => {
        setSelectedRecords(prev => ({
            ...prev,
            [category]: null
        }));
    };

    // 类型名称映射
    const TYPE_LABELS = {
        bazi: '八字命理',
        ziwei: '紫微斗数',
        mbti: '心理测试',
        big5: '心理测试',
        archetype: '心理测试',
        enneagram: '心理测试'
    };

    // 格式化报告编号: 类型+YYYY-MM-DD_HH:mm:SS
    const formatRecordId = (category, record) => {
        if (!record) return '';
        const typeLabel = TYPE_LABELS[category] || '报告';
        const date = new Date(record.created_at);
        const yyyy = date.getFullYear();
        const MM = String(date.getMonth() + 1).padStart(2, '0');
        const dd = String(date.getDate()).padStart(2, '0');
        const HH = String(date.getHours()).padStart(2, '0');
        const mm = String(date.getMinutes()).padStart(2, '0');
        const SS = String(date.getSeconds()).padStart(2, '0');
        return `${typeLabel}_${yyyy}-${MM}-${dd}_${HH}:${mm}:${SS}`;
    };

    // 获取报告摘要显示（用于卡片 Tag）
    const getRecordSummary = (category, record) => {
        if (!record) return '待选择';

        switch (category) {
            case 'bazi':
            case 'ziwei':
                return formatRecordId(category, record);
            case 'mbti':
                return record.result_data?.type_code || formatRecordId(category, record);
            case 'big5':
                return formatRecordId(category, record);
            case 'archetype':
                return record.result_data?.primary?.name || formatRecordId(category, record);
            case 'enneagram':
                return record.result_data?.primary_type ? `${record.result_data.primary_type}号` : formatRecordId(category, record);
            default:
                return formatRecordId(category, record);
        }
    };

    // 执行融合分析
    const runFusionAnalysis = async () => {
        if (!canAnalyze) {
            message.warning('请至少选择一项历史报告');
            return;
        }

        setLoading(true);
        setStep(1);

        try {
            // 从选中的历史记录提取数据
            const requestData = {
                bazi_data: selectedRecords.bazi?.result_data || null,
                ziwei_data: selectedRecords.ziwei?.result_data || null,
                mbti_type: selectedRecords.mbti?.result_data?.type_code || null,
                big5_scores: selectedRecords.big5?.result_data?.scores || null,
                archetype: selectedRecords.archetype?.result_data?.primary?.name || null,
                enneagram_type: selectedRecords.enneagram?.result_data?.primary_type || null
            };

            const res = await api.post('/fusion/analyze', requestData);

            if (res.data.success) {
                setAnalysisResult(res.data.result);
                setStep(2);
            }
        } catch (err) {
            message.error('分析失败，请重试');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // 生成完整报告
    const generateReport = async () => {
        setLoading(true);

        try {
            const requestData = {
                bazi_data: selectedRecords.bazi?.result_data || null,
                ziwei_data: selectedRecords.ziwei?.result_data || null,
                mbti_type: selectedRecords.mbti?.result_data?.type_code || null,
                big5_scores: selectedRecords.big5?.result_data?.scores || null,
                archetype: selectedRecords.archetype?.result_data?.primary?.name || null,
                enneagram_type: selectedRecords.enneagram?.result_data?.primary_type || null
            };

            const res = await api.post('/fusion/report', requestData);

            if (res.data.success) {
                setReport(res.data.report);
                setStep(3);
            }
        } catch (err) {
            message.error('生成报告失败');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // 渲染数据收集状态
    const renderDataStatus = () => (
        <Card className="data-status-card">
            <Title level={4}>
                <HistoryOutlined style={{ marginRight: 8 }} />
                选择历史报告进行融合分析
            </Title>
            <Paragraph type="secondary" style={{ marginBottom: 16 }}>
                点击下方卡片从历史记录中选择报告，至少选择一项后即可开始融合分析
            </Paragraph>
            <Row gutter={[16, 16]}>
                {Object.entries(CATEGORIES).map(([key, config]) => (
                    <Col span={8} key={key}>
                        <div
                            className={`status-item clickable ${selectedRecords[key] ? 'completed' : ''}`}
                            onClick={() => openSelectModal(key)}
                        >
                            {config.icon}
                            <Text>{config.name}</Text>
                            <Tag color={selectedRecords[key] ? 'green' : 'default'}>
                                {getRecordSummary(key, selectedRecords[key])}
                            </Tag>
                            {selectedRecords[key] && (
                                <Button
                                    type="text"
                                    size="small"
                                    danger
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        clearSelection(key);
                                    }}
                                    style={{ marginTop: 4 }}
                                >
                                    取消选择
                                </Button>
                            )}
                        </div>
                    </Col>
                ))}
            </Row>

            <div className="action-buttons">
                <Text type="secondary" style={{ marginRight: 16 }}>
                    已选择 {selectedCount}/6 项
                </Text>
                <Button
                    type="primary"
                    onClick={runFusionAnalysis}
                    loading={loading}
                    disabled={!canAnalyze}
                    icon={<ThunderboltOutlined />}
                >
                    开始融合分析
                </Button>
            </div>
        </Card>
    );

    // 渲染分析结果
    const renderAnalysisResult = () => {
        if (!analysisResult) return null;

        const { personality_fusion, consistency_analysis, life_guidance, confidence } = analysisResult;

        return (
            <div className="analysis-result">
                <Card className="result-card">
                    <Title level={3}>融合分析结果</Title>

                    {/* 置信度 */}
                    <div className="confidence-section">
                        <Text>分析置信度</Text>
                        <Progress
                            percent={confidence}
                            strokeColor={{ '0%': '#722ed1', '100%': '#eb2f96' }}
                        />
                    </div>

                    {/* 人格融合 */}
                    <Collapse defaultActiveKey={['1', '2', '3']}>
                        <Panel header="🌟 核心人格特质" key="1">
                            <Paragraph>{personality_fusion?.description}</Paragraph>
                            <div className="traits-grid">
                                {personality_fusion?.core_traits?.map((trait, i) => (
                                    <Tag key={i} color="purple">{trait}</Tag>
                                ))}
                            </div>

                            <Divider />

                            <Title level={5}>优势</Title>
                            <div className="traits-grid">
                                {personality_fusion?.strengths?.map((s, i) => (
                                    <Tag key={i} color="green">{s}</Tag>
                                ))}
                            </div>

                            <Title level={5}>成长空间</Title>
                            <div className="traits-grid">
                                {personality_fusion?.challenges?.map((c, i) => (
                                    <Tag key={i} color="orange">{c}</Tag>
                                ))}
                            </div>
                        </Panel>

                        <Panel header="☯️ 东西方一致性分析" key="2">
                            <div className="consistency-score">
                                <Text>一致性得分</Text>
                                <Progress
                                    type="circle"
                                    percent={consistency_analysis?.score || 50}
                                    width={80}
                                    strokeColor={consistency_analysis?.score >= 70 ? '#52c41a' : '#faad14'}
                                />
                            </div>

                            {consistency_analysis?.matches?.length > 0 && (
                                <>
                                    <Title level={5}>一致之处</Title>
                                    {consistency_analysis.matches.map((m, i) => (
                                        <Paragraph key={i}>✅ {m.description}</Paragraph>
                                    ))}
                                </>
                            )}

                            {consistency_analysis?.insights?.length > 0 && (
                                <>
                                    <Title level={5}>洞察</Title>
                                    {consistency_analysis.insights.map((ins, i) => (
                                        <Paragraph key={i}>💡 {ins}</Paragraph>
                                    ))}
                                </>
                            )}
                        </Panel>

                        <Panel header="🧭 人生发展指南" key="3">
                            {life_guidance?.career?.length > 0 && (
                                <>
                                    <Title level={5}>💼 事业方向</Title>
                                    <div className="traits-grid">
                                        {life_guidance.career.map((c, i) => (
                                            <Tag key={i} color="blue">{c}</Tag>
                                        ))}
                                    </div>
                                </>
                            )}

                            {life_guidance?.growth?.length > 0 && (
                                <>
                                    <Title level={5}>🌱 成长建议</Title>
                                    {life_guidance.growth.map((g, i) => (
                                        <Paragraph key={i}>• {g}</Paragraph>
                                    ))}
                                </>
                            )}

                            {life_guidance?.caution?.length > 0 && (
                                <>
                                    <Title level={5}>⚠️ 注意事项</Title>
                                    {life_guidance.caution.map((c, i) => (
                                        <Paragraph key={i} type="warning">• {c}</Paragraph>
                                    ))}
                                </>
                            )}
                        </Panel>
                    </Collapse>

                    <div className="action-buttons">
                        <Button onClick={() => { setStep(0); setAnalysisResult(null); }}>
                            重新分析
                        </Button>
                        <Button
                            type="primary"
                            onClick={generateReport}
                            loading={loading}
                            icon={<FileTextOutlined />}
                        >
                            生成完整报告
                        </Button>
                    </div>
                </Card>
            </div>
        );
    };

    // 渲染报告
    const renderReport = () => {
        if (!report) return null;

        return (
            <div className="report-section">
                <Card className="report-card">
                    <div className="report-header">
                        <Title level={3}>
                            <FileTextOutlined /> 融合分析报告
                        </Title>
                        <Button type="primary" onClick={() => navigator.clipboard.writeText(report)}>
                            复制报告
                        </Button>
                    </div>

                    <div className="markdown-content">
                        <ReactMarkdown>{report}</ReactMarkdown>
                    </div>

                    <div className="action-buttons">
                        <Button onClick={() => { setStep(0); setReport(null); setAnalysisResult(null); }}>
                            返回首页
                        </Button>
                    </div>
                </Card>
            </div>
        );
    };

    if (loading) {
        return (
            <div className="loading-container">
                <Spin size="large" tip="正在进行融合分析..." />
            </div>
        );
    }

    return (
        <div className="fusion-page">
            <Title level={2} className="page-title">
                <ThunderboltOutlined /> 东西方融合分析
            </Title>
            <Paragraph className="page-desc">
                整合东方命理与西方心理学，获得全方位的人格洞察
            </Paragraph>

            <Steps current={step} className="fusion-steps">
                <Steps.Step title="数据收集" description="选择历史报告" />
                <Steps.Step title="融合分析" description="整合东西方视角" />
                <Steps.Step title="生成报告" description="个性化分析报告" />
            </Steps>

            {step === 0 && renderDataStatus()}
            {step === 2 && renderAnalysisResult()}
            {step === 3 && renderReport()}

            {/* 选择历史记录弹窗 */}
            <Modal
                title={modalCategory ? `选择 ${CATEGORIES[modalCategory]?.name} 历史记录` : '选择历史记录'}
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                footer={null}
                width={600}
            >
                {historyLoading ? (
                    <div style={{ textAlign: 'center', padding: 40 }}>
                        <Spin tip="加载历史记录..." />
                    </div>
                ) : historyList.length === 0 ? (
                    <Empty
                        description={
                            <span>
                                暂无 {modalCategory ? CATEGORIES[modalCategory]?.name : ''} 历史记录
                                <br />
                                <Button
                                    type="link"
                                    onClick={() => {
                                        setModalVisible(false);
                                        if (modalCategory === 'bazi') navigate('/bazi');
                                        else if (modalCategory === 'ziwei') navigate('/ziwei');
                                        else navigate('/psychology');
                                    }}
                                >
                                    去进行测试
                                </Button>
                            </span>
                        }
                    />
                ) : (
                    <List
                        dataSource={historyList}
                        renderItem={(record) => (
                            <List.Item
                                className="history-list-item"
                                actions={[
                                    <Button
                                        type="primary"
                                        size="small"
                                        icon={<CheckOutlined />}
                                        onClick={() => selectRecord(record)}
                                    >
                                        选择
                                    </Button>
                                ]}
                            >
                                <List.Item.Meta
                                    title={
                                        <span>
                                            {getRecordSummary(modalCategory, record)}
                                            <Tag style={{ marginLeft: 8 }}>
                                                {new Date(record.created_at).toLocaleString()}
                                            </Tag>
                                        </span>
                                    }
                                    description={
                                        modalCategory === 'bazi' || modalCategory === 'ziwei'
                                            ? `ID: ${record.id}`
                                            : (typeof record.result_data?.description === 'string'
                                                ? record.result_data.description.slice(0, 50)
                                                : '')
                                    }
                                />
                            </List.Item>
                        )}
                    />
                )}
            </Modal>
        </div>
    );
};

export default FusionPage;
