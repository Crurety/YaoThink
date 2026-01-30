import { create } from 'zustand'
import { persist } from 'zustand/middleware'

/**
 * 用户状态管理
 */
export const useUserStore = create(
    persist(
        (set, get) => ({
            // 状态
            user: null,
            token: null,
            isAuthenticated: false,

            // Actions
            setUser: (user) => set({ user, isAuthenticated: !!user }),

            setToken: (token) => set({ token }),

            login: (user, token) => set({
                user,
                token,
                isAuthenticated: true
            }),

            logout: () => set({
                user: null,
                token: null,
                isAuthenticated: false
            }),

            updateUser: (userData) => set((state) => ({
                user: { ...state.user, ...userData }
            }))
        }),
        {
            name: 'yaothink-user-storage',
            partialize: (state) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated
            })
        }
    )
)


/**
 * 分析记录状态管理
 */
export const useAnalysisStore = create((set, get) => ({
    // 八字分析结果
    baziResult: null,
    // 紫微分析结果
    ziweiResult: null,
    // 易经占卜结果
    yijingResult: null,
    // 心理测试结果
    psychologyResult: null,
    // 融合分析结果
    fusionResult: null,

    // 历史记录
    history: [],

    // Actions
    setBaziResult: (result) => set({ baziResult: result }),
    setZiweiResult: (result) => set({ ziweiResult: result }),
    setYijingResult: (result) => set({ yijingResult: result }),
    setPsychologyResult: (result) => set({ psychologyResult: result }),
    setFusionResult: (result) => set({ fusionResult: result }),

    addToHistory: (record) => set((state) => ({
        history: [record, ...state.history].slice(0, 50)  // 保留最近50条
    })),

    clearHistory: () => set({ history: [] }),

    clearAll: () => set({
        baziResult: null,
        ziweiResult: null,
        yijingResult: null,
        psychologyResult: null,
        fusionResult: null
    })
}))


/**
 * UI状态管理
 */
export const useUIStore = create((set) => ({
    // 主题
    theme: 'dark',
    // 侧边栏是否收起
    sidebarCollapsed: false,
    // 加载状态
    globalLoading: false,
    // 当前激活的模块
    activeModule: null,

    // Actions
    setTheme: (theme) => set({ theme }),
    toggleTheme: () => set((state) => ({
        theme: state.theme === 'dark' ? 'light' : 'dark'
    })),

    setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    toggleSidebar: () => set((state) => ({
        sidebarCollapsed: !state.sidebarCollapsed
    })),

    setGlobalLoading: (loading) => set({ globalLoading: loading }),
    setActiveModule: (module) => set({ activeModule: module })
}))


/**
 * 出生信息状态管理
 */
export const useBirthInfoStore = create(
    persist(
        (set) => ({
            // 当前选中的出生信息
            currentBirthInfo: null,
            // 保存的出生信息列表
            savedBirthInfoList: [],

            // Actions
            setCurrentBirthInfo: (info) => set({ currentBirthInfo: info }),

            saveBirthInfo: (info) => set((state) => {
                const exists = state.savedBirthInfoList.some(
                    item => item.id === info.id
                )
                if (exists) {
                    return {
                        savedBirthInfoList: state.savedBirthInfoList.map(
                            item => item.id === info.id ? info : item
                        )
                    }
                }
                return {
                    savedBirthInfoList: [...state.savedBirthInfoList, info]
                }
            }),

            removeBirthInfo: (id) => set((state) => ({
                savedBirthInfoList: state.savedBirthInfoList.filter(
                    item => item.id !== id
                )
            })),

            clearSavedBirthInfo: () => set({ savedBirthInfoList: [] })
        }),
        {
            name: 'yaothink-birthinfo-storage'
        }
    )
)
