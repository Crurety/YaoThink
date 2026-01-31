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

    // Helper to determine star color class
    const getStarColorClass = (name) => {
        const purpleStars = ['紫微', '天府', '天相', '天梁'];
        const redStars = ['太阳', '廉贞', '七杀', '贪狼', '火星', '铃星'];
        const greenStars = ['天机', '太阴', '天同', '武曲', '破军', '巨门'];

        if (purpleStars.some(s => name.includes(s))) return 'purple';
        if (redStars.some(s => name.includes(s))) return 'red';
        if (greenStars.some(s => name.includes(s))) return 'green';
        return 'gold';
    }

    return (
        <div className="ziwei-grid">
            {grid.map((row, rowIndex) => (
                row.map((palace, colIndex) => {
                    // 中间区域
                    if ((rowIndex === 1 || rowIndex === 2) && (colIndex === 1 || colIndex === 2)) {
                        if (rowIndex === 1 && colIndex === 1) {
                            return (
                                <div
                                    key={`center-${rowIndex}-${colIndex}`}
                                    className="ziwei-center"
                                >
                                    <div style={{ zIndex: 2 }}>
                                        <div style={{ fontSize: 32, marginBottom: 8, filter: 'drop-shadow(0 0 10px #7c3aed)' }}>☯</div>
                                        <div style={{ color: '#DAA520', fontWeight: 'bold', letterSpacing: 2 }}>紫微斗数</div>
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
                                className="ziwei-cell"
                                style={{ opacity: 0.3 }}
                            />
                        )
                    }

                    const mainStars = palace.stars?.main || []
                    const auxStars = palace.stars?.auxiliary || []
                    const shaStars = palace.stars?.sha || []
                    const isMingGong = palace.name === '命宫';

                    return (
                        <div
                            key={palace.name}
                            className={`ziwei-cell ${isMingGong ? 'ming-gong' : ''}`}
                        >
                            <div className="palace-name">
                                <span>{palace.name}</span>
                                <span style={{
                                    fontSize: 10,
                                    opacity: 0.6,
                                    fontFamily: 'monospace'
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
                                    const colorClass = getStarColorClass(name);

                                    return (
                                        <div key={name} className={`star-main ${colorClass}`}>
                                            {name}
                                            <span style={{ fontSize: 10, opacity: 0.8 }}>{brightness}{hua}</span>
                                        </div>
                                    )
                                })}

                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                                    {auxStars.map(star => (
                                        <div key={star} className="star-item star-aux">{star}</div>
                                    ))}
                                    {shaStars.map(star => (
                                        <div key={star} className="star-item star-sha">{star}</div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )
                })
            ))}
        </div>
    )
}

export default ZiWeiChart
