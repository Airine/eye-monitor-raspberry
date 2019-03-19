def pre_process():
    fs = 48000
    N = 0.005*fs
    n = range(N)
    t = n/fs
    fcut = f - 2e3


    data = list() # 4

    # TODO: 对data进行带通滤波 (中心频率22k, 0.5k 半径)


    # TODO: 解调
    cosSig = cos(2*pi*f*t)';
    sinSig = sin(2*pi*f*t)';
    rc1 = 2 * r1 .* cosSig;
    rs1 = -2 * r1 .* sinSig;
    rc2 = 2 * r2 .* cosSig;
    rs2 = -2 * r2 .* sinSig;
    rc3 = 2 * r3 .* cosSig;
    rs3 = -2 * r3 .* sinSig;
    rc4 = 2 * r4 .* cosSig;
    rs4 = -2 * r4 .* sinSig;

    # TODO: 低通滤波 100Hz

    c1 = filter(b, a, rc1);
    s1 = filter(b, a, rs1);

    c2 = filter(b, a, rc2);
    s2 = filter(b, a, rs2);

    c3 = filter(b, a, rc3);
    s3 = filter(b, a, rs3);

    c4 = filter(b, a, rc4);
    s4 = filter(b, a, rs4);

    return (c1,s1,c2,s2,c3,s3,c4,c4)
