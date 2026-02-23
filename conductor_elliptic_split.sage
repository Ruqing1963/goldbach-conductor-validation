from sage.all import *

def audit_goldbach_frey_local(p, q):
    print(f"📡 泰坦审计启动: 轨道 p={p}, q={q} (2N ≈ {p+q})")
    print("=" * 60)
    
    # 1. Kani-Rosen 分裂构造 (Genus 2 -> Genus 1 x Genus 1)
    # E1: y^2 = x(x-p)(x-q)
    # E2: y^2 = x(x+p)(x+q)
    E1 = EllipticCurve([0, -(p + q), 0, p * q, 0])
    E2 = EllipticCurve([0, (p + q), 0, p * q, 0])
    
    # 2. 目标素数审计 (3, 5, 61)
    target_primes = [3, 5, 61]
    
    print(f"{'素数 r':<8} | {'导体指数 f_r':<12} | {'Kodaira 符号 (E1/E2)':<25} | {'状态'}")
    print("-" * 65)
    
    for r in target_primes:
        # 计算两条曲线在 r 处的局部数据
        # SageMath 的 local_data 接口在处理椭圆曲线时极其稳定
        ld1 = E1.local_data(r)
        ld2 = E2.local_data(r)
        
        # 真实导体指数 f_r(J) = f_r(E1) + f_r(E2)
        fr_total = ld1.conductor_valuation() + ld2.conductor_valuation()
        
        # 提取 Kodaira 符号以判定约化类型
        k1 = ld1.kodaira_symbol()
        k2 = ld2.kodaira_symbol()
        
        # 判定约化性质
        if fr_total == 0:
            status = "良约化 (Good)"
        elif fr_total <= 2:
            status = "半稳定 (Semi-stable)"
        else:
            status = "极坏约化 (Bad)"
            
        print(f"{r:<8} | {fr_total:<12} | {str(k1) + ' / ' + str(k2):<25} | {status}")

# 执行审计任务
audit_goldbach_frey_local(3, 125)