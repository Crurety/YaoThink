import React from 'react'

// 五行颜色映射
const WUXING_COLORS = {
    '木': '#228B22',
    '火': '#DC143C',
    '土': '#DAA520',
    '金': '#C0C0C0',
    '水': '#1E90FF'
}

// 天干五行
const GAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

// 地支五行
const ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

/**
 * 八字命盘组件
 * @param {Object} sizhu - 四柱对象 { year: "庚午", month: "辛巳", day: "甲子", hour: "己巳" }
 */
function BaZiChart({ sizhu }) {
    if (!sizhu) return null

    const pillars = [
        { title: '年柱', value: sizhu.year },
        { title: '月柱', value: sizhu.month },
        { title: '日柱', value: sizhu.day },
        { title: '时柱', value: sizhu.hour }
    ]

    return (
        <div className="bazi-chart">
            {pillars.map(pillar => {
                const gan = pillar.value[0]
                const zhi = pillar.value[1]
                const ganWuxing = GAN_WUXING[gan]
                const zhiWuxing = ZHI_WUXING[zhi]

                return (
                    <div key={pillar.title} className="bazi-pillar">
                        <div className="bazi-pillar-title">{pillar.title}</div>
                        <div
                            className="bazi-gan"
                            style={{ color: WUXING_COLORS[ganWuxing] }}
                            title={`${gan} - ${ganWuxing}`}
                        >
                            {gan}
                        </div>
                        <div
                            className="bazi-zhi"
                            style={{ color: WUXING_COLORS[zhiWuxing] }}
                            title={`${zhi} - ${zhiWuxing}`}
                        >
                            {zhi}
                        </div>
                        <div style={{
                            marginTop: 8,
                            fontSize: 12,
                            color: 'var(--text-muted)'
                        }}>
                            {ganWuxing}/{zhiWuxing}
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

export default BaZiChart
