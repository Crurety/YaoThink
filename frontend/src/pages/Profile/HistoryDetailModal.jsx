import React from 'react';
import { Modal, Descriptions, Tag, Typography, Divider, List, Card, Progress, Row, Col, Empty, Space, Statistic, theme } from 'antd';
import {
    GoldOutlined, FireOutlined,
    ThunderboltOutlined, CloudOutlined,
    ExperimentOutlined, DatabaseOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { useToken } = theme;

const HistoryDetailModal = ({ visible, onClose, record, type }) => {
    const { token } = useToken();

    if (!record) return null;

    // --- 样式辅助函数 ---
    const getCardStyle = () => ({
        background: token.colorFillAlter,
        borderRadius: token.borderRadiusLG,
        border: `1px solid ${token.colorBorderSecondary}`,
        boxShadow: token.boxShadowTertiary,
        overflow: 'hidden'
    });

    // --- 命理分析 (Bazi) ---
    const renderBaZiDetail = (data) => {
        // Fix Data Mapping: Backend returns structure inside 'basic_info'
        const sizhu = data.basic_info?.sizhu || data.sizhu || {};
        // Try to get wuxing from data.wuxing or data.basic_info?.wuxing if structure varies
        const wuxing = data.wuxing || {};

        if (!sizhu.year && !data.basic_info) return <Empty description="数据结构不匹配" />;

        const renderPillar = (title, gan, zhi) => (
            <div style={{
                ...getCardStyle(),
                padding: '16px',
                textAlign: 'center',
                background: 'linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 100%)'
            }}>
                <Text type="secondary" style={{ fontSize: '12px', display: 'block', marginBottom: '8px' }}>{title}</Text>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: token.colorPrimary }}>{gan || '-'}</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{zhi || '-'}</div>
            </div>
        );

        return (
            <div className="detail-content">
                <Title level={4} style={{ marginBottom: 24, textAlign: 'center' }}>
                    八字命盘
                </Title>

                <Row gutter={[12, 12]} style={{ marginBottom: '32px' }}>
                    <Col span={6}>{renderPillar("年柱", sizhu.year?.[0], sizhu.year?.[1])}</Col>
                    <Col span={6}>{renderPillar("月柱", sizhu.month?.[0], sizhu.month?.[1])}</Col>
                    <Col span={6}>{renderPillar("日柱", sizhu.day?.[0], sizhu.day?.[1])}</Col>
                    <Col span={6}>{renderPillar("时柱", sizhu.hour?.[0], sizhu.hour?.[1])}</Col>
                </Row>

                {wuxing.scores && (
                    <Card size="small" title="五行能量分布" style={{ marginBottom: 24, ...getCardStyle() }} bordered={false}>
                        <Row gutter={[24, 12]}>
                            {['gold', 'wood', 'water', 'fire', 'earth'].map(key => {
                                const colorMap = { gold: '#fbbf24', wood: '#34d399', water: '#60a5fa', fire: '#f87171', earth: '#a8a29e' };
                                const labelMap = { gold: '金', wood: '木', water: '水', fire: '火', earth: '土' };
                                const score = wuxing.scores[key] || 0;
                                const percent = Math.min(100, (score / (Object.values(wuxing.scores).reduce((a, b) => a + b, 0) || 1)) * 100);

                                return (
                                    <Col span={24} key={key}>
                                        <Row align="middle" gutter={8}>
                                            <Col span={2}><Text strong style={{ color: colorMap[key] }}>{labelMap[key]}</Text></Col>
                                            <Col span={18}>
                                                <Progress
                                                    percent={percent}
                                                    strokeColor={colorMap[key]}
                                                    showInfo={false}
                                                    trailColor={token.colorFillSecondary}
                                                    size="small"
                                                />
                                            </Col>
                                            <Col span={4} style={{ textAlign: 'right' }}><Text type="secondary">{score}</Text></Col>
                                        </Row>
                                    </Col>
                                );
                            })}
                        </Row>
                        <div style={{ marginTop: 16, display: 'flex', gap: 16, justifyContent: 'center' }}>
                            <Tag color="red">最强: {wuxing.strongest || '-'}</Tag>
                            <Tag color="blue">最弱: {wuxing.weakest || '-'}</Tag>
                            <Tag color="green">喜用: {data.xi_yong_shen?.yong_shen || '-'}</Tag>
                        </div>
                    </Card>
                )}

                {(data.summary || data.day_master_analysis) && (
                    <Card size="small" title="综合简评" style={getCardStyle()} bordered={false}>
                        <Paragraph style={{ margin: 0 }}>
                            {data.summary || data.day_master_analysis?.description || "暂无详细评语"}
                        </Paragraph>
                    </Card>
                )}
            </div>
        );
    };

    // --- 紫微斗数 (Ziwei) ---
    const renderZiWeiDetail = (data) => {
        // Fix Data Mapping
        const chart = data.chart_data || data;
        const analysis = data.analysis || {};

        if (!chart.ming_gong) return <Empty description="数据结构不匹配" />;

        return (
            <div className="detail-content">
                <Card style={{ ...getCardStyle(), marginBottom: 24, textAlign: 'center' }}>
                    <Row gutter={24} divide>
                        <Col span={8}>
                            <Statistic title="命宫主星" value={analysis.ming_gong_stars?.map(s => s.name).join(' ') || '无'} valueStyle={{ fontSize: 20 }} />
                        </Col>
                        <Col span={8}>
                            <Statistic title="五行局" value={chart.wuxing_ju} valueStyle={{ fontSize: 20 }} />
                        </Col>
                        <Col span={8}>
                            <Statistic title="身宫" value={chart.shen_gong} valueStyle={{ fontSize: 20 }} />
                        </Col>
                    </Row>
                </Card>

                <Title level={5}>命盘格局</Title>
                <div style={{ marginBottom: 24 }}>
                    {analysis.advanced_patterns?.length > 0 ? (
                        analysis.advanced_patterns.map((pt, idx) => (
                            <Tag key={idx} color="purple" style={{ padding: '4px 10px', marginBottom: 8 }}>
                                {pt.name}
                            </Tag>
                        ))
                    ) : <Text type="secondary">平稳格局，无特殊显示</Text>}
                </div>

                <Title level={5}>核心宫位分析</Title>
                <List
                    grid={{ gutter: 16, column: 1 }}
                    dataSource={Object.entries(analysis.palace_scores || {}).slice(0, 3)} // Show top 3 or specific ones
                    renderItem={([name, score]) => (
                        <List.Item>
                            <Card size="small" style={{ background: 'rgba(255,255,255,0.02)' }} bordered={false}>
                                <Row justify="space-between">
                                    <Col>{name}</Col>
                                    <Col><Text type="warning">能量指数: {score}</Text></Col>
                                </Row>
                            </Card>
                        </List.Item>
                    )}
                />
            </div>
        );
    };

    // --- 易经占卜 (Divination) ---
    const renderDivinationDetail = (data) => {
        // Fix Data Mapping
        const mainGua = data.main_gua || data;
        const fortune = data.overall_fortune || {};

        const GuaSymbol = ({ symbol, big }) => (
            <div style={{
                fontSize: big ? '64px' : '32px',
                lineHeight: 1,
                fontFamily: 'Segoe UI Symbol, sans-serif' // Ensure support for trigram chars
            }}>
                {symbol}
            </div>
        );

        return (
            <div className="detail-content">
                <div style={{
                    textAlign: 'center',
                    padding: '32px 0',
                    background: token.colorFillAlter,
                    borderRadius: token.borderRadiusLG,
                    marginBottom: 24
                }}>
                    <GuaSymbol symbol={mainGua.lower?.symbol} />
                    {/* Note: Ideally we want hexagram symbol. If unavailable, use name */}

                    <Title level={2} style={{ marginTop: 16, marginBottom: 4 }}>{mainGua.name}</Title>
                    <Text type="secondary">{mainGua.upper?.name}上 {mainGua.lower?.name}下</Text>
                </div>

                <Card title="断语判断" style={{ ...getCardStyle(), marginBottom: 24 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
                        <Tag color={fortune.level?.includes('吉') ? 'green' : fortune.level?.includes('凶') ? 'red' : 'orange'}>
                            {fortune.level || '平'}
                        </Tag>
                        <Text strong style={{ fontSize: 16 }}>{fortune.description}</Text>
                    </div>
                    <Paragraph type="secondary">
                        {mainGua.interpretation?.summary}
                    </Paragraph>
                </Card>

                {data.dong_yao && (
                    <Card size="small" title={`动爻：第 ${data.dong_yao} 爻`} style={getCardStyle()}>
                        <Paragraph>{data.dong_yao_meaning}</Paragraph>
                    </Card>
                )}
            </div>
        );
    };

    // --- 心理测试 (Psychology) ---
    const renderPsychologyDetail = (data) => {
        const isMBTI = data.type_code; // MBTI structure check
        const isBig5 = data.scores;    // Big5 structure check

        if (isMBTI) {
            return (
                <div className="detail-content">
                    <div style={{ textAlign: 'center', padding: '40px 0' }}>
                        <div style={{
                            fontSize: 48, fontWeight: 900,
                            background: 'linear-gradient(45deg, #1890ff, #a0d911)',
                            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
                        }}>
                            {data.type_code}
                        </div>
                        <Title level={4} style={{ marginTop: 8 }}>{data.type_name}</Title>
                    </div>
                    <Divider>维度倾向</Divider>
                    {data.dimensions && Object.entries(data.dimensions).map(([k, v]) => (
                        <div key={k} style={{ marginBottom: 12 }}>
                            <Row align="middle" gutter={8}>
                                <Col span={4}><Text strong>{k}</Text></Col>
                                <Col span={16}><Progress percent={v} showInfo={false} strokeColor={token.colorPrimary} /></Col>
                                <Col span={4} style={{ textAlign: 'right' }}>{v}%</Col>
                            </Row>
                        </div>
                    ))}
                    <Paragraph style={{ marginTop: 24, fontSize: 16, lineHeight: 1.8 }}>
                        {data.description}
                    </Paragraph>
                </div>
            )
        }

        if (isBig5) {
            return (
                <div className="detail-content">
                    <List
                        grid={{ gutter: 16, column: 2 }}
                        dataSource={Object.entries(data.scores || {})}
                        renderItem={([trait, score]) => (
                            <List.Item>
                                <Card size="small" style={{ background: token.colorFillAlter, border: 'none' }}>
                                    <Statistic
                                        title={trait}
                                        value={score}
                                        suffix="/ 50"
                                        valueStyle={{ color: score > 35 ? token.colorSuccess : token.colorText }}
                                    />
                                    <Progress percent={score * 2} showInfo={false} size="small" style={{ marginTop: 8 }} />
                                </Card>
                            </List.Item>
                        )}
                    />
                    <Divider orientation="left">详细解读</Divider>
                    {data.interpretation && Object.entries(data.interpretation).map(([k, v]) => (
                        <div key={k} style={{ marginBottom: 16 }}>
                            <Text strong>{k}</Text>
                            <Paragraph type="secondary">{v}</Paragraph>
                        </div>
                    ))}
                </div>
            )
        }

        return <Paragraph>{JSON.stringify(data)}</Paragraph>;
    };

    const renderContent = () => {
        const data = record.result_data || {};
        const safeType = type === 'analyses' ? record.type : type; // Handle type variation

        switch (safeType) {
            case 'bazi': return renderBaZiDetail(data);
            case 'ziwei': return renderZiWeiDetail(data);
            case 'divinations':
            case 'meihua_time': // Handle specific divination methods if passed as type
            case 'meihua_number':
            case 'meihua_text':
            case 'liuyao':
                return renderDivinationDetail(data);
            case 'psychology': return renderPsychologyDetail(data);
            default: return <Empty description="暂不支持的类型" />;
        }
    };

    return (
        <Modal
            title={<Space>
                <Tag color={token.colorPrimary}>{record.type || record.method || '详情'}</Tag>
                <Text>历史记录详情</Text>
            </Space>}
            open={visible}
            onCancel={onClose}
            footer={null}
            width={720}
            centered
            bodyStyle={{ maxHeight: '75vh', overflowY: 'auto', padding: '24px' }}
        >
            {renderContent()}
        </Modal>
    );
};

export default HistoryDetailModal;
