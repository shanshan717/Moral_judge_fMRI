# 以每组5个人为例，进行了组分析，混合方差分析
import os
import numpy as np
import pandas as pd
from glob import glob
from bids import BIDSLayout
import matplotlib.pyplot as plt
from nilearn.image import mean_img
from nilearn.glm import threshold_stats_img
from nilearn.glm.first_level import FirstLevelModel
from nilearn.glm.second_level import SecondLevelModel
from nilearn.reporting import make_glm_report, get_clusters_table
from nilearn.plotting import plot_stat_map, plot_anat, plot_img, show, plot_glass_brain, plot_design_matrix, plot_contrast_matrix
outdir = '../results'
list_z_maps = glob(os.path.join(outdir, '*.nii.gz'))
# print(list_z_maps)

# path = r'D:\PsychologyJudgeProjection\Judges_MRI\bids'
# temp = glob(os.path.join(path,'sub-*'))
# subs = [i.split('\\')[-1][-3:] for i in temp]
subs = ['001', '002', '003', '004', '005', '049', '050', '051', '052', '053']

# TODO：设计矩阵
n1 = np.tile(np.eye(3), (5, 1))
n0 = np.zeros(n1.shape)
X1 = np.concatenate((n1, n0), 1)
X2 = np.concatenate((n0, n1), 1)

# n11 = np.tile(np.eye(3), (2, 1))
# n00 = np.zeros(n11.shape)
# X1_5 = np.concatenate((n11, n00), 1)
# X = np.concatenate((X1, X1_5, X2), 0).astype(int)

#TODO 编写设计矩阵，并展示
X = np.concatenate((X1, X2), 0).astype(int)
X_left = pd.DataFrame(X)
sub_id = []
for s in range(len(subs)):
    sub_id.extend([s]*3)
sub_means = pd.DataFrame([sub_id==x for x in np.unique(sub_id)]).T
X_right = sub_means.replace({True :1 ,False :0})
X = pd.concat([X_left, X_right], axis=1)
X.columns = ['G1_common_sense', 'G1_judge', 'G1_moral'] + ['G2_common_sense', 'G2_judge', 'G2_moral'] + subs
design_matrix = X
plot_design_matrix(design_matrix)
plt.show()


second_level_model = SecondLevelModel()
second_level_model = second_level_model.fit(list_z_maps, design_matrix=design_matrix)

#TODO 编写对比矩阵
conditions = {"one": np.zeros(16), "two": np.zeros(16)}
conditions['one'][0:5] = [1, -1, 0, -1, 1]
conditions['two'][0:6] = [1, 0, -1, -1, 0, 1]
contrast_matrix = np.vstack((conditions["one"], conditions["two"]))
# plot_contrast_matrix(contrast_matrix, design_matrix)
# plt.show()

z_map_group = second_level_model.compute_contrast(contrast_matrix, output_type='effect_size')
# z_map_group = second_level_model.compute_contrast(contrast_matrix, output_type='all')


# clean_map, threshold = threshold_stats_img(
#     z_map_group, alpha=0.05, height_control="fdr", cluster_threshold=10
# )
# plot_stat_map(
#     clean_map,
#     # bg_img=mean_img,
#     threshold=threshold,
#     display_mode="z",
#     cut_coords=3,
#     black_bg=True,
#     title="Effects of interest (fdr=0.05), clusters > 10 voxels",
# )
# plt.show()
# from scipy.stats import norm
# p001_unc = norm.isf(0.001)

# plot_glass_brain(z_map_group, colorbar=True, threshold=p001_unc, title='Group Finger tapping (unc p<0.001)', plot_abs=False, display_mode='x', cmap='magma')
# plot_glass_brain(z_map_group, colorbar=True, threshold=0.001, title='Group Finger tapping (unc p<0.001)', plot_abs=False, display_mode='x', cmap='magma')
# plt.show()

table = get_clusters_table(z_map_group, stat_threshold=3, cluster_threshold=20)
print(table)

# report = make_glm_report(second_level_model, contrasts=contrast_matrix)
# report.open_in_browser()



