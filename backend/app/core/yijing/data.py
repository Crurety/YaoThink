
"""
玄心理命 - 六十四卦详细解读数据
"""

GUA_INTERPRETATIONS = {
    "乾为天": {
        "summary": "元亨利贞，刚健中正",
        "keywords": ["刚健", "进取", "领导", "成功"],
        "fortune": "大吉，进取必成，但需防骄傲",
        "career": "事业顺利，可大展宏图",
        "relationship": "桃花旺盛，但需真诚",
        "wealth": "财运亨通，利于投资"
    },
    "坤为地": {
        "summary": "元亨，利牝马之贞",
        "keywords": ["柔顺", "包容", "谨慎", "守成"],
        "fortune": "吉，宜守不宜攻",
        "career": "稳扎稳打，不宜冒进",
        "relationship": "顺从柔和，利于感情",
        "wealth": "积少成多，稳定增长"
    },
    "水雷屯": {
        "summary": "元亨利贞，勿用有攸往",
        "keywords": ["艰难", "初创", "等待", "积累"],
        "fortune": "初期困难，坚持必成",
        "career": "创业艰难，需要耐心",
        "relationship": "感情初期磨合较多",
        "wealth": "暂时困难，后有转机"
    },
    "山水蒙": {
        "summary": "亨，匪我求童蒙，童蒙求我",
        "keywords": ["启蒙", "学习", "迷惑", "求教"],
        "fortune": "需要学习和请教",
        "career": "多学习，虚心请教",
        "relationship": "需要时间了解对方",
        "wealth": "理财需要学习"
    },
    "水天需": {
        "summary": "有孚，光亨，贞吉",
        "keywords": ["等待", "时机", "饮食", "宴乐"],
        "fortune": "时机未到，宜耐心等待",
        "career": "暂缓行动，积蓄力量",
        "relationship": "感情需要时间培养",
        "wealth": "财运平稳，不宜急进"
    },
    "天水讼": {
        "summary": "有孚，窒惕，中吉，终凶",
        "keywords": ["争执", "诉讼", "矛盾", "警惕"],
        "fortune": "易生口舌，凡事退让",
        "career": "避免冲突，以和为贵",
        "relationship": "容易争吵，多沟通",
        "wealth": "防破财，不宜投资"
    },
    "地水师": {
        "summary": "贞，丈人吉，无咎",
        "keywords": ["军队", "出征", "严肃", "纪律"],
        "fortune": "行事需严谨，有贵人",
        "career": "可担重任，需团队合作",
        "relationship": "感情专一，需主动",
        "wealth": "正财较好，偏财少"
    },
    "水地比": {
        "summary": "吉，原筮，元永贞，无咎",
        "keywords": ["亲近", "合作", "依附", "和谐"],
        "fortune": "人际关系好，有贵人",
        "career": "适合合作，团队和谐",
        "relationship": "感情融洽，相亲相爱",
        "wealth": "合作生财"
    },
    "风天小畜": {
        "summary": "亨，密云不雨，自我西郊",
        "keywords": ["积蓄", "暂时", "阻碍", "小成"],
        "fortune": "时机未成熟，宜积蓄",
        "career": "小有成就，不可贪大",
        "relationship": "有小波折，需忍耐",
        "wealth": "积少成多"
    },
    "天泽履": {
        "summary": "履虎尾，不咥人，亨",
        "keywords": ["实践", "冒险", "礼仪", "小心"],
        "fortune": "虽有险阻，有惊无险",
        "career": "脚踏实地，步步为营",
        "relationship": "相敬如宾，注重礼仪",
        "wealth": "稳健经营"
    },
    "地天泰": {
        "summary": "小往大来，吉亨",
        "keywords": ["通达", "和谐", "安泰", "顺利"],
        "fortune": "诸事顺遂，大吉大利",
        "career": "事业蒸蒸日上",
        "relationship": "感情和睦，喜结连理",
        "wealth": "财运亨通"
    },
    "天地否": {
        "summary": "否之匪人，不利君子贞，大往小来",
        "keywords": ["闭塞", "不通", "困难", "孤独"],
        "fortune": "诸事不顺，宜守待时",
        "career": "小人当道，怀才不遇",
        "relationship": "感情冷淡，易分手",
        "wealth": "财运低迷"
    },
    "天火同人": {
        "summary": "同人于野，亨，利涉大川，利君子贞",
        "keywords": ["合作", "团结", "志同", "道合"],
        "fortune": "得人相助，大业可成",
        "career": "团队协作，共创辉煌",
        "relationship": "情投意合，相处融洽",
        "wealth": "合伙求财"
    },
    "火天大有": {
        "summary": "元亨",
        "keywords": ["富有", "盛大", "收获", "光明"],
        "fortune": "运势极佳，如日中天",
        "career": "事业有成，名利双收",
        "relationship": "感情丰富，受人欢迎",
        "wealth": "财源广进"
    },
    "地山谦": {
        "summary": "亨，君子有终",
        "keywords": ["谦虚", "低调", "礼让", "内敛"],
        "fortune": "谦虚受益，吉无不利",
        "career": "以退为进，受人尊敬",
        "relationship": "互敬互爱，长久",
        "wealth": "平稳增长"
    },
    "雷地豫": {
        "summary": "利建侯行师",
        "keywords": ["快乐", "安逸", "准备", "顺动"],
        "fortune": "顺心如意，由于准备充分",
        "career": "得心应手，注意安逸",
        "relationship": "快乐幸福，相处愉快",
        "wealth": "财运不错"
    },
    "泽雷随": {
        "summary": "元亨利贞，无咎",
        "keywords": ["跟随", "顺从", "随时", "应变"],
        "fortune": "顺应时势，可得吉兆",
        "career": "跟随领导，顺势而为",
        "relationship": "夫唱妇随，和谐",
        "wealth": "随缘得财"
    },
    "山风蛊": {
        "summary": "元亨，利涉大川，先甲三日，后甲三日",
        "keywords": ["腐败", "整治", "革新", "麻烦"],
        "fortune": "有隐患，需及时整治",
        "career": "整顿内部，解决问题",
        "relationship": "感情有隔阂，需沟通",
        "wealth": "防漏财"
    },
    "地泽临": {
        "summary": "元亨利贞，至于八月有凶",
        "keywords": ["亲临", "统御", "观察", "时机"],
        "fortune": "时运正佳，宜把握",
        "career": "领导力强，管理有方",
        "relationship": "感情升温，注意时机",
        "wealth": "目前财运好"
    },
    "风地观": {
        "summary": "盥而不荐，有孚颙若",
        "keywords": ["观察", "展示", "榜样", "沉思"],
        "fortune": "静观其变，不宜妄动",
        "career": "多看少动，寻找机会",
        "relationship": "互相了解，注重精神",
        "wealth": "观望为主"
    },
    "火雷噬嗑": {
        "summary": "亨，利用狱",
        "keywords": ["咬合", "刑法", "障碍", "去除"],
        "fortune": "遇阻碍，需强硬排除",
        "career": "清除障碍，方可前进",
        "relationship": "有争执，需磨合",
        "wealth": "辛苦得财"
    },
    "山火贲": {
        "summary": "亨，小利有攸往",
        "keywords": ["装饰", "文饰", "外表", "礼仪"],
        "fortune": "表面光鲜，主要小事",
        "career": "注重形象，因文获利",
        "relationship": "外表吸引，注重情调",
        "wealth": "花销较大"
    },
    "山地剥": {
        "summary": "不利有攸往",
        "keywords": ["剥落", "衰退", "小人", "侵蚀"],
        "fortune": "运势衰退，宜守",
        "career": "防小人，不宜扩张",
        "relationship": "感情破裂，被排挤",
        "wealth": "损财"
    },
    "地雷复": {
        "summary": "亨，出入无疾，朋来无咎",
        "keywords": ["复兴", "回归", "希望", "循环"],
        "fortune": "否极泰来，好运将至",
        "career": "重新开始，逐渐好转",
        "relationship": "破镜重圆，旧情复燃",
        "wealth": "财运回升"
    },
    "天雷无妄": {
        "summary": "元亨利贞，其匪正有眚，不利有攸往",
        "keywords": ["真实", "自然", "意外", "无妄"],
        "fortune": "顺其自然，不可强求",
        "career": "脚踏实地，勿存妄想",
        "relationship": "真诚相待，不可欺骗",
        "wealth": "正财可得"
    },
    "山天大畜": {
        "summary": "利贞，不家食，吉，利涉大川",
        "keywords": ["积蓄", "停止", "富有", "充实"],
        "fortune": "积少成多，大有收获",
        "career": "才华施展，积蓄力量",
        "relationship": "感情深厚，积蓄情感",
        "wealth": "大有积蓄"
    },
    "山雷颐": {
        "summary": "贞吉，观颐，自求口实",
        "keywords": ["养育", "颐养", "饮食", "言语"],
        "fortune": "祸从口出，病从口入",
        "career": "言语谨慎，修身养性",
        "relationship": "相互照顾，注重沟通",
        "wealth": "适合餐饮"
    },
    "泽风大过": {
        "summary": "栋桡，利有攸往，亨",
        "keywords": ["过重", "压力", "非常", "过度"],
        "fortune": "压力巨大，需非常手段",
        "career": "任务繁重，需抗压",
        "relationship": "负担过重，或老少配",
        "wealth": "大进大出"
    },
    "坎为水": {
        "summary": "习坎，有孚，维心亨，行有尚",
        "keywords": ["险陷", "重重", "习以为常", "如水"],
        "fortune": "重重困难，需坚韧",
        "career": "处于低谷，努力坚持",
        "relationship": "波折多，需经考验",
        "wealth": "财运不佳"
    },
    "离为火": {
        "summary": "利贞，亨，畜牝牛吉",
        "keywords": ["附丽", "光明", "依赖", "热情"],
        "fortune": "前途光明，但需依附",
        "career": "才华出众，适合合作",
        "relationship": "热情如火，但易反复",
        "wealth": "财运旺"
    },
    "泽山咸": {
        "summary": "亨，利贞，取女吉",
        "keywords": ["感应", "情感", "交流", "迅速"],
        "fortune": "心有灵犀，诸事顺遂",
        "career": "人际关系好，沟通顺畅",
        "relationship": "彼此爱慕，速成",
        "wealth": "和气生财"
    },
    "雷风恒": {
        "summary": "亨，无咎，利贞，利有攸往",
        "keywords": ["恒久", "坚持", "长远", "稳定"],
        "fortune": "持之以恒，终有成就",
        "career": "工作稳定，长期发展",
        "relationship": "白头偕老，长久",
        "wealth": "长线投资"
    },
    "天山遁": {
        "summary": "亨，小利贞",
        "keywords": ["退避", "隐居", "逃避", "保存"],
        "fortune": "退一步海阔天空",
        "career": "急流勇退，明哲保身",
        "relationship": "有缘无份，宜放手",
        "wealth": "见好就收"
    },
    "雷天大壮": {
        "summary": "利贞",
        "keywords": ["壮大", "强盛", "莽撞", "声势"],
        "fortune": "气势强盛，不可鲁莽",
        "career": "事业扩展，需防过激",
        "relationship": "过于强势，需柔和",
        "wealth": "财力雄厚"
    },
    "火地晋": {
        "summary": "康侯用锡马蕃庶，昼日三接",
        "keywords": ["晋升", "前进", "受赏", "光明"],
        "fortune": "旭日东升，步步高升",
        "career": "升职加薪，受重视",
        "relationship": "感情进展，受欢迎",
        "wealth": "财源滚滚"
    },
    "地火明夷": {
        "summary": "利艰贞",
        "keywords": ["受伤", "晦暗", "掩饰", "受难"],
        "fortune": "如日落山，运势晦暗",
        "career": "怀才不遇，被压制",
        "relationship": "有裂痕，心情低落",
        "wealth": "破财"
    },
    "风火家人": {
        "summary": "利女贞",
        "keywords": ["家庭", "内部", "责任", "温暖"],
        "fortune": "家和万事兴",
        "career": "内部团结，稳固基础",
        "relationship": "家庭责任，幸福",
        "wealth": "积庆之家"
    },
    "火泽睽": {
        "summary": "小事吉",
        "keywords": ["乖离", "背离", "反目", "异心"],
        "fortune": "人心不齐，事多阻碍",
        "career": "意见分歧，合作难",
        "relationship": "争吵冷战，貌合神离",
        "wealth": "财散"
    },
    "水山蹇": {
        "summary": "利西南，不利东北，利见大人，贞吉",
        "keywords": ["艰难", "险阻", "停止", "反省"],
        "fortune": "寸步难行，宜止不宜进",
        "career": "困难重重，寻求帮助",
        "relationship": "无法沟通，停滞",
        "wealth": "难求财"
    },
    "雷水解": {
        "summary": "利西南，无所往，其来复吉，有攸往，夙吉",
        "keywords": ["解脱", "缓解", "解决", "宽松"],
        "fortune": "困难消除，雨过天晴",
        "career": "问题解决，轻松发展",
        "relationship": "误会冰释，重归于好",
        "wealth": "困境解脱"
    },
    "山泽损": {
        "summary": "有孚，元吉，无咎，可贞，利有攸往",
        "keywords": ["减损", "牺牲", "奉献", "先失"],
        "fortune": "先损后益，吃亏是福",
        "career": "投入成本，后期获益",
        "relationship": "付出真情，虽苦亦甜",
        "wealth": "花钱消灾"
    },
    "风雷益": {
        "summary": "利有攸往，利涉大川",
        "keywords": ["增益", "获利", "帮助", "成长"],
        "fortune": "损上益下，大吉大利",
        "career": "得贵人助，事业有成",
        "relationship": "良缘天作，互补",
        "wealth": "获利丰厚"
    },
    "泽天夬": {
        "summary": "扬于王庭，孚号，有厉，告自邑，不利即戎，利有攸往",
        "keywords": ["决断", "清除", "果断", "公开"],
        "fortune": "当机立断，清除隐患",
        "career": "解决难题，不可拖延",
        "relationship": "分手或摊牌，不论拖",
        "wealth": "结算"
    },
    "天风姤": {
        "summary": "女壮，勿用取女",
        "keywords": ["相遇", "邂逅", "机遇", "由于"],
        "fortune": "不期而遇，可能有变",
        "career": "遇新机会，需辨真假",
        "relationship": "桃花泛滥，未必正缘",
        "wealth": "意外之财"
    },
    "泽地萃": {
        "summary": "亨，王假有庙，利见大人，亨，利贞，用大牲吉，利有攸往",
        "keywords": ["聚集", "精英", "繁荣", "团队"],
        "fortune": "群英荟萃，运势昌隆",
        "career": "人才济济，事业兴旺",
        "relationship": "追求者多，聚会",
        "wealth": "财源汇聚"
    },
    "地风升": {
        "summary": "元亨，用见大人，勿恤，南征吉",
        "keywords": ["上升", "生长", "积小", "成大"],
        "fortune": "如树生长，步步高升",
        "career": "稳步发展，前程似锦",
        "relationship": "感情升温，日久生情",
        "wealth": "资产增值"
    },
    "泽水困": {
        "summary": "亨，贞，大人吉，无咎，有言不信",
        "keywords": ["困境", "穷困", "考验", "守正"],
        "fortune": "身处困境，才智难展",
        "career": "资源匮乏，进退两难",
        "relationship": "感情受困，无力感",
        "wealth": "破财"
    },
    "水风井": {
        "summary": "改邑不改井，无丧无得，往来井井",
        "keywords": ["井养", "资源", "无穷", "服务"],
        "fortune": "安身立命，守正不移",
        "career": "坚守岗位，服务他人",
        "relationship": "平淡是真，细水长流",
        "wealth": "固定收入"
    },
    "泽火革": {
        "summary": "己日乃孚，元亨利贞，悔亡",
        "keywords": ["变革", "去旧", "改变", "时机"],
        "fortune": "顺应时变，大变革",
        "career": "转型升级，由于创新",
        "relationship": "旧情结束，新恋情",
        "wealth": "改革获利"
    },
    "火风鼎": {
        "summary": "元吉，亨",
        "keywords": ["鼎新", "合作", "稳重", "取新"],
        "fortune": "三足鼎立，稳重吉利",
        "career": "建立基业，得力助手",
        "relationship": "多角关系，或稳固",
        "wealth": "合资获利"
    },
    "震为雷": {
        "summary": "亨，震来虩虩，笑言哑哑，震惊百里，不丧匕鬯",
        "keywords": ["震动", "惊恐", "奋起", "长子"],
        "fortune": "虽有惊恐，终无大碍",
        "career": "声势浩大，处变不惊",
        "relationship": "争吵剧烈，后和好",
        "wealth": "动中求财"
    },
    "艮为山": {
        "summary": "艮其背，不获其身，行其庭，不见其人，无咎",
        "keywords": ["停止", "稳重", "阻碍", "静止"],
        "fortune": "动静失宜，宜止则止",
        "career": "停滞不前，宜休整",
        "relationship": "关系冷淡，难进展",
        "wealth": "资金冻结"
    },
    "风山渐": {
        "summary": "女归吉，利贞",
        "keywords": ["循序", "渐进", "出嫁", "归宿"],
        "fortune": "循序渐进，水到渠成",
        "career": "按部就班，由于积累",
        "relationship": "如礼如仪，好事多磨",
        "wealth": "慢钱"
    },
    "雷泽归妹": {
        "summary": "征凶，无攸利",
        "keywords": ["嫁娶", "非常", "错位", "急进"],
        "fortune": "违背常规，结果不佳",
        "career": "急功近利，必有损失",
        "relationship": "畸形恋情，不伦之恋",
        "wealth": "贪小失大"
    },
    "雷火丰": {
        "summary": "亨，王假之，勿忧，宜日中",
        "keywords": ["丰盛", "顶点", "光明", "盛大"],
        "fortune": "运势极盛，需防盛极",
        "career": "如日中天，成就巨大",
        "relationship": "热恋期，激情",
        "wealth": "大富"
    },
    "火山旅": {
        "summary": "小亨，旅贞吉",
        "keywords": ["旅行", "漂泊", "不安定", "过客"],
        "fortune": "奔波劳碌，不安定",
        "career": "出差频繁，跳槽",
        "relationship": "聚少离多，不稳定",
        "wealth": "外地求财"
    },
    "巽为风": {
        "summary": "小亨，利有攸往，利见大人",
        "keywords": ["顺从", "进入", "谦逊", "风"],
        "fortune": "顺水推舟，无孔不入",
        "career": "深入基层，顺势而为",
        "relationship": "温柔体贴，顺从",
        "wealth": "流动资金"
    },
    "兑为泽": {
        "summary": "亨，利贞",
        "keywords": ["喜悦", "口舌", "交流", "少女"],
        "fortune": "喜气洋洋，口才得利",
        "career": "善于交际，说服力强",
        "relationship": "甜言蜜语，开心",
        "wealth": "可得财"
    },
    "风水涣": {
        "summary": "亨，王假有庙，利涉大川，利贞",
        "keywords": ["离散", "化解", "传播", "远行"],
        "fortune": "冰释前嫌，厄运消散",
        "career": "虽然涣散，利于重组",
        "relationship": "离别，或误会消除",
        "wealth": "散财"
    },
    "水泽节": {
        "summary": "亨，苦节不可贞",
        "keywords": ["节制", "规矩", "有限", "止损"],
        "fortune": "适可而止，过犹不及",
        "career": "制定规矩，节约成本",
        "relationship": "发乎情止乎礼",
        "wealth": "节流"
    },
    "风泽中孚": {
        "summary": "豚鱼吉，利涉大川，利贞",
        "keywords": ["诚信", "感应", "信实", "中心"],
        "fortune": "以诚待人，必然获信",
        "career": "信用第一，合作顺利",
        "relationship": "真心实意，心心相印",
        "wealth": "信誉生财"
    },
    "雷山小过": {
        "summary": "亨，利贞，可小事，不可大事，飞鸟遗之音，不宜上，宜下，大吉",
        "keywords": ["小过", "过度", "飞鸟", "小事"],
        "fortune": "小事可成，大事不宜",
        "career": "稍有过失，需谨慎",
        "relationship": "略有争执，小别扭",
        "wealth": "小财"
    },
    "水火既济": {
        "summary": "亨，小利贞，初吉终乱",
        "keywords": ["完成", "完美", "盛极", "守成"],
        "fortune": "功德圆满，需防盛极必衰",
        "career": "目标达成，安享成果",
        "relationship": "终成眷属，完美",
        "wealth": "收益落袋"
    },
    "火水未济": {
        "summary": "亨，小狐汔济，濡其尾，无攸利",
        "keywords": ["未成", "希望", "再接再厉", "循环"],
        "fortune": "尚未成功，仍需努力",
        "career": "新的开始，前途无量",
        "relationship": "还未确定，长跑",
        "wealth": "未来可期"
    }
}
