import React, { useState } from 'react'
import {
    Card, Form, Input, Button, Row, Col, Spin, Tabs, Radio,
    Tag, Descriptions, Typography, Space, Alert, Divider, message
} from 'antd'
import { BookOutlined, ThunderboltOutlined, NumberOutlined, FontSizeOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title, Paragraph, Text } = Typography
const { TextArea } = Input

function YiJing() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [method, setMethod] = useState('time')

    // 时间起卦
    const handleTimeMethod = async () => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const response = await api.post('/api/yijing/meihua/time', {
                question: ''
            })
            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '起卦失败')
                message.error(response.data.error || '起卦失败')
            }
        } catch (err) {
            console.error('起卦失败:', err)
            const errorMsg = err.response?.data?.error || err.message || '服务器连接失败，请稍后重试'
            setError(errorMsg)
            message.error(errorMsg)
        } finally {
            setLoading(false)
        }
    }

    // 数字起卦
    const handleNumberMethod = async (values) => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const response = await api.post('/api/yijing/meihua/number', {
                number1: values.number1,
                number2: values.number2,
                question: values.question
            })
            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '起卦失败')
                message.error(response.data.error || '起卦失败')
            }
        } catch (err) {
            console.error('起卦失败:', err)
            const errorMsg = err.response?.data?.error || err.message || '服务器连接失败，请稍后重试'
            setError(errorMsg)
            message.error(errorMsg)
        } finally {
            setLoading(false)
        }
    }

    // 文字起卦
    const handleTextMethod = async (values) => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const response = await api.post('/api/yijing/meihua/text', {
                text: values.text,
                question: values.question
            })
            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '起卦失败')
                message.error(response.data.error || '起卦失败')
            }
        } catch (err) {
            console.error('起卦失败:', err)
            const errorMsg = err.response?.data?.error || err.message || '服务器连接失败，请稍后重试'
            setError(errorMsg)
            message.error(errorMsg)
        } finally {
            setLoading(false)
        }
    }

    // 六爻起卦
    const handleLiuyaoMethod = async () => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const response = await api.post('/api/yijing/liuyao', {
                question: ''
            })
            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '摇卦失败')
                message.error(response.data.error || '摇卦失败')
            }
        } catch (err) {
            console.error('摇卦失败:', err)
            const errorMsg = err.response?.data?.error || err.message || '服务器连接失败，请稍后重试'
            setError(errorMsg)
            message.error(errorMsg)
        } finally {
            setLoading(false)
        }
    }

    const methodTabs = [
        {
            key: 'time',
            label: <><ThunderboltOutlined /> 时间起卦</>,
            children: (
                <div style={{ textAlign: 'center', padding: 24 }}>
                    <Paragraph style={{ color: '#b0b0b0', marginBottom: 24 }}>
                        根据当前时间自动起卦，适合即时占问
                    </Paragraph>
                    <Button type="primary" size="large" onClick={handleTimeMethod}>
                        立即起卦
                    </Button>
                </div>
            )
        },
        {
            key: 'number',
            label: <><NumberOutlined /> 数字起卦</>,
            children: (
                <Form layout="vertical" onFinish={handleNumberMethod}>
                    <Row gutter={16}>
                        <Col span={8}>
                            <Form.Item
                                name="number1"
                                label="第一个数字"
                                rules={[{ required: true, message: '请输入数字' }]}
                            >
                                <Input type="number" placeholder="1-999" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item
                                name="number2"
                                label="第二个数字"
                                rules={[{ required: true, message: '请输入数字' }]}
                            >
                                <Input type="number" placeholder="1-999" />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item name="question" label="问题（选填）">
                                <Input placeholder="想问什么？" />
                            </Form.Item>
                        </Col>
                    </Row>
                    <Button type="primary" htmlType="submit">起卦</Button>
                </Form>
            )
        },
        {
            key: 'text',
            label: <><FontSizeOutlined /> 文字起卦</>,
            children: (
                <Form layout="vertical" onFinish={handleTextMethod}>
                    <Form.Item
                        name="text"
                        label="输入任意文字"
                        rules={[{ required: true, message: '请输入文字' }]}
                    >
                        <Input placeholder="输入一句话或几个字" />
                    </Form.Item>
                    <Form.Item name="question" label="问题（选填）">
                        <Input placeholder="想问什么？" />
                    </Form.Item>
                    <Button type="primary" htmlType="submit">起卦</Button>
                </Form>
            )
        },
        {
            key: 'liuyao',
            label: <><BookOutlined /> 六爻摇卦</>,
            children: (
                <div style={{ textAlign: 'center', padding: 24 }}>
                    <Paragraph style={{ color: '#b0b0b0', marginBottom: 24 }}>
                        模拟三枚铜钱摇卦，传统六爻占卜方式
                    </Paragraph>
                    <Button type="primary" size="large" onClick={handleLiuyaoMethod}>
                        开始摇卦
                    </Button>
                </div>
            )
        }
    ]

    return (
        <div>
            <Card
                title={<><BookOutlined /> 易经占卜</>}
                style={{ marginBottom: 24 }}
            >
                <Tabs
                    items={methodTabs}
                    activeKey={method}
                    onChange={setMethod}
                />
            </Card>

            {loading && (
                <div style={{ textAlign: 'center', padding: 60 }}>
                    <Spin size="large" tip="正在起卦..." />
                </div>
            )}

            {result && !loading && (
                <HexagramResult result={result} />
            )}
        </div>
    )
}

function HexagramResult({ result }) {
    const mainGua = result.main_gua
    const changedGua = result.changed_gua
    const fortune = result.overall_fortune

    return (
        <Card>
            <Row gutter={[32, 24]}>
                {/* 主卦展示 */}
                <Col xs={24} md={12}>
                    <div className="hexagram-display">
                        <Title level={3} style={{ color: '#DAA520' }}>本卦</Title>

                        {/* 卦象符号 */}
                        <div style={{ marginBottom: 20 }}>
                            <div style={{ fontSize: 48 }}>
                                {mainGua.upper_symbol}
                            </div>
                            <div style={{ fontSize: 48 }}>
                                {mainGua.lower_symbol}
                            </div>
                        </div>

                        <div className="hexagram-name">{mainGua.name}</div>

                        <div style={{ marginBottom: 16 }}>
                            <Tag color="gold">{mainGua.upper.name}（{mainGua.upper.nature}）</Tag>
                            <Tag>上</Tag>
                            <span style={{ margin: '0 8px' }}>+</span>
                            <Tag color="blue">{mainGua.lower.name}（{mainGua.lower.nature}）</Tag>
                            <Tag>下</Tag>
                        </div>

                        {result.dong_yao && (
                            <Alert
                                message={`第${result.dong_yao}爻为动爻`}
                                description={result.dong_yao_meaning}
                                type="warning"
                                showIcon
                                style={{ textAlign: 'left' }}
                            />
                        )}
                    </div>
                </Col>

                {/* 变卦展示 */}
                {changedGua && (
                    <Col xs={24} md={12}>
                        <div className="hexagram-display">
                            <Title level={3} style={{ color: '#DC143C' }}>变卦</Title>
                            <div className="hexagram-name">{changedGua.name}</div>
                            <Paragraph style={{ color: '#b0b0b0' }}>
                                {changedGua.interpretation?.summary}
                            </Paragraph>
                        </div>
                    </Col>
                )}

                {/* 卦辞解读 */}
                <Col span={24}>
                    <Divider />
                    <Title level={4} style={{ color: '#DAA520' }}>卦辞解读</Title>
                    <Paragraph style={{ fontSize: 16 }}>
                        <Text strong style={{ color: '#DAA520' }}>「{mainGua.interpretation?.summary}」</Text>
                    </Paragraph>

                    <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
                        <Col xs={24} sm={12} md={6}>
                            <Card size="small" title="总体运势">
                                <Tag color={
                                    fortune?.level?.includes('吉') ? 'gold' :
                                        fortune?.level?.includes('凶') ? 'red' : 'default'
                                } style={{ fontSize: 16 }}>
                                    {fortune?.level}
                                </Tag>
                                <Paragraph style={{ marginTop: 8, color: '#b0b0b0', marginBottom: 0 }}>
                                    {fortune?.description}
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6}>
                            <Card size="small" title="事业">
                                <Paragraph style={{ color: '#b0b0b0', marginBottom: 0 }}>
                                    {mainGua.interpretation?.career}
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6}>
                            <Card size="small" title="财运">
                                <Paragraph style={{ color: '#b0b0b0', marginBottom: 0 }}>
                                    {mainGua.interpretation?.wealth}
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} sm={12} md={6}>
                            <Card size="small" title="感情">
                                <Paragraph style={{ color: '#b0b0b0', marginBottom: 0 }}>
                                    {mainGua.interpretation?.relationship}
                                </Paragraph>
                            </Card>
                        </Col>
                    </Row>

                    {mainGua.interpretation?.keywords && (
                        <div style={{ marginTop: 24 }}>
                            <Text strong>关键词：</Text>
                            {mainGua.interpretation.keywords.map(kw => (
                                <Tag key={kw} color="gold" style={{ marginLeft: 8 }}>{kw}</Tag>
                            ))}
                        </div>
                    )}
                </Col>
            </Row>
        </Card>
    )
}

export default YiJing
