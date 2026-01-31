import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useUserStore } from '../../stores'

/**
 * 私有路由守卫组件
 * 未登录用户将被重定向到首页
 */
function PrivateRoute({ children, onAuthRequired }) {
    const { isAuthenticated } = useUserStore()
    const location = useLocation()

    if (!isAuthenticated) {
        // 调用认证回调（弹出登录框）
        if (onAuthRequired) {
            onAuthRequired()
        }
        // 重定向到首页，保存原始路径
        return <Navigate to="/" state={{ from: location }} replace />
    }

    return children
}

export default PrivateRoute
