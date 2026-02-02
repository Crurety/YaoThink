import React from 'react';
import { Modal, Descriptions, Tag, Typography, Divider, List, Card, Progress, Row, Col, Empty } from 'antd';

const { Title, Text, Paragraph } = Typography;

const HistoryDetailModal = ({ visible, onClose, record, type }) => {
    if (!record) return null;

    // --- 命理分析 (Bazi) ---
    const renderBaZiDetail = (data) => {
        if (!data) return <Empty description="无详细数据" />;

        //Helper to format pillar
        const renderPillar = (title, value) => (
            <div style={{ textAlign: 'center', background: '#f5f5f5', padding: '10px', borderRadius: '4px' }}>
                <Text type="secondary" style={{ fontSize: '12px' }}>{title}</Text>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '4px' }}>{value || '-'}</div>
            </div>
        );

        return (
            <div className="detail-content">
                <Title level={4}>八字命盘</Title>
                <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                    <Col span={6}>{renderPillar("年柱", data.bazi?.year)}</Col>
                    <Col span={6}>{renderPillar("月柱", data.bazi?.month)}</Col>
                    <Col span={6}>{renderPillar("日柱", data.bazi?.day)}</Col>
                    <Col span={6}>{renderPillar("时柱", data.bazi?.hour)}</Col>
                </Row>

                {data.wuxing && (
                    <>
                        <Divider orientation="left">五行能量</Divider>
                        <Descriptions column={2} size="small">
                            <Descriptions.Item label="最强五行"><Tag color="red">{data.wuxing.strongest || '-'}</Tag></Descriptions.Item>
                            <Descriptions.Item label="喜用神"><Tag color="green">{data.wuxing.favorable || '-'}</Tag></Descriptions.Item>
                        </Descriptions>
                        <div style={{ marginTop: '12px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                            {Object.entries(data.wuxing).filter(([k]) => ['gold', 'wood', 'water', 'fire', 'earth'].includes(k)).map(([k, v]) => {
                                const colorMap = { gold: 'gold', wood: 'green', water: 'blue', fire: 'volcano', earth: 'brown' };
                                const labelMap = { gold: '金', wood: '木', water: '水', fire: '火', earth: '土' };
                                return <Tag key={k} color={colorMap[k]}>{labelMap[k]}: {v}</Tag>
                            })}
                        </div>
                    </>
                )}

                {data.summary && (
                    <>
                        <Divider orientation="left">综合分析</Divider>
                        <Paragraph>{data.summary}</Paragraph>
                    </>
                )}
            </div>
        );
    };

    // --- 紫微斗数 (Ziwei) ---
    const renderZiWeiDetail = (data) => {
        if (!data) return <Empty description="无详细数据" />;
        return (
            <div className="detail-content">
                <Descriptions title="紫微命盘概览" bordered column={1} size="small">
                    <Descriptions.Item label="命宫主星">{data.ming_gong?.stars?.map(s => s.name).join(' + ') || '无主星'}</Descriptions.Item>
                    <Descriptions.Item label="身宫">{data.shen_gong?.name || '-'}</Descriptions.Item>
                    <Descriptions.Item label="五行局">{data.wuxing_ju || '-'}</Descriptions.Item>
                </Descriptions>

                {data.patterns && data.patterns.length > 0 && (
                    <>
                        <Divider orientation="left">格局分析</Divider>
                        <List
                            size="small"
                            dataSource={data.patterns}
                            renderItem={item => (
                                <List.Item>
                                    <List.Item.Meta
                                        title={<Tag color="purple">{item.name}</Tag>}
                                        description={item.description}
                                    />
                                </List.Item>
                            )}
                        />
                    </>
                )}
            </div>
        );
    };

    // --- 易经占卜 (Divination) ---
    const renderDivinationDetail = (data) => {
        if (!data) return <Empty description="无详细数据" />;
        return (
            <div className="detail-content">
                <Card style={{ textAlign: 'center', background: '#fafafa', marginBottom: '16px' }}>
                    <Title level={3} style={{ margin: 0 }}>{data.hexagram_name}</Title>
                    <Text type="secondary">{data.hexagram_code || ''}</Text>
                    <Paragraph style={{ marginTop: '16px', fontSize: '16px' }}>
                        {data.hexagram_text}
                    </Paragraph>
                </Card>

                <Descriptions bordered column={1} size="small">
                    <Descriptions.Item label="求测问题">{record.question || '未填写'}</Descriptions.Item>
                    <Descriptions.Item label="起卦方式">{record.method}</Descriptions.Item>
                </Descriptions>

                {data.changing_lines && data.changing_lines.length > 0 && (
                    <>
                        <Divider orientation="left">变爻 / 动向</Divider>
                        <List
                            size="small"
                            bordered
                            dataSource={data.changing_lines}
                            renderItem={line => <List.Item>{line}</List.Item>}
                        />
                    </>
                )}

                {data.judgment && (
                    <>
                        <Divider orientation="left">断语</Divider>
                        <Paragraph>{data.judgment}</Paragraph>
                    </>
                )}
            </div>
        );
    };

    // --- 心理测试 (Psychology) ---
    const renderPsychologyDetail = (data) => {
        if (!data) return <Empty description="无详细数据" />;
        const testType = record.test_type;

        // MBTI Rendering
        if (testType === 'mbti') {
            return (
                <div className="detail-content">
                    <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                        <Title level={2} style={{ color: '#1890ff', margin: 0 }}>{data.type_code}</Title>
                        <Title level={5} type="secondary">{data.type_name}</Title>
                    </div>

                    <Divider orientation="left">维度倾向</Divider>
                    {data.dimensions && Object.entries(data.dimensions).map(([key, value]) => {
                        // Simple visualization for E/I, S/N etc. 
                        // Assuming keys like E, I, S, N or combined.
                        // Let's just list them for now unless we know the pair structure perfectly.
                        return (
                            <div key={key} style={{ marginBottom: '8px' }}>
                                <Row align="middle">
                                    <Col span={4}><Text strong>{key}</Text></Col>
                                    <Col span={16}>
                                        <Progress percent={value} showInfo={false} strokeColor="#1890ff" />
                                    </Col>
                                    <Col span={4} style={{ textAlign: 'right' }}>{value}%</Col>
                                </Row>
                            </div>
                        );
                    })}

                    <Divider orientation="left">类型描述</Divider>
                    <Paragraph>{data.description}</Paragraph>
                </div>
            );
        }

        // Big5 Rendering
        if (testType === 'big5') {
            return (
                <div className="detail-content">
                    <Title level={4}>大五人格分析</Title>
                    <div style={{ marginBottom: '24px' }}>
                        {data.scores && Object.entries(data.scores).map(([key, score]) => (
                            <div key={key} style={{ marginBottom: '12px' }}>
                                <Row justify="space-between">
                                    <Col><Text strong>{key}</Text></Col>
                                    <Col><Text>{data.levels?.[key] || score}</Text></Col>
                                </Row>
                                <Progress
                                    percent={data.percentiles?.[key] || (score / 50) * 100}
                                    status="active"
                                    strokeColor={score > 50 ? '#52c41a' : '#faad14'}
                                />
                            </div>
                        ))}
                    </div>
                    {data.interpretation && (
                        <>
                            <Divider orientation="left">结果解读</Divider>
                            <List
                                dataSource={Object.entries(data.interpretation)}
                                renderItem={([k, v]) => (
                                    <List.Item>
                                        <List.Item.Meta title={k} description={v} />
                                    </List.Item>
                                )}
                            />
                        </>
                    )}
                </div>
            );
        }

        // Archetype / Enneagram fallback to generic pretty view
        return (
            <div className="detail-content">
                <Descriptions title="测试结果" column={1} bordered>
                    {data.primary_type && <Descriptions.Item label="主类型">{data.primary_type}</Descriptions.Item>}
                    {data.primary && <Descriptions.Item label="主原型">{data.primary.name || data.primary}</Descriptions.Item>}
                    {data.secondary && <Descriptions.Item label="次原型">{data.secondary.name || data.secondary}</Descriptions.Item>}
                    {data.wing && <Descriptions.Item label="侧翼">{data.wing}</Descriptions.Item>}
                </Descriptions>

                {data.profile && (
                    <Card size="small" title="详细分析" style={{ marginTop: '16px' }}>
                        <Paragraph>{JSON.stringify(data.profile, null, 2)}</Paragraph> {/* Fallback for complex text */}
                    </Card>
                )}
            </div>
        );
    };

    const renderFusionDetail = (data) => (
        <div className="detail-content">
            <Title level={4}>{data.title || '融合分析'}</Title>
            <Paragraph>{data.content || '暂无详细内容'}</Paragraph>
            {data.confidence && <Tag color="blue">置信度: {data.confidence}%</Tag>}
        </div>
    );

    const renderContent = () => {
        const data = record.result_data || {};
        switch (type) {
            case 'analyses':
                if (record.type === 'bazi') return renderBaZiDetail(data);
                if (record.type === 'ziwei') return renderZiWeiDetail(data);
                return <Empty description="未知分析类型" />;
            case 'divinations':
                return renderDivinationDetail(data);
            case 'psychology':
                return renderPsychologyDetail(data);
            case 'fusions':
                return renderFusionDetail(data);
            default:
                return <Paragraph>{JSON.stringify(data)}</Paragraph>;
        }
    };

    return (
        <Modal
            title={<Space><Tag color="blue">{type === 'psychology' ? record.test_type?.toUpperCase() : (record.type || record.method)}</Tag> 详情查看</Space>}
            open={visible}
            onCancel={onClose}
            footer={null}
            width={700}
            bodyStyle={{ maxHeight: '70vh', overflowY: 'auto' }}
        >
            {renderContent()}
        </Modal>
    );
};

export default HistoryDetailModal;
