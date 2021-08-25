%I learned about Stochastic dynamics after I learned about Markov chains.  The underlying idea is based on the Boltzmann distribution. In Boltzmann, probability is the exponential of minus energy (divided by kT but let's ignore nuisance variables). So energy, or more precisely potential energy, is minus log probability. It's a function of q, the position. So what about potential energy?  That's p^2/2 where p is momentum (ignoring m here). So its probability is exp(-p^2/2)  (i.e. Gaussian).
%Next we define a Hamiltonian equal to potential energy plus kinetic energy.  To generate random q, I generate Gaussian p, and simulate the evolution of the dynamical system in time.
%The parameter p is pulled out of thin air. We are only interested in seeing what q does. That's what's really cute about this.
%So you input p, a Gaussian, and out pops q, in this case Cauchy.

dUdq = @(q) 2*q./(1+q.*q);
pq = @(q) 1./(1+q.*q)/pi;

num = 50000;
eps = 5e-2;
vec= zeros(num, 1);
numStep = 100;

q = 0;
for i=1:num
    
    p = randn(1);
    
    p = p - eps/2 * dUdq(q);
    for j=1:numStep
        q = q + eps*p;
        p = p - eps*dUdq(q);
    end
    
    p = p - eps/2*dUdq(q);
    
    vec(i) = q;
    
end


[n, g] = hist(vec, 200);
figure, plot(g, n/sum(n)/(g(2)-g(1)))
hold on

plot(g, pq(g), 'r');
hold off



legend('Stochastic Dynamics', 'Theory')

