import React from 'react';
import { Card, Tag, Typography, Row, Col, Progress, Statistic, Space, Button, theme, Tooltip } from 'antd';
import {
    ClockCircleOutlined,
    DeleteOutlined,
    EyeOutlined,
    ThunderboltOutlined,
    DeploymentUnitOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';

const { Text, Title, Paragraph } = Typography;
const { useToken } = theme;

const HistoryCard = ({ record, type, onClick, onDelete }) => {
    const { token } = useToken();
    const data = record.result_data || record.fusion_result || {};

    const cardStyle = {
        background: 'rgba(255, 255, 255, 0.03)',
        border: `1px solid ${token.colorBorderSecondary}`,
        borderRadius: token.borderRadiusLG,
        marginBottom: 16,
        backdropFilter: 'blur(10px)',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
    };

    const hoverStyle = {
        transform: 'translateY(-4px)',
        boxShadow: token.boxShadowSecondary,
        borderColor: token.colorPrimary
    };

    // --- Specific Renderers ---

    // 1. Bazi Card
    const renderBazi = () => {
        const sizhu = data.basic_info?.sizhu || data.sizhu || {};
        const wuxing = data.wuxing || {};
        const dayMaster = data.basic_info?.day_master_wuxing || '';
        const dayMasterTitle = data.basic_info?.day_master || '';

        return (
            <>
                <div style={{ marginBottom: 12 }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>日主</Text>
                    <div style={{ fontSize: 20, fontWeight: 'bold' }}>
                        <span style={{ color: token.colorPrimary }}>{dayMasterTitle}</span>
                        <span style={{ fontSize: 14, marginLeft: 8, opacity: 0.8 }}>{dayMaster}</span>
                    </div>
                </div>

                {data.geju && (
                    <Tag color="gold" style={{ marginBottom: 16 }}>{data.geju.name || '格局'}</Tag>
                )}

                <Row gutter={[4, 4]}>
                    <Col span={6}>
                        <div style={{ textAlign: 'center', background: 'rgba(255,255,255,0.05)', borderRadius: 4, padding: '4px 0' }}>
                            <div style={{ fontSize: 12, opacity: 0.7 }}>年</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.year?.[0]}</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.year?.[1]}</div>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div style={{ textAlign: 'center', background: 'rgba(255,255,255,0.05)', borderRadius: 4, padding: '4px 0' }}>
                            <div style={{ fontSize: 12, opacity: 0.7 }}>月</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.month?.[0]}</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.month?.[1]}</div>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div style={{ textAlign: 'center', background: token.colorPrimaryBg, borderRadius: 4, padding: '4px 0', border: `1px solid ${token.colorPrimaryBorder}` }}>
                            <div style={{ fontSize: 12, opacity: 0.7, color: token.colorPrimary }}>日</div>
                            <div style={{ fontWeight: 500, color: token.colorPrimary }}>{sizhu.day?.[0]}</div>
                            <div style={{ fontWeight: 500, color: token.colorPrimary }}>{sizhu.day?.[1]}</div>
                        </div>
                    </Col>
                    <Col span={6}>
                        <div style={{ textAlign: 'center', background: 'rgba(255,255,255,0.05)', borderRadius: 4, padding: '4px 0' }}>
                            <div style={{ fontSize: 12, opacity: 0.7 }}>时</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.hour?.[0]}</div>
                            <div style={{ fontWeight: 500 }}>{sizhu.hour?.[1]}</div>
                        </div>
                    </Col>
                </Row>

                {wuxing.strongest && (
                    <div style={{ marginTop: 12, fontSize: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
                        <Text type="secondary">最旺:</Text>
                        <Tag color="red" style={{ margin: 0 }}>{wuxing.strongest}</Tag>
                        <Text type="secondary" style={{ marginLeft: 8 }}>喜用:</Text>
                        <Tag color="green" style={{ margin: 0 }}>{data.xi_yong_shen?.yong_shen || '-'}</Tag>
                    </div>
                )}
            </>
        );
    };

    // 2. Ziwei Card
    const renderZiwei = () => {
        const chart = data.chart_data || data;
        const analysis = data.analysis || {};
        const mingGong = analysis.ming_gong_stars || [];

        return (
            <>
                <div style={{ marginBottom: 12 }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>命宫主星</Text>
                    <div style={{ fontSize: 20, fontWeight: 'bold', color: token.colorPrimary }}>
                        {mingGong.length > 0 ? mingGong.map(s => s.name).join(' · ') : '命无正曜'}
                    </div>
                </div>

                <Space size={[0, 8]} wrap style={{ marginBottom: 16 }}>
                    <Tag>{chart.wuxing_ju}</Tag>
                    {analysis.advanced_patterns?.slice(0, 2).map((p, i) => (
                        <Tag key={i} color="purple">{p.name}</Tag>
                    ))}
                </Space>

                <div style={{
                    background: 'rgba(255,255,255,0.02)',
                    padding: 12,
                    borderRadius: 8,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}>
                    <div style={{ textAlign: 'center' }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>身宫</Text>
                        <div style={{ fontWeight: 500 }}>{chart.shen_gong}</div>
                    </div>
                    <div style={{ width: 1, height: 20, background: 'rgba(255,255,255,0.1)' }} />
                    <div style={{ textAlign: 'center' }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>命盘概况</Text>
                        <div style={{ fontWeight: 500 }}>{analysis.pattern_summary?.substring(0, 4) || '常规局'}</div>
                    </div>
                </div>
            </>
        );
    };

    // 3. Divination Card
    const renderDivination = () => {
        const mainGua = data.main_gua || data;
        const fortune = data.overall_fortune || {};

        const isGood = fortune.level?.includes('吉');
        const isBad = fortune.level?.includes('凶');
        const color = isGood ? token.colorSuccess : isBad ? token.colorError : token.colorWarning;

        return (
            <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                    <div>
                        <div style={{ fontSize: 32, lineHeight: 1, fontFamily: 'Segoe UI Symbol' }}>
                            {mainGua.upper?.symbol || '☰'}
                        </div>
                        <div style={{ fontSize: 32, lineHeight: 0.8, fontFamily: 'Segoe UI Symbol' }}>
                            {mainGua.lower?.symbol || '☷'}
                        </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: 24, fontWeight: 'bold' }}>{mainGua.name}</div>
                        <Tag color={color} style={{ margin: 0, marginTop: 4 }}>{fortune.level}</Tag>
                    </div>
                </div>

                <div style={{ marginBottom: 12 }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>{record.method === 'liuyao' ? '六爻起卦' : '梅花易数'}</Text>
                    <div style={{ fontWeight: 500, fontSize: 16, marginTop: 4 }}>
                        {record.question}
                    </div>
                </div>

                <Paragraph ellipsis={{ rows: 2 }} type="secondary" style={{ fontSize: 13, margin: 0 }}>
                    {fortune.description}
                </Paragraph>
            </>
        );
    };

    // 4. Psychology Card
    const renderPsychology = () => {
        const testType = record.test_type;
        const themeColor = {
            mbti: '#722ed1',
            big5: '#13c2c2',
            archetype: '#eb2f96',
            enneagram: '#fa8c16'
        }[testType] || token.colorPrimary;

        // Render specific content based on test type
        const renderInner = () => {
            if (testType === 'mbti') {
                return (
                    <div style={{ textAlign: 'center', padding: '12px 0' }}>
                        <div style={{
                            fontSize: 36,
                            fontWeight: 900,
                            color: themeColor,
                            marginBottom: 4,
                            lineHeight: 1.2
                        }}>
                            {data.type_code}
                        </div>
                        <Text strong style={{ fontSize: 16 }}>{data.type_name}</Text>
                        <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 6 }}>
                            {data.dimensions && Object.entries(data.dimensions).slice(0, 3).map(([k, v]) => (
                                <Progress key={k} percent={v.clarity} strokeColor={themeColor} size="small" showInfo={false} />
                            ))}
                        </div>
                    </div>
                );
            }
            if (testType === 'big5') {
                return (
                    <div>
                        <div style={{ textAlign: 'center', marginBottom: 16 }}>
                            <div style={{ fontSize: 24, fontWeight: 'bold', color: themeColor }}>完成</div>
                            <Text type="secondary">大五人格评估</Text>
                        </div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
                            {data.levels && Object.entries(data.levels).slice(0, 4).map(([k, v]) => (
                                <Tag key={k} color={v === '高' ? 'green' : v === '低' ? 'red' : 'default'} style={{ margin: 0 }}>
                                    {k}:{v}
                                </Tag>
                            ))}
                        </div>
                    </div>
                )
            }
            if (testType === 'archetype') {
                return (
                    <div style={{ textAlign: 'center', padding: '12px 0' }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>主原型</Text>
                        <div style={{
                            fontSize: 28,
                            fontWeight: 'bold',
                            color: themeColor,
                            margin: '4px 0 8px'
                        }}>
                            {data.primary?.name || '-'}
                        </div>
                        {data.secondary && (
                            <Tag color="purple">次: {data.secondary.name}</Tag>
                        )}
                    </div>
                )
            }
            if (testType === 'enneagram') {
                return (
                    <div style={{ textAlign: 'center', padding: '12px 0' }}>
                        <div style={{
                            fontSize: 36,
                            fontWeight: 900,
                            color: themeColor,
                            marginBottom: 4
                        }}>
                            {data.primary_type}号
                        </div>
                        <Text strong>{data.primary_info?.name}</Text>
                        <div style={{ marginTop: 8 }}>
                            {data.wing && <Tag color="orange">侧翼 {data.wing}w</Tag>}
                        </div>
                    </div>
                )
            }
            // Fallback
            return (
                <div style={{ textAlign: 'center', padding: '20px 0' }}>
                    <Text type="secondary">查看测试结果</Text>
                </div>
            )
        };

        return (
            <>
                <div style={{ marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Tag color={themeColor} style={{ marginRight: 0 }}>{record.test_type.toUpperCase()}</Tag>
                </div>
                {renderInner()}
            </>
        );
    };

    // 5. Fusion Card
    const renderFusion = () => {
        return (
            <>
                <div style={{ marginBottom: 16 }}>
                    <Tag color="volcano" icon={<DeploymentUnitOutlined />}>AI 融合</Tag>
                </div>
                <Title level={5} ellipsis={{ rows: 2 }} style={{ marginBottom: 16, height: 44 }}>
                    {record.title}
                </Title>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Text type="secondary">可信度</Text>
                    <Progress type="circle" percent={Math.round(record.confidence * 100)} width={40} size="small" />
                </div>
            </>
        );
    };


    const renderContent = () => {
        const safeType = type === 'analyses' ? record.type : type;
        if (type === 'fusions') return renderFusion();

        switch (safeType) {
            case 'bazi': return renderBazi();
            case 'ziwei': return renderZiwei();
            case 'divinations':
            case 'meihua':
            case 'meihua_time':
            case 'meihua_number':
            case 'meihua_text':
            case 'liuyao':
                return renderDivination();
            case 'psychology': return renderPsychology();
            default: return <Text>未知类型</Text>;
        }
    };

    return (
        <Card
            hoverable
            style={{
                ...cardStyle,
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden', // Ensure footer is clipped to corners
                padding: 0 // Remove default card padding to control it manually
            }}
            bodyStyle={{
                padding: 0,
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                flex: 1
            }}
            onClick={() => onClick(record)}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform = hoverStyle.transform;
                e.currentTarget.style.boxShadow = hoverStyle.boxShadow;
                e.currentTarget.style.borderColor = hoverStyle.borderColor;
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'none';
                e.currentTarget.style.borderColor = token.colorBorderSecondary;
            }}
        >
            {/* Content Area */}
            <div style={{ padding: '20px 20px 12px 20px', flex: 1 }}>
                <div style={{ minHeight: 160 }}>
                    {renderContent()}
                </div>
            </div>

            {/* Custom Seamless Footer */}
            <div style={{
                borderTop: `1px solid ${token.colorBorderSecondary}`,
                padding: '12px 16px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                background: 'rgba(0,0,0,0.02)', // Slightly different bg for footer if needed, or transparent
            }}>
                <Tooltip title="查看详情">
                    <Button
                        type="text"
                        size="small"
                        icon={<EyeOutlined />}
                        style={{ color: token.colorTextSecondary }}
                        onClick={(e) => { e.stopPropagation(); onClick(record); }}
                    />
                </Tooltip>

                <Text type="secondary" style={{ fontSize: 12 }}>
                    {dayjs(record.created_at).format('YYYY-MM-DD HH:mm:ss')}
                </Text>

                <Tooltip title="删除记录">
                    <Button
                        type="text"
                        size="small"
                        danger
                        icon={<DeleteOutlined />}
                        onClick={(e) => { e.stopPropagation(); onDelete(record.id); }}
                    />
                </Tooltip>
            </div>
        </Card>
    );
};

export default HistoryCard;
