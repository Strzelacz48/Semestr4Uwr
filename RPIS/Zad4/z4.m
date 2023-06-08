
function retval = z4 (n, k, x)
  retval = [];
  for i = 1 : numel(x)
    A = factorial(n)/(factorial(k-1)* factorial(n-k));
    B = gestosc(x(i)) * (dystrybuanta(x(i))^(k - 1));
    C = (1 - dystrybuanta(x(i)))^(n-k);
    retval = [retval, A * B * C];
    #retval = n * nchoosek(n-1,k-1) * x^(k-1) * (1-x)^(n-k)
   endfor
endfunction
