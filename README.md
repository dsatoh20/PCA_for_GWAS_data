# PCA_for_GWAS_data
# Features
- PCA for GWAS data not by tensorflow, but just by numpy.
# Installation
- numpy
- pandas
# USAGE
1. plink形式でGWASデータを取得
2. pedファイルから、SNPのデータを切り出す
3. 頻度に基づき、ATGCに0か1を割り当て、ホモ:0 or 2、ヘテロ:1とする
   ー＞ 人数 x SNP数のマトリクスを得る：SNP_data.npz
4. PCA.pyを用いて、PCAを実行する
