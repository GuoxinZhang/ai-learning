import csv  # 导入 csv 模块，用于读写 CSV 文件


# ============================================================
# 旧版本实现（已弃用，仅保留备查，不再调用）
# 封装成函数的作用：
#   1. 局部变量（rows/total/best）不会泄漏到全局，避免和新代码冲突
#   2. 想对比新旧结果时，临时调用 legacy_main() 即可，不改主流程
# ============================================================
def legacy_main():
    """旧版本：手写循环找最高分。保留用于对比，不参与主流程。"""
    # 打开 CSV 文件并读成字典列表
    # newline="" 是 csv 模块要求的写法，避免换行符被重复处理
    # encoding="utf-8-sig" 能正确处理 Excel 导出 CSV 时文件开头的 BOM
    # with 块结束时自动关闭文件（不用像 C 那样手动 fclose）
    with open("scores.csv", newline="", encoding="utf-8-sig") as f:
        # DictReader 把每行读成字典（键是表头），list(...) 一次性转成列表
        # 结果形如 [{"name": "张三", "score": "90"}, ...]
        rows = list(csv.DictReader(f))

    total = 0  # 累加总分，初始为 0
    for row in rows:  # 遍历每一行（row 是字典）
        # row["score"] 是字符串（如 "90"），用 int() 转成整数再累加
        total += int(row["score"])

    best = rows[0]  # 先假设第一行是最高分（文件为空时会 IndexError）
    for row in rows:  # 再遍历一遍，找真正的最高分
        # 字符串转整数后比较大小
        if int(row["score"]) > int(best["score"]):
            best = row  # 当前行更高，更新 best（存的是字典引用，不是拷贝）

    # f-string 输出：len(rows) 是人数；total / len(rows) 是平均分
    # :.1f 表示保留 1 位小数（类似 C 的 printf("%.1f")）
    print(f"共 {len(rows)} 人，平均分 {total / len(rows):.1f}")
    # 字典用字符串键取值打印
    print(f"最高分：{best['name']} {best['score']}")


# ============================================================
# 新版本实现（当前生效）
# 拆成三个职责单一的函数：读文件 / 算平均 / 找最高
# ============================================================
def read_scores(path):
    """读取 CSV 文件，返回“每行一个字典”的列表。path 是文件路径字符串。"""
    with open(path, newline="", encoding="utf-8-sig") as f:
        # 与旧版相同的读取方式，只是把路径变成参数，函数更通用
        return list(csv.DictReader(f))


def average(rows):
    """计算平均分。rows 是 read_scores 返回的列表。"""
    # sum(... for r in rows) 是生成器表达式，等价于 C 里写个 for 循环累加
    # 每项把 r["score"]（字符串）用 int() 转成整数再求和
    # Python 3 的 / 是浮点除法，不会像 C 的整数除法那样截断
    return sum(int(r["score"]) for r in rows) / len(rows)


def top(rows):
    """返回分数最高的那一行（字典）。"""
    # max(可迭代对象, key=函数) 按 key 指定的规则取最大值
    # lambda r: int(r["score"]) 是匿名函数，等价于 C 里传给 qsort 的比较回调：
    #   int cmp(const Row *r) { return atoi(r->score); }
    # max 返回使 key 最大的那个元素，即分数最高的人（字典）
    return max(rows, key=lambda r: int(r["score"]))


# ============================================================
# 主流程：读取数据 → 找最高分 → 打印统计
# ============================================================
rows = read_scores("scores.csv")  # 调用函数读取，得到字典列表
best = top(rows)                   # 调用函数，得到最高分那一行（字典）

# f-string 输出：len(rows) 是人数，average(rows) 是平均分，:.1f 保留 1 位小数
print(f"共 {len(rows)} 人，平均分 {average(rows):.1f}")
# best 是字典，用字符串键取值打印
print(f"最高分：{best['name']} {best['score']}")


# ============================================================
# 备注：想临时对比旧版结果时，取消下面这行的注释即可
# 注意：旧版用的是写死的 "scores.csv"，新版用的是传入的路径
# ============================================================
# legacy_main()