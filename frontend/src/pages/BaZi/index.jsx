import React, { useState } from 'react'
import {
    Card, Form, DatePicker, Select, Button, Row, Col, Spin, Tabs,
    Statistic, Tag, Descriptions, Progress, Divider, Typography
} from 'antd'
import { CompassOutlined, FireOutlined } from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import dayjs from 'dayjs'
import BaZiChart from '../../components/BaZiChart'
import api from '../../services/api'

const { Title, Paragraph, Text } = Typography
const { Option } = Select

// 五行颜色映射
const WUXING_COLORS = {
    '木': '#228B22',
    '火': '#DC143C',
    '土': '#DAA520',
    '金': '#C0C0C0',
    '水': '#1E90FF'
}

function BaZi() {
    const [form] = Form.useForm()
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)

    const handleSubmit = async (values) => {
        setLoading(true)
        try {
            const date = values.datetime
            const response = await api.post('/api/bazi/analyze', {
                year: date.year(),
                month: date.month() + 1,
                day: date.date(),
                hour: date.hour(),
                gender: values.gender
            })

            if (response.data.success) {
                setResult(response.data.data)
            }
        } catch (error) {
            console.error('分析失败:', error)
            // 使用模拟数据进行演示
            setResult(getMockData())
        } finally {
            setLoading(false)
        }
    }

    // 五行雷达图配置
    const getWuxingRadarOption = () => {
        if (!result) return {}

        const percentages = result.wuxing.percentages
        return {
            backgroundColor: 'transparent',
            radar: {
                indicator: [
                    { name: '木', max: 50 },
                    { name: '火', max: 50 },
                    { name: '土', max: 50 },
                    { name: '金', max: 50 },
                    { name: '水', max: 50 }
                ],
                shape: 'polygon',
                splitNumber: 5,
                axisName: {
                    color: '#DAA520'
                },
                splitLine: {
                    lineStyle: { color: 'rgba(218, 165, 32, 0.3)' }
                },
                splitArea: {
                    areaStyle: { color: ['rgba(30, 30, 50, 0.5)'] }
                },
                axisLine: {
                    lineStyle: { color: 'rgba(218, 165, 32, 0.5)' }
                }
            },
            series: [{
                type: 'radar',
                data: [{
                    value: [
                        percentages['木'],
                        percentages['火'],
                        percentages['土'],
                        percentages['金'],
                        percentages['水']
                    ],
                    name: '五行分布',
                    areaStyle: {
                        color: 'rgba(218, 165, 32, 0.3)'
                    },
                    lineStyle: {
                        color: '#DAA520'
                    },
                    itemStyle: {
                        color: '#DAA520'
                    }
                }]
            }]
        }
    }

    // 五行饼图配置
    const getWuxingPieOption = () => {
        if (!result) return {}

        const scores = result.wuxing.scores
        return {
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            series: [{
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: true,
                    formatter: '{b}\n{d}%',
                    color: '#f5f5f5'
                },
                data: Object.entries(scores).map(([name, value]) => ({
                    name,
                    value: value.toFixed(2),
                    itemStyle: { color: WUXING_COLORS[name] }
                }))
            }]
        }
    }

    const tabItems = [
        {
            key: 'basic',
            label: '基本信息',
            children: result && (
                <Row gutter={[24, 24]}>
                    <Col span={24}>
                        <BaZiChart sizhu={result.basic_info.sizhu} />
                    </Col>
                    <Col xs={24} md={12}>
                        <Descriptions column={1} bordered size="small">
                            <Descriptions.Item label="出生时间">
                                {result.basic_info.birth_datetime}
                            </Descriptions.Item>
                            <Descriptions.Item label="性别">
                                {result.basic_info.gender}
                            </Descriptions.Item>
                            <Descriptions.Item label="生肖">
                                {result.basic_info.shengxiao}
                            </Descriptions.Item>
                            <Descriptions.Item label="日主">
                                <Text strong style={{ color: WUXING_COLORS[result.basic_info.day_master_wuxing] }}>
                                    {result.basic_info.day_master}（{result.basic_info.day_master_wuxing}）
                                </Text>
                            </Descriptions.Item>
                        </Descriptions>
                    </Col>
                    <Col xs={24} md={12}>
                        <Card size="small" title="日主强弱">
                            <Statistic
                                title={result.day_master_analysis.strength_level}
                                value={`${(result.day_master_analysis.strength_ratio * 100).toFixed(1)}%`}
                                prefix={<FireOutlined style={{ color: '#DAA520' }} />}
                            />
                            <Paragraph style={{ marginTop: 12, color: '#b0b0b0' }}>
                                {result.day_master_analysis.description}
                            </Paragraph>
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'wuxing',
            label: '五行分析',
            children: result && (
                <Row gutter={[24, 24]}>
                    <Col xs={24} md={12}>
                        <Card size="small" title="五行雷达图">
                            <ReactECharts option={getWuxingRadarOption()} style={{ height: 300 }} />
                        </Card>
                    </Col>
                    <Col xs={24} md={12}>
                        <Card size="small" title="五行分布">
                            <ReactECharts option={getWuxingPieOption()} style={{ height: 300 }} />
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="五行平衡分析">
                            <Row gutter={[16, 16]}>
                                {Object.entries(result.wuxing.balance).map(([wx, status]) => (
                                    <Col key={wx} xs={12} sm={8} md={4}>
                                        <div style={{ textAlign: 'center' }}>
                                            <div style={{
                                                fontSize: 28,
                                                color: WUXING_COLORS[wx],
                                                marginBottom: 8
                                            }}>
                                                {wx}
                                            </div>
                                            <Tag color={
                                                status === '过旺' ? 'red' :
                                                    status === '偏旺' ? 'orange' :
                                                        status === '平衡' ? 'green' :
                                                            status === '偏弱' ? 'blue' : 'purple'
                                            }>
                                                {status}
                                            </Tag>
                                        </div>
                                    </Col>
                                ))}
                            </Row>
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="喜用神分析">
                            <Row gutter={[16, 16]}>
                                <Col xs={12} md={6}>
                                    <Statistic
                                        title="用神"
                                        value={result.xi_yong_shen.yong_shen?.join('、') || '-'}
                                        valueStyle={{ color: '#DAA520' }}
                                    />
                                </Col>
                                <Col xs={12} md={6}>
                                    <Statistic
                                        title="喜神"
                                        value={result.xi_yong_shen.xi_shen?.join('、') || '-'}
                                        valueStyle={{ color: '#2E8B57' }}
                                    />
                                </Col>
                                <Col xs={12} md={6}>
                                    <Statistic
                                        title="忌神"
                                        value={result.xi_yong_shen.ji_shen?.join('、') || '-'}
                                        valueStyle={{ color: '#DC143C' }}
                                    />
                                </Col>
                                <Col xs={12} md={6}>
                                    <Statistic
                                        title="仇神"
                                        value={result.xi_yong_shen.chou_shen?.join('、') || '-'}
                                        valueStyle={{ color: '#666' }}
                                    />
                                </Col>
                            </Row>
                            <Divider />
                            <Paragraph>{result.xi_yong_shen.analysis}</Paragraph>
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'shishen',
            label: '十神格局',
            children: result && (
                <Row gutter={[24, 24]}>
                    <Col span={24}>
                        <Card size="small" title="格局判断">
                            <Title level={4} style={{ color: '#DAA520' }}>
                                {result.geju.main_geju}
                            </Title>
                            <Paragraph>{result.geju.description}</Paragraph>
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="性格特征">
                            {result.personality.keywords && (
                                <div style={{ marginBottom: 16 }}>
                                    {result.personality.keywords.map(kw => (
                                        <Tag key={kw} color="gold" style={{ marginBottom: 8 }}>{kw}</Tag>
                                    ))}
                                </div>
                            )}
                            <Paragraph>{result.personality.summary}</Paragraph>
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'dayun',
            label: '大运流年',
            children: result && result.dayun_liunian && (
                <Row gutter={[24, 24]}>
                    <Col span={24}>
                        <Card size="small" title={`大运（当前${result.dayun_liunian.current_age}岁）`}>
                            <div style={{ display: 'flex', gap: 12, overflowX: 'auto', padding: '8px 0' }}>
                                {result.dayun_liunian.dayun_list?.map(dy => (
                                    <div
                                        key={dy.order}
                                        style={{
                                            minWidth: 100,
                                            padding: 16,
                                            textAlign: 'center',
                                            background: dy.is_current ? 'rgba(218, 165, 32, 0.2)' : 'rgba(30, 30, 50, 0.8)',
                                            border: dy.is_current ? '2px solid #DAA520' : '1px solid rgba(218, 165, 32, 0.3)',
                                            borderRadius: 8
                                        }}
                                    >
                                        <div style={{ fontSize: 12, color: '#888' }}>{dy.range}</div>
                                        <div style={{ fontSize: 20, fontWeight: 'bold', margin: '8px 0' }}>
                                            {dy.ganzhi}
                                        </div>
                                        <div style={{ fontSize: 12 }}>{dy.shishen}</div>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="流年运势">
                            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                                {result.dayun_liunian.liunian_list?.map(ln => (
                                    <Tag
                                        key={ln.year}
                                        color={
                                            ln.rating === '大吉' ? 'gold' :
                                                ln.rating === '吉' ? 'green' :
                                                    ln.rating === '平' ? 'default' :
                                                        ln.rating === '凶' ? 'orange' : 'red'
                                        }
                                        style={{
                                            padding: '4px 12px',
                                            border: ln.is_current ? '2px solid #DAA520' : undefined
                                        }}
                                    >
                                        {ln.year}年 {ln.ganzhi} [{ln.rating}]
                                    </Tag>
                                ))}
                            </div>
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'shensha',
            label: '神煞',
            children: result && (
                <Row gutter={[24, 24]}>
                    <Col xs={24} md={8}>
                        <Card size="small" title="吉神" style={{ borderColor: '#2E8B57' }}>
                            {result.shensha.ji_shensha?.map(s => (
                                <Tag key={s.name} color="green" style={{ marginBottom: 8 }}>
                                    {s.name}（{s.position}）
                                </Tag>
                            ))}
                        </Card>
                    </Col>
                    <Col xs={24} md={8}>
                        <Card size="small" title="凶煞" style={{ borderColor: '#DC143C' }}>
                            {result.shensha.xiong_shensha?.map(s => (
                                <Tag key={s.name} color="red" style={{ marginBottom: 8 }}>
                                    {s.name}（{s.position}）
                                </Tag>
                            ))}
                        </Card>
                    </Col>
                    <Col xs={24} md={8}>
                        <Card size="small" title="中性神煞">
                            {result.shensha.zhong_shensha?.map(s => (
                                <Tag key={s.name} style={{ marginBottom: 8 }}>
                                    {s.name}（{s.position}）
                                </Tag>
                            ))}
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="神煞总结">
                            <Paragraph>{result.shensha.summary}</Paragraph>
                        </Card>
                    </Col>
                </Row>
            )
        }
    ]

    return (
        <div>
            <Card
                title={<><CompassOutlined /> 八字命理分析</>}
                style={{ marginBottom: 24 }}
            >
                <Form
                    form={form}
                    layout="inline"
                    onFinish={handleSubmit}
                    initialValues={{
                        gender: '男'
                    }}
                >
                    <Form.Item
                        name="datetime"
                        label="出生时间"
                        rules={[{ required: true, message: '请选择出生时间' }]}
                    >
                        <DatePicker
                            showTime={{ format: 'HH:mm' }}
                            format="YYYY-MM-DD HH:mm"
                            placeholder="选择出生日期时间"
                            style={{ width: 200 }}
                        />
                    </Form.Item>
                    <Form.Item name="gender" label="性别">
                        <Select style={{ width: 80 }}>
                            <Option value="男">男</Option>
                            <Option value="女">女</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" loading={loading}>
                            开始分析
                        </Button>
                    </Form.Item>
                </Form>
            </Card>

            {loading && (
                <div style={{ textAlign: 'center', padding: 60 }}>
                    <Spin size="large" tip="正在分析八字..." />
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
        basic_info: {
            birth_datetime: "1990年5月15日 10时",
            gender: "男",
            shengxiao: "马",
            bazi: "庚午 辛巳 甲子 己巳",
            sizhu: {
                year: "庚午",
                month: "辛巳",
                day: "甲子",
                hour: "己巳"
            },
            day_master: "甲",
            day_master_wuxing: "木"
        },
        wuxing: {
            scores: { "木": 2.4, "火": 3.6, "土": 2.1, "金": 4.2, "水": 1.8 },
            percentages: { "木": 17, "火": 26, "土": 15, "金": 30, "水": 12 },
            balance: { "木": "偏弱", "火": "偏旺", "土": "平衡", "金": "过旺", "水": "偏弱" }
        },
        day_master_analysis: {
            strength_level: "身弱",
            strength_ratio: 0.38,
            description: "日主甲木力量不足，需要水木生扶"
        },
        xi_yong_shen: {
            yong_shen: ["水"],
            xi_shen: ["木"],
            ji_shen: ["火", "土"],
            chou_shen: ["金"],
            analysis: "八字身弱，需要生扶。用神为水，喜神为木。宜接近用神属性的人事物，增强自身能量。"
        },
        geju: {
            main_geju: "七杀格",
            description: "七杀格者，有魄力胆识，敢于担当，适合军警或企业管理。"
        },
        personality: {
            keywords: ["权威", "果断", "进取", "压力"],
            summary: "您的八字以七杀为主导，属于官杀旺的格局，有责任感，事业心强。"
        },
        dayun_liunian: {
            current_age: 35,
            dayun_list: [
                { order: 1, range: "3-12岁", ganzhi: "壬午", shishen: "偏印/正官", is_current: false },
                { order: 2, range: "13-22岁", ganzhi: "癸未", shishen: "正印/七杀", is_current: false },
                { order: 3, range: "23-32岁", ganzhi: "甲申", shishen: "比肩/七杀", is_current: false },
                { order: 4, range: "33-42岁", ganzhi: "乙酉", shishen: "劫财/正官", is_current: true },
                { order: 5, range: "43-52岁", ganzhi: "丙戌", shishen: "食神/偏财", is_current: false }
            ],
            liunian_list: [
                { year: 2024, ganzhi: "甲辰", rating: "平", is_current: false },
                { year: 2025, ganzhi: "乙巳", rating: "凶", is_current: false },
                { year: 2026, ganzhi: "丙午", rating: "吉", is_current: true },
                { year: 2027, ganzhi: "丁未", rating: "平", is_current: false },
                { year: 2028, ganzhi: "戊申", rating: "大吉", is_current: false }
            ]
        },
        shensha: {
            ji_shensha: [
                { name: "天乙贵人", position: "月支" },
                { name: "文昌贵人", position: "时支" }
            ],
            xiong_shensha: [
                { name: "羊刃", position: "年支" }
            ],
            zhong_shensha: [
                { name: "驿马", position: "日支" },
                { name: "桃花", position: "时支" }
            ],
            summary: "八字带有2个吉神，主一生多贵人相助。同时带有1个凶煞，需注意意外。"
        }
    }
}

export default BaZi
