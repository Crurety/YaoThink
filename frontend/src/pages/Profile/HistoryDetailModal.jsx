import React, { useState, useEffect } from 'react';
import { Modal, Descriptions, Tag, Typography, Divider, List, Card, Progress, Row, Col, Empty, Space, Statistic, theme, Spin, message } from 'antd';
import {
    GoldOutlined, FireOutlined,
    ThunderboltOutlined, CloudOutlined,
    ExperimentOutlined, DatabaseOutlined,
    UserOutlined, RocketOutlined, HeartOutlined, StarOutlined, CheckCircleOutlined
} from '@ant-design/icons';
import api from '../../services/api';

const { Title, Text, Paragraph } = Typography;
const { useToken } = theme;

const HistoryDetailModal = ({ visible, onClose, record, type }) => {
    const { token } = useToken();
    const [loading, setLoading] = useState(false);
    const [detailData, setDetailData] = useState(null);

    // Fetch full detail when modal opens or record changes
    useEffect(() => {
        if (visible && record) {
            // Check if record already has result_data with enough details to skip fetch?
            // Usually result_data in list view might be partial. To be safe/consistent with detail view requirements,
            // we should fetch if we suspect missing data, or just use what we have if it looks complete.
            // For now, let's trust the logic: if we have comprehensive data, use it.
            // But since we observed missing data in the original report, force fetching might be safer if `record` came from a summary list.
            // However, the original code logic was:
            if (record.result_data && Object.keys(record.result_data).length > 2) {
                setDetailData(record.result_data);
            } else {
                fetchDetail(record.id, type);
            }
        } else {
            setDetailData(null);
        }
    }, [visible, record, type]);

    const fetchDetail = async (id, recordType) => {
        setLoading(true);
        try {
            let endpoint = '';
            // Determine endpoint based on type
            if (recordType === 'analyses' || (record && (record.type === 'bazi' || record.type === 'ziwei'))) {
                // Fallback if recordType is generic 'analyses' but record has specific type
                const specificType = record.type || 'bazi'; // default to bazi if missing?
                endpoint = `/user/history/analyses/${id}`;
            } else if (recordType === 'divinations' || recordType === 'meihua' || recordType === 'liuyao') {
                endpoint = `/user/history/divinations/${id}`;
            } else if (recordType === 'psychology') {
                endpoint = `/user/history/psychology/${id}`;
            } else if (recordType === 'fusions') {
                endpoint = `/user/history/fusions/${id}`;
            }

            if (!endpoint) {
                // Try to guess from record if type is ambiguous
                if (record.analysis_type) endpoint = `/user/history/analyses/${id}`;
                else if (record.method) endpoint = `/user/history/divinations/${id}`;
                else if (record.test_type) endpoint = `/user/history/psychology/${id}`;
                else throw new Error("Unknown record type");
            }

            const res = await api.get(endpoint);
            if (res.data.success) {
                setDetailData(res.data.data.result_data || res.data.data.fusion_result || {});
            }
        } catch (err) {
            console.error(err);
            message.error("获取详情失败");
        } finally {
            setLoading(false);
        }
    };

    if (!record) return null;

    // --- 样式辅助函数 ---
    const getCardStyle = () => ({
        background: token.colorFillAlter,
        borderRadius: token.borderRadiusLG,
        border: `1px solid ${token.colorBorderSecondary}`,
        boxShadow: 'none', // token.boxShadowTertiary,
        overflow: 'hidden'
    });

    // --- 命理分析 (Bazi) ---
    const renderBaZiDetail = (data) => {
        const sizhu = data.basic_info?.sizhu || data.sizhu || {};
        const wuxing = data.wuxing || {};
        const shishen = data.shishen || {}; // Ten Gods
        const shensha = data.shensha || {}; // Shen Sha
        const dayun = data.dayun_liunian || {}; // Luck Pillars

        // Fix Data Mapping for Wu Xing Scores
        // Backend returns Chinese keys: { "金": 10, "木": 20 ... }
        // Frontend expects English keys for map loop: ['gold', 'wood',...] or needs to map.
        // Let's create a mapped scores object.
        const originScores = wuxing.scores || {};
        const wuxingScores = {
            gold: originScores['金'] || originScores.gold || 0,
            wood: originScores['木'] || originScores.wood || 0,
            water: originScores['水'] || originScores.water || 0,
            fire: originScores['火'] || originScores.fire || 0,
            earth: originScores['土'] || originScores.earth || 0
        };

        if (!sizhu.year && !data.basic_info) return <Empty description="数据结构不匹配" />;

        const renderPillar = (title, gan, zhi, pillarKey) => {
            // Get Ten Gods for this pillar's Heaven Stem
            const pillarShishen = shishen[pillarKey]?.gan || '-';

            return (
                <div style={{
                    ...getCardStyle(),
                    padding: '12px',
                    textAlign: 'center',
                    background: 'linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 100%)',
                    position: 'relative'
                }}>
                    <Text type="secondary" style={{ fontSize: '12px' }}>{title}</Text>
                    <div style={{ fontSize: '12px', color: token.colorTextSecondary, margin: '4px 0' }}>[{pillarShishen}]</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: token.colorPrimary }}>{gan || '-'}</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{zhi || '-'}</div>
                </div>
            );
        };

        return (
            <div className="detail-content">
                <Title level={4} style={{ marginBottom: 24, textAlign: 'center' }}>
                    八字命盘详解
                </Title>

                <Row gutter={[12, 12]} style={{ marginBottom: '24px' }}>
                    <Col span={6}>{renderPillar("年柱", sizhu.year?.[0], sizhu.year?.[1], 'year')}</Col>
                    <Col span={6}>{renderPillar("月柱", sizhu.month?.[0], sizhu.month?.[1], 'month')}</Col>
                    <Col span={6}>{renderPillar("日柱", sizhu.day?.[0], sizhu.day?.[1], 'day')}</Col>
                    <Col span={6}>{renderPillar("时柱", sizhu.hour?.[0], sizhu.hour?.[1], 'hour')}</Col>
                </Row>

                <Card size="small" title="五行能量分布" style={{ marginBottom: 24, ...getCardStyle() }} bordered={false}>
                    <Row gutter={[24, 12]}>
                        {['gold', 'wood', 'water', 'fire', 'earth'].map(key => {
                            const colorMap = { gold: '#fbbf24', wood: '#34d399', water: '#60a5fa', fire: '#f87171', earth: '#a8a29e' };
                            const labelMap = { gold: '金', wood: '木', water: '水', fire: '火', earth: '土' };
                            const score = Number(wuxingScores[key] || 0);
                            // Re-calculate total properly
                            const totalScore = Object.values(wuxingScores).reduce((a, b) => a + Number(b || 0), 0);
                            const percent = totalScore > 0 ? Math.min(100, (score / totalScore) * 100) : 0;

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
                                        <Col span={4} style={{ textAlign: 'right' }}><Text type="secondary">{score.toFixed(1)}</Text></Col>
                                    </Row>
                                </Col>
                            );
                        })}
                    </Row>
                    <div style={{ marginTop: 16, display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
                        <Tag color="red">最强: {wuxing.strongest?.[0] || wuxing.strongest || '-'}</Tag>
                        <Tag color="blue">最弱: {wuxing.weakest?.[0] || wuxing.weakest || '-'}</Tag>
                        <Tag color="green">喜用: {data.xi_yong_shen?.yong_shen?.[0] || '-'}</Tag>
                    </div>
                    {/* DEBUG SECTION - Remove after fix */}
                    <div style={{ marginTop: 12, padding: 8, background: '#000', borderRadius: 4, display: 'none' }}>
                        <Text type="secondary" style={{ fontSize: 10 }}>Debug: {JSON.stringify(wuxing)}</Text>
                    </div>
                    <details style={{ marginTop: 8 }}>
                        <summary style={{ color: token.colorTextSecondary, cursor: 'pointer', fontSize: 12 }}>显示调试数据</summary>
                        <pre style={{ fontSize: 10, overflow: 'auto', maxHeight: 100, marginTop: 4 }}>
                            OriginScores Keys: {JSON.stringify(Object.keys(originScores))}
                            Full Wuxing: {JSON.stringify(wuxing, null, 2)}
                        </pre>
                    </details>
                </Card>

                {/* 大运 & 神煞 (New Sections) */}
                <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
                    <Col span={24}>
                        <Card size="small" title="当前大运" style={getCardStyle()} bordered={false}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                {dayun.current_dayun ? (
                                    <>
                                        <div style={{ textAlign: 'center' }}>
                                            <Text type="secondary">大运</Text>
                                            <div style={{ fontSize: '20px', fontWeight: 'bold' }}>{dayun.current_dayun.ganzhi}</div>
                                        </div>
                                        <div style={{ textAlign: 'center' }}>
                                            <Text type="secondary">起运年份</Text>
                                            <div>{dayun.current_dayun.start_year}年</div>
                                        </div>
                                        <div style={{ textAlign: 'center' }}>
                                            <Text type="secondary">止运年份</Text>
                                            <div>{dayun.current_dayun.end_year}年</div>
                                        </div>
                                    </>
                                ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无大运信息" />}
                            </div>
                        </Card>
                    </Col>
                    <Col span={24}>
                        <Card size="small" title="神煞信息" style={getCardStyle()} bordered={false}>
                            {shensha && Object.keys(shensha).length > 0 ? (
                                <List
                                    grid={{ gutter: 16, column: 2 }}
                                    dataSource={Object.entries(shensha)}
                                    renderItem={([pillar, shas]) => (
                                        <List.Item>
                                            <Card size="small" type="inner" title={`${pillar === 'year' ? '年柱' : pillar === 'month' ? '月柱' : pillar === 'day' ? '日柱' : '时柱'}`}>
                                                {Array.isArray(shas) && shas.length > 0 ? shas.map((sha, idx) => (
                                                    <Tag key={idx} color="purple" style={{ marginBottom: 4 }}>
                                                        {typeof sha === 'object' ? (sha?.name || JSON.stringify(sha)) : sha}
                                                    </Tag>
                                                )) : <Text type="secondary">{typeof shas === 'string' ? shas : '无'}</Text>}
                                            </Card>
                                        </List.Item>
                                    )}
                                />
                            ) : <Text type="secondary">无显著神煞</Text>}
                        </Card>
                    </Col>
                </Row>

                {/* 综合简评 */}
                {(data.summary || data.day_master_analysis) && (
                    <Card size="small" title="综合简评" style={getCardStyle()} bordered={false}>
                        <Paragraph style={{ margin: 0 }}>
                            {data.summary || data.day_master_analysis?.description || "暂无详细评语"}
                        </Paragraph>
                        {/* 喜用建议 */}
                        {data.xi_yong_shen?.analysis && (
                            <>
                                <Divider style={{ margin: '12px 0' }} />
                                <Paragraph>
                                    <Text strong>喜用建议：</Text>
                                    {data.xi_yong_shen.analysis}
                                </Paragraph>
                            </>
                        )}
                        {/* 性格分析 */}
                        {data.personality && (
                            <>
                                <Divider style={{ margin: '12px 0' }} />
                                <Paragraph>
                                    <Text strong>性格特征：</Text>
                                    {typeof data.personality === 'string' ? data.personality :
                                        Object.values(data.personality).join('；')}
                                </Paragraph>
                            </>
                        )}
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
                    dataSource={Object.entries(analysis.palace_scores || {}).sort(([, a], [, b]) => b.score - a.score).slice(0, 3)} // Sort by score desc, show top 3
                    renderItem={([name, data]) => (
                        <List.Item>
                            <Card size="small" style={{ background: 'rgba(255,255,255,0.02)', borderColor: token.colorBorderSecondary }} bordered={true}>
                                <Row justify="space-between" align="middle" style={{ marginBottom: 8 }}>
                                    <Col>
                                        <Space>
                                            <Text strong>{name}</Text>
                                            <Tag color={data.level === '极佳' || data.level === '良好' ? 'green' : data.level === '中等' ? 'orange' : 'red'}>
                                                {data.level}
                                            </Tag>
                                        </Space>
                                    </Col>
                                    <Col>
                                        <Text type="warning" strong style={{ fontSize: 16 }}>{data.score}分</Text>
                                    </Col>
                                </Row>

                                {data.positive_factors && data.positive_factors.length > 0 && (
                                    <div style={{ marginBottom: 4 }}>
                                        <Text type="secondary" style={{ fontSize: 12 }}>加分项：</Text>
                                        <Space wrap size={[4, 4]}>
                                            {data.positive_factors.map((f, i) => (
                                                <Tag key={i} color="blue" bordered={false} style={{ fontSize: 10 }}>{f}</Tag>
                                            ))}
                                        </Space>
                                    </div>
                                )}

                                {data.negative_factors && data.negative_factors.length > 0 && (
                                    <div>
                                        <Text type="secondary" style={{ fontSize: 12 }}>减分项：</Text>
                                        <Space wrap size={[4, 4]}>
                                            {data.negative_factors.map((f, i) => (
                                                <Tag key={i} color="red" bordered={false} style={{ fontSize: 10 }}>{f}</Tag>
                                            ))}
                                        </Space>
                                    </div>
                                )}
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
                    <GuaSymbol symbol={mainGua.lower?.symbol} big />
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
        // Determine type based on data structure if record.test_type not explicit
        const safeTestType = record?.test_type || (data.type_code ? 'mbti' : data.scores && !data.primary ? 'big5' : data.primary && data.secondary ? 'archetype' : data.primary_type ? 'enneagram' : 'unknown');

        const COLORS = {
            mbti: '#722ed1',
            big5: '#13c2c2',
            archetype: '#eb2f96',
            enneagram: '#fa8c16'
        };

        const themeColor = COLORS[safeTestType] || token.colorPrimary;

        const renderMBTI = () => (
            <div className="detail-content">
                <div style={{ textAlign: 'center', padding: '32px 0 24px', background: `linear-gradient(180deg, ${themeColor}15 0%, rgba(0,0,0,0) 100%)`, borderRadius: token.borderRadiusLG, marginBottom: 24 }}>
                    <div style={{
                        fontSize: 48, fontWeight: 900,
                        color: themeColor,
                        marginBottom: 8
                    }}>
                        {data.type_code}
                    </div>
                    <Title level={3} style={{ margin: 0 }}>{data.type_name}</Title>
                    <Paragraph type="secondary" style={{ maxWidth: 600, margin: '12px auto 0' }}>
                        {data.description?.description || data.description}
                    </Paragraph>
                </div>

                <Divider>维度倾向</Divider>
                <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
                    {data.dimensions && Object.entries(data.dimensions).map(([dim, val]) => (
                        <Col span={12} sm={6} key={dim}>
                            <Card size="small" style={{ ...getCardStyle(), textAlign: 'center' }}>
                                <Text strong>{dim}</Text>
                                <Progress
                                    percent={val.clarity || 0}
                                    showInfo={false}
                                    strokeColor={themeColor}
                                    size="small"
                                    style={{ margin: '8px 0' }}
                                />
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                                    <Tag color={themeColor} bordered={false} style={{ margin: 0 }}>{val.preference}</Tag>
                                    <Text type="secondary">{Math.round(val.clarity)}%</Text>
                                </div>
                            </Card>
                        </Col>
                    ))}
                </Row>

                {data.description?.strengths && (
                    <Card size="small" title="性格优势" style={{ ...getCardStyle(), marginBottom: 16 }}>
                        <Space wrap>
                            {Array.isArray(data.description.strengths) ?
                                data.description.strengths.map((s, i) => <Tag key={i} color="green">{s}</Tag>) :
                                <Text>{data.description.strengths}</Text>
                            }
                        </Space>
                    </Card>
                )}

                {data.description?.career && (
                    <Card size="small" title="职业建议" style={getCardStyle()}>
                        <Space wrap>
                            {Array.isArray(data.description.career) ?
                                data.description.career.map((c, i) => <Tag key={i} color="blue">{c}</Tag>) :
                                <Text>{data.description.career}</Text>
                            }
                        </Space>
                    </Card>
                )}
            </div>
        );

        const renderBig5 = () => (
            <div className="detail-content">
                <Card style={{ ...getCardStyle(), marginBottom: 24 }}>
                    <Title level={4} style={{ textAlign: 'center', marginBottom: 16 }}>人格画像</Title>
                    <Paragraph style={{ textAlign: 'center' }}>{data.profile?.summary}</Paragraph>
                </Card>

                <List
                    grid={{ gutter: 16, column: 1, sm: 2 }}
                    dataSource={Object.entries(data.scores || {})}
                    renderItem={([trait, score]) => {
                        const level = data.levels?.[trait];
                        const levelColor = level === '高' ? 'green' : level === '低' ? 'red' : 'orange';
                        return (
                            <List.Item>
                                <Card size="small" style={getCardStyle()}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                                        <Text strong>{data.interpretation?.[trait]?.dimension || trait}</Text>
                                        <Tag color={levelColor}>{level}</Tag>
                                    </div>
                                    <Progress
                                        percent={score}
                                        steps={5}
                                        strokeColor={themeColor}
                                        format={(p) => <Text style={{ fontSize: 12 }}>{p}分</Text>}
                                    />
                                    <Paragraph type="secondary" style={{ fontSize: 12, marginTop: 12, marginBottom: 0 }} ellipsis={{ rows: 2, expandable: true, symbol: '展开' }}>
                                        {data.interpretation?.[trait]?.description || data.interpretation?.[trait]}
                                    </Paragraph>
                                </Card>
                            </List.Item>
                        );
                    }}
                />
            </div>
        );

        const renderArchetype = () => (
            <div className="detail-content">
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                    <Card style={{ ...getCardStyle(), borderColor: themeColor, borderTopWidth: 4 }}>
                        <Tag color={themeColor} style={{ marginBottom: 16 }}>主要原型</Tag>
                        <Title level={2} style={{ color: themeColor, margin: '0 0 8px' }}>{data.primary?.name}</Title>
                        <Text type="secondary" style={{ fontSize: 16 }}>{data.primary?.english}</Text>
                        <Paragraph style={{ marginTop: 16, fontSize: 16 }}>
                            “{data.primary?.motto}”
                        </Paragraph>
                        <div style={{ marginTop: 16 }}>
                            {data.primary?.keywords?.map((k, i) => (
                                <Tag key={i} color="purple">{k}</Tag>
                            ))}
                        </div>
                    </Card>
                </div>

                <Row gutter={[16, 16]}>
                    <Col span={24} md={12}>
                        <Card size="small" title="原型特质" style={getCardStyle()}>
                            <Descriptions column={1} size="small">
                                <Descriptions.Item label="渴望">{data.primary?.core_desire}</Descriptions.Item>
                                <Descriptions.Item label="目标">{data.primary?.goal}</Descriptions.Item>
                                <Descriptions.Item label="恐惧">{data.primary?.fear}</Descriptions.Item>
                                <Descriptions.Item label="天赋">{data.primary?.gift}</Descriptions.Item>
                            </Descriptions>
                        </Card>
                    </Col>
                    <Col span={24} md={12}>
                        {data.secondary && (
                            <Card size="small" title="次要原型" style={getCardStyle()}>
                                <Title level={4} style={{ marginTop: 0 }}>{data.secondary.name}</Title>
                                <Text type="secondary">{data.secondary.english}</Text>
                                <Paragraph style={{ marginTop: 12 }} ellipsis={{ rows: 3 }}>
                                    {data.secondary.description}
                                </Paragraph>
                                <Progress percent={Math.round(data.secondary.score)} size="small" strokeColor={token.colorTextSecondary} />
                            </Card>
                        )}
                    </Col>
                </Row>

                <Card size="small" title="详细分析" style={{ ...getCardStyle(), marginTop: 16 }}>
                    <Paragraph>{data.profile}</Paragraph>
                </Card>
            </div>
        );

        const renderEnneagram = () => (
            <div className="detail-content">
                <div style={{ textAlign: 'center', padding: '32px 0', background: `linear-gradient(135deg, ${themeColor}15 0%, rgba(0,0,0,0) 100%)`, borderRadius: token.borderRadiusLG, marginBottom: 24 }}>
                    <div style={{
                        width: 80, height: 80, lineHeight: '80px',
                        background: themeColor, color: '#fff',
                        fontSize: 36, fontWeight: 'bold',
                        borderRadius: '50%', margin: '0 auto 16px'
                    }}>
                        {data.primary_type}号
                    </div>
                    <Title level={3} style={{ margin: 0 }}>{data.primary_info?.name}</Title>
                    <Text type="secondary">{data.primary_info?.english}</Text>
                </div>

                <Row gutter={[16, 16]}>
                    <Col span={24} md={14}>
                        <Card size="small" title="核心动力" style={getCardStyle()}>
                            <Paragraph><strong>核心渴望：</strong>{data.primary_info?.core_desire}</Paragraph>
                            <Paragraph><strong>核心恐惧：</strong>{data.primary_info?.core_fear}</Paragraph>
                            <Paragraph><strong>基本动机：</strong>{data.primary_info?.core_motivation}</Paragraph>
                        </Card>
                    </Col>
                    <Col span={24} md={10}>
                        <Card size="small" title="侧翼与状态" style={getCardStyle()}>
                            {data.wing && <div style={{ marginBottom: 12 }}><Text strong>侧翼：</Text><Tag color="orange">{data.wing}号</Tag></div>}
                            {data.stress_direction && <div style={{ marginBottom: 12 }}><Text strong>压力方向：</Text><Tag color="red">{data.stress_direction}号</Tag></div>}
                            {data.growth_direction && <div><Text strong>成长方向：</Text><Tag color="green">{data.growth_direction}号</Tag></div>}
                        </Card>
                    </Col>
                </Row>

                <Card size="small" title="成长建议" style={{ ...getCardStyle(), marginTop: 16 }}>
                    <Paragraph>{data.primary_info?.growth_advice}</Paragraph>
                </Card>
            </div>
        );

        switch (safeTestType) {
            case 'mbti': return renderMBTI();
            case 'big5': return renderBig5();
            case 'archetype': return renderArchetype();
            case 'enneagram': return renderEnneagram();
            default: return <Empty description="未知心理测试类型" />;
        }
    };

    // --- 融合分析 (Fusion) ---
    const renderFusionDetail = (data) => {
        return (
            <div className="detail-content">
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                    <Title level={3}>{data.title || "融合分析报告"}</Title>
                    {data.confidence && <Tag color="blue">置信度: {data.confidence}</Tag>}
                </div>
                <Card style={getCardStyle()}>
                    {/* Using pre-wrap to preserve formatting of markdown-like text if not using a markdown renderer */}
                    <div style={{ whiteSpace: 'pre-wrap' }}>
                        {data.report_markdown || JSON.stringify(data.fusion_result, null, 2)}
                    </div>
                </Card>
            </div>
        )
    }

    const renderContent = () => {
        if (loading) {
            return <div style={{ textAlign: 'center', padding: '40px' }}><Spin size="large" tip="加载详细数据..." /></div>;
        }

        if (!detailData) {
            return <Empty description="无法获取详细数据" />;
        }

        const data = detailData;
        const safeType = type === 'analyses' || (record && (record.type === 'bazi' || record.type === 'ziwei')) ? (record.type || 'bazi') : type;

        switch (safeType) {
            case 'bazi': return renderBaZiDetail(data);
            case 'ziwei': return renderZiWeiDetail(data);
            case 'divinations':
            case 'meihua':
            case 'meihua_time':
            case 'meihua_number':
            case 'meihua_text':
            case 'liuyao':
                return renderDivinationDetail(data);
            case 'psychology': return renderPsychologyDetail(data);
            case 'fusions': return renderFusionDetail(data);
            default: return <Empty description="暂不支持的类型" />;
        }
    };

    return (
        <Modal
            title={<Space>
                <Tag color={token.colorPrimary}>{record.type || record.method || record.test_type || '详情'}</Tag>
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
