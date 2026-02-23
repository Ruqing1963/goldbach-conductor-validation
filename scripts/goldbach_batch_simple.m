// goldbach_batch_simple.m — Just get conductor factorizations
// The Ogg warning only affects r=2. Odd parts are reliable.

R<x> := PolynomialRing(Rationals());

pairs := [
    <3, 7>,      // 2N=10,  |p-q|=4=2^2
    <7, 23>,     // 2N=30,  |p-q|=16=2^4
    <11, 19>,    // 2N=30,  |p-q|=8=2^3
    <13, 17>,    // 2N=30,  |p-q|=4=2^2
    <3, 17>,     // 2N=20,  |p-q|=14=2*7  *** NEW ODD PRIME 7 ***
    <7, 19>,     // 2N=26,  |p-q|=12=2^2*3 *** NEW ODD PRIME 3 ***
    <3, 37>,     // 2N=40,  |p-q|=34=2*17  *** NEW ODD PRIME 17 ***
    <7, 41>,     // 2N=48,  |p-q|=34=2*17  *** NEW ODD PRIME 17 ***
    <7, 53>,     // 2N=60,  |p-q|=46=2*23  *** NEW ODD PRIME 23 ***
    <11, 37>     // 2N=48,  |p-q|=26=2*13  *** NEW ODD PRIME 13 ***
];

printf "%4o %4o %5o %6o  %o\n", "p", "q", "2N", "|p-q|", "Conductor factorization";
printf "-----------------------------------------------------------\n";

for pair in pairs do
    p := pair[1]; q := pair[2];
    f := x * (x^2 - p^2) * (x^2 - q^2);
    C := HyperellipticCurve(f);
    cond := Conductor(C);
    printf "%4o %4o %5o %6o  %o\n", p, q, p+q, q-p, Factorization(cond);
end for;

quit;
