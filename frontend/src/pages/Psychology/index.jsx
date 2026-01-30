import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Progress, Radio, Space, Typography, Tag, Tabs, Spin, message, Result } from 'antd';
import {
    UserOutlined,
    RocketOutlined,
    HeartOutlined,
    StarOutlined,
    CheckCircleOutlined,
    ArrowRightOutlined,
    ArrowLeftOutlined
} from '@ant-design/icons';
import axios from 'axios';
import './index.css';

const { Title, Text, Paragraph } = Typography;

// 测试类型配置
const TEST_TYPES = {
    mbti: {
        name: 'MBTI人格类型',
        icon: <UserOutlined />,
        color: '#722ed1',
        description: '探索你的16种人格类型',
        questions: 32,
        time: '10-15分钟'
    },
    big5: {
        name: '大五人格',
        icon: <StarOutlined />,
        color: '#13c2c2',
        description: '科学评估五大人格维度',
        questions: 60,
        time: '15-20分钟'
    },
    archetype: {
        name: '荣格原型',
        icon: <HeartOutlined />,
        color: '#eb2f96',
        description: '发现你的心理原型',
        questions: 36,
        time: '10-15分钟'
    },
    enneagram: {
        name: '九型人格',
        icon: <RocketOutlined />,
        color: '#fa8c16',
        description: '了解你的核心人格类型',
        questions: 36,
        time: '10-15分钟'
    }
};

// 测试选择页面
const TestSelection = ({ onSelect }) => {
    return (
        <div className="test-selection">
            <Title level={2} className="section-title">选择心理测试</Title>
            <Paragraph className="section-desc">
                探索你的内心世界，发现真实的自己
            </Paragraph>

            <Row gutter={[24, 24]} className="test-cards">
                {Object.entries(TEST_TYPES).map(([key, test]) => (
                    <Col xs={24} sm={12} lg={6} key={key}>
                        <Card
                            className="test-card"
                            hoverable
                            onClick={() => onSelect(key)}
                            style={{ borderTop: `3px solid ${test.color}` }}
                        >
                            <div className="test-icon" style={{ color: test.color }}>
                                {test.icon}
                            </div>
                            <Title level={4}>{test.name}</Title>
                            <Text type="secondary">{test.description}</Text>
                            <div className="test-meta">
                                <Tag>{test.questions}题</Tag>
                                <Tag>{test.time}</Tag>
                            </div>
                            <Button type="primary" block style={{ marginTop: 16, background: test.color, borderColor: test.color }}>
                                开始测试
                            </Button>
                        </Card>
                    </Col>
                ))}
            </Row>
        </div>
    );
};

// 测试进行页面
const TestInProgress = ({ testType, questions, onComplete, onBack }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const test = TEST_TYPES[testType];

    const currentQuestion = questions[currentIndex];
    const progress = Math.round(((currentIndex + 1) / questions.length) * 100);

    const handleAnswer = (value) => {
        const newAnswers = {
            ...answers,
            [currentQuestion.id]: value
        };
        setAnswers(newAnswers);

        // 自动进入下一题
        if (currentIndex < questions.length - 1) {
            setTimeout(() => setCurrentIndex(currentIndex + 1), 300);
        }
    };

    const handleNext = () => {
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(currentIndex + 1);
        }
    };

    const handlePrev = () => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        }
    };

    const handleSubmit = () => {
        // 转换答案格式
        let formattedAnswers;
        if (testType === 'mbti') {
            formattedAnswers = Object.entries(answers).map(([qId, optIdx]) => ({
                question_id: parseInt(qId),
                option_index: optIdx
            }));
        } else {
            formattedAnswers = Object.entries(answers).map(([qId, value]) => ({
                question_id: parseInt(qId),
                value: value
            }));
        }
        onComplete(formattedAnswers);
    };

    const isComplete = Object.keys(answers).length === questions.length;

    return (
        <div className="test-progress">
            <div className="test-header">
                <Button icon={<ArrowLeftOutlined />} onClick={onBack}>返回</Button>
                <Title level={4} style={{ margin: 0, color: test.color }}>{test.name}</Title>
                <Text>{currentIndex + 1} / {questions.length}</Text>
            </div>

            <Progress percent={progress} strokeColor={test.color} showInfo={false} />

            <Card className="question-card">
                <Title level={4} className="question-text">{currentQuestion.text}</Title>

                {testType === 'mbti' ? (
                    <Radio.Group
                        onChange={(e) => handleAnswer(e.target.value)}
                        value={answers[currentQuestion.id]}
                        className="options-group"
                    >
                        <Space direction="vertical" size="large" style={{ width: '100%' }}>
                            {currentQuestion.options.map((opt, idx) => (
                                <Radio key={idx} value={idx} className="option-item">
                                    {opt.text}
                                </Radio>
                            ))}
                        </Space>
                    </Radio.Group>
                ) : (
                    <Radio.Group
                        onChange={(e) => handleAnswer(e.target.value)}
                        value={answers[currentQuestion.id]}
                        className="likert-group"
                    >
                        <Space size="middle">
                            {currentQuestion.options.map((opt) => (
                                <Radio.Button key={opt.value} value={opt.value} className="likert-item">
                                    {opt.text}
                                </Radio.Button>
                            ))}
                        </Space>
                    </Radio.Group>
                )}
            </Card>

            <div className="nav-buttons">
                <Button
                    onClick={handlePrev}
                    disabled={currentIndex === 0}
                    icon={<ArrowLeftOutlined />}
                >
                    上一题
                </Button>

                {currentIndex === questions.length - 1 ? (
                    <Button
                        type="primary"
                        onClick={handleSubmit}
                        disabled={!isComplete}
                        icon={<CheckCircleOutlined />}
                        style={{ background: test.color, borderColor: test.color }}
                    >
                        提交测试
                    </Button>
                ) : (
                    <Button
                        onClick={handleNext}
                        disabled={!answers[currentQuestion.id]}
                        icon={<ArrowRightOutlined />}
                    >
                        下一题
                    </Button>
                )}
            </div>
        </div>
    );
};

// 结果展示页面
const TestResult = ({ testType, result, onBack }) => {
    const test = TEST_TYPES[testType];

    const renderMBTIResult = () => (
        <div className="result-content">
            <div className="type-badge" style={{ background: test.color }}>
                {result.type_code}
            </div>
            <Title level={2}>{result.type_name}</Title>
            <Paragraph>{result.description?.description}</Paragraph>

            <Row gutter={16} className="dimensions">
                {Object.entries(result.dimensions).map(([dim, data]) => (
                    <Col span={6} key={dim}>
                        <Card size="small">
                            <Text strong>{dim}</Text>
                            <div className="dim-bar">
                                <Progress
                                    percent={data.clarity}
                                    size="small"
                                    strokeColor={test.color}
                                />
                            </div>
                            <Tag color={test.color}>{data.preference}</Tag>
                        </Card>
                    </Col>
                ))}
            </Row>

            {result.description?.strengths && (
                <Card title="优势" className="traits-card" size="small">
                    <Space wrap>
                        {result.description.strengths.map((s, i) => (
                            <Tag key={i} color="green">{s}</Tag>
                        ))}
                    </Space>
                </Card>
            )}

            {result.description?.career && (
                <Card title="适合职业" className="traits-card" size="small">
                    <Space wrap>
                        {result.description.career.map((c, i) => (
                            <Tag key={i} color="blue">{c}</Tag>
                        ))}
                    </Space>
                </Card>
            )}
        </div>
    );

    const renderBig5Result = () => (
        <div className="result-content">
            <Title level={3}>你的大五人格画像</Title>
            <Paragraph>{result.profile?.summary}</Paragraph>

            {Object.entries(result.scores).map(([dim, score]) => (
                <div key={dim} className="dimension-row">
                    <Text strong>{result.interpretation?.[dim]?.dimension || dim}</Text>
                    <Progress
                        percent={score}
                        strokeColor={test.color}
                        format={(p) => `${p}分`}
                    />
                    <Tag color={result.levels?.[dim] === '高' ? 'green' : result.levels?.[dim] === '低' ? 'red' : 'default'}>
                        {result.levels?.[dim]}
                    </Tag>
                </div>
            ))}
        </div>
    );

    const renderArchetypeResult = () => (
        <div className="result-content">
            <Title level={3}>你的荣格原型</Title>

            <Card className="primary-archetype" style={{ borderColor: test.color }}>
                <Title level={2} style={{ color: test.color }}>{result.primary?.name}</Title>
                <Text type="secondary">{result.primary?.english}</Text>
                <Paragraph style={{ marginTop: 16 }}>{result.primary?.description}</Paragraph>
                <div className="archetype-keywords">
                    {result.primary?.keywords?.map((k, i) => (
                        <Tag key={i} color="purple">{k}</Tag>
                    ))}
                </div>
            </Card>

            <Card title="次要原型" size="small" style={{ marginTop: 16 }}>
                <Title level={4}>{result.secondary?.name}</Title>
                <Text>{result.secondary?.english}</Text>
            </Card>

            <Paragraph className="profile-text">{result.profile}</Paragraph>
        </div>
    );

    const renderEnneagramResult = () => (
        <div className="result-content">
            <div className="type-badge" style={{ background: test.color }}>
                {result.primary_type}号
            </div>
            <Title level={2}>{result.primary_info?.name}</Title>
            <Text type="secondary">{result.primary_info?.english}</Text>

            <Card className="info-card" style={{ marginTop: 24 }}>
                <Paragraph><strong>核心恐惧：</strong>{result.primary_info?.core_fear}</Paragraph>
                <Paragraph><strong>核心渴望：</strong>{result.primary_info?.core_desire}</Paragraph>
                <Paragraph><strong>基本动机：</strong>{result.primary_info?.core_motivation}</Paragraph>
            </Card>

            {result.wing && (
                <Card title="翼型" size="small">
                    <Text>{result.wing}号翼型</Text>
                </Card>
            )}

            <Card title="关键词" size="small">
                <Space wrap>
                    {result.primary_info?.keywords?.map((k, i) => (
                        <Tag key={i} color="orange">{k}</Tag>
                    ))}
                </Space>
            </Card>

            <Card title="成长建议" size="small" style={{ marginTop: 16 }}>
                <Paragraph>{result.primary_info?.growth_advice}</Paragraph>
            </Card>
        </div>
    );

    const renderResult = () => {
        switch (testType) {
            case 'mbti': return renderMBTIResult();
            case 'big5': return renderBig5Result();
            case 'archetype': return renderArchetypeResult();
            case 'enneagram': return renderEnneagramResult();
            default: return null;
        }
    };

    return (
        <div className="test-result">
            <Result
                icon={<CheckCircleOutlined style={{ color: test.color }} />}
                title="测试完成！"
                subTitle="以下是你的测试结果"
            />

            {renderResult()}

            <div className="result-actions">
                <Button onClick={onBack} size="large">重新测试</Button>
                <Button type="primary" size="large" style={{ background: test.color, borderColor: test.color }}>
                    保存结果
                </Button>
            </div>
        </div>
    );
};

// 主页面组件
const PsychologyPage = () => {
    const [testType, setTestType] = useState(null);
    const [stage, setStage] = useState('select'); // select, testing, result
    const [questions, setQuestions] = useState([]);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

    // 加载题目
    const loadQuestions = async (type) => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/api/psychology/${type}/questions`);
            setQuestions(res.data.questions);
            setTestType(type);
            setStage('testing');
        } catch (err) {
            message.error('加载题目失败');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // 提交测试
    const submitTest = async (answers) => {
        setLoading(true);
        try {
            const res = await axios.post(`${API_BASE}/api/psychology/${testType}/submit`, { answers });
            setResult(res.data.result);
            setStage('result');
        } catch (err) {
            message.error('提交测试失败');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // 返回选择页
    const handleBack = () => {
        setStage('select');
        setTestType(null);
        setQuestions([]);
        setResult(null);
    };

    if (loading) {
        return (
            <div className="loading-container">
                <Spin size="large" tip="加载中..." />
            </div>
        );
    }

    return (
        <div className="psychology-page">
            {stage === 'select' && (
                <TestSelection onSelect={loadQuestions} />
            )}

            {stage === 'testing' && questions.length > 0 && (
                <TestInProgress
                    testType={testType}
                    questions={questions}
                    onComplete={submitTest}
                    onBack={handleBack}
                />
            )}

            {stage === 'result' && result && (
                <TestResult
                    testType={testType}
                    result={result}
                    onBack={handleBack}
                />
            )}
        </div>
    );
};

export default PsychologyPage;
