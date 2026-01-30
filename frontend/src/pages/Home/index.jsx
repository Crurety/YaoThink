import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Row, Col, Card, Button, Typography, Space } from 'antd'
import {
    CompassOutlined,
    StarOutlined,
    BookOutlined,
    ExperimentOutlined,
    RightOutlined
} from '@ant-design/icons'

const { Title, Paragraph } = Typography

const features = [
    {
        key: 'bazi',
        path: '/bazi',
        icon: <CompassOutlined style={{ fontSize: 48, color: '#DAA520' }} />,
        title: '八字命理',
        description: '四柱排盘、五行分析、十神推演、大运流年、神煞判断',
        color: '#DAA520'
    },
    {
        key: 'ziwei',
        path: '/ziwei',
        icon: <StarOutlined style={{ fontSize: 48, color: '#DC143C' }} />,
        title: '紫微斗数',
        description: '十二宫排列、十四主星、格局判断、运势分析',
        color: '#DC143C'
    },
    {
        key: 'yijing',
        path: '/yijing',
        icon: <BookOutlined style={{ fontSize: 48, color: '#2E8B57' }} />,
        title: '易经占卜',
        description: '梅花易数、六爻占卜、六十四卦解读',
        color: '#2E8B57'
    },
    {
        key: 'psychology',
        path: '/psychology',
        icon: <ExperimentOutlined style={{ fontSize: 48, color: '#1E90FF' }} />,
        title: '心理测评',
        description: 'MBTI人格测试、大五人格、九型人格、荣格原型',
        color: '#1E90FF',
        disabled: true
    }
]

function Home() {
    const navigate = useNavigate()

    return (
        <div className="home-page">
            {/* Hero Section */}
            <div style={{ textAlign: 'center', marginBottom: 60 }}>
                <div style={{ fontSize: 80, marginBottom: 20 }}>☯</div>
                <Title style={{
                    fontFamily: "'Noto Serif SC', serif",
                    fontSize: 48,
                    background: 'linear-gradient(90deg, #DAA520, #D2691E)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    marginBottom: 16
                }}>
                    玄心理命
                </Title>
                <Paragraph style={{
                    fontSize: 18,
                    color: '#b0b0b0',
                    maxWidth: 600,
                    margin: '0 auto 30px'
                }}>
                    融合东方传统玄学智慧与西方心理学理论
                    <br />
                    多维度了解自我，科学规划人生
                </Paragraph>
                <Space size="large">
                    <Button
                        type="primary"
                        size="large"
                        onClick={() => navigate('/bazi')}
                    >
                        开始测算 <RightOutlined />
                    </Button>
                    <Button
                        size="large"
                        style={{
                            borderColor: '#DAA520',
                            color: '#DAA520',
                            background: 'transparent'
                        }}
                    >
                        了解更多
                    </Button>
                </Space>
            </div>

            {/* Features Grid */}
            <Row gutter={[24, 24]} style={{ maxWidth: 1200, margin: '0 auto' }}>
                {features.map(feature => (
                    <Col xs={24} sm={12} lg={6} key={feature.key}>
                        <Card
                            hoverable={!feature.disabled}
                            style={{
                                height: '100%',
                                opacity: feature.disabled ? 0.5 : 1,
                                cursor: feature.disabled ? 'not-allowed' : 'pointer'
                            }}
                            onClick={() => !feature.disabled && navigate(feature.path)}
                        >
                            <div style={{ textAlign: 'center' }}>
                                {feature.icon}
                                <Title level={4} style={{
                                    marginTop: 16,
                                    marginBottom: 8,
                                    color: feature.color
                                }}>
                                    {feature.title}
                                </Title>
                                <Paragraph style={{ color: '#b0b0b0', marginBottom: 0 }}>
                                    {feature.description}
                                </Paragraph>
                                {feature.disabled && (
                                    <div style={{
                                        marginTop: 12,
                                        color: '#666',
                                        fontSize: 12
                                    }}>
                                        即将上线
                                    </div>
                                )}
                            </div>
                        </Card>
                    </Col>
                ))}
            </Row>

            {/* Features Description */}
            <div style={{
                maxWidth: 800,
                margin: '60px auto 0',
                textAlign: 'center'
            }}>
                <Title level={3} style={{ color: '#DAA520', marginBottom: 24 }}>
                    东西方智慧融合
                </Title>
                <Row gutter={[40, 24]}>
                    <Col xs={24} md={12}>
                        <div style={{ padding: 20 }}>
                            <Title level={5} style={{ color: '#DC143C' }}>🔮 东方玄学</Title>
                            <Paragraph style={{ color: '#b0b0b0' }}>
                                八字命理、紫微斗数、易经占卜等传统术数，
                                蕴含数千年东方智慧，揭示命运规律。
                            </Paragraph>
                        </div>
                    </Col>
                    <Col xs={24} md={12}>
                        <div style={{ padding: 20 }}>
                            <Title level={5} style={{ color: '#1E90FF' }}>🧠 西方心理学</Title>
                            <Paragraph style={{ color: '#b0b0b0' }}>
                                MBTI人格类型、荣格原型、积极心理学等现代理论，
                                科学解析性格特质与发展潜力。
                            </Paragraph>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
    )
}

export default Home
