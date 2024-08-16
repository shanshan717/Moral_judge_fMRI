library(tidyverse)
library(ggstatsplot)
library(devtools)
library(bruceR)

# 读取数据
df <- read.csv("/Users/ss/Desktop/bea_data_0501.csv")

# 剔除fmri数据质量不合格的被试
exclude_ids <- c(32, 39, 40, 41, 43, 45, 48, 52, 
                 4, 11, 12, 13, 16, 17, 18, 20)

# 剔除指定被试的数据
df1 <- df[!(df$sub_id %in% exclude_ids), ]

head(df1)

# 查看R函数的帮助文档
?MANOVA
?EMMEANS

# 进行 2×3 的混合设计的重复测量方差分析
anova_result <- MANOVA(
  data = df1,
  dv = "RT.s.",              # 因变量：反应时间
  between = "group",         # 组间变量
  within = "trial_type",     # 组内变量
  subID = "sub_id",           # 试次编号
  sph.correction = "GG"      # 使用 Greenhouse-Geisser 校正
)

# 使用EMMEANS 函数进行简单效应分析
simple_effects <- EMMEANS(
  model = anova_result,         # 使用之前的 ANOVA 结果
  effect = "trial_type",        # 主要关注 trial_type 的效果
  by = "group",                 # 按照 group 进行分层
  contrast = "pairwise",        # 进行成对比较
  p.adjust = "bonferroni"       # 使用 Bonferroni 校正 p 值
)

# 查看简单效应分析结果
print(simple_effects)

# 使用 EMMEANS 函数进一步分析边际均值和多重比较
emmeans_result <- EMMEANS(
  anova_result,
  effect = "trial_type",          # 测试判断类型的效应
  by = "group",                  # 按组别进行分层
  contrast = "pairwise",         # 进行成对比较
  p.adjust = "bonferroni"        # 使用 Bonferroni 校正 p 值
)

# 查看结果
print(emmeans_result)

# 使用 emmip 函数创建交互图
interaction_plot <- emmip(emmeans_result, trial_type ~ group, CIs = TRUE)

# 美化图表
interaction_plot <- interaction_plot +
  theme_minimal() +  # 去掉灰色背景，使用简单的白色背景
  theme(
    panel.border = element_rect(color = "black", fill = NA, linewidth = 1),  # 添加黑色边框
    panel.grid.major = element_line(color = "grey95"),  # 更改网格线颜色
    panel.grid.minor = element_line(color = "grey95")  # 更改次网格线颜色
  ) +
  scale_x_discrete(labels = c("judges", "controls")) +  # 更改x轴标签
  labs(
    title = "Interaction Plot of Judging Type by Group",
    x = "Group",
    y = "Linear Prediction",
    color = "Judging Type"
  )

# 显示图表
print(interaction_plot)

# 保存图表为png文件
ggsave("interaction_plot.png", plot = interaction_plot, width = 8, height = 6, dpi = 300)
