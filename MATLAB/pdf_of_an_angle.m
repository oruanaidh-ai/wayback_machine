sig = 0.5+rand*2;
L = rand*2; % length of vector
 
% Generate Some Data
N = 1000000;
y = sig*randn(N, 1);
x = L + sig*randn(N, 1);
 
R = L/sig;
 
% Mathematical expression for pdf
f = @(x) (exp(-R*R/2) + sqrt(pi/2) * R*cos(x).*(1 + erf( R*cos(x)/sqrt(2))) .* exp( -R^2*sin(x).^2/ 2))/2/pi;
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Make histograms
 
[n, g ] = hist(atan2(y, x), 100);
 
figure
n = n/sum(n)/(g(2)-g(1));  % normalize 
 
bar(g*180/pi, n)
 
hold on
 
plot(g*180/pi, f(g), 'g', 'Linewidth', 3)
xlabel('angle (degrees)')
ylabel('Prob. density')
 
legend('Observed', 'Theory')
 
hold off
 
quad(f, 0, 2*pi)
