pi = 0.0;
n = 1;
for i = 1:100000 {
    # TODO bad parsing of arithmetic
    pi += 4.0 / n - 4.0 / (n + 2);
    # print pi, test, 4.0 / n, 4.0 / (n + 2);
    n += 4;
}
print pi;
