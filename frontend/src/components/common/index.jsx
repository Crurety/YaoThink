import React from 'react'
import { Card, Button, Typography, Space } from 'antd'

const { Title, Paragraph } = Typography

/**
 * 功能卡片组件
 */
export function FeatureCard({ icon, title, description, color, onClick, disabled }) {
    return (
        <Card
            hoverable={!disabled}
            onClick={!disabled ? onClick : undefined}
            style={{
                height: '100%',
                opacity: disabled ? 0.5 : 1,
                cursor: disabled ? 'not-allowed' : 'pointer',
                background: 'var(--bg-card)',
                borderColor: 'var(--border-color)'
            }}
        >
            <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>{icon}</div>
                <Title level={4} style={{ color, marginBottom: 8 }}>{title}</Title>
                <Paragraph style={{ color: 'var(--text-secondary)', marginBottom: 0 }}>
                    {description}
                </Paragraph>
                {disabled && (
                    <div style={{ marginTop: 12, color: '#666', fontSize: 12 }}>
                        即将上线
                    </div>
                )}
            </div>
        </Card>
    )
}


/**
 * 统计卡片组件
 */
export function StatCard({ title, value, suffix, icon, color }) {
    return (
        <Card size="small" style={{ background: 'var(--bg-card)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                {icon && (
                    <div style={{
                        fontSize: 24,
                        color,
                        opacity: 0.8
                    }}>
                        {icon}
                    </div>
                )}
                <div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: 12 }}>
                        {title}
                    </div>
                    <div style={{
                        fontSize: 24,
                        fontWeight: 'bold',
                        color: color || 'var(--text-primary)'
                    }}>
                        {value}
                        {suffix && <span style={{ fontSize: 14, marginLeft: 4 }}>{suffix}</span>}
                    </div>
                </div>
            </div>
        </Card>
    )
}


/**
 * 标签组组件
 */
export function TagGroup({ tags, colorMap }) {
    return (
        <Space wrap>
            {tags.map(tag => (
                <span
                    key={tag}
                    style={{
                        padding: '4px 12px',
                        borderRadius: 4,
                        background: colorMap?.[tag] || 'var(--bg-secondary)',
                        color: 'var(--text-primary)',
                        fontSize: 12
                    }}
                >
                    {tag}
                </span>
            ))}
        </Space>
    )
}


/**
 * 分割线带标题
 */
export function DividerWithTitle({ title, color }) {
    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            margin: '24px 0',
            gap: 16
        }}>
            <div style={{
                flex: 1,
                height: 1,
                background: 'var(--border-color)'
            }} />
            <span style={{
                color: color || 'var(--accent-gold)',
                fontWeight: 'bold'
            }}>
                {title}
            </span>
            <div style={{
                flex: 1,
                height: 1,
                background: 'var(--border-color)'
            }} />
        </div>
    )
}


/**
 * 五行标签组件
 */
export function WuxingTag({ wuxing }) {
    const colors = {
        '木': '#228B22',
        '火': '#DC143C',
        '土': '#DAA520',
        '金': '#C0C0C0',
        '水': '#1E90FF'
    }

    return (
        <span style={{
            padding: '2px 8px',
            borderRadius: 4,
            background: colors[wuxing] + '30',
            color: colors[wuxing],
            fontWeight: 'bold'
        }}>
            {wuxing}
        </span>
    )
}


/**
 * 加载骨架屏
 */
export function LoadingSkeleton({ rows = 3 }) {
    return (
        <div style={{ padding: 24 }}>
            {Array(rows).fill(0).map((_, i) => (
                <div
                    key={i}
                    style={{
                        height: 20,
                        background: 'linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-card) 50%, var(--bg-secondary) 75%)',
                        backgroundSize: '200% 100%',
                        animation: 'shimmer 1.5s infinite',
                        borderRadius: 4,
                        marginBottom: 12,
                        width: i === rows - 1 ? '60%' : '100%'
                    }}
                />
            ))}
            <style>{`
        @keyframes shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
        </div>
    )
}


/**
 * 空状态组件
 */
export function EmptyState({ icon, title, description, action, actionText }) {
    return (
        <div style={{
            textAlign: 'center',
            padding: 60,
            color: 'var(--text-secondary)'
        }}>
            <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.5 }}>
                {icon || '📭'}
            </div>
            <Title level={4} style={{ color: 'var(--text-secondary)' }}>
                {title || '暂无数据'}
            </Title>
            {description && (
                <Paragraph style={{ color: 'var(--text-muted)' }}>
                    {description}
                </Paragraph>
            )}
            {action && (
                <Button type="primary" onClick={action}>
                    {actionText || '开始'}
                </Button>
            )}
        </div>
    )
}
