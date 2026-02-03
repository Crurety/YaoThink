import React, { useState } from 'react'
import {
    Card, Form, DatePicker, Select, Button, Row, Col, Spin, Tabs,
    Statistic, Tag, Descriptions, Progress, Divider, Typography, message
} from 'antd'
import { CompassOutlined, FireOutlined } from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import dayjs from 'dayjs'
import BaZiChart from '../../components/BaZiChart'
import MarkdownViewer from '../../components/MarkdownViewer'
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
    const [error, setError] = useState(null)
    const [analysisLoading, setAnalysisLoading] = useState(false)
    const [analysisResult, setAnalysisResult] = useState(null)

    const handleBigDataAnalysis = async () => {
        if (!result) return
        setAnalysisLoading(true)
        try {
            // 构建完整的多维度分析数据
            const analysisData = {
                // 基础信息
                day_master: result.basic_info?.day_master,
                day_master_wuxing: result.basic_info?.day_master_wuxing,
                // 月支信息（用于季节分析）
                month: {
                    zhi: result.basic_info?.sizhu?.month?.zhi || result.basic_info?.sizhu?.month?.branch
                },
                // 格局信息
                geju: result.geju?.main_geju,
                // 十神分布（主导十神）
                shishen_profile: {
                    dominant: result.geju?.shishen_prominent || []
                },
                // 五行能量分数
                wuxing_scores: result.wuxing?.scores || {},
                // 当前大运
                current_dayun: (() => {
                    const currentDy = result.dayun_liunian?.dayun_list?.find(d => d.is_current)
                    if (!currentDy) return null
                    // ganzhi 是字符串如 "甲子"
                    const gz = currentDy.ganzhi || ''
                    // 优先取 shishen_gan，如果没有则尝试从 shishen 解析
                    let ganShishen = currentDy.shishen_gan
                    if (!ganShishen && currentDy.shishen) {
                        ganShishen = currentDy.shishen.split('/')[0]
                    }
                    return {
                        gan: gz[0] || null,
                        zhi: gz[1] || null,
                        shishen: ganShishen || null
                    }
                })(),
                // 当前流年
                current_liunian: (() => {
                    const currentLn = result.dayun_liunian?.liunian_list?.find(ln => ln.is_current)
                    if (!currentLn) return null
                    const gz = currentLn.ganzhi || ''
                    // 同理优先取 backend 直接给的（如果有），或者解析
                    // 这里我们假设流年数据结构和 dayun 类似
                    let ganShishen = currentLn.shishen_gan
                    if (!ganShishen && currentLn.shishen) {
                        ganShishen = currentLn.shishen.split('/')[0]
                    }
                    return {
                        year: currentLn.year,
                        gan: gz[0] || null,
                        zhi: gz[1] || null,
                        shishen: ganShishen || null,
                        rating: currentLn.rating
                    }
                })(),
                // 神煞列表
                shensha: [
                    ...(result.shensha?.ji_shensha?.map(s => s.name) || []),
                    ...(result.shensha?.xiong_shensha?.map(s => s.name) || [])
                ]
            }

            const response = await api.post('/analysis/analyze', {
                data: analysisData,
                type: 'bazi'
            })
            if (response.data.success) {
                setAnalysisResult(response.data.data)
                message.success('大数据分析完成')
            }
        } catch (err) {
            message.error('分析失败')
        } finally {
            setAnalysisLoading(false)
        }
    }

    const handleSubmit = async (values) => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const date = values.datetime
            const response = await api.post('/bazi/analyze', {
                year: date.year(),
                month: date.month() + 1,
                day: date.date(),
                hour: date.hour(),
                gender: values.gender
            })

            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error || '分析失败')
                message.error(response.data.error || '分析失败')
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

    // tabItems has been replaced by bazi-dashboard layout

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
                <div className="bazi-dashboard" style={{ marginTop: 24 }}>
                    {/* 第一行：命盘核心 + 基本强弱 */}
                    <Row gutter={[24, 24]}>
                        <Col xs={24} lg={16}>
                            <Card title="八字命盘" className="feature-card" style={{ height: '100%' }}
                                extra={
                                    <Button
                                        type="dashed"
                                        onClick={handleBigDataAnalysis}
                                        loading={analysisLoading}
                                        style={{ borderColor: '#DAA520', color: '#DAA520' }}
                                    >
                                        大数据详批
                                    </Button>
                                }
                            >
                                <BaZiChart sizhu={result.basic_info.sizhu} />
                            </Card>
                        </Col>
                        <Col xs={24} lg={8}>
                            <Card title="命主信息" className="feature-card" style={{ height: '100%' }}>
                                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                                    <div style={{ fontSize: 14, color: '#94a3b8', marginBottom: 4 }}>日主天干</div>
                                    <div style={{
                                        fontSize: 48,
                                        fontWeight: 'bold',
                                        color: WUXING_COLORS[result.basic_info.day_master_wuxing],
                                        textShadow: `0 0 20px ${WUXING_COLORS[result.basic_info.day_master_wuxing]}40`
                                    }}>
                                        {result.basic_info.day_master}
                                    </div>
                                    <Tag color={WUXING_COLORS[result.basic_info.day_master_wuxing]}>
                                        {result.basic_info.day_master_wuxing}命人
                                    </Tag>
                                </div>
                                <Divider style={{ margin: '16px 0' }} />
                                <Statistic
                                    title="身强身弱"
                                    value={result.day_master_analysis.strength_level}
                                    valueStyle={{ color: '#fff', fontSize: 24 }}
                                    prefix={<FireOutlined style={{ color: '#f59e0b' }} />}
                                    suffix={
                                        <span style={{ fontSize: 14, color: '#94a3b8', marginLeft: 8 }}>
                                            ({(result.day_master_analysis.strength_ratio * 100).toFixed(0)}%)
                                        </span>
                                    }
                                />
                                <Paragraph style={{ marginTop: 12, color: '#cbd5e1', fontSize: 13 }}>
                                    {result.day_master_analysis.description}
                                </Paragraph>
                            </Card>
                        </Col>
                    </Row>

                    {analysisResult && (
                        <Row style={{ marginTop: 24 }}>
                            <Col span={24}>
                                <Card title="大数据引擎分析报告" className="feature-card" style={{ border: '1px solid #DAA520' }}>
                                    <MarkdownViewer
                                        structured={typeof analysisResult === 'object' ? analysisResult.structured : null}
                                        showDividers={false}
                                    />
                                    <div style={{ marginTop: 16, textAlign: 'right', fontSize: 12, color: '#64748b' }}>
                                        Power by Local Rule Engine (50MB Corpus)
                                    </div>
                                </Card>
                            </Col>
                        </Row>
                    )}

                    {/* 第二行：五行数据 + 喜用神 */}
                    <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                        <Col xs={24} md={12} lg={8}>
                            <Card title="五行能量" className="feature-card" style={{ height: '100%' }}>
                                <ReactECharts option={getWuxingRadarOption()} style={{ height: 250 }} />
                            </Card>
                        </Col>
                        <Col xs={24} md={12} lg={8}>
                            <Card title="五行分布" className="feature-card" style={{ height: '100%' }}>
                                <ReactECharts option={getWuxingPieOption()} style={{ height: 250 }} />
                            </Card>
                        </Col>
                        <Col xs={24} lg={8}>
                            <Card title="喜用神调整" className="feature-card" style={{ height: '100%' }}>
                                <Row gutter={[16, 16]}>
                                    <Col span={12}>
                                        <Statistic
                                            title="用神 (最需)"
                                            value={result.xi_yong_shen.yong_shen?.join('、') || '-'}
                                            valueStyle={{ color: '#fbbf24', fontWeight: 'bold' }}
                                        />
                                    </Col>
                                    <Col span={12}>
                                        <Statistic
                                            title="喜神 (辅助)"
                                            value={result.xi_yong_shen.xi_shen?.join('、') || '-'}
                                            valueStyle={{ color: '#34d399', fontWeight: 'bold' }}
                                        />
                                    </Col>
                                    <Col span={12}>
                                        <Statistic
                                            title="忌神 (应避)"
                                            value={result.xi_yong_shen.ji_shen?.join('、') || '-'}
                                            valueStyle={{ color: '#f87171' }}
                                        />
                                    </Col>
                                    <Col span={12}>
                                        <Statistic
                                            title="仇神 (有害)"
                                            value={result.xi_yong_shen.chou_shen?.join('、') || '-'}
                                            valueStyle={{ color: '#94a3b8' }}
                                        />
                                    </Col>
                                </Row>
                                <div style={{ marginTop: 16, background: 'rgba(255,255,255,0.05)', padding: 12, borderRadius: 8 }}>
                                    <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 4 }}>建议</div>
                                    <div style={{ color: '#e2e8f0', fontSize: 13, lineHeight: 1.5 }}>
                                        {result.xi_yong_shen.analysis}
                                    </div>
                                </div>
                            </Card>
                        </Col>
                    </Row>

                    {/* 第三行：大运流年 (全宽) */}
                    {result.dayun_liunian && (
                        <Row style={{ marginTop: 24 }}>
                            <Col span={24}>
                                <Card title="大运流年趋势" className="feature-card">
                                    <div style={{ overflowX: 'auto', paddingBottom: 16 }}>
                                        <div style={{ display: 'flex', gap: 16, minWidth: 'max-content' }}>
                                            {result.dayun_liunian.dayun_list?.map(dy => (
                                                <div
                                                    key={dy.order}
                                                    style={{
                                                        minWidth: 120,
                                                        padding: 16,
                                                        textAlign: 'center',
                                                        background: dy.is_current
                                                            ? 'linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.05))'
                                                            : 'rgba(255, 255, 255, 0.02)',
                                                        border: dy.is_current ? '1px solid #fbbf24' : '1px solid rgba(255,255,255,0.05)',
                                                        borderRadius: 12,
                                                        position: 'relative'
                                                    }}
                                                >
                                                    {dy.is_current && (
                                                        <div style={{
                                                            position: 'absolute', top: 0, right: 0,
                                                            background: '#fbbf24', color: '#000',
                                                            fontSize: 10, padding: '2px 6px',
                                                            borderBottomLeftRadius: 8, borderTopRightRadius: 12
                                                        }}>当前</div>
                                                    )}
                                                    <div style={{ fontSize: 12, color: '#94a3b8' }}>{dy.range}</div>
                                                    <div style={{
                                                        fontSize: 24,
                                                        fontWeight: 'bold',
                                                        margin: '8px 0',
                                                        color: dy.is_current ? '#fbbf24' : '#e2e8f0'
                                                    }}>
                                                        {dy.ganzhi}
                                                    </div>
                                                    <Tag color="geekblue" style={{ margin: 0 }}>{dy.shishen}</Tag>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </Card>
                            </Col>
                        </Row>
                    )}

                    {/* 第四行：性格与神煞 */}
                    <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                        <Col xs={24} md={12}>
                            <Card title="性格格局" className="feature-card" style={{ height: '100%' }}>
                                <Title level={4} style={{ color: '#fbbf24', marginTop: 0 }}>
                                    {result.geju.main_geju}
                                </Title>
                                <div style={{ marginBottom: 16 }}>
                                    {result.personality.keywords?.map(kw => (
                                        <Tag key={kw} color="purple" style={{ marginRight: 8, marginBottom: 8 }}>#{kw}</Tag>
                                    ))}
                                </div>
                                <Paragraph style={{ color: '#cbd5e1' }}>
                                    {result.personality.summary}
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} md={12}>
                            <Card title="神煞提示" className="feature-card" style={{ height: '100%' }}>
                                <div style={{ marginBottom: 16 }}>
                                    <div style={{ fontSize: 13, color: '#94a3b8', marginBottom: 8 }}>吉神</div>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                        {result.shensha.ji_shensha?.map(s => (
                                            <Tag key={s.name} color="success" style={{ padding: '4px 8px' }}>
                                                {s.name} <span style={{ opacity: 0.6 }}>{s.position}</span>
                                            </Tag>
                                        )) || <span style={{ color: '#666' }}>无</span>}
                                    </div>
                                </div>
                                <div>
                                    <div style={{ fontSize: 13, color: '#94a3b8', marginBottom: 8 }}>凶煞</div>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                        {result.shensha.xiong_shensha?.map(s => (
                                            <Tag key={s.name} color="error" style={{ padding: '4px 8px' }}>
                                                {s.name} <span style={{ opacity: 0.6 }}>{s.position}</span>
                                            </Tag>
                                        )) || <span style={{ color: '#666' }}>无</span>}
                                    </div>
                                </div>
                            </Card>
                        </Col>
                    </Row>
                </div>
            )}
        </div>
    )
}

export default BaZi
