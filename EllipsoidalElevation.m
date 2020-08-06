matrix = zeros(325, 992);
matrix2 = zeros(325, 992);
matrix3 = zeros(325, 992);

q=1;

while q < 322401
    for n= 1:325
        for p = 1:992
            matrix(n, p) = N(q);
            matrix2(n,p) = A(q) - N(q);
            matrix3(n,p) = A(q);
            q = q+1;
        end
        p=1;
    end
end

figure(1)
contour(matrix, 30)
title('Geoid Height')
colormap(hot)

figure(2)
contour(matrix2)
title('Orthometric Height')
colormap(hot)

figure(3)
contour(matrix3)
title('Ellipsoidal Height')
colormap(hot)

