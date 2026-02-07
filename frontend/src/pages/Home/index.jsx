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
import { useTheme } from '../../stores'

const { Title, Paragraph } = Typography

const features = [
    {
        key: 'bazi',
        path: '/bazi',
        icon: <CompassOutlined style={{ fontSize: 28 }} />,
        title: '八字命理',
        subtitle: 'BaZi Analysis',
        description: '四柱排盘・五行生克・大运流年',
        color: '#fbbf24',
        lightColor: '#d97706'
    },
    {
        key: 'ziwei',
        path: '/ziwei',
        icon: <StarOutlined style={{ fontSize: 28 }} />,
        title: '紫微斗数',
        subtitle: 'Zi Wei Dou Shu',
        description: '十二宫位・星曜布局・命运轨迹',
        color: '#f472b6',
        lightColor: '#db2777'
    },
    {
        key: 'yijing',
        path: '/yijing',
        icon: <BookOutlined style={{ fontSize: 28 }} />,
        title: '易经占卜',
        subtitle: 'I Ching Oracle',
        description: '六爻卦象・变卦推演・AI智解',
        color: '#34d399',
        lightColor: '#059669'
    },
    {
        key: 'psychology',
        path: '/psychology',
        icon: <ExperimentOutlined style={{ fontSize: 28 }} />,
        title: '心理测评',
        subtitle: 'Psychology Test',
        description: 'MBTI人格・大五量表・荣格原型',
        color: '#60a5fa',
        lightColor: '#2563eb'
    }
]

function Home() {
    const navigate = useNavigate()
    const { isDark } = useTheme()

    return (
        <div className="home-page animate-fadeIn" style={{ paddingBottom: 60 }}>
            {/* Hero Section - 简洁大气 */}
            <div style={{
                textAlign: 'center',
                padding: '60px 20px 80px',
                position: 'relative'
            }}>
                {/* 背景装饰 */}
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '500px',
                    height: '500px',
                    background: `radial-gradient(circle, ${isDark ? 'rgba(139, 92, 246, 0.12)' : 'rgba(99, 102, 241, 0.08)'} 0%, transparent 70%)`,
                    zIndex: 0,
                    pointerEvents: 'none'
                }} />

                {/* Logo */}
                <div style={{
                    fontSize: 64,
                    marginBottom: 20,
                    filter: `drop-shadow(0 0 30px ${isDark ? 'rgba(139, 92, 246, 0.4)' : 'rgba(99, 102, 241, 0.3)'})`
                }}>
                    ☯
                </div>

                {/* 标题 */}
                <Title style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: 48,
                    fontWeight: 700,
                    color: 'var(--text-primary)',
                    marginBottom: 16,
                    letterSpacing: 6,
                    position: 'relative'
                }}>
                    玄心理命
                </Title>

                {/* 副标题 */}
                <Paragraph style={{
                    fontSize: 18,
                    color: 'var(--text-muted)',
                    maxWidth: 400,
                    margin: '0 auto 32px',
                    lineHeight: 1.8,
                    position: 'relative'
                }}>
                    东方玄学 × 现代心理
                    <br />
                    <span style={{
                        color: 'var(--primary)',
                        fontWeight: 500
                    }}>
                        探索内心・洞见未来
                    </span>
                </Paragraph>

                <Button
                    type="primary"
                    size="large"
                    style={{
                        height: 48,
                        padding: '0 36px',
                        fontSize: 16,
                        borderRadius: 'var(--radius-full)'
                    }}
                    onClick={() => navigate('/bazi')}
                >
                    开始探索 <RightOutlined />
                </Button>
            </div>

            {/* 功能卡片 - Bento Grid */}
            <div style={{
                maxWidth: 900,
                margin: '0 auto',
                padding: '0 20px',
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: 20
            }}>
                {features.map((feature) => (
                    <div
                        key={feature.key}
                        className="feature-card"
                        style={{
                            background: 'var(--bg-card)',
                            backdropFilter: 'blur(16px)'
                        }}
                        onClick={() => navigate(feature.path)}
                    >
                        {/* 图标 */}
                        <div style={{
                            color: isDark ? feature.color : feature.lightColor,
                            background: `${isDark ? feature.color : feature.lightColor}15`,
                            width: 56,
                            height: 56,
                            borderRadius: 16,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            marginBottom: 20
                        }}>
                            {feature.icon}
                        </div>

                        {/* 标题 */}
                        <Title level={4} style={{
                            color: 'var(--text-primary)',
                            marginBottom: 4,
                            fontSize: 20,
                            fontWeight: 600
                        }}>
                            {feature.title}
                        </Title>

                        {/* 英文副标题 */}
                        <div style={{
                            fontSize: 12,
                            color: 'var(--text-muted)',
                            letterSpacing: 1,
                            marginBottom: 12,
                            textTransform: 'uppercase'
                        }}>
                            {feature.subtitle}
                        </div>

                        {/* 描述 */}
                        <Paragraph style={{
                            color: 'var(--text-secondary)',
                            marginBottom: 0,
                            fontSize: 14
                        }}>
                            {feature.description}
                        </Paragraph>

                        {/* 箭头 */}
                        <div style={{
                            position: 'absolute',
                            top: 24,
                            right: 24,
                            color: 'var(--text-muted)',
                            opacity: 0.5
                        }}>
                            <RightOutlined />
                        </div>

                        {/* 装饰光晕 */}
                        <div style={{
                            position: 'absolute',
                            bottom: -30,
                            right: -30,
                            width: 100,
                            height: 100,
                            background: isDark ? feature.color : feature.lightColor,
                            opacity: 0.08,
                            borderRadius: '50%',
                            filter: 'blur(30px)'
                        }} />
                    </div>
                ))}
            </div>

            {/* 底部说明 */}
            <div style={{
                maxWidth: 700,
                margin: '80px auto 0',
                textAlign: 'center',
                padding: '0 20px'
            }}>
                <Row gutter={[32, 24]}>
                    <Col xs={24} md={12}>
                        <div style={{
                            padding: 24,
                            background: 'var(--bg-card)',
                            borderRadius: 'var(--radius-lg)',
                            border: '1px solid var(--border-default)'
                        }}>
                            <div style={{ fontSize: 28, marginBottom: 12 }}>🔮</div>
                            <Title level={5} style={{
                                color: isDark ? '#fda4af' : '#b45309',
                                marginBottom: 8
                            }}>
                                东方玄学
                            </Title>
                            <Paragraph style={{
                                color: 'var(--text-secondary)',
                                fontSize: 13,
                                marginBottom: 0
                            }}>
                                汲取八字、紫微、易经千年智慧精髓
                            </Paragraph>
                        </div>
                    </Col>
                    <Col xs={24} md={12}>
                        <div style={{
                            padding: 24,
                            background: 'var(--bg-card)',
                            borderRadius: 'var(--radius-lg)',
                            border: '1px solid var(--border-default)'
                        }}>
                            <div style={{ fontSize: 28, marginBottom: 12 }}>🧠</div>
                            <Title level={5} style={{
                                color: isDark ? '#d8b4fe' : '#0d9488',
                                marginBottom: 8
                            }}>
                                现代心理
                            </Title>
                            <Paragraph style={{
                                color: 'var(--text-secondary)',
                                fontSize: 13,
                                marginBottom: 0
                            }}>
                                融合MBTI、荣格原型等科学理论
                            </Paragraph>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
    )
}

export default Home

