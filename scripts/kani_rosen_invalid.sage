from sage.all import *

def audit_conductor_sage(p, q):
    print(f"📡 正在审计 Goldbach-Frey 轨道: p={p}, q={q}")
    print("-" * 50)
    
    # 1. 构造 Kani-Rosen 分裂出的两条椭圆曲线
    # E1: y^2 = x(x-p)(x-q) -> y^2 = x^3 - (p+q)x^2 + pqx
    E1 = EllipticCurve([0, -(p + q), 0, p * q, 0])
    # E2: y^2 = x(x+p)(x+q) -> y^2 = x^3 + (p+q)x^2 + pqx
    E2 = EllipticCurve([0, (p + q), 0, p * q, 0])
    
    # 2. 计算两条曲线的导体
    cond1 = E1.conductor()
    cond2 = E2.conductor()
    
    # 3. 雅可比簇的全局导体 (Kani-Rosen 定理)
    total_conductor = cond1 * cond2
    
    print(f"E1 导体: {cond1} (分解: {cond1.factor()})")
    print(f"E2 导体: {cond2} (分解: {cond2.factor()})")
    print(f"==> 雅可比簇 J 的真实总导体: {total_conductor}")
    print(f"==> 全局导体分解: {total_conductor.factor()}")
    
    # 4. 提取局部细节 (r=2, 7, 23)
    print("\n[局部能级审计]")
    relevant_primes = sorted(list(set([2] + [f[0] for f in total_conductor.factor()])))
    print(f"{'素数 r':<10} | {'真实 f_r':<10} | {'Kodaira 符号 (E1/E2)'}")
    for r in relevant_primes:
        f_r = total_conductor.valuation(r)
        k1 = E1.local_data(r).kodaira_symbol()
        k2 = E2.local_data(r).kodaira_symbol()
        print(f"{r:<10} | {f_r:<10} | {k1} / {k2}")

# 执行审计任务 (p=7, q=23)
audit_conductor_sage(7, 23)