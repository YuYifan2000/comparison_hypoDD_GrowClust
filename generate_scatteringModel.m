
nx=4800;
nz=1600;
Vp=zeros(nx,nz)+6.0;
Vp = Vp';
dV = generate_scatter_rand2d(nx,nz,.005,.5,.1,.107,.04);

% 
% % Vp = Vp'.*(1 + dV);
Vp = Vp *(1 + dV);
Vs = Vs *(1 + dV);
Den = Den * (1+dV*0.8);
% Vs = Vs + dV./1.8;
% Den = Vp.*0 + 33./((Vs).^2);
Vs=Vp./(3^0.5);
Den=0.23.*(Vp.*3281).^(0.25);


id = 'scatterT';
fid=fopen(strcat(id,'.vp'),'wb');
fwrite(fid,Vp,'single');
fclose(fid);

fid=fopen(strcat(id,'.vs'),'wb');
fwrite(fid,Vs,'single');
fclose(fid);

fid=fopen(strcat(id,'.den'),'wb');
fwrite(fid,Den,'single');
fclose(fid);

figure()
imagesc(Vp);


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
figure()
imagesc(P_K);

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
end
