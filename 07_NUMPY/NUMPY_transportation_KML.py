# -*- coding: utf-8 -*-
"""
correlation_total_plots.py  (최종판)
- ./merged_2022.csv, ./merged_2023.csv 를 입력으로 사용
- 최종 그래프만 ./total_plot/ 에 저장 (동일 파일명은 덮어쓰기)

저장 목록(대표):
  1) same_2022_bar.png                 : 동일 카테고리 상관 (2022)
  2) same_2023_bar.png                 : 동일 카테고리 상관 (2023)
  3) regional_2022.png                 : 지역별 상권 vs 물류 상관 (2022, viridis 팔레트)
  4) regional_2023.png                 : 지역별 상권 vs 물류 상관 (2023, viridis 팔레트)
  5) growth_rate_bar.png               : 2022→2023 상권 증감률(평균, viridis 팔레트)
  6) cross_heatmap_2022.png            : 2022 상권↔물류 교차 상관 히트맵 (샘플 스타일)
  7) cross_heatmap_2023.png            : 2023 상권↔물류 교차 상관 히트맵 (샘플 스타일)
  8) regional_compare_2022_grouped.png : 지역별 상권합/물류합 그룹형(2022)
  9) regional_compare_2023_grouped.png : 지역별 상권합/물류합 그룹형(2023)
 10) regional_compare_2022_scatter.png : 지역별 상권합 vs 물류합 산점도(2022)
 11) regional_compare_2023_scatter.png : 지역별 상권합 vs 물류합 산점도(2023)
 12) regional_compare_2022_norm.png    : 지역별 정규화 그룹형(2022)
 13) regional_compare_2023_norm.png    : 지역별 정규화 그룹형(2023)
 14) regional_compare_2022_dualaxis.png: 이중축(상권 막대/물류 선, 2022)
 15) regional_compare_2023_dualaxis.png: 이중축(상권 막대/물류 선, 2023)
 16) regional_stacked_2022_market.png  : 지역×카테고리 스택(상권, 2022, 범례 오른쪽 세로)
 17) regional_stacked_2022_logi.png    : 지역×카테고리 스택(물류, 2022, 범례 오른쪽 세로)
 18) regional_stacked_2023_market.png  : 지역×카테고리 스택(상권, 2023, 범례 오른쪽 세로)
 19) regional_stacked_2023_logi.png    : 지역×카테고리 스택(물류, 2023, 범례 오른쪽 세로)
"""

import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 자동 설정
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ========= 경로/설정 =========
DIR = "./"
FILE_MERGED_2022 = os.path.join(DIR, "merged_2022.csv")
FILE_MERGED_2023 = os.path.join(DIR, "merged_2023.csv")

TOTAL_DIR = os.path.join(DIR, "total_plot")
os.makedirs(TOTAL_DIR, exist_ok=True)

# 기존 PNG 정리 여부 (원하면 True)
CLEAN_OLD_PNG = False
if CLEAN_OLD_PNG:
    for p in glob.glob(os.path.join(TOTAL_DIR, "*.png")):
        try: os.remove(p)
        except: pass

CATEGORY_LIST = [
    "가구/인테리어","기타","도서/음반","디지털/가전","생활/건강",
    "스포츠/레저","식품","출산/육아","패션의류","패션잡화","화장품/미용"
]

# 색상/팔레트
BAR_POS   = "#3b82f6"
BAR_NEG   = "tomato"
HEAT_CMAP = "YlGnBu"
HEAT_VMIN = 0.7
HEAT_VMAX = 1.0
HEAT_MASK = 0.6

FINAL_PLOTS = {
    "same_2022": True,
    "same_2023": True,
    "regional_2022": True,   
    "regional_2023": True,
    "growth_rate_bar": True,
    "cross_heatmap_2022": True,
    "cross_heatmap_2023": True,
    "regional_grouped_2022": True,
    "regional_grouped_2023": True,
    "regional_scatter_2022": True,
    "regional_scatter_2023": True,
    "regional_norm_2022": True,
    "regional_norm_2023": True,
    "regional_dualaxis_2022": True,
    "regional_dualaxis_2023": True,
    "regional_stacked_2022_market": True,
    "regional_stacked_2022_logi":   True,
    "regional_stacked_2023_market": True,
    "regional_stacked_2023_logi":   True,
}

# ========= 공통 유틸 =========
def corr_same_category(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in CATEGORY_LIST:
        x = merged[f"{c}_상권"]; y = merged[f"{c}_물류"]
        if x.std(ddof=0)==0 or y.std(ddof=0)==0:
            r = np.nan
        else:
            r = x.corr(y)
        rows.append({"카테고리": c, "상관계수": r})
    return pd.DataFrame(rows).sort_values("상관계수", ascending=False)

def corr_regional(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for region, sub in merged.groupby("지역"):
        xs = sub[[f"{c}_상권" for c in CATEGORY_LIST]].sum(axis=0).values
        ys = sub[[f"{c}_물류" for c in CATEGORY_LIST]].sum(axis=0).values
        if np.std(xs)==0 or np.std(ys)==0:
            r = np.nan
        else:
            r = np.corrcoef(xs, ys)[0,1]
        rows.append({"지역": region, "상관계수": r})
    return pd.DataFrame(rows).sort_values("상관계수", ascending=False)

def corr_matrix_cross(merged: pd.DataFrame) -> pd.DataFrame:
    mcols = [f"{c}_상권" for c in CATEGORY_LIST]
    lcols = [f"{c}_물류" for c in CATEGORY_LIST]
    m = merged[mcols]; l = merged[lcols]
    mat = np.zeros((len(CATEGORY_LIST), len(CATEGORY_LIST)), dtype=float)
    for i, mc in enumerate(mcols):
        for j, lc in enumerate(lcols):
            x = m[mc]; y = l[lc]
            if x.std(ddof=0)==0 or y.std(ddof=0)==0 or len(merged)<2:
                mat[i, j] = np.nan
            else:
                mat[i, j] = x.corr(y)
    return pd.DataFrame(mat, index=CATEGORY_LIST, columns=CATEGORY_LIST)

def _regional_totals(merged: pd.DataFrame):
    msum = merged.groupby("지역")[[f"{c}_상권" for c in CATEGORY_LIST]].sum()
    lsum = merged.groupby("지역")[[f"{c}_물류" for c in CATEGORY_LIST]].sum()
    df = pd.DataFrame({"상권합": msum.sum(axis=1), "물류합": lsum.sum(axis=1)}).reset_index()
    return df.sort_values(["상권합","물류합"], ascending=False)

# ========= 플로팅 =========
def bar_same(df_corr: pd.DataFrame, year: int, out_png: str):
    x = df_corr["카테고리"]; y = df_corr["상관계수"]
    colors = [BAR_POS if (pd.notna(v) and v >= 0) else BAR_NEG for v in y]
    fig, ax = plt.subplots(figsize=(12,6))
    bars = ax.bar(x, y, color=colors)
    ax.set_title(f"{year} 동일 카테고리 상관(피어슨)")
    ax.set_ylim(-1,1); ax.set_ylabel("상관계수")
    ax.set_xticklabels(x, rotation=45, ha="right")
    for b, v in zip(bars, y):
        if pd.notna(v):
            ax.text(b.get_x()+b.get_width()/2, v, f"{v:.2f}",
                    ha="center", va="bottom" if v>=0 else "top", fontsize=9)
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def bar_region(df_corr: pd.DataFrame, year: int, out_png: str):
    """지역별 상권 vs 물류 상관 막대 - viridis 팔레트 적용 + 컬러바"""
    x = df_corr["지역"].tolist()
    y = df_corr["상관계수"].values

    cmap = cm.get_cmap("viridis")
    norm = mcolors.Normalize(vmin=np.nanmin(y), vmax=np.nanmax(y))
    colors = [cmap(norm(v)) if pd.notna(v) else (0.8,0.8,0.8,1) for v in y]

    fig, ax = plt.subplots(figsize=(14,6))
    bars = ax.bar(x, y, color=colors)
    ax.set_title(f"{year} 지역별 상권 vs 물류 상관")
    ax.set_ylim(-1,1); ax.set_ylabel("상관계수")
    ax.set_xticklabels(x, rotation=45, ha="right")
    for b, v in zip(bars, y):
        if pd.notna(v):
            ax.text(b.get_x()+b.get_width()/2, v, f"{v:.2f}",
                    ha="center", va="bottom" if v>=0 else "top", fontsize=9)

    sm = cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax); cbar.set_label("상관계수")

    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def growth_rate_plot(m22: pd.DataFrame, m23: pd.DataFrame, out_png: str):
    keep = ["지역"] + [f"{c}_상권" for c in CATEGORY_LIST]
    m22m = m22[keep].rename(columns={f"{c}_상권": c for c in CATEGORY_LIST})
    m23m = m23[keep].rename(columns={f"{c}_상권": c for c in CATEGORY_LIST})
    m22s, m23s = m22m.set_index("지역"), m23m.set_index("지역")
    diffs = (m23s - m22s) / (m22s.replace(0, np.nan)) * 100
    mean_growth = diffs.mean().sort_values(ascending=False)

    cmap = cm.get_cmap("viridis")
    norm = mcolors.Normalize(vmin=mean_growth.min(), vmax=mean_growth.max())
    colors = [cmap(norm(v)) for v in mean_growth.values]

    fig, ax = plt.subplots(figsize=(12,6))
    bars = ax.bar(mean_growth.index, mean_growth.values, color=colors)
    ax.set_title("2022→2023 평균 증감률(%) (상권 기준)")
    ax.set_ylabel("증감률(%)")
    ax.set_xticks(range(len(mean_growth.index)))
    ax.set_xticklabels(mean_growth.index, rotation=45, ha="right")

    for b, v in zip(bars, mean_growth.values):
        ax.text(b.get_x()+b.get_width()/2, v, f"{v:.1f}%",
                ha="center", va="bottom" if v>=0 else "top", fontsize=9)

    sm = cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax); cbar.set_label("증감률(%)")

    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_corr_heatmap(corr_df: pd.DataFrame, title: str, out_png: str,
                      vmin=HEAT_VMIN, vmax=HEAT_VMAX, mask_th=HEAT_MASK, cmap=HEAT_CMAP):
    data = corr_df.values.astype(float)
    fig, ax = plt.subplots(figsize=(12,9))
    im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')

    mid = (vmin + vmax) / 2.0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if not np.isnan(val) and abs(val) < mask_th:
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, color=(0.5,0.5,0.5,0.45)))
            txt = "" if np.isnan(val) else f"{val:.2f}"
            color = "white" if (not np.isnan(val) and val > mid) else "black"
            ax.text(j, i, txt, ha="center", va="center", color=color, fontsize=9)

    ax.set_title(title)
    ax.set_xticks(range(corr_df.shape[1])); ax.set_yticks(range(corr_df.shape[0]))
    ax.set_xticklabels([f"{c}\n(물류)" for c in corr_df.columns], rotation=90)
    ax.set_yticklabels([f"{c} (상권)" for c in corr_df.index])
    ax.set_xlabel("물류 카테고리"); ax.set_ylabel("상권 카테고리")

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("상관계수", rotation=90)
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_regional_grouped(merged: pd.DataFrame, year: int, out_png: str):
    df = _regional_totals(merged)
    x = np.arange(len(df)); w = 0.38
    fig, ax = plt.subplots(figsize=(14,7))
    b1 = ax.bar(x - w/2, df["상권합"], width=w, label="상권(합)", color="#60a5fa")
    b2 = ax.bar(x + w/2, df["물류합"], width=w, label="물류(합)", color="#10b981")
    ax.set_title(f"{year} 지역별 상권 밀집도 vs 물류 배송량")
    ax.set_xticks(x); ax.set_xticklabels(df["지역"], rotation=45, ha="right")
    ax.set_ylabel("합계(지역별)")
    ax.legend()
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height(), f"{int(b.get_height()):,}",
                    ha="center", va="bottom", fontsize=8)
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_regional_scatter(merged: pd.DataFrame, year: int, out_png: str):
    df = _regional_totals(merged)
    x = df["상권합"].values; y = df["물류합"].values
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(x, y, s=48, alpha=0.85, color="#0ea5e9")
    if len(x) >= 2 and np.std(x) > 1e-12:
        m, b = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, m*xs + b, color="#111827", linewidth=1.8, label="회귀선")
    if len(x) >= 2:
        r = np.corrcoef(x, y)[0,1]
        ax.text(0.02, 0.95, f"r={r:.2f}", transform=ax.transAxes,
                ha="left", va="top", fontsize=10, bbox=dict(boxstyle="round", fc="white", ec="#bbb"))
    for xi, yi, name in zip(x, y, df["지역"]):
        ax.text(xi, yi, name, fontsize=8, ha="left", va="bottom")
    ax.set_title(f"{year} 지역별 상권합 vs 물류합 (산점도)")
    ax.set_xlabel("상권합"); ax.set_ylabel("물류합")
    ax.legend(loc="lower right")
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_regional_grouped_normalized(merged: pd.DataFrame, year: int, out_png: str):
    df = _regional_totals(merged)
    m = df["상권합"].astype(float); l = df["물류합"].astype(float)
    m_norm = (m / m.max()) * 100 if m.max() > 0 else m
    l_norm = (l / l.max()) * 100 if l.max() > 0 else l
    x = np.arange(len(df)); w = 0.38
    fig, ax = plt.subplots(figsize=(14,7))
    b1 = ax.bar(x - w/2, m_norm, width=w, label="상권(정규화 %)", color="#60a5fa")
    b2 = ax.bar(x + w/2, l_norm, width=w, label="물류(정규화 %)", color="#10b981")
    ax.set_title(f"{year} 지역별 상권 vs 물류 (정규화 0~100%)")
    ax.set_xticks(x); ax.set_xticklabels(df["지역"], rotation=45, ha="right")
    ax.set_ylabel("정규화 비율(%)"); ax.set_ylim(0,110); ax.legend()
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height(), f"{b.get_height():.1f}%",
                    ha="center", va="bottom", fontsize=8)
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_regional_dualaxis(merged: pd.DataFrame, year: int, out_png: str):
    df = _regional_totals(merged)
    x = np.arange(len(df))
    fig, ax1 = plt.subplots(figsize=(14,7))
    b = ax1.bar(x, df["상권합"], color="#60a5fa", label="상권(합)")
    ax1.set_ylabel("상권 합계", color="#1f2937"); ax1.tick_params(axis='y', labelcolor="#1f2937")
    ax2 = ax1.twinx()
    ax2.plot(x, df["물류합"], marker="o", linewidth=2.0, color="#10b981", label="물류(합)")
    ax2.set_ylabel("물류 합계", color="#065f46"); ax2.tick_params(axis='y', labelcolor="#065f46")
    ax1.set_xticks(x); ax1.set_xticklabels(df["지역"], rotation=45, ha="right")
    ax1.set_title(f"{year} 지역별 상권(막대) vs 물류(선) - 이중축")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc="upper left")
    for bb in b:
        ax1.text(bb.get_x()+bb.get_width()/2, bb.get_height(), f"{int(bb.get_height()):,}",
                 ha="center", va="bottom", fontsize=8)
    for xi, yi in zip(x, df["물류합"].values):
        ax2.text(xi, yi, f"{int(yi):,}", ha="center", va="bottom", fontsize=8, color="#065f46")
    plt.tight_layout(); plt.savefig(out_png, dpi=160); plt.close()

def plot_regional_category_stacked(merged: pd.DataFrame, year: int, kind: str, out_png: str):
    """지역×카테고리 스택 (범례 오른쪽 세로)"""
    assert kind in ("market", "logi")
    suffix = "_상권" if kind == "market" else "_물류"
    cols = ["지역"] + [f"{c}{suffix}" for c in CATEGORY_LIST]
    df = merged[cols].groupby("지역").sum().reset_index()
    df["총합"] = df[[f"{c}{suffix}" for c in CATEGORY_LIST]].sum(axis=1)
    df = df.sort_values("총합", ascending=False).drop(columns=["총합"])

    fig, ax = plt.subplots(figsize=(14,7))
    bottom = np.zeros(len(df))
    for c in CATEGORY_LIST:
        vals = df[f"{c}{suffix}"].values
        ax.bar(df["지역"], vals, bottom=bottom, label=c)
        bottom += vals

    totals = bottom
    for i, v in enumerate(totals):
        ax.text(i, v, f"{int(v):,}", ha="center", va="bottom", fontsize=8)

    title_head = "상권" if kind == "market" else "물류"
    ax.set_title(f"{year} 지역별 {title_head} 카테고리 분해(스택)")
    ax.set_ylabel("합계")
    ax.set_xticklabels(df["지역"], rotation=45, ha="right")
    ax.legend(title="카테고리", bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.savefig(out_png, dpi=160)
    plt.close()

# ✅ 교차 상관 히트맵(샘플 스타일)
def plot_cross_heatmap_pretty(merged_df: pd.DataFrame, year: int, out_png: str):
    """
    행=상권(11), 열=물류(11) 교차 상관행렬을 Seaborn heatmap으로 예쁘게 그린다.
    - 숫자 주석(.2f), 컬러바 라벨, 축 라벨, 0.70~1.00 범위, YlGnBu 팔레트
    """
    categories = CATEGORY_LIST
    mcols = [f"{c}_상권" for c in categories]
    lcols = [f"{c}_물류" for c in categories]

    m = merged_df[mcols].copy()
    l = merged_df[lcols].copy()
    mat = np.full((len(categories), len(categories)), np.nan, dtype=float)
    for i, mc in enumerate(mcols):
        for j, lc in enumerate(lcols):
            x = m[mc]; y = l[lc]
            if x.std(ddof=0) == 0 or y.std(ddof=0) == 0 or len(merged_df) < 2:
                continue
            mat[i, j] = x.corr(y)

    corr_df = pd.DataFrame(
        mat,
        index=[f"{c} (상권)" for c in categories],
        columns=[f"{c}\n(물류)" for c in categories],
    )

    plt.figure(figsize=(12, 9))
    ax = sns.heatmap(
        corr_df, annot=True, fmt=".2f",
        cmap="YlGnBu", vmin=0.70, vmax=1.00,
        cbar_kws={"label": "상관계수"},
        linewidths=0.3, linecolor="white",
    )
    ax.set_title(f"{year} 상권→물류 교차 상관(피어슨)")
    ax.set_xlabel("물류 카테고리")
    ax.set_ylabel("상권 카테고리")
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()

# ========= 메인 =========
def main():
    m22 = pd.read_csv(FILE_MERGED_2022, encoding="utf-8-sig")
    m23 = pd.read_csv(FILE_MERGED_2023, encoding="utf-8-sig")

    # 동일 카테고리 상관
    if FINAL_PLOTS["same_2022"]:
        bar_same(corr_same_category(m22), 2022, os.path.join(TOTAL_DIR, "same_2022_bar.png"))
    if FINAL_PLOTS["same_2023"]:
        bar_same(corr_same_category(m23), 2023, os.path.join(TOTAL_DIR, "same_2023_bar.png"))

    # 지역별 상관 (2022/2023 모두 저장, viridis 팔레트)
    if FINAL_PLOTS["regional_2022"]:
        bar_region(corr_regional(m22), 2022, os.path.join(TOTAL_DIR, "regional_2022.png"))
    if FINAL_PLOTS["regional_2023"]:
        bar_region(corr_regional(m23), 2023, os.path.join(TOTAL_DIR, "regional_2023.png"))

    # 증감률(상권 기준, viridis 팔레트)
    if FINAL_PLOTS["growth_rate_bar"]:
        growth_rate_plot(m22, m23, os.path.join(TOTAL_DIR, "growth_rate_bar.png"))

    # 교차 카테고리 히트맵 (샘플 스타일로 덮어쓰기)
    if FINAL_PLOTS["cross_heatmap_2022"]:
        plot_cross_heatmap_pretty(m22, 2022, os.path.join(TOTAL_DIR, "cross_heatmap_2022.png"))
    if FINAL_PLOTS["cross_heatmap_2023"]:
        plot_cross_heatmap_pretty(m23, 2023, os.path.join(TOTAL_DIR, "cross_heatmap_2023.png"))

    # 지역별 비교(그룹형, 산점도)
    if FINAL_PLOTS["regional_grouped_2022"]:
        plot_regional_grouped(m22, 2022, os.path.join(TOTAL_DIR, "regional_compare_2022_grouped.png"))
    if FINAL_PLOTS["regional_grouped_2023"]:
        plot_regional_grouped(m23, 2023, os.path.join(TOTAL_DIR, "regional_compare_2023_grouped.png"))
    if FINAL_PLOTS["regional_scatter_2022"]:
        plot_regional_scatter(m22, 2022, os.path.join(TOTAL_DIR, "regional_compare_2022_scatter.png"))
    if FINAL_PLOTS["regional_scatter_2023"]:
        plot_regional_scatter(m23, 2023, os.path.join(TOTAL_DIR, "regional_compare_2023_scatter.png"))

    # 정규화(0~100%)
    if FINAL_PLOTS["regional_norm_2022"]:
        plot_regional_grouped_normalized(m22, 2022, os.path.join(TOTAL_DIR, "regional_compare_2022_norm.png"))
    if FINAL_PLOTS["regional_norm_2023"]:
        plot_regional_grouped_normalized(m23, 2023, os.path.join(TOTAL_DIR, "regional_compare_2023_norm.png"))

    # 이중축
    if FINAL_PLOTS["regional_dualaxis_2022"]:
        plot_regional_dualaxis(m22, 2022, os.path.join(TOTAL_DIR, "regional_compare_2022_dualaxis.png"))
    if FINAL_PLOTS["regional_dualaxis_2023"]:
        plot_regional_dualaxis(m23, 2023, os.path.join(TOTAL_DIR, "regional_compare_2023_dualaxis.png"))

    # 지역×카테고리 스택
    if FINAL_PLOTS["regional_stacked_2022_market"]:
        plot_regional_category_stacked(m22, 2022, "market",
                                       os.path.join(TOTAL_DIR, "regional_stacked_2022_market.png"))
    if FINAL_PLOTS["regional_stacked_2022_logi"]:
        plot_regional_category_stacked(m22, 2022, "logi",
                                       os.path.join(TOTAL_DIR, "regional_stacked_2022_logi.png"))
    if FINAL_PLOTS["regional_stacked_2023_market"]:
        plot_regional_category_stacked(m23, 2023, "market",
                                       os.path.join(TOTAL_DIR, "regional_stacked_2023_market.png"))
    if FINAL_PLOTS["regional_stacked_2023_logi"]:
        plot_regional_category_stacked(m23, 2023, "logi",
                                       os.path.join(TOTAL_DIR, "regional_stacked_2023_logi.png"))

    print("[DONE] 최종 그래프 저장:", TOTAL_DIR)

if __name__ == "__main__":
    main()
