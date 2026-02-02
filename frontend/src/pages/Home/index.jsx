import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Row, Col, Card, Button, Typography, Space } from 'antd'
import {
    CompassOutlined,
    StarOutlined,
    BookOutlined,
    ExperimentOutlined,
    RightOutlined,
    ThunderboltOutlined,
    FireOutlined
} from '@ant-design/icons'

const { Title, Paragraph } = Typography

const features = [
    {
        key: 'bazi',
        path: '/bazi',
        icon: <CompassOutlined style={{ fontSize: 32 }} />,
        title: '八字命理',
        description: 'AI深度解析你的命运代码，揭示五行真谛',
        color: '#fbbf24', // Amber
        bgGradient: 'linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%)',
        gridArea: 'span 2 / span 1' // Tall card
    },
    {
        key: 'ziwei',
        path: '/ziwei',
        icon: <StarOutlined style={{ fontSize: 32 }} />,
        title: '紫微斗数',
        description: '十二宫全景扫描，掌控星运轨迹',
        color: '#f472b6', // Pink
        bgGradient: 'linear-gradient(135deg, rgba(244, 114, 182, 0.1) 0%, rgba(244, 114, 182, 0.05) 100%)',
        gridArea: 'span 1 / span 1'
    },
    {
        key: 'yijing',
        path: '/yijing',
        icon: <BookOutlined style={{ fontSize: 32 }} />,
        title: '易经占卜',
        description: '六爻神算，决断当下困惑',
        color: '#34d399', // Emerald
        bgGradient: 'linear-gradient(135deg, rgba(52, 211, 153, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%)',
        gridArea: 'span 1 / span 1'
    },
    {
        key: 'psychology',
        path: '/psychology',
        icon: <ExperimentOutlined style={{ fontSize: 32 }} />,
        title: '心理测评',
        description: 'MBTI/人格原型，科学读心',
        color: '#60a5fa', // Blue
        bgGradient: 'linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(96, 165, 250, 0.05) 100%)',
        gridArea: 'span 1 / span 2', // Wide card
    }
]

function Home() {
    const navigate = useNavigate()

    return (
        <div className="home-page" style={{ paddingBottom: 60 }}>
            {/* Hero Section */}
            <div style={{ textAlign: 'center', margin: '40px 0 80px', position: 'relative' }}>
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '600px',
                    height: '600px',
                    background: 'radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, rgba(0,0,0,0) 70%)',
                    zIndex: 0,
                    pointerEvents: 'none'
                }} />

                <div className="animate-float" style={{ fontSize: 80, marginBottom: 24, textShadow: '0 0 40px rgba(139, 92, 246, 0.4)' }}>
                    ☯
                </div>

                <Title style={{
                    fontFamily: "var(--font-display)",
                    fontSize: 56,
                    background: 'linear-gradient(135deg, #fff 0%, #a78bfa 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    marginBottom: 24,
                    letterSpacing: 4,
                    position: 'relative'
                }}>
                    玄心理命
                </Title>

                <Paragraph style={{
                    fontSize: 20,
                    color: '#94a3b8',
                    maxWidth: 500,
                    margin: '0 auto 40px',
                    lineHeight: 1.8,
                    position: 'relative'
                }}>
                    解锁你的 <span style={{ color: '#a78bfa', fontWeight: 'bold' }}>命运源代码</span>
                    <br />
                    赛博修仙与心理科学的终极融合
                </Paragraph>

                <Space size="large" style={{ position: 'relative' }}>
                    <Button
                        type="primary"
                        size="large"
                        style={{ height: 50, padding: '0 40px', fontSize: 18 }}
                        onClick={() => navigate('/bazi')}
                    >
                        立即开始 <RightOutlined />
                    </Button>
                </Space>
            </div>

            {/* Bento Grid Layout - Custom CSS Grid */}
            <div style={{
                maxWidth: 1000,
                margin: '0 auto',
                padding: '0 20px',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: 24
            }}>
                {features.map((feature, index) => (
                    <div
                        key={feature.key}
                        className="feature-card"
                        style={{
                            background: feature.bgGradient,
                            border: '1px solid rgba(255,255,255,0.05)',
                            borderRadius: 24,
                            padding: 32,
                            cursor: feature.disabled ? 'not-allowed' : 'pointer',
                            transition: 'all 0.3s ease',
                            position: 'relative',
                            overflow: 'hidden',
                            backdropFilter: 'blur(10px)',
                            gridColumn: index === 3 ? '1 / -1' : 'auto', // Last item spans full width on mobile/tablet
                        }}
                        onClick={() => !feature.disabled && navigate(feature.path)}
                    >
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'flex-start',
                            marginBottom: 20
                        }}>
                            <div style={{
                                color: feature.color,
                                background: 'rgba(255,255,255,0.05)',
                                padding: 12,
                                borderRadius: 16,
                                display: 'inline-flex'
                            }}>
                                {feature.icon}
                            </div>
                            {!feature.disabled && <RightOutlined style={{ color: '#64748b' }} />}
                            {feature.disabled && (
                                <span style={{
                                    background: 'rgba(0,0,0,0.3)',
                                    padding: '4px 12px',
                                    borderRadius: 12,
                                    fontSize: 12,
                                    color: '#94a3b8'
                                }}>
                                    开发中
                                </span>
                            )}
                        </div>

                        <Title level={3} style={{
                            color: '#fff',
                            marginBottom: 8,
                            fontSize: 24,
                            fontWeight: 600
                        }}>
                            {feature.title}
                        </Title>

                        <Paragraph style={{
                            color: '#94a3b8',
                            marginBottom: 0,
                            fontSize: 16
                        }}>
                            {feature.description}
                        </Paragraph>

                        {/* Decoration Circle */}
                        <div style={{
                            position: 'absolute',
                            bottom: -20,
                            right: -20,
                            width: 100,
                            height: 100,
                            background: feature.color,
                            opacity: 0.1,
                            borderRadius: '50%',
                            filter: 'blur(20px)'
                        }} />
                    </div>
                ))}
            </div>

            {/* Bottom Info */}
            <div style={{
                maxWidth: 800,
                margin: '100px auto 0',
                textAlign: 'center'
            }}>
                <Title level={3} style={{ color: '#fbbf24', marginBottom: 32 }}>
                    东西方智慧融合
                </Title>
                <Row gutter={[40, 24]}>
                    <Col xs={24} md={12}>
                        <div style={{
                            padding: 24,
                            background: 'rgba(255,255,255,0.02)',
                            borderRadius: 16,
                            border: '1px solid rgba(255,255,255,0.05)'
                        }}>
                            <div style={{ fontSize: 32, marginBottom: 16 }}>🔮</div>
                            <Title level={5} style={{ color: '#fda4af', marginBottom: 8 }}>东方玄学体系</Title>
                            <Paragraph style={{ color: '#cbd5e1', fontSize: 14 }}>
                                挖掘八字命理、紫微斗数、易经占卜等传统术数背后的数据模型
                            </Paragraph>
                        </div>
                    </Col>
                    <Col xs={24} md={12}>
                        <div style={{
                            padding: 24,
                            background: 'rgba(255,255,255,0.02)',
                            borderRadius: 16,
                            border: '1px solid rgba(255,255,255,0.05)'
                        }}>
                            <div style={{ fontSize: 32, marginBottom: 16 }}>🧠</div>
                            <Title level={5} style={{ color: '#d8b4fe', marginBottom: 8 }}>现代心理科学</Title>
                            <Paragraph style={{ color: '#cbd5e1', fontSize: 14 }}>
                                结合MBTI人格类型、荣格原型现代理论，科学解析性格特质
                            </Paragraph>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
    )
}

export default Home
