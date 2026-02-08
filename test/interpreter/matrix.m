A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 0] = 42;
D[1:3, 2:4] = 7; # dla chetnych
print D;
print D[2, 2];

E = [2, 1, 3, 7];
print E;
E[2] = 8;
print E;

F = [
    1, 2;
    3, 4;
    5, 6;
];
print F;
