import React from 'react'

/**
 * 紫微斗数命盘组件
 * 按照传统方形排列十二宫
 */
function ZiWeiChart({ palaces }) {
    if (!palaces || palaces.length === 0) return null

    // 宫位在方形盘中的位置映射
    // 传统紫微盘是顺时针排列
    const positionMap = {
        // 上排 (从右到左)
        0: { row: 0, col: 3 },  // 命宫 (位置根据实际计算)
        1: { row: 0, col: 2 },
        2: { row: 0, col: 1 },
        3: { row: 0, col: 0 },
        // 左排 (从上到下)
        4: { row: 1, col: 0 },
        5: { row: 2, col: 0 },
        6: { row: 3, col: 0 },
        // 下排 (从左到右)
        7: { row: 3, col: 1 },
        8: { row: 3, col: 2 },
        9: { row: 3, col: 3 },
        // 右排 (从下到上)
        10: { row: 2, col: 3 },
        11: { row: 1, col: 3 }
    }

    // 创建4x4的网格，中间2x2为命盘中心信息区
    const grid = Array(4).fill(null).map(() => Array(4).fill(null))

    // 按十二宫标准顺序排列
    const standardOrder = [
        "命宫", "兄弟宫", "夫妻宫", "子女宫",
        "财帛宫", "疾厄宫", "迁移宫", "仆役宫",
        "官禄宫", "田宅宫", "福德宫", "父母宫"
    ]

    // 将宫位数据映射到网格
    standardOrder.forEach((palaceName, index) => {
        const palace = palaces.find(p => p.name === palaceName)
        if (palace && positionMap[index]) {
            const { row, col } = positionMap[index]
            grid[row][col] = palace
        }
    })

    return (
        <div className="ziwei-chart">
            {grid.map((row, rowIndex) => (
                row.map((palace, colIndex) => {
                    // 中间区域
                    if ((rowIndex === 1 || rowIndex === 2) && (colIndex === 1 || colIndex === 2)) {
                        if (rowIndex === 1 && colIndex === 1) {
                            return (
                                <div
                                    key={`center-${rowIndex}-${colIndex}`}
                                    className="ziwei-palace center"
                                    style={{ gridColumn: '2 / 4', gridRow: '2 / 4' }}
                                >
                                    <div style={{ textAlign: 'center' }}>
                                        <div style={{ fontSize: 24, marginBottom: 8 }}>☯</div>
                                        <div style={{ color: '#DAA520' }}>紫微斗数命盘</div>
                                    </div>
                                </div>
                            )
                        }
                        return null
                    }

                    if (!palace) {
                        return (
                            <div
                                key={`empty-${rowIndex}-${colIndex}`}
                                className="ziwei-palace"
                                style={{ background: 'rgba(30, 30, 50, 0.3)' }}
                            />
                        )
                    }

                    const mainStars = palace.stars?.main || []
                    const auxStars = palace.stars?.auxiliary || []
                    const shaStars = palace.stars?.sha || []

                    return (
                        <div
                            key={palace.name}
                            className="ziwei-palace"
                            style={{
                                background: palace.name === '命宫'
                                    ? 'rgba(218, 165, 32, 0.1)'
                                    : 'var(--bg-card)'
                            }}
                        >
                            <div className="palace-name">
                                {palace.name}
                                <span style={{
                                    fontSize: 10,
                                    color: '#888',
                                    marginLeft: 4
                                }}>
                                    {palace.position}
                                </span>
                            </div>
                            <div className="palace-stars">
                                {mainStars.map(star => {
                                    // Handle both object (from backend) and string (fallback) formats
                                    const name = star.name || star
                                    const brightness = star.brightness ? `(${star.brightness})` : ''
                                    const hua = star.hua ? `·${star.hua}` : ''

                                    return (
                                        <div key={name} className="star-main">
                                            {name}
                                            <span style={{ fontSize: 10, opacity: 0.8 }}>{brightness}{hua}</span>
                                        </div>
                                    )
                                })}
                                {auxStars.map(star => (
                                    <div key={star} className="star-aux">{star}</div>
                                ))}
                                {shaStars.map(star => (
                                    <div key={star} className="star-sha">{star}</div>
                                ))}
                            </div>
                        </div>
                    )
                })
            ))}
        </div>
    )
}

export default ZiWeiChart
