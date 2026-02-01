
import React from 'react';
import { Modal, Descriptions, Tag, Typography, Divider, List, Card } from 'antd';

const { Title, Text, Paragraph } = Typography;

const HistoryDetailModal = ({ visible, onClose, record, type }) => {
    if (!record) return null;

    const renderBaZiDetail = (data) => (
        <div className="detail-content">
            <Descriptions title="八字排盘" bordered column={2}>
                <Descriptions.Item label="公历时间">{data.solar_date}</Descriptions.Item>
                <Descriptions.Item label="农历时间">{data.lunar_date}</Descriptions.Item>
                <Descriptions.Item label="年柱">{data.bazi?.year}</Descriptions.Item>
                <Descriptions.Item label="月柱">{data.bazi?.month}</Descriptions.Item>
                <Descriptions.Item label="日柱">{data.bazi?.day}</Descriptions.Item>
                <Descriptions.Item label="时柱">{data.bazi?.hour}</Descriptions.Item>
            </Descriptions>

            <Divider orientation="left">五行分析</Divider>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <Tag color="gold">金: {data.wuxing?.gold || 0}</Tag>
                <Tag color="green">木: {data.wuxing?.wood || 0}</Tag>
                <Tag color="blue">水: {data.wuxing?.water || 0}</Tag>
                <Tag color="volcano">火: {data.wuxing?.fire || 0}</Tag>
                <Tag color="brown">土: {data.wuxing?.earth || 0}</Tag>
            </div>
            <Paragraph style={{ marginTop: 16 }}>
                <strong>喜用神：</strong> {data.wuxing?.favorable}
            </Paragraph>

            <Divider orientation="left">核心分析</Divider>
            <Paragraph>{data.summary}</Paragraph>
        </div>
    );

    const renderZiWeiDetail = (data) => (
        <div className="detail-content">
            <Descriptions title="紫微斗数" bordered column={2}>
                <Descriptions.Item label="命宫主星">{data.ming_gong?.stars?.map(s => s.name).join(' ') || '无'}</Descriptions.Item>
                <Descriptions.Item label="身宫">{data.shen_gong?.name}</Descriptions.Item>
                <Descriptions.Item label="五行局">{data.wuxing_ju}</Descriptions.Item>
            </Descriptions>

            <Divider orientation="left">格局分析</Divider>
            <List
                dataSource={data.patterns || []}
                renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            title={<Tag color="purple">{item.name}</Tag>}
                            description={item.description}
                        />
                    </List.Item>
                )}
            />
        </div>
    );

    const renderDivinationDetail = (data) => (
        <div className="detail-content">
            <Title level={4}>{data.hexagram_name}</Title>
            <Paragraph>{data.hexagram_text}</Paragraph>

            <Divider />
            <Descriptions column={1}>
                <Descriptions.Item label="问题">{record.question}</Descriptions.Item>
                <Descriptions.Item label="起卦方式">{record.method}</Descriptions.Item>
            </Descriptions>

            {data.changing_lines && data.changing_lines.length > 0 && (
                <>
                    <Divider orientation="left">变爻</Divider>
                    <List
                        dataSource={data.changing_lines}
                        renderItem={line => <List.Item>{line}</List.Item>}
                    />
                </>
            )}
        </div>
    );

    const renderPsychologyDetail = (data) => (
        <div className="detail-content">
            <Title level={4}>{record.test_type?.toUpperCase()} 测试结果</Title>
            <Paragraph>
                {JSON.stringify(data, null, 2)}
            </Paragraph>
        </div>
    );

    const renderContent = () => {
        const data = record.result_data || {};
        switch (type) {
            case 'analyses':
                if (record.type === 'bazi') return renderBaZiDetail(data);
                if (record.type === 'ziwei') return renderZiWeiDetail(data);
                return <Paragraph>暂不支持此类型分析详情</Paragraph>;
            case 'divinations':
                return renderDivinationDetail(data);
            case 'psychology':
                return renderPsychologyDetail(data);
            default:
                return <Paragraph>{JSON.stringify(data)}</Paragraph>;
        }
    };

    return (
        <Modal
            title="详情查看"
            open={visible}
            onCancel={onClose}
            footer={null}
            width={800}
        >
            {renderContent()}
        </Modal>
    );
};

export default HistoryDetailModal;
