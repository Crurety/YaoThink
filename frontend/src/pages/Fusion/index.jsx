import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Steps, Typography, Tag, Spin, message, Result, Progress, Collapse, Divider } from 'antd';
import {
    ThunderboltOutlined,
    UserOutlined,
    StarOutlined,
    CheckCircleOutlined,
    FileTextOutlined,
    SyncOutlined
} from '@ant-design/icons';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './index.css';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

// 融合分析页面
const FusionPage = () => {
    const [loading, setLoading] = useState(false);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [report, setReport] = useState(null);
    const [step, setStep] = useState(0);

    // 用户已有的分析数据（模拟/从状态获取）
    const [userData, setUserData] = useState({
        bazi: null,
        ziwei: null,
        mbti: null,
        big5: null,
        archetype: null,
        enneagram: null
    });

    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

    // 执行融合分析
    const runFusionAnalysis = async () => {
        setLoading(true);
        setStep(1);

        try {
            // 收集所有可用数据
            const requestData = {
                bazi_data: userData.bazi,
                ziwei_data: userData.ziwei,
                mbti_type: userData.mbti,
                big5_scores: userData.big5,
                archetype: userData.archetype,
                enneagram_type: userData.enneagram
            };

            const res = await axios.post(`${API_BASE}/api/fusion/analyze`, requestData);

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
                bazi_data: userData.bazi,
                ziwei_data: userData.ziwei,
                mbti_type: userData.mbti,
                big5_scores: userData.big5,
                archetype: userData.archetype,
                enneagram_type: userData.enneagram
            };

            const res = await axios.post(`${API_BASE}/api/fusion/report`, requestData);

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

    // 快速测试（使用示例数据）
    const runQuickDemo = async () => {
        setUserData({
            mbti: 'INTJ',
            big5: { O: 75, C: 70, E: 35, A: 50, N: 40 },
            archetype: 'SAGE',
            enneagram: 5,
            bazi: {
                wuxing: { '木': 25, '火': 15, '土': 20, '金': 30, '水': 40 },
                shishen: { '正印': 2, '偏印': 1, '正官': 1, '七杀': 1 }
            }
        });

        message.success('已加载示例数据');
    };

    // 渲染数据收集状态
    const renderDataStatus = () => (
        <Card className="data-status-card">
            <Title level={4}>数据收集状态</Title>
            <Row gutter={[16, 16]}>
                <Col span={8}>
                    <div className={`status-item ${userData.bazi ? 'completed' : ''}`}>
                        <StarOutlined />
                        <Text>八字命理</Text>
                        <Tag color={userData.bazi ? 'green' : 'default'}>
                            {userData.bazi ? '已分析' : '待分析'}
                        </Tag>
                    </div>
                </Col>
                <Col span={8}>
                    <div className={`status-item ${userData.mbti ? 'completed' : ''}`}>
                        <UserOutlined />
                        <Text>MBTI测试</Text>
                        <Tag color={userData.mbti ? 'green' : 'default'}>
                            {userData.mbti || '待测试'}
                        </Tag>
                    </div>
                </Col>
                <Col span={8}>
                    <div className={`status-item ${userData.big5 ? 'completed' : ''}`}>
                        <StarOutlined />
                        <Text>大五人格</Text>
                        <Tag color={userData.big5 ? 'green' : 'default'}>
                            {userData.big5 ? '已测试' : '待测试'}
                        </Tag>
                    </div>
                </Col>
                <Col span={8}>
                    <div className={`status-item ${userData.archetype ? 'completed' : ''}`}>
                        <ThunderboltOutlined />
                        <Text>荣格原型</Text>
                        <Tag color={userData.archetype ? 'green' : 'default'}>
                            {userData.archetype || '待测试'}
                        </Tag>
                    </div>
                </Col>
                <Col span={8}>
                    <div className={`status-item ${userData.enneagram ? 'completed' : ''}`}>
                        <UserOutlined />
                        <Text>九型人格</Text>
                        <Tag color={userData.enneagram ? 'green' : 'default'}>
                            {userData.enneagram ? `${userData.enneagram}号` : '待测试'}
                        </Tag>
                    </div>
                </Col>
                <Col span={8}>
                    <div className={`status-item ${userData.ziwei ? 'completed' : ''}`}>
                        <StarOutlined />
                        <Text>紫微斗数</Text>
                        <Tag color={userData.ziwei ? 'green' : 'default'}>
                            {userData.ziwei ? '已分析' : '待分析'}
                        </Tag>
                    </div>
                </Col>
            </Row>

            <div className="action-buttons">
                <Button onClick={runQuickDemo} icon={<SyncOutlined />}>
                    加载示例数据
                </Button>
                <Button
                    type="primary"
                    onClick={runFusionAnalysis}
                    loading={loading}
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
                <Steps.Step title="数据收集" description="收集分析数据" />
                <Steps.Step title="融合分析" description="整合东西方视角" />
                <Steps.Step title="生成报告" description="个性化分析报告" />
            </Steps>

            {step === 0 && renderDataStatus()}
            {step === 2 && renderAnalysisResult()}
            {step === 3 && renderReport()}
        </div>
    );
};

export default FusionPage;
