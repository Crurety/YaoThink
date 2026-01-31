import React, { useEffect } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useUserStore } from '../../stores'

/**
 * 私有路由守卫组件
 * 未登录用户将被重定向到首页并弹出登录框
 */
function PrivateRoute({ children, onAuthRequired }) {
    const { isAuthenticated } = useUserStore()
    const location = useLocation()

    useEffect(() => {
        // 未登录时触发认证回调
        if (!isAuthenticated && onAuthRequired) {
            onAuthRequired()
        }
    }, [isAuthenticated, onAuthRequired])

    if (!isAuthenticated) {
        // 重定向到首页，保存原始路径
        return <Navigate to="/" state={{ from: location }} replace />
    }

    return children
}

export default PrivateRoute
