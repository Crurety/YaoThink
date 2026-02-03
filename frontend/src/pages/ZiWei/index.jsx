import React, { useState } from 'react'
import {
    Card, Form, InputNumber, Button, Row, Col, Spin, Tabs, DatePicker,
    Tag, Descriptions, Typography, Select, Space, Alert, message, Divider
} from 'antd'
import { StarOutlined } from '@ant-design/icons'
import ZiWeiChart from '../../components/ZiWeiChart'
import api from '../../services/api'

const { Title, Paragraph, Text } = Typography
const { Option } = Select

const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

const renderContent = (content) => {
    if (content && typeof content === 'object' && content.content) {
        return content.content
    }
    return content
}

function ZiWei() {
    const [form] = Form.useForm()
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleSubmit = async (values) => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const date = values.datetime
            // 调用公历分析接口
            const response = await api.post('/ziwei/analyze_solar', {
                year: date.year(),
                month: date.month() + 1,
                day: date.date(),
                hour: date.hour()
            })

            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '排盘失败')
                message.error(response.data.error || '排盘失败')
            }
        } catch (err) {
            console.error('分析失败:', err)
            const errorMsg = err.response?.data?.error || err.message || '服务器连接失败，请稍后重试'
            setError(errorMsg)
            message.error(errorMsg)
        } finally {
            setLoading(false)
        }
    }

    // tabItems has been replaced by ziwei-dashboard layout

    return (
        <div>
            <Card
                title={<><StarOutlined /> 紫微斗数排盘</>}
                style={{ marginBottom: 24 }}
            >
                <Alert
                    message="请输入出生时间（公历/阳历）"
                    type="info"
                    showIcon
                    style={{ marginBottom: 16 }}
                />
                <Form
                    form={form}
                    layout="inline"
                    onFinish={handleSubmit}
                    initialValues={{
                        hour: 12
                    }}
                >
                    <Space wrap>
                        <Form.Item
                            name="datetime"
                            label="出生时间"
                            rules={[{ required: true, message: '请选择出生日期' }]}
                        >
                            <DatePicker
                                showTime={{ format: 'HH' }}
                                format="YYYY-MM-DD HH:00"
                                placeholder="选择公历时间"
                                style={{ width: 220 }}
                            />
                        </Form.Item>

                        <Form.Item>
                            <Button type="primary" htmlType="submit" loading={loading} icon={<StarOutlined />}>
                                排盘分析
                            </Button>
                        </Form.Item>
                    </Space>
                </Form>
            </Card>

            {loading && (
                <div style={{ textAlign: 'center', padding: 60 }}>
                    <Spin size="large" tip="正在排盘..." />
                </div>
            )}

            {result && !loading && (
                <div className="ziwei-dashboard" style={{ marginTop: 24 }}>
                    {/* 第一行：命盘 + 核心参数 */}
                    <Row gutter={[24, 24]}>
                        <Col xs={24} lg={16}>
                            <Card title="紫微斗数命盘" className="feature-card" style={{ height: '100%' }}>
                                <ZiWeiChart palaces={result.chart_data.palaces} centerInfo={result.chart_data.wuxing_ju} />
                            </Card>
                        </Col>
                        <Col xs={24} lg={8}>
                            <Card title="命格概览" className="feature-card" style={{ height: '100%' }}>
                                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                                    <div style={{ fontSize: 40, fontWeight: 'bold', color: '#a78bfa', fontFamily: 'var(--font-display)' }}>
                                        {result.chart_data.wuxing_ju}
                                    </div>
                                    <Tag color="purple">五行局</Tag>
                                </div>
                                <Divider />
                                <Descriptions column={1} bordered size="small" style={{ marginTop: 16 }}>
                                    <Descriptions.Item label="命宫" labelStyle={{ width: 80 }}>
                                        <Text strong style={{ color: '#fbbf24' }}>{result.chart_data.ming_gong}宫</Text>
                                    </Descriptions.Item>
                                    <Descriptions.Item label="身宫">
                                        <Text strong style={{ color: '#34d399' }}>{result.chart_data.shen_gong}宫</Text>
                                    </Descriptions.Item>
                                    <Descriptions.Item label="格局">
                                        <Text strong style={{ color: '#f472b6' }}>{result.analysis.pattern.name}</Text>
                                    </Descriptions.Item>
                                </Descriptions>
                                <div style={{ marginTop: 16, background: 'rgba(255,255,255,0.05)', padding: 12, borderRadius: 8 }}>
                                    <Paragraph style={{ fontSize: 13, color: '#e2e8f0', margin: 0 }}>
                                        {renderContent(result.analysis.pattern.description)}
                                    </Paragraph>
                                </div>
                            </Card>
                        </Col>
                    </Row>

                    {/* 第二行：四大运势 (2x2 Grid) */}
                    <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                        <Col xs={24} md={12}>
                            <Card title={<><StarOutlined /> 命宫·核心</>} className="feature-card" style={{ height: '100%' }}>
                                <div style={{ minHeight: 120 }}>
                                    {result.analysis.ming_analysis.main_star ? (
                                        <>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                                                <Title level={4} style={{ color: '#a78bfa', margin: 0 }}>
                                                    {result.analysis.ming_analysis.main_star}
                                                </Title>
                                                <div>
                                                    {result.analysis.ming_analysis.keywords?.map(kw => (
                                                        <Tag key={kw} color="geekblue">{kw}</Tag>
                                                    ))}
                                                </div>
                                            </div>
                                            <Paragraph style={{ color: '#cbd5e1' }}>
                                                {renderContent(result.analysis.ming_analysis.description)}
                                            </Paragraph>
                                            {result.extra_info?.ai_analysis_structured?.core && (
                                                <div style={{ marginTop: 12, padding: 8, background: 'rgba(167, 139, 250, 0.1)', borderRadius: 8, border: '1px solid rgba(167, 139, 250, 0.2)' }}>
                                                    <Tag color="purple" style={{ marginBottom: 4 }}>AI 深度透视</Tag>
                                                    <Paragraph style={{ color: '#e2e8f0', fontSize: 13, margin: 0 }}>
                                                        {result.extra_info.ai_analysis_structured.core.join('\n')}
                                                    </Paragraph>
                                                </div>
                                            )}
                                        </>
                                    ) : (
                                        <div style={{ color: '#94a3b8', fontStyle: 'italic', textAlign: 'center', padding: 20 }}>
                                            命宫无主星，借对宫（迁移宫）之星
                                        </div>
                                    )}
                                </div>
                            </Card>
                        </Col>
                        <Col xs={24} md={12}>
                            <Card title={<><span role="img" aria-label="money">💰</span> 财帛·财运</>} className="feature-card" style={{ height: '100%' }}>
                                <div style={{ minHeight: 120 }}>
                                    {result.analysis.wealth_analysis.main_star ? (
                                        <>
                                            <Title level={4} style={{ color: '#fbbf24', marginTop: 0 }}>
                                                {result.analysis.wealth_analysis.main_star}
                                            </Title>
                                            <Paragraph style={{ color: '#cbd5e1' }}>
                                                {renderContent(result.analysis.wealth_analysis.description)}
                                            </Paragraph>
                                            {result.extra_info?.ai_analysis_structured?.wealth && (
                                                <div style={{ marginTop: 12, padding: 8, background: 'rgba(251, 191, 36, 0.1)', borderRadius: 8, border: '1px solid rgba(251, 191, 36, 0.2)' }}>
                                                    <Tag color="gold" style={{ marginBottom: 4 }}>AI 财运洞察</Tag>
                                                    <Paragraph style={{ color: '#e2e8f0', fontSize: 13, margin: 0 }}>
                                                        {result.extra_info.ai_analysis_structured.wealth.join('\n')}
                                                    </Paragraph>
                                                </div>
                                            )}
                                        </>
                                    ) : <div style={{ color: '#666' }}>财帛宫无主星，参考对宫（福德宫）</div>}
                                </div>
                            </Card>
                        </Col>
                        <Col xs={24} md={12}>
                            <Card title={<><span role="img" aria-label="work">💼</span> 官禄·事业</>} className="feature-card" style={{ height: '100%' }}>
                                <div style={{ minHeight: 120 }}>
                                    {result.analysis.career_analysis.main_star ? (
                                        <>
                                            <Title level={4} style={{ color: '#34d399', marginTop: 0 }}>
                                                {result.analysis.career_analysis.main_star}
                                            </Title>
                                            <Paragraph style={{ color: '#cbd5e1' }}>
                                                {renderContent(result.analysis.career_analysis.career_hint)}
                                            </Paragraph>
                                            {result.extra_info?.ai_analysis_structured?.career && (
                                                <div style={{ marginTop: 12, padding: 8, background: 'rgba(52, 211, 153, 0.1)', borderRadius: 8, border: '1px solid rgba(52, 211, 153, 0.2)' }}>
                                                    <Tag color="green" style={{ marginBottom: 4 }}>AI 职场建议</Tag>
                                                    <Paragraph style={{ color: '#e2e8f0', fontSize: 13, margin: 0 }}>
                                                        {result.extra_info.ai_analysis_structured.career.join('\n')}
                                                    </Paragraph>
                                                </div>
                                            )}
                                        </>
                                    ) : <div style={{ color: '#666' }}>官禄宫无主星，参考对宫（夫妻宫）</div>}
                                </div>
                            </Card>
                        </Col>
                        <Col xs={24} md={12}>
                            <Card title={<><span role="img" aria-label="heart">❤️</span> 夫妻·情感</>} className="feature-card" style={{ height: '100%' }}>
                                <div style={{ minHeight: 120 }}>
                                    {result.analysis.marriage_analysis.main_star ? (
                                        <>
                                            <Title level={4} style={{ color: '#f472b6', marginTop: 0 }}>
                                                {result.analysis.marriage_analysis.main_star}
                                            </Title>
                                            <Paragraph style={{ color: '#cbd5e1' }}>
                                                {renderContent(result.analysis.marriage_analysis.description)}
                                            </Paragraph>
                                            {result.extra_info?.ai_analysis_structured?.love && (
                                                <div style={{ marginTop: 12, padding: 8, background: 'rgba(244, 114, 182, 0.1)', borderRadius: 8, border: '1px solid rgba(244, 114, 182, 0.2)' }}>
                                                    <Tag color="magenta" style={{ marginBottom: 4 }}>AI 情感指引</Tag>
                                                    <Paragraph style={{ color: '#e2e8f0', fontSize: 13, margin: 0 }}>
                                                        {result.extra_info.ai_analysis_structured.love.join('\n')}
                                                    </Paragraph>
                                                </div>
                                            )}
                                        </>
                                    ) : <div style={{ color: '#666' }}>夫妻宫无主星，参考对宫（官禄宫）</div>}
                                </div>
                            </Card>
                        </Col>
                    </Row>

                    {/* 第三行：十二宫详情 (Refined Grid) */}
                    <div style={{ marginTop: 24 }}>
                        <Divider orientation="left" style={{ borderColor: 'rgba(255,255,255,0.1)', color: '#94a3b8' }}>十二宫完整星曜</Divider>
                        <Row gutter={[12, 12]}>
                            {result.analysis.palaces_detail?.map(palace => (
                                <Col xs={24} sm={12} md={6} lg={4} key={palace.name}>
                                    <div style={{
                                        background: 'rgba(255,255,255,0.03)',
                                        borderRadius: 12,
                                        padding: 12,
                                        border: '1px solid rgba(255,255,255,0.05)',
                                        height: '100%'
                                    }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                                            <span style={{ fontWeight: 'bold', color: '#e2e8f0' }}>{palace.name}</span>
                                            <span style={{ fontSize: 12, color: '#64748b' }}>{palace.position}</span>
                                        </div>
                                        <div style={{ fontSize: 12 }}>
                                            <div style={{ marginBottom: 4 }}>
                                                <span style={{ color: '#fca5a5' }}>主: </span>
                                                {palace.main_stars?.map(s => <span key={s} style={{ color: '#fca5a5', marginRight: 4 }}>{s}</span>) || '-'}
                                            </div>
                                            <div style={{ marginBottom: 4 }}>
                                                <span style={{ color: '#86efac' }}>吉: </span>
                                                {palace.aux_stars?.map(s => <span key={s} style={{ color: '#86efac', marginRight: 4 }}>{s}</span>) || '-'}
                                            </div>
                                            <div>
                                                <span style={{ color: '#cbd5e1' }}>煞: </span>
                                                {palace.sha_stars?.map(s => <span key={s} style={{ color: '#94a3b8', marginRight: 4 }}>{s}</span>) || '-'}
                                            </div>
                                        </div>
                                    </div>
                                </Col>
                            ))}
                        </Row>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ZiWei
