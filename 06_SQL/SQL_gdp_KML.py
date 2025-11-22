# -*- coding: utf-8 -*-
# ========================== 0) DB → DataFrame (원문 유지) ==========================
from matplotlib import pyplot as plt
import pymysql
import pandas as pd

def load_table(table_name, host='172.20.51.204', user='KML', password='1234', db='miniProject_team5', charset='utf8mb4'):
    conn = None
    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)   # 경고는 무시 가능(필요 시 SQLAlchemy 권장)
        return df
    except Exception as e:
        print(f"[ERROR] {table_name} 불러오기 실패:", e)
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()

# 1) 테이블 로드
df_macro   = load_table("yearly_macro_simple")
df_gender  = load_table("employment_gender_age")
df_economic= load_table("employment_economic")
df_marriage= load_table("employment_marriage")

# ========================== 2) 공통 전처리/유틸 ==========================
# -*- coding: utf-8 -*-
# ========================== 0) DB → DataFrame (사용자 코드 유지) ==========================
from matplotlib import pyplot as plt
import pymysql
import pandas as pd

def load_table(table_name, host='172.20.51.204', user='KML', password='1234', db='miniProject_team5', charset='utf8mb4'):
    conn = None
    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)   # 경고는 무시 가능(필요 시 SQLAlchemy 권장)
        return df
    except Exception as e:
        print(f"[ERROR] {table_name} 불러오기 실패:", e)
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()

# 1) 테이블 로드
df_macro   = load_table("yearly_macro_simple")
df_gender  = load_table("employment_gender_age")
df_economic= load_table("employment_economic")
df_marriage= load_table("employment_marriage")

# ========================== 2) 공통 전처리/유틸 ==========================
import numpy as np
from matplotlib import rcParams

rcParams['font.family'] = 'Malgun Gothic'
rcParams['axes.unicode_minus'] = False

AGE_ORDER = ['15-19세','20-29세','30-39세','40-49세','50-59세','60세이상']
YOUTH_SET = {'15-19세','20-29세'}
OLDER_SET = {'50-59세','60세이상'}

def to_num(x):
    if pd.isna(x): return np.nan
    try: return float(str(x).replace(',', '').strip())
    except: return np.nan

def norm_age(s):
    if pd.isna(s): return s
    return str(s).replace(' ', '').replace('–','-').replace('~','-')

def find_col(df, key):
    key = key.lower()
    for c in df.columns:
        if str(c).lower() == key: return c
    for c in df.columns:
        if key in str(c).lower(): return c
    return None

# 공통 컬럼/형 정리
for _df in (df_macro, df_gender, df_economic, df_marriage):
    if not _df.empty:
        _df.columns = [str(c).strip() for c in _df.columns]
        if 'year' in _df.columns:
            _df['year'] = pd.to_numeric(_df['year'], errors='coerce')

if 'persons' in df_gender.columns:   df_gender['persons']   = df_gender['persons'].apply(to_num)
if 'persons' in df_economic.columns: df_economic['persons'] = df_economic['persons'].apply(to_num)
if 'persons' in df_marriage.columns: df_marriage['persons'] = df_marriage['persons'].apply(to_num)

if 'age_group' in df_gender.columns:   df_gender['age_group']   = df_gender['age_group'].map(norm_age)
if 'age_group' in df_economic.columns: df_economic['age_group'] = df_economic['age_group'].map(norm_age)
if 'age_group' in df_marriage.columns: df_marriage['age_group'] = df_marriage['age_group'].map(norm_age)

# 매크로 지표(혼인/청년·장년 그래프에서 사용) + 지수화
gdp_col = find_col(df_macro, 'gdp') or 'gdp'
cpi_col = find_col(df_macro, 'cpi') or 'cpi'
macro = df_macro[['year', gdp_col, cpi_col]].dropna(subset=['year']).sort_values('year').copy()
for c in [gdp_col, cpi_col]:
    macro[c] = pd.to_numeric(macro[c], errors='coerce')
macro_idx = macro.set_index('year').copy()
macro_idx['GDP_IDX'] = macro_idx[gdp_col] / macro_idx[gdp_col].iloc[0] * 100
macro_idx['CPI_IDX'] = macro_idx[cpi_col] / macro_idx[cpi_col].iloc[0] * 100

YEARS_ALL = sorted(macro['year'].dropna().unique().tolist())

# ========================== 3) 그래프 (1) 성별·연령별 정규/비정규 "비중" ==========================
need1 = {'year','work_type','gender','age_group','persons'}
if need1.issubset(df_gender.columns) and not df_gender.empty:
    gg = df_gender.dropna(subset=list(need1)).copy()
    gg = gg[gg['age_group'].isin(AGE_ORDER)]
    gg['age_group'] = pd.Categorical(gg['age_group'], categories=AGE_ORDER, ordered=True)

    base = gg.groupby(['year','gender','age_group','work_type'], as_index=False)['persons'].sum()
    denom = base.groupby(['year','gender','age_group'])['persons'].sum().rename('total').reset_index()
    merged = pd.merge(base, denom, on=['year','gender','age_group'], how='left')
    merged['share(%)'] = merged['persons'] / merged['total'] * 100

    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=False, sharey=True)
    axes = axes.ravel()

    for i, age in enumerate(AGE_ORDER):
        ax = axes[i]
        sub = merged[merged['age_group']==age].pivot_table(
            index='year', columns=['gender','work_type'], values='share(%)', aggfunc='mean'
        ).sort_index()
        for key in [('남자','정규직'),('남자','비정규직'),('여자','정규직'),('여자','비정규직')]:
            if key not in sub.columns: sub[key] = np.nan

        ax.plot(sub.index, sub[('남자','정규직')], marker='o', label='남자 정규')
        ax.plot(sub.index, sub[('남자','비정규직')], marker='o', linestyle='--', label='남자 비정')
        ax.plot(sub.index, sub[('여자','정규직')], marker='o', linestyle=':', label='여자 정규')
        ax.plot(sub.index, sub[('여자','비정규직')], marker='o', linestyle='-.', label='여자 비정')

        ax.set_title(age); ax.set_xticks(YEARS_ALL)
        ax.grid(True, alpha=0.4, linewidth=0.5)

    fig.suptitle('성별·연령별 정규/비정규 비중 추이 (x축: 연도, y축: 비중%)', fontsize=14, y=0.98)
    for ax in axes[::3]:
        ax.set_ylabel('비중(%)')
    for ax in axes[-3:]:
        ax.set_xlabel('연도')

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.93))
    fig.subplots_adjust(top=0.88); plt.tight_layout(rect=[0,0,1,0.88]); plt.show()
else:
    print("[그래프 (1)] employment_gender_age 테이블의 필수 컬럼이 없습니다.")

# ========================== 4) 그래프 (2) 연령별 취업·실업·비경제활동 ==========================
need2 = {'year','item','age_group','persons'}
if need2.issubset(df_economic.columns) and not df_economic.empty:
    econ = df_economic.dropna(subset=['year','item','age_group']).copy()
    econ['age_group'] = pd.Categorical(econ['age_group'], categories=AGE_ORDER, ordered=True)
    econ['item'] = econ['item'].astype(str).str.replace(' ', '')
    econ['item'] = econ['item'].replace({
        '취업자(천명)':'취업자(천명)','취업자':'취업자(천명)',
        '실업자(천명)':'실업자(천명)','실업자':'실업자(천명)',
        '비경제활동인구(천명)':'비경제활동인구(천명)','비경제활동인구':'비경제활동인구(천명)'
    })
    has_gender = 'gender' in econ.columns

    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=False)
    axes = axes.ravel()

    for i, age in enumerate(AGE_ORDER):
        ax = axes[i]
        sub = econ[econ['age_group']==age].copy()
        if has_gender:
            for sex, ls in [('남','-'),('여','--')]:
                ss = sub[sub['gender'].astype(str).str.contains(sex)]
                piv = ss.pivot_table(index='year', columns='item', values='persons', aggfunc='sum').sort_index()
                for col, label in [('취업자(천명)',f'취업({sex})'),
                                   ('실업자(천명)',f'실업({sex})'),
                                   ('비경제활동인구(천명)',f'비경활({sex})')]:
                    if col in piv.columns: ax.plot(piv.index, piv[col], marker='o', linestyle=ls, label=label)
        else:
            piv = sub.pivot_table(index='year', columns='item', values='persons', aggfunc='sum').sort_index()
            for col, label in [('취업자(천명)','취업'), ('실업자(천명)','실업'), ('비경제활동인구(천명)','비경활')]:
                if col in piv.columns: ax.plot(piv.index, piv[col], marker='o', label=label)

        ax.set_title(age); ax.set_xticks(YEARS_ALL); ax.grid(True, alpha=0.4, linewidth=0.5)

    fig.suptitle('연령별 취업·실업·비경제활동 추이 (x축: 연도)', fontsize=14, y=0.98)
    for ax in axes[::3]:
        ax.set_ylabel('인원(천명)')
    for ax in axes[-3:]:
        ax.set_xlabel('연도')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=6, frameon=False, bbox_to_anchor=(0.5, 0.93))
    fig.subplots_adjust(top=0.88); plt.tight_layout(rect=[0,0,1,0.88]); plt.show()

    if not has_gender:
        print("※ employment_economic에 성별 컬럼이 없어 총계 기준으로 그렸습니다.")
else:
    print("[그래프 (2)] employment_economic 테이블의 필수 컬럼이 없습니다.")

# ========================== 5) 그래프 (3) 남녀 혼인수 + GDP/CPI(채워진 꺾은선) ==========================
need3 = {'year','gender','persons'}
if need3.issubset(df_marriage.columns) and not df_marriage.empty and not macro.empty:
    m = df_marriage.dropna(subset=['year','gender','persons']).copy()
    male   = m[m['gender'].astype(str).str.contains('남')].groupby('year')['persons'].sum()
    female = m[m['gender'].astype(str).str.contains('여')].groupby('year')['persons'].sum()

    years = sorted(set(male.index).union(set(female.index)).intersection(set(macro_idx.index)))
    fig, ax1 = plt.subplots(figsize=(12,5))
    if not male.empty:   ax1.plot(male.index, male.values, marker='o', label='남자 혼인수')
    if not female.empty: ax1.plot(female.index, female.values, marker='o', linestyle='--', label='여자 혼인수')
    ax1.set_xlabel('연도'); ax1.set_ylabel('혼인 건수'); ax1.grid(True, alpha=0.4, linewidth=0.5)

    ax2 = ax1.twinx()
    ax2.fill_between(years, macro_idx.loc[years, 'GDP_IDX'].values, alpha=0.25, label='GDP(지수)')
    ax2.plot(years, macro_idx.loc[years, 'GDP_IDX'].values, linestyle='-')
    ax2.fill_between(years, macro_idx.loc[years, 'CPI_IDX'].values, alpha=0.25, label='CPI(지수)')
    ax2.plot(years, macro_idx.loc[years, 'CPI_IDX'].values, linestyle='-')
    ax2.set_ylabel('지수(=100, 기준: 최초연도)')

    fig.suptitle('남녀 혼인수와 GDP/CPI 추이 비교', y=0.98)
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    fig.legend(l1+l2, lab1+lab2, loc='upper center', ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.93))
    fig.subplots_adjust(top=0.88); plt.tight_layout(rect=[0,0,1,0.88]); plt.show()
else:
    print("[그래프 (3)] employment_marriage 또는 macro 데이터가 부족합니다.")

# ========================== 6) 청년/장년 취업률·실업률 × GDP/CPI (2020·2023 강조) ==========================
# 취업률 = 취업자 / (취업+실업+비경활), 실업률 = 실업자 / (취업+실업)
need2 = {'year','item','age_group','persons'}
if need2.issubset(df_economic.columns) and not df_economic.empty and not macro.empty:
    eco = df_economic.dropna(subset=['year','item','age_group']).copy()
    eco['age_group'] = eco['age_group'].map(norm_age)
    eco['item'] = eco['item'].astype(str).str.replace(' ', '')
    eco['item'] = eco['item'].replace({
        '취업자(천명)':'취업자','취업자':'취업자',
        '실업자(천명)':'실업자','실업자':'실업자',
        '비경제활동인구(천명)':'비경활','비경제활동인구':'비경활'
    })

    def group_rate(target_set):
        sub = eco[eco['age_group'].isin(target_set)]
        p = sub.pivot_table(index='year', columns='item', values='persons', aggfunc='sum').sort_index()
        for col in ['취업자','실업자','비경활']:
            if col not in p.columns: p[col]=0.0
        labor_force = p['취업자'] + p['실업자']
        population  = labor_force + p['비경활']
        emp_rate  = np.where(population>0,  p['취업자']/population*100, np.nan)
        unemp_rate= np.where(labor_force>0, p['실업자']/labor_force*100,  np.nan)
        return pd.DataFrame({'고용률(%)':emp_rate, '실업률(%)':unemp_rate}, index=p.index)

    youth = group_rate(YOUTH_SET)
    older = group_rate(OLDER_SET)
    years = sorted(set(youth.index).intersection(older.index).intersection(set(macro_idx.index)))

    def plot_rate(rate_col, title):
        fig, ax1 = plt.subplots(figsize=(12,5))
        ax1.plot(years, youth.loc[years, rate_col], marker='o', label=f'청년 {rate_col}')
        ax1.plot(years, older.loc[years, rate_col], marker='o', linestyle='--', label=f'장년 {rate_col}')
        ax1.set_xlabel('연도'); ax1.set_ylabel(rate_col); ax1.grid(True, alpha=0.4, linewidth=0.5)

        # 2020, 2023 강조 (밴드 + 어노테이션)
        for y, lab in [(2020,'2020'), (2023,'2023')]:
            ax1.axvspan(y-0.5, y+0.5, color='gray', alpha=0.1)
            if y in years:
                ax1.scatter([y], [youth.loc[y, rate_col]], s=60)
                ax1.scatter([y], [older.loc[y, rate_col]], s=60)

        ax2 = ax1.twinx()
        ax2.fill_between(years, macro_idx.loc[years, 'GDP_IDX'].values, alpha=0.20, label='GDP(지수)')
        ax2.plot(years, macro_idx.loc[years, 'GDP_IDX'].values, linestyle='-')
        ax2.fill_between(years, macro_idx.loc[years, 'CPI_IDX'].values, alpha=0.20, label='CPI(지수)')
        ax2.plot(years, macro_idx.loc[years, 'CPI_IDX'].values, linestyle='-')
        ax2.set_ylabel('지수(=100)')

        fig.suptitle(title + ' (2020·2023 강조)', y=0.98)
        l1, lab1 = ax1.get_legend_handles_labels()
        l2, lab2 = ax2.get_legend_handles_labels()
        fig.legend(l1+l2, lab1+lab2, loc='upper center', ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.93))
        fig.subplots_adjust(top=0.88); plt.tight_layout(rect=[0,0,1,0.88]); plt.show()

    plot_rate('고용률(%)', '청년/장년 고용률 × GDP/CPI')
    plot_rate('실업률(%)', '청년/장년 실업률 × GDP/CPI')
else:
    print("[그래프 (청년/장년)] employment_economic 또는 macro 데이터가 부족합니다.")

# ========================== 7) (추가) Δ비정규 비중 vs GDP YoY ==========================
needg = {'year','work_type','gender','age_group','persons'}
if needg.issubset(df_gender.columns) and not df_gender.empty and not macro.empty:
    base = df_gender.dropna(subset=list(needg)).copy()
    share = (base.pivot_table(index=['year','age_group','gender'], columns='work_type',
                              values='persons', aggfunc='sum').reset_index())
    for col in ['정규직','비정규직']:
        if col not in share.columns: share[col]=0.0
    share['share'] = share['비정규직']/(share['정규직']+share['비정규직'])
    tot = share.groupby('year', as_index=False)['share'].mean().sort_values('year')
    tot['Δshare(%)'] = tot['share'].diff()*100
    mac = macro[['year', gdp_col]].copy()
    mac['GDP_YoY(%)'] = mac[gdp_col].pct_change()*100
    j = pd.merge(tot[['year','Δshare(%)']], mac[['year','GDP_YoY(%)']], on='year', how='inner').dropna()
    if len(j) >= 2:
        plt.figure(figsize=(7.5,5.6))
        plt.scatter(j['GDP_YoY(%)'], j['Δshare(%)'])
        for _, r in j.iterrows():
            plt.text(r['GDP_YoY(%)'], r['Δshare(%)'], str(int(r['year'])), fontsize=9)
        plt.title('Δ비정규 비중(YoY, p.p.) vs GDP YoY(%)')
        plt.xlabel('GDP YoY(%)'); plt.ylabel('Δ비정규 비중 (p.p.)')
        plt.grid(True, alpha=0.4, linewidth=0.5)
        plt.tight_layout(); plt.show()

# ========================== 8) (추가) 2019→2020 비정규 비중 슬로프 ==========================
if needg.issubset(df_gender.columns) and not df_gender.empty:
    g = df_gender.dropna(subset=list(needg)).copy()
    s = (g.pivot_table(index=['year','age_group','gender'], columns='work_type',
                       values='persons', aggfunc='sum').reset_index())
    for col in ['정규직','비정규직']:
        if col not in s.columns: s[col]=0.0
    s['share'] = s['비정규직']/(s['정규직']+s['비정규직'])
    pre  = s[s['year']==2019].set_index(['age_group','gender'])['share']
    post = s[s['year']==2020].set_index(['age_group','gender'])['share']
    idx = list(set(pre.index).intersection(set(post.index)))
    if idx:
        vals = pd.DataFrame({'2019':pre.loc[idx].values*100, '2020':post.loc[idx].values*100},
                            index=pd.MultiIndex.from_tuples(idx, names=['age','sex']))
        xs = [2019, 2020]
        plt.figure(figsize=(8,6))
        for (age,sex), row in vals.iterrows():
            plt.plot(xs, [row['2019'], row['2020']], marker='o')
            plt.text(2019-0.08, row['2019'], f"{sex}-{age}", ha='right', va='center', fontsize=8)
            plt.text(2020+0.05, row['2020'], f"{row['2020']:.1f}%", ha='left', va='center', fontsize=8)
        plt.xticks(xs, xs)
        plt.title('비정규 비중 슬로프: 2019 → 2020')
        plt.ylabel('비정규 비중(%)'); plt.grid(True, axis='y', alpha=0.4, linewidth=0.5)
        plt.tight_layout(); plt.show()

# ========================== 9) (추가) 성별 히트맵 ==========================
def draw_heatmap(mat, years, ages, title):
    fig, ax = plt.subplots(figsize=(9,4.8))
    im = ax.imshow(mat, aspect='auto', origin='lower')
    ax.set_xticks(np.arange(len(years))); ax.set_xticklabels(years)
    ax.set_yticks(np.arange(len(ages)));  ax.set_yticklabels(ages)
    ax.set_title(title); ax.set_xlabel('연도'); ax.set_ylabel('연령대')
    fig.colorbar(im, ax=ax, label='비정규 비중(%)')
    plt.tight_layout(); plt.show()

if needg.issubset(df_gender.columns) and not df_gender.empty:
    g = df_gender.dropna(subset=list(needg)).copy()
    s = (g.pivot_table(index=['year','age_group','gender'], columns='work_type',
                       values='persons', aggfunc='sum').reset_index())
    for col in ['정규직','비정규직']:
        if col not in s.columns: s[col]=0.0
    s['share(%)'] = s['비정규직']/(s['정규직']+s['비정규직'])*100
    years = sorted(s['year'].dropna().unique().tolist())
    for sex in ['남자','여자']:
        mat = []
        for age in AGE_ORDER:
            row = s[(s['gender']==sex)&(s['age_group']==age)].set_index('year').reindex(years)['share(%)']
            mat.append(row.values.astype(float))
        mat = np.array(mat)
        draw_heatmap(mat, years, AGE_ORDER, f'비정규 비중 히트맵 - {sex}')
