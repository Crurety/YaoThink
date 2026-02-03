import React from 'react'
import { Typography, Tag, Divider } from 'antd'

const { Paragraph } = Typography

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
            .replace(/## \*\*(.+?)\*\*/g, '<h3 style="color:#DAA520;margin:16px 0 8px">$1</h3>')
            .replace(/## (.+?)(<br\/>|$)/g, '<h3 style="color:#DAA520;margin:16px 0 8px">$1</h3>')
            .replace(/\*\*(.+?)\*\*/g, '<b style="color:#fbbf24">$1</b>')
            .replace(/✅/g, '<span style="color:#10b981">✅</span>')
            .replace(/❌/g, '<span style="color:#ef4444">❌</span>')
            .replace(/⚠️/g, '<span style="color:#f59e0b">⚠️</span>')
            .replace(/📈/g, '<span style="color:#3b82f6">📈</span>')
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
        health: { color: 'red', label: '健康提示', bg: 'rgba(239, 68, 68, 0.05)', border: 'rgba(239, 68, 68, 0.2)' }
    }

    // 渲染单个维度卡片
    const renderDimensionCard = (key, items) => {
        const config = dimensionConfig[key] || { color: 'default', label: key, bg: 'rgba(100,100,100,0.05)', border: 'rgba(100,100,100,0.2)' }

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
                            color: '#e2e8f0',
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
    const dimensionOrder = ['core', 'luck', 'career', 'wealth', 'personality', 'relationship', 'advice', 'shensha', 'health']

    return (
        <div style={{ ...style }}>
            {/* 纯文本内容 */}
            {content && !structured && (
                <Paragraph style={{ fontSize: 15, color: '#e2e8f0' }}>
                    <div dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }} />
                </Paragraph>
            )}

            {/* 结构化多维度内容 */}
            {structured && (
                <div>
                    {showDividers && Object.keys(structured).length > 0 && (
                        <Divider style={{ borderColor: 'rgba(255,255,255,0.1)', color: '#94a3b8', margin: '16px 0' }}>
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
            )}

            {/* 纯文本补充（当有structured时） */}
            {content && structured && (
                <Paragraph style={{ fontSize: 14, color: '#94a3b8', marginTop: 16 }}>
                    <div dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }} />
                </Paragraph>
            )}
        </div>
    )
}

export default MarkdownViewer
