import React, { useState } from 'react'
import {
    Card, Form, InputNumber, Button, Row, Col, Spin, Tabs,
    Tag, Descriptions, Typography, Select, Space, Alert, message, Divider
} from 'antd'
import { StarOutlined } from '@ant-design/icons'
import ZiWeiChart from '../../components/ZiWeiChart'
import api from '../../services/api'

const { Title, Paragraph } = Typography
const { Option } = Select

const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

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
            const response = await api.post('/api/ziwei/analyze', {
                year_gan: values.year_gan,
                year_zhi: values.year_zhi,
                lunar_month: values.lunar_month,
                lunar_day: values.lunar_day,
                birth_hour_zhi: values.birth_hour_zhi
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

    const tabItems = [
        {
            key: 'chart',
            label: '命盘',
            children: result && (
                <div>
                    <Row gutter={[24, 24]} style={{ marginBottom: 24 }}>
                        <Col xs={24} md={8}>
                            <Descriptions column={1} bordered size="small">
                                <Descriptions.Item label="命宫">
                                    {result.chart_data.ming_gong}宫
                                </Descriptions.Item>
                                <Descriptions.Item label="身宫">
                                    {result.chart_data.shen_gong}宫
                                </Descriptions.Item>
                                <Descriptions.Item label="五行局">
                                    {result.chart_data.wuxing_ju}
                                </Descriptions.Item>
                            </Descriptions>
                        </Col>
                        <Col xs={24} md={16}>
                            <Card size="small" title="格局">
                                <Title level={4} style={{ color: '#DAA520', margin: 0 }}>
                                    {result.analysis.pattern.name}
                                </Title>
                                <Paragraph style={{ marginTop: 8, marginBottom: 0, color: '#b0b0b0' }}>
                                    {result.analysis.pattern.description}
                                </Paragraph>
                            </Card>
                        </Col>
                    </Row>
                    <ZiWeiChart palaces={result.chart_data.palaces} />
                </div>
            )
        },
        {
            key: 'analysis',
            label: '详细分析',
            children: result && (
                <Row gutter={[24, 24]}>
                    <Col xs={24} md={12}>
                        <Card size="small" title="命宫分析" style={{ height: '100%' }}>
                            {result.analysis.ming_analysis.main_star ? (
                                <>
                                    <Title level={4} style={{ color: '#DC143C' }}>
                                        {result.analysis.ming_analysis.main_star}
                                    </Title>
                                    <div style={{ marginBottom: 12 }}>
                                        {result.analysis.ming_analysis.keywords?.map(kw => (
                                            <Tag key={kw} color="gold">{kw}</Tag>
                                        ))}
                                    </div>
                                    <Paragraph style={{ color: '#b0b0b0' }}>
                                        {result.analysis.ming_analysis.description}
                                    </Paragraph>
                                </>
                            ) : (
                                <Paragraph style={{ color: '#888' }}>
                                    命宫无主星，需看对宫借星
                                </Paragraph>
                            )}
                        </Card>
                    </Col>
                    <Col xs={24} md={12}>
                        <Card size="small" title="事业分析" style={{ height: '100%' }}>
                            {result.analysis.career_analysis.main_star ? (
                                <>
                                    <Title level={4} style={{ color: '#2E8B57' }}>
                                        {result.analysis.career_analysis.main_star}
                                    </Title>
                                    <Paragraph style={{ color: '#b0b0b0' }}>
                                        {result.analysis.career_analysis.career_hint}
                                    </Paragraph>
                                </>
                            ) : (
                                <Paragraph style={{ color: '#888' }}>
                                    官禄宫无主星
                                </Paragraph>
                            )}
                        </Card>
                    </Col>
                    <Col xs={24} md={12}>
                        <Card size="small" title="财运分析" style={{ height: '100%' }}>
                            {result.analysis.wealth_analysis.main_star ? (
                                <>
                                    <Title level={4} style={{ color: '#DAA520' }}>
                                        {result.analysis.wealth_analysis.main_star}
                                    </Title>
                                    <Paragraph style={{ color: '#b0b0b0' }}>
                                        {result.analysis.wealth_analysis.description}
                                    </Paragraph>
                                </>
                            ) : (
                                <Paragraph style={{ color: '#888' }}>
                                    财帛宫无主星
                                </Paragraph>
                            )}
                        </Card>
                    </Col>
                    <Col xs={24} md={12}>
                        <Card size="small" title="感情分析" style={{ height: '100%' }}>
                            {result.analysis.marriage_analysis.main_star ? (
                                <>
                                    <Title level={4} style={{ color: '#DC143C' }}>
                                        {result.analysis.marriage_analysis.main_star}
                                    </Title>
                                    <Paragraph style={{ color: '#b0b0b0' }}>
                                        {result.analysis.marriage_analysis.description}
                                    </Paragraph>
                                </>
                            ) : (
                                <Paragraph style={{ color: '#888' }}>
                                    夫妻宫无主星
                                </Paragraph>
                            )}
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'palaces',
            label: '十二宫详情',
            children: result && (
                <Row gutter={[16, 16]}>
                    {result.analysis.palaces_detail?.map(palace => (
                        <Col xs={24} sm={12} md={8} lg={6} key={palace.name}>
                            <Card
                                size="small"
                                title={palace.name}
                                extra={<span style={{ color: '#888' }}>{palace.position}</span>}
                            >
                                <div>
                                    <strong style={{ color: '#DC143C' }}>主星：</strong>
                                    {palace.main_stars?.join('、') || '无'}
                                </div>
                                <div style={{ marginTop: 4 }}>
                                    <strong style={{ color: '#2E8B57' }}>吉星：</strong>
                                    {palace.aux_stars?.join('、') || '无'}
                                </div>
                                <div style={{ marginTop: 4 }}>
                                    <strong style={{ color: '#888' }}>煞星：</strong>
                                    {palace.sha_stars?.join('、') || '无'}
                                </div>
                            </Card>
                        </Col>
                    ))}
                </Row>
            )
        }
    ]

    return (
        <div>
            <Card
                title={<><StarOutlined /> 紫微斗数排盘</>}
                style={{ marginBottom: 24 }}
            >
                <Alert
                    message="请输入农历生日信息"
                    type="info"
                    showIcon
                    style={{ marginBottom: 16 }}
                />
                <Form
                    form={form}
                    layout="inline"
                    onFinish={handleSubmit}
                >
                    <Space wrap>
                        <Form.Item name="year_gan" label="年干" rules={[{ required: true }]}>
                            <Select style={{ width: 80 }}>
                                {TIAN_GAN.map(g => <Option key={g} value={g}>{g}</Option>)}
                            </Select>
                        </Form.Item>
                        <Form.Item name="year_zhi" label="年支" rules={[{ required: true }]}>
                            <Select style={{ width: 80 }}>
                                {DI_ZHI.map(z => <Option key={z} value={z}>{z}</Option>)}
                            </Select>
                        </Form.Item>
                        <Form.Item name="lunar_month" label="农历月" rules={[{ required: true }]}>
                            <InputNumber min={1} max={12} />
                        </Form.Item>
                        <Form.Item name="lunar_day" label="农历日" rules={[{ required: true }]}>
                            <InputNumber min={1} max={30} />
                        </Form.Item>
                        <Form.Item name="birth_hour_zhi" label="时辰" rules={[{ required: true }]}>
                            <Select style={{ width: 80 }}>
                                {DI_ZHI.map(z => <Option key={z} value={z}>{z}时</Option>)}
                            </Select>
                        </Form.Item>
                        <Form.Item>
                            <Button type="primary" htmlType="submit" loading={loading}>
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
                <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
                    {tabItems.map(item => (
                        <div key={item.key} id={`section-${item.key}`}>
                            <Divider orientation="left" style={{
                                fontSize: 18,
                                color: '#DAA520',
                                borderColor: 'rgba(218, 165, 32, 0.3)',
                                margin: '0 0 24px 0'
                            }}>
                                {item.label}
                            </Divider>
                            {item.children}
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default ZiWei
