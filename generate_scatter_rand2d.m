%%%% Function for generating inhomogeneties
%%%% Output the horizontal layer velocity pertubation dV(M,N)
%%%% Need Input:
%%%%  dimensions and grid size for layer with heterogenities: M, N, delta
%%%%  Correlation length for the layer inhomogeneties: ax, az (km), sigma(standard deviation)             
%%%%
%%%% Ouput:
%%%%  Velcoity perturbation of a horizontal layer

%%%% Return: dV(NX,NZ): velocity pertubation in a slab with heterogenties



function dV = generate_scatter_rand2d(M,N,delta,ax,az,sigma,k)

%%Double the size to make sure the slab is inside the box
M = 2*M;
N = 2*N;


%%%Give the random V distribution for the grid
Vs = 2*rand([N M])-1;

%%%2D FFT
Y2 = fft2(Vs);

%%%Define wavenumber along x and z
kx1 = mod( 1/2 + (0:(M-1))/M , 1 ) - 1/2;
kx = kx1*(2*pi/delta);
kz1 = mod( 1/2 + (0:(N-1))/N , 1 ) - 1/2;
kz = kz1*(2*pi/delta);
[KX,KZ] = meshgrid(kx,kz);


K_sq = KX.^2*ax^2 + KZ.^2*az^2;
%%%Von Karman distribution
P_K = (4*pi*gamma(k+1)*(ax.*az))./(gamma(abs(k)).*(1+K_sq).^(k+1));
% P_K = (4*pi*gamma(k+1)*(ax^2+az^2))./(gamma(abs(k)).*(1+K_sq).^(3/2));
%P_K = (ax^2+az^2)./((1+K_sq).^(3/2));
%P_K = (ax.*az)./((1+K_sq).^(3/2));
%P_K = (ax.*az)./(1+K_sq);


Y2 = Y2 .*sqrt(P_K);

%%%IFFT
newV = ifft2(Y2);

test = real(newV(1:N,1:M));
%size(test)
%std(test(:));
%%%Format the amplitude to std
test = sigma/std(test(:))*test;
%std(test(:));
%%Cut to the slab size
Mid_M = floor(M/4);
Mid_N = floor(N/4);
M = M/2;
N = N/2;
dV(1:N,1:M) = test(Mid_N+1:Mid_N+N,Mid_M+1:Mid_M+M);
