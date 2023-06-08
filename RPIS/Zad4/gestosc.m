
function retval = gestosc (x)
  if (0 <= x && x <= 1)
    retval = (2* x)/9;
    return
   elseif (1 < x && x <= 4)
    retval = 2/9;
    return
   elseif (4 < x && x <= 6)
    retval = -(1/9)*x + (6/9);
    return
   else
    retval = 0;
    return
  endif
endfunction