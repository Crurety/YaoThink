import React, { useState } from 'react'
import {
    Card, Form, InputNumber, Button, Row, Col, Spin, Tabs,
    Tag, Descriptions, Typography, Select, Space, Alert
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

    const handleSubmit = async (values) => {
        setLoading(true)
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
            }
        } catch (error) {
            console.error('分析失败:', error)
            setResult(getMockData())
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
                    initialValues={{
                        year_gan: '庚',
                        year_zhi: '午',
                        lunar_month: 5,
                        lunar_day: 15,
                        birth_hour_zhi: '巳'
                    }}
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
                <Card>
                    <Tabs items={tabItems} />
                </Card>
            )}
        </div>
    )
}

// 模拟数据
function getMockData() {
    return {
        chart_data: {
            wuxing_ju: "火六局",
            ming_gong: "卯",
            shen_gong: "未",
            palaces: [
                { name: "命宫", position: "甲卯", stars: { main: ["紫微", "天相"], auxiliary: ["文昌"], sha: [] } },
                { name: "兄弟宫", position: "乙寅", stars: { main: ["天机"], auxiliary: [], sha: ["火星"] } },
                { name: "夫妻宫", position: "丙丑", stars: { main: ["太阳"], auxiliary: ["左辅"], sha: [] } },
                { name: "子女宫", position: "丁子", stars: { main: ["武曲", "天府"], auxiliary: [], sha: [] } },
                { name: "财帛宫", position: "戊亥", stars: { main: ["天同"], auxiliary: ["右弼"], sha: [] } },
                { name: "疾厄宫", position: "己戌", stars: { main: ["廉贞"], auxiliary: [], sha: ["擎羊"] } },
                { name: "迁移宫", position: "庚酉", stars: { main: ["天府"], auxiliary: [], sha: [] } },
                { name: "仆役宫", position: "辛申", stars: { main: ["太阴"], auxiliary: ["文曲"], sha: [] } },
                { name: "官禄宫", position: "壬未", stars: { main: ["贪狼"], auxiliary: [], sha: ["铃星"] } },
                { name: "田宅宫", position: "癸午", stars: { main: ["巨门"], auxiliary: [], sha: [] } },
                { name: "福德宫", position: "甲巳", stars: { main: ["天梁"], auxiliary: [], sha: [] } },
                { name: "父母宫", position: "乙辰", stars: { main: ["七杀"], auxiliary: [], sha: [] } }
            ]
        },
        analysis: {
            basic_info: {
                ming_gong: "卯宫",
                shen_gong: "未宫",
                wuxing_ju: "火六局"
            },
            ming_analysis: {
                main_star: "紫微",
                description: "领导力强，有气度，受人尊敬，志向远大",
                keywords: ["领导", "尊贵", "权威"],
                career_hint: "适合管理、政治、大企业领导"
            },
            career_analysis: {
                main_star: "贪狼",
                description: "多才多艺，交际能力强，有艺术天赋",
                keywords: ["才艺", "桃花", "多变"],
                career_hint: "适合艺术、娱乐、销售、公关"
            },
            wealth_analysis: {
                main_star: "天同",
                description: "性格温和，有福气，财运稳定",
                keywords: ["福气", "稳定"],
                career_hint: "适合服务、休闲行业"
            },
            marriage_analysis: {
                main_star: "太阳",
                description: "热情开朗，乐于助人，感情丰富",
                keywords: ["热情", "博爱"],
                career_hint: "感情主动热烈"
            },
            pattern: {
                name: "紫府同宫",
                description: "帝王之相，大富大贵，领导才能出众"
            },
            palaces_detail: [
                { name: "命宫", position: "甲卯", main_stars: ["紫微", "天相"], aux_stars: ["文昌"], sha_stars: [] },
                { name: "兄弟宫", position: "乙寅", main_stars: ["天机"], aux_stars: [], sha_stars: ["火星"] },
                { name: "夫妻宫", position: "丙丑", main_stars: ["太阳"], aux_stars: ["左辅"], sha_stars: [] },
                { name: "子女宫", position: "丁子", main_stars: ["武曲", "天府"], aux_stars: [], sha_stars: [] },
                { name: "财帛宫", position: "戊亥", main_stars: ["天同"], aux_stars: ["右弼"], sha_stars: [] },
                { name: "疾厄宫", position: "己戌", main_stars: ["廉贞"], aux_stars: [], sha_stars: ["擎羊"] },
                { name: "迁移宫", position: "庚酉", main_stars: ["天府"], aux_stars: [], sha_stars: [] },
                { name: "仆役宫", position: "辛申", main_stars: ["太阴"], aux_stars: ["文曲"], sha_stars: [] },
                { name: "官禄宫", position: "壬未", main_stars: ["贪狼"], aux_stars: [], sha_stars: ["铃星"] },
                { name: "田宅宫", position: "癸午", main_stars: ["巨门"], aux_stars: [], sha_stars: [] },
                { name: "福德宫", position: "甲巳", main_stars: ["天梁"], aux_stars: [], sha_stars: [] },
                { name: "父母宫", position: "乙辰", main_stars: ["七杀"], aux_stars: [], sha_stars: [] }
            ]
        }
    }
}

export default ZiWei
