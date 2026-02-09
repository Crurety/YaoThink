import React from 'react'
import { Tag, Divider } from 'antd'

/**
 * MarkdownViewer - AI分析数据Markdown展示器
 * 
 * 支持的Markdown语法:
 * - ## 标题
 * - **粗体**
 * - - 列表项
 * - ✅ ❌ ⚠️ 📈 emoji标记
 * - \n 换行
 */
const MarkdownViewer = ({
    content,
    structured,
    style = {},
    showDividers = true
}) => {

    // Markdown转HTML渲染函数
    const renderMarkdown = (text) => {
        if (!text) return ''
        return text
            .replace(/\n/g, '<br/>')
            .replace(/## \*\*(.+?)\*\*/g, '<h3 style="color:var(--accent-gold);margin:16px 0 8px">$1</h3>')
            .replace(/## (.+?)(<br\/>|$)/g, '<h3 style="color:var(--accent-gold);margin:16px 0 8px">$1</h3>')
            .replace(/\*\*(.+?)\*\*/g, '<b style="color:var(--accent-gold)">$1</b>')
            .replace(/✅/g, '<span style="color:var(--accent-green)">✅</span>')
            .replace(/❌/g, '<span style="color:var(--accent-red)">❌</span>')
            .replace(/⚠️/g, '<span style="color:var(--accent-gold)">⚠️</span>')
            .replace(/📈/g, '<span style="color:var(--primary)">📈</span>')
    }

    // 维度配置：颜色和标签
    const dimensionConfig = {
        core: { color: 'gold', label: '核心格局', bg: 'rgba(218, 165, 32, 0.08)', border: 'rgba(218, 165, 32, 0.3)' },
        career: { color: 'green', label: '事业格局', bg: 'rgba(52, 211, 153, 0.05)', border: 'rgba(52, 211, 153, 0.2)' },
        personality: { color: 'purple', label: '性格剖析', bg: 'rgba(167, 139, 250, 0.05)', border: 'rgba(167, 139, 250, 0.2)' },
        advice: { color: 'orange', label: '发展建议', bg: 'rgba(251, 191, 36, 0.05)', border: 'rgba(251, 191, 36, 0.2)' },
        wealth: { color: 'volcano', label: '财运格局', bg: 'rgba(245, 158, 11, 0.05)', border: 'rgba(245, 158, 11, 0.2)' },
        relationship: { color: 'pink', label: '人际感情', bg: 'rgba(236, 72, 153, 0.05)', border: 'rgba(236, 72, 153, 0.2)' },
        luck: { color: 'cyan', label: '大运流年', bg: 'rgba(56, 189, 248, 0.05)', border: 'rgba(56, 189, 248, 0.2)' },
        shensha: { color: 'magenta', label: '神煞启示', bg: 'rgba(244, 114, 182, 0.05)', border: 'rgba(244, 114, 182, 0.2)' },
        health: { color: 'red', label: '健康提示', bg: 'rgba(239, 68, 68, 0.05)', border: 'rgba(239, 68, 68, 0.2)' },
        // 易经专用维度
        trigram: { color: 'geekblue', label: '卦象分析', bg: 'rgba(59, 130, 246, 0.08)', border: 'rgba(59, 130, 246, 0.3)' },
        relation: { color: 'lime', label: '体用关系', bg: 'rgba(132, 204, 22, 0.08)', border: 'rgba(132, 204, 22, 0.3)' },
        moving: { color: 'volcano', label: '动爻详解', bg: 'rgba(255, 77, 79, 0.08)', border: 'rgba(255, 77, 79, 0.3)' },
        change: { color: 'purple', label: '变卦趋势', bg: 'rgba(147, 51, 234, 0.08)', border: 'rgba(147, 51, 234, 0.3)' }
    }

    // 渲染单个维度卡片
    const renderDimensionCard = (key, items) => {
        const config = dimensionConfig[key] || { color: 'default', label: key, bg: 'var(--bg-card)', border: 'var(--border-default)' }

        return (
            <div
                key={key}
                style={{
                    background: config.bg,
                    padding: 16,
                    borderRadius: 8,
                    border: `1px solid ${config.border}`,
                    marginBottom: 16
                }}
            >
                <Tag color={config.color} style={{ marginBottom: 12, fontSize: 13 }}>{config.label}</Tag>
                {items.map((text, i) => (
                    <div
                        key={i}
                        style={{
                            color: 'var(--text-primary)',
                            fontSize: 14,
                            lineHeight: 1.8,
                            marginBottom: i < items.length - 1 ? 12 : 0
                        }}
                        dangerouslySetInnerHTML={{ __html: renderMarkdown(text) }}
                    />
                ))}
            </div>
        )
    }

    // 维度显示顺序
    const dimensionOrder = ['core', 'trigram', 'relation', 'moving', 'change', 'luck', 'career', 'wealth', 'personality', 'relationship', 'advice', 'shensha', 'health']

    return (
        <div style={{ ...style }}>
            {/* 结构化多维度内容 */}
            {structured ? (
                <div>
                    {showDividers && Object.keys(structured).length > 0 && (
                        <Divider style={{ borderColor: 'var(--border-default)', color: 'var(--text-muted)', margin: '16px 0' }}>
                            多维深度分析
                        </Divider>
                    )}

                    {/* 按预定顺序渲染各维度 */}
                    {dimensionOrder.map(key =>
                        structured[key] && structured[key].length > 0
                            ? renderDimensionCard(key, structured[key])
                            : null
                    )}

                    {/* 渲染未在预定顺序中的其他维度 */}
                    {Object.keys(structured)
                        .filter(key => !dimensionOrder.includes(key) && structured[key]?.length > 0)
                        .map(key => renderDimensionCard(key, structured[key]))
                    }
                </div>
            ) : content ? (
                <div
                    style={{
                        color: 'var(--text-primary)',
                        fontSize: 14,
                        lineHeight: 1.8,
                        padding: 16,
                        borderRadius: 8,
                        background: 'var(--bg-input)', // 适配日夜间
                        border: '1px solid var(--border-default)'
                    }}
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
                />
            ) : null}
        </div>
    )
}

export default MarkdownViewer
