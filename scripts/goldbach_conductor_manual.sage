from sage.all import *

def goldbach_conductor_odd(p_val, q_val, verbose=True):
    # Step 1: 从判别式中识别坏奇素数 [cite: 2, 3]
    disc_factors = set()
    for v in [p_val, q_val, abs(p_val - q_val), p_val + q_val]:
        if v != 0:
            for (r, _) in ZZ(abs(v)).factor():
                if r > 2: disc_factors.add(r)
    bad_odd = sorted(disc_factors)
    
    if verbose:
        print(f"Curve: y^2 = x(x^2 - {p_val}^2)(x^2 - {q_val}^2)")
        print(f"Bad odd primes: {bad_odd}")
    
    result = {}
    for r in bad_odd:
        Fr = GF(r)
        Pr = PolynomialRing(Fr, 'xr')
        xr = Pr.gen()
        f_r = xr * (xr^2 - Fr(p_val)^2) * (xr^2 - Fr(q_val)^2)
        
        # --- 核心修正点：设置 check_squarefree=False ---
        # 允许在坏素数处构造带有奇异点的曲线 
        Cr = HyperellipticCurve(f_r, check_squarefree=False)
        
        # 点计数：C(F_r) 
        nr1 = Cr.count_points(1)[0]
        
        # 计算迹 a1 = r + 1 - nr1
        a1 = r + 1 - nr1
        
        # 判定局部 L-因子阶数 (deg_L)
        # 对于坏素数 r，局部 L-因子次数会由于退化而降低 [cite: 8]
        # 典型的退化模式：a1=0 通常对应次数降为 0 或更高维坍塌
        if a1 == 0:
            deg_L = 0 
        else:
            deg_L = 1
            
        # 对于驯分歧素数 (Tame primes): f_r = 4 - deg_L [cite: 1]
        f_r_val = 4 - deg_L
        
        if verbose:
            print(f"r={r:<3} | #C(Fr)={nr1:<5} | a1={a1:<3} | f_r={f_r_val}")
        
        result[r] = f_r_val
    return result

# 示例运行
goldbach_conductor_odd(7, 23)