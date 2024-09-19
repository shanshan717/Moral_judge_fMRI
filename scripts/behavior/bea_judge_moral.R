library(tidyverse)
library(ggstatsplot)
library(devtools)
library(bruceR)
library(ggplot2)
library(dplyr)
library(emmeans)

# 读取数据
df <- read.csv("/Users/ss/Desktop/bea_data_0501.csv")

# 剔除fmri数据质量不合格的被试
exclude_ids <- c(32, 39, 40, 41, 43, 45, 48, 52, 
                 4, 11, 12, 13, 16, 17, 18, 20)

# 剔除指定被试的数据
df1 <- df[!(df$sub_id %in% exclude_ids), ]

head(df1)

# 查看R函数的帮助文档
# ?MANOVA
# ?EMMEANS

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
# interaction_plot <- emmip(emmeans_result, group ~ trial_type, CIs = TRUE)
# interaction_plot

# 使用 emmeans 提取简单效应分析结果
emmeans_result <- emmeans(anova_result, ~ trial_type | group)

# 将结果转换为数据框
emmeans_df <- as.data.frame(emmeans_result)

# 查看数据框结构（可选）
head(emmeans_df)

# 使用 ggplot 进行可视化 (bar + error bar)
interaction_plot <- ggplot(emmeans_df, aes(x = trial_type, y = emmean, fill = group)) +
  geom_bar(stat = "identity", position = "dodge", color = "black", width = 0.7) +
  geom_errorbar(aes(ymin = emmean - SE, ymax = emmean + SE), 
                position = position_dodge(0.7), width = 0.2) +
  labs(x = "trial_type", 
       y = "Estimated Marginal Means", 
       fill = "Group") +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"),
    panel.background = element_blank(),
    plot.title = element_text(size = 14, hjust = 0.5, margin = margin(b = 15)),
    axis.line = element_line(color = "black"),
    axis.title.x = element_text(size = 12, color = "black"), # 调整 X 轴标题字体，去掉加粗
    axis.title.y = element_text(size = 12, color = "black", margin = margin(r = 10)), # 调整 Y 轴标题字体，去掉加粗
    axis.text = element_text(size = 12, color = "black"),
    axis.text.x = element_text(margin = margin(t = 10)),
    axis.text.y = element_text(size = 12),
    axis.ticks.x = element_blank(),
    legend.position = c(0.20, 0.8),
    legend.background = element_rect(color = "black"),
    legend.text = element_text(size = 10),
    legend.margin = margin(t = 5, l = 5, r = 5, b = 5),
    legend.key = element_rect(color = NA, fill = NA)
  )

# 显示图表
print(interaction_plot)

# 保存图表为png文件
ggsave("judge_plot.png", plot = interaction_plot, width = 8, height = 6, dpi = 300)
